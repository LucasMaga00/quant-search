"""Calibra o M de E1 com erro observado perto do alvo e mede a referência original.

A calibração usa a identidade exata da paridade put-call para os straddles;
os tempos usam carteira.calcular_var, com a reavaliação completa das N x K opções.
Não estima o tempo de 0,1%: essa precisão continua uma extrapolação em E3.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import platform
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from scipy.special import ndtr, ndtri
from scipy.stats import qmc

import carteira as car

NS = [2**k for k in range(10)]
METODOS = ("mc", "qmc")
MS_PILOTO = (2**10, 2**12, 2**14)
EPS_REL = 0.01
N_SEMENTES = 50


def perdas_validacao(N: int, M: int, metodo: str, semente: int) -> np.ndarray:
    """Mesmas perdas de carteira.perdas, avaliando cada straddle uma só vez.

    Cada straddle vendido vale -2*call + S - strike*exp(-rT).
    A geração de normais e a correlação por Cholesky são as de E1.
    O processamento em blocos limita memória e preserva a ordem dos cenários.
    """
    if metodo == "qmc" and M & (M - 1):
        raise ValueError("Sobol requer um total de cenários potência de dois.")
    rng = (np.random.default_rng(semente) if metodo == "mc"
           else qmc.Sobol(d=N, scramble=True, seed=semente))
    C = np.full((N, N), car.RHO)
    np.fill_diagonal(C, 1.0)
    cholesky = np.linalg.cholesky(C).T
    _, strike, call, qtd, acoes = car.montar_carteira(N)
    v0 = car.black_scholes(car.S0, strike, car.VENC, call) @ qtd + acoes.sum() * car.S0
    strikes = car.S0 * car.STRIKES
    T = car.VENC - car.DT
    df = np.exp(-car.R * T)
    sigma_raiz = car.SIGMA * np.sqrt(T)
    constante = (car.R + car.SIGMA**2 / 2) * T
    perda = np.empty(M)
    # A primeira chamada Sobol tem tamanho potência de dois, inclusive no piloto.
    bloco = min(1024, M)
    for inicio in range(0, M, bloco):
        tamanho = min(bloco, M - inicio)
        if metodo == "mc":
            normais = rng.standard_normal((tamanho, N))
        else:
            normais = ndtri(np.clip(rng.random(tamanho), 1e-10, 1 - 1e-10))
        S = car.preco_em_1_dia(normais @ cholesky)
        S3 = S[..., None]
        d1 = (np.log(S3 / strikes) + constante) / sigma_raiz
        calls = S3 * ndtr(d1) - strikes * df * ndtr(d1 - sigma_raiz)
        valor_por_acao = -2 * calls.sum(axis=-1) + (len(strikes) + acoes[0]) * S - strikes.sum() * df
        perda[inicio:inicio + tamanho] = v0 - valor_por_acao.sum(axis=1)
    return perda


def conferir_identidade() -> float:
    """Verificação numérica da identidade usada apenas para calibrar o erro."""
    maior = 0.0
    for N in (1, 3, 32):
        for metodo in METODOS:
            M = 2048
            referencia = car.perdas(N, M, metodo, 17, car.montar_carteira(N))
            obtida = perdas_validacao(N, M, metodo, 17)
            diferenca = float(np.max(np.abs(referencia - obtida)))
            maior = max(maior, diferenca)
            if not np.allclose(referencia, obtida, rtol=1e-10, atol=1e-8):
                raise AssertionError((N, metodo, diferenca))
    return maior


def _estatisticas(valores: list[float]) -> dict:
    media = float(np.mean(valores))
    desvio = float(np.std(valores, ddof=1))
    return {"media_var": media, "desvio_var": desvio,
            "erro_rel_medido": desvio / media, "sementes": len(valores)}


def calibrar(N: int, metodo: str, cache_dir: str, sementes: int = N_SEMENTES) -> dict:
    """Confirma o erro em M próximo do alvo, sem usar a reta como validação."""
    cache_path = Path(cache_dir) / f"{metodo}_{N}_{sementes}.json"
    if cache_path.exists():
        cache = json.loads(cache_path.read_text())
        medidas = {int(k): v for k, v in cache.items()}
    else:
        medidas = {}

    def medir(ms: list[int]) -> None:
        novos = sorted(set(ms) - medidas.keys())
        if not novos:
            return
        maximo = max(novos)
        valores = {m: [] for m in novos}
        for semente in range(sementes):
            perdas = perdas_validacao(N, maximo, metodo, semente)
            for M in novos:
                valores[M].append(float(np.quantile(perdas[:M], car.ALPHA)))
        for M in novos:
            medidas[M] = _estatisticas(valores[M])
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(medidas))

    medir(list(MS_PILOTO))
    b, a = np.polyfit(np.log(MS_PILOTO),
                      np.log([medidas[m]["erro_rel_medido"] for m in MS_PILOTO]), 1)
    if b >= 0:
        raise ValueError(f"Inclinação não decrescente em N={N}, {metodo}: {b}")
    M_reta = float(np.exp((np.log(EPS_REL) - a) / b))
    M_potencia2_reta = 2 ** int(math.ceil(math.log2(M_reta)))
    M_arredondado_reta = (M_potencia2_reta
                          if metodo == "qmc" else math.ceil(M_reta))
    if metodo == "mc":
        # MC tem expoente teórico -1/2: uma reta ruidosa em três pontos não
        # determina mais M. A medição perto do alvo confirma esta previsão local.
        ancora = MS_PILOTO[-1]
        M_local = ancora * (medidas[ancora]["erro_rel_medido"] / (0.95 * EPS_REL)) ** 2
        candidato = max(1024, math.ceil(M_local))
    else:
        M_local = M_reta
        candidato = max(1024, M_arredondado_reta)

    for _ in range(8):
        if candidato > 2**21:
            raise RuntimeError(f"Calibração excedeu orçamento: N={N}, {metodo}, M={candidato}")
        medir([candidato])
        erro = medidas[candidato]["erro_rel_medido"]
        if metodo == "qmc":
            if erro > EPS_REL:
                candidato *= 2
                continue
            menor = candidato // 2
            if menor >= 512:
                medir([menor])
                if medidas[menor]["erro_rel_medido"] <= EPS_REL:
                    candidato = menor
                    continue
            break
        if erro > EPS_REL:
            # Um tamanho maior já validado fecha o intervalo; não é preciso
            # extrapolar novamente e acabar acima de uma amostra que já serve.
            if any(m > candidato and r["erro_rel_medido"] <= EPS_REL
                   for m, r in medidas.items()):
                break
            candidato = math.ceil(candidato * (erro / (0.95 * EPS_REL))**2)
            continue
        if erro < 0.85 * EPS_REL:
            if any(m < candidato and r["erro_rel_medido"] > EPS_REL
                   and m > MS_PILOTO[-1] for m, r in medidas.items()):
                break
            proximo = max(1024, math.ceil(candidato * (erro / (0.95 * EPS_REL))**2))
            if proximo not in medidas:
                candidato = proximo
                continue
        break
    validos = [m for m, r in medidas.items() if r["erro_rel_medido"] <= EPS_REL]
    if not validos:
        raise RuntimeError(f"Nenhum M atingiu o erro-alvo: {N}, {metodo}")
    M = min(validos)
    inferiores = [m for m in medidas if m < M]
    menor = max(inferiores) if inferiores else None
    return {"N": N, "K": car.K, "metodo": metodo, "M": M,
            "inclinacao_erro": float(b), "eps": EPS_REL,
            "M_previsto_reta": M_reta, "M_arredondado_reta": M_arredondado_reta,
            "fator_arredondamento_reta": M_arredondado_reta / M_reta,
            "M_potencia2_reta": M_potencia2_reta,
            "fator_potencia2_reta": M_potencia2_reta / M_reta,
            "M_previsao_local": M_local,
            "M_menor_medido": menor or "",
            "erro_rel_menor": medidas[menor]["erro_rel_medido"] if menor else "",
            "erro_rel_medido": medidas[M]["erro_rel_medido"],
            "sementes": sementes, "tipo_tempo": "medido",
            "medidas": [{"N": N, "metodo": metodo, "M": m, **r}
                         for m, r in sorted(medidas.items())]}


def escrever_csv(path: Path, linhas: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(linhas[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(linhas)


def executar(dados: Path, cache_dir: Path, workers: int = 4,
             apenas_calibrar: bool = False) -> list[dict]:
    max_diferenca = conferir_identidade()
    print(f"Paridade conferida: diferença absoluta máxima {max_diferenca:.3g}", flush=True)
    print(platform.platform(), "numpy", np.__version__, flush=True)
    resultados = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        tarefas = [pool.submit(calibrar, N, metodo, str(cache_dir))
                   for N in NS for metodo in METODOS]
        for tarefa in as_completed(tarefas):
            linha = tarefa.result()
            resultados.append(linha)
            print(f"Validado N={linha['N']:3d} {linha['metodo']}: "
                  f"M={linha['M']}, erro={100 * linha['erro_rel_medido']:.3f}%", flush=True)
    resultados.sort(key=lambda r: (r["N"], r["metodo"]))
    diagnostico = [m for r in resultados for m in r["medidas"]]
    escrever_csv(dados / "e1_validacao_erro.csv", diagnostico)
    if apenas_calibrar:
        print("Calibração pronta; cronometração pendente.", flush=True)
        return resultados
    print("Iniciando cronometração sequencial da reavaliação completa (3 repetições).", flush=True)
    saida = []
    for r in resultados:
        carteira = car.montar_carteira(r["N"])
        tempos = []
        for semente in range(3):
            inicio = time.perf_counter()
            car.calcular_var(r["N"], r["M"], r["metodo"], semente, carteira)
            tempos.append(time.perf_counter() - inicio)
        linha = {k: v for k, v in r.items() if k != "medidas"}
        linha["tau_c_s"] = float(np.median(tempos))
        linha["tau_c_min_s"] = min(tempos)
        linha["tau_c_max_s"] = max(tempos)
        saida.append(linha)
        print(f"Tempo N={r['N']:3d} {r['metodo']}: {linha['tau_c_s']:.6f} s", flush=True)
    # Mantém os seis campos originais primeiro; os consumidores podem continuar
    # lendo N, K, metodo, M, inclinacao_erro e tau_c_s sem adaptação.
    campos = ("N", "K", "metodo", "M", "inclinacao_erro", "tau_c_s")
    saida = [{**{k: r[k] for k in campos},
              **{k: v for k, v in r.items() if k not in campos}} for r in saida]
    escrever_csv(dados / "tau_c.csv", saida)
    return saida


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--cache-dir", type=Path,
                        default=Path(tempfile.gettempdir()) / "quant-e1-validacao")
    parser.add_argument("--dados", type=Path, default=Path(__file__).resolve().parents[1] / "dados")
    parser.add_argument("--apenas-calibrar", action="store_true")
    args = parser.parse_args()
    executar(args.dados, args.cache_dir, args.workers, args.apenas_calibrar)
