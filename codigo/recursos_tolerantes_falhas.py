"""Estimação física local com Microsoft QDK QRE, sem simulação de amplitudes.

Este módulo NÃO afirma ter compilado o oráculo completo. Recebe a contagem
analítica de E3 e torna explícitos dois escalonamentos de suas operações. O QRE
converte esses modelos lógicos condicionais em qubits físicos, duração e
fábricas de estados mágicos. Nenhum preço comercial entra nesta conta.

Executar, depois do notebook 3::

    python codigo/recursos_tolerantes_falhas.py

Fontes primárias da API e do modelo físico:
https://github.com/microsoft/qdk/wiki/QREv3
https://github.com/microsoft/qdk/tree/main/samples/qre
https://arxiv.org/abs/2211.07629
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from importlib.metadata import version
import hashlib
import json
import math
from pathlib import Path
import re
import tempfile

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
T_ROTACAO = 130
ERRO_FISICO_MAXIMO = 0.01
DISTANCIAS = list(range(3, 52, 2))


def auditar_primitivas(tau_q: pd.DataFrame) -> pd.DataFrame:
    """Conta circuitos Q# concretos de Toffoli e Cuccaro sem estado quântico.

    O backend de trace executa apenas o controle clássico. T e T-dagger custam
    um estado T cada. A profundidade propaga dependências inclusive por portas
    Clifford, atribuindo duração zero a estas somente na métrica T-depth.
    """
    from qdk import qsharp
    from qdk.qre.interop import trace_from_entry_expr
    from qdk.qre.instruction_ids import T, T_DAG

    qsharp.eval('''namespace RecursosVaR {
        // Decomposição exata padrão: 7 T/T-dagger, 6 CNOT, 2 H.
        operation Toffoli7(a : Qubit, b : Qubit, c : Qubit) : Unit is Adj {
            H(c); CNOT(b,c); Adjoint T(c); CNOT(a,c); T(c);
            CNOT(b,c); Adjoint T(c); CNOT(a,c); T(b); T(c); H(c);
            CNOT(a,b); T(a); Adjoint T(b); CNOT(a,b);
        }
        operation Maj(a : Qubit, b : Qubit, c : Qubit) : Unit {
            CNOT(a,b); CNOT(a,c); Toffoli7(c,b,a);
        }
        operation Uma(a : Qubit, b : Qubit, c : Qubit) : Unit {
            Toffoli7(c,b,a); CNOT(a,c); CNOT(c,b);
        }
        operation Somador(n : Int) : Unit {
            use a = Qubit[n]; use b = Qubit[n];
            use c = Qubit(); use z = Qubit();
            Maj(a[0],b[0],c);
            for i in 1..n-1 { Maj(a[i],b[i],a[i-1]); }
            CNOT(a[n-1],z);
            for i in n-1..-1..1 { Uma(a[i],b[i],a[i-1]); }
            Uma(a[0],b[0],c);
        }
        operation PortaToffoli() : Unit {
            use q = Qubit[3]; Toffoli7(q[0],q[1],q[2]);
        }
    }''')
    larguras = sorted(set(tau_q["bits_acum"].astype(int)) | set(tau_q["n"].astype(int) + 3))
    registros = []
    for nome, bits, expr in [("toffoli", 0, "RecursosVaR.PortaToffoli()"), *[
        ("somador_cuccaro", b, f"RecursosVaR.Somador({b})") for b in larguras
    ]]:
        trace = trace_from_entry_expr(expr, use_trace_backend=True)
        niveis: dict[int, int] = {}
        t_count = 0
        for porta in trace.flatten():
            nao_clifford = porta.id in (T, T_DAG)
            nivel = max((niveis.get(q, 0) for q in porta.qubits), default=0) + int(nao_clifford)
            for q in porta.qubits:
                niveis[q] = nivel
            t_count += int(nao_clifford)
        esperado = 7 if nome == "toffoli" else 14 * bits
        if t_count != esperado:
            raise ValueError(f"Primitiva {nome} não confere contagem: {t_count} != {esperado}")
        registros.append({
            "primitiva": nome, "bits": bits, "qubits_trace": trace.compute_qubits,
            "T_count_trace": t_count, "T_depth_trace": max(niveis.values()),
            "portas_totais_trace": trace.num_gates,
        })
    return pd.DataFrame(registros)


def recursos_logicos(tau_q: pd.DataFrame, primitivas: pd.DataFrame) -> pd.DataFrame:
    """Calcula profundidade de escalonamentos declarados, não a profundidade ótima.

    Cada normal ocupa um registrador distinto: suas sequências de rotações
    podem correr em paralelo. Dentro de cada preparação, as 2**n rotações e
    suas sequências de síntese permanecem em série. Toda a aritmética de
    correlação, perda, comparação e descomputação permanece em série; não se
    pressupõem cópias gratuitas de controles nem acumuladores independentes.
    A profundidade interna dos somadores e Toffolis é contada em circuitos Q#
    concretos, pelo backend de trace do QDK, antes da composição dos blocos.
    """
    registros = []
    d_soma = primitivas.loc[primitivas["primitiva"] == "somador_cuccaro"].set_index("bits")["T_depth_trace"].to_dict()
    d_toffoli = int(primitivas.loc[primitivas["primitiva"] == "toffoli", "T_depth_trace"].iloc[0])
    for row in tau_q.loc[tau_q["carga"].isin(["cholesky", "fator unico"])].to_dict("records"):
        n, N = int(row["n"]), int(row["N"])
        m, s = int(row["bits_acum"]), int(row["segmentos"])
        nx = n + 3
        repeticoes = int(row["bissecoes"]) * int(row["chamadas_grover"])
        normais = N if row["carga"] == "cholesky" else N + 1
        # Dois sentidos: preparação e sua inversa, na contagem original de E3.
        t_normais_grover = 2 * normais * (2**n) * T_ROTACAO
        t_grover = int(round(row["T_por_grover"]))
        t_aritmetica = t_grover - t_normais_grover
        if t_aritmetica < 0:
            raise ValueError("Contagem de rotações excede T_por_grover")
        total = t_grover * repeticoes
        if not np.isclose(total, row["T_total"], rtol=1e-12):
            raise ValueError("Contagem total inconsistente com os parâmetros de E3")

        # Registrador da AE canônica e workspace da iteração unária da QROM.
        # Os dois acumuladores de m bits já estão na contagem original.
        fase = math.ceil(math.log2(int(row["chamadas_grover"])))
        qrom = max(0, n - 1)
        qubits = int(row["qubits"]) + fase + qrom
        mults = N * (N + 1) // 2 if row["carga"] == "cholesky" else 2 * N
        d_correlacao = mults * n * d_soma[nx]
        custo_linear = s * (2 * nx + nx * 2 * m + 2 * m)
        custo_tabela = 2**n + 2 * m
        d_perda_acao = (
            s * (d_soma[nx] + nx * d_soma[m] + d_soma[m])
            if custo_linear < custo_tabela else 2**n * d_toffoli + d_soma[m]
        )
        # As consultas QROM são seriadas e limitadas por um Toffoli por passo.
        # Somadores/multiplicações que compartilham controles ou acumulador
        # permanecem seriados; não se presume fan-out gratuito.
        d_resto = 2 * N * d_perda_acao + d_soma[m]
        d_aritmetica = 2 * (d_correlacao + d_resto)
        for esquema in ("serial", "normais_paralelas"):
            d_normais = t_normais_grover if esquema == "serial" else 2 * (2**n) * T_ROTACAO
            profundidade = (d_normais + d_aritmetica) * repeticoes
            registros.append({
                "N": N, "eps": row["eps"], "carga": row["carga"],
                "escalonamento": esquema, "n": n,
                "qubits_modelo_original": int(row["qubits"]),
                "qubits_fase": fase, "qubits_qrom": qrom,
                "qubits_logicos_modelo": qubits,
                "T_total": total, "T_depth_escalonamento": profundidade,
                "T_normais_por_grover": t_normais_grover,
                "T_aritmetica_por_grover": t_aritmetica,
                "T_depth_aritmetica_por_grover": d_aritmetica,
                "T_depth_por_grover": d_normais + d_aritmetica,
                "paralelismo_T_medio": total / profundidade,
                "tau_c_s": row["tau_c_s"],
                "taxa_T_empate": total / row["tau_c_s"],
                "camadas_T_por_s_empate": profundidade / row["tau_c_s"],
            })
    return pd.DataFrame(registros)


def estimar_fisicos(logicos: pd.DataFrame, raiz: Path = RAIZ) -> pd.DataFrame:
    """Executa QRE com código de superfície e destilação em fábricas paralelas.

    O transform PSSPC padrão serializa todas as portas T. Por isso aplicamos
    somente seu footprint de layout e entregamos ao estimador uma Trace já na
    camada LATTICE_SURGERY: uma operação por camada T do escalonamento, com a
    demanda total de estados T em separado. Não se converte throughput em
    duração ignorando a profundidade. O custo Clifford/routing é o da abstração
    de layout, não uma compilação independente de cada subrotina do oráculo.
    """
    from qdk.qre import Application, PSSPC, Trace, estimate
    from qdk.qre.instruction_ids import LATTICE_SURGERY, T
    from qdk.qre.models import GateBased, RoundBasedFactory, SurfaceCode
    from qdk.qre.property_keys import PHYSICAL_COMPUTE_QUBITS, PHYSICAL_FACTORY_QUBITS

    @dataclass
    class ModeloCamadas(Application[None]):
        qubits: int
        profundidade: int
        estados_t: int

        def get_trace(self, parameters: None = None):
            # Usa o overhead de layout PSSPC implementado pelo próprio QRE.
            original = Trace(self.qubits)
            original.add_operation(T, [0])
            layout = PSSPC(num_ts_per_rotation=T_ROTACAO).transform(original)
            if layout is None:
                raise RuntimeError("QRE não produziu footprint PSSPC")
            trace = Trace(layout.compute_qubits)
            bloco = trace.add_block(repetitions=self.profundidade)
            bloco.add_operation(LATTICE_SURGERY, list(range(layout.compute_qubits)))
            trace.increment_resource_state(T, self.estados_t)
            return trace

    saidas = []
    cache = Path(tempfile.gettempdir()) / "quant-search-qre-factories"
    cache.mkdir(parents=True, exist_ok=True)
    for erro in (1e-4, 1e-3):
        hardware = GateBased(error_rate=erro, gate_time=50, measurement_time=100)
        # Mesma família de códigos na computação e nas unidades de destilação.
        codigos = SurfaceCode.q(distance=DISTANCIAS)
        fabrica = RoundBasedFactory.q(code_query=codigos, cache_dir=cache, use_cache=True)
        arquitetura = codigos * fabrica
        for row in logicos.to_dict("records"):
            app = ModeloCamadas(
                int(row["qubits_logicos_modelo"]),
                int(row["T_depth_escalonamento"]), int(row["T_total"]),
            )
            estimativas = estimate(
                app, hardware, arquitetura, trace_query=Application.q(),
                max_error=ERRO_FISICO_MAXIMO,
                # Evita poda de ISA que pode omitir pontos Pareto globais.
                use_graph=False,
            )
            if not len(estimativas):
                raise RuntimeError(f"Nenhuma estimativa física viável: {row}, p={erro}")
            for posicao, resultado in enumerate(estimativas):
                fab = resultado.factories.get(T)
                fonte = str(resultado.source)
                distancia = re.search(r"SurfaceCode\([^\n]*distance=(\d+)", fonte)
                saidas.append({
                    **row, "erro_porta_fisica": erro,
                    "gate_time_ns": 50, "measurement_time_ns": 100,
                    "orcamento_falha_hardware": ERRO_FISICO_MAXIMO,
                    "ponto_pareto": posicao,
                    "runtime_s": resultado.runtime / 1e9,
                    "qubits_fisicos": resultado.qubits,
                    "qubits_fisicos_computacao": resultado.properties.get(PHYSICAL_COMPUTE_QUBITS),
                    "qubits_fisicos_fabricas": resultado.properties.get(PHYSICAL_FACTORY_QUBITS),
                    "distancia_codigo_computacao": int(distancia.group(1)) if distancia else None,
                    "fabricas_T_paralelas": fab.copies if fab else 0,
                    "estados_T_consumidos": fab.states if fab else 0,
                    "rodadas_fabrica": fab.runs if fab else 0,
                    "erro_estado_T": fab.error_rate if fab else 0,
                    "probabilidade_falha_hardware": resultado.error,
                    "runtime_sobre_classico": resultado.runtime / 1e9 / row["tau_c_s"],
                    "recalculo_em_60s": resultado.runtime <= 60e9,
                    "modelo_isa": fonte,
                })
        print(f"QRE: concluído erro físico {erro:g}", flush=True)
    return pd.DataFrame(saidas)


def executar(raiz: Path = RAIZ, fisicos: bool = True) -> tuple[pd.DataFrame, pd.DataFrame | None]:
    raiz = Path(raiz)
    entradas = pd.read_csv(raiz / "dados/tau_q.csv")
    requeridas = {"n", "bits_acum", "segmentos", "bissecoes", "chamadas_grover", "T_por_grover"}
    if not requeridas.issubset(entradas):
        raise ValueError("Execute primeiro o notebook 3 atualizado; faltam parâmetros do circuito")
    primitivas = auditar_primitivas(entradas)
    primitivas.to_csv(raiz / "dados/recursos_primitivas.csv", index=False)
    logicos = recursos_logicos(entradas, primitivas)
    logicos.to_csv(raiz / "dados/recursos_logicos.csv", index=False)
    resultados = estimar_fisicos(logicos, raiz) if fisicos else None
    if resultados is not None:
        resultados.to_csv(raiz / "dados/recursos_fisicos.csv", index=False)
    premissas = {
        "qdk_version": version("qdk"),
        "sha256_tau_q_entrada": hashlib.sha256((raiz / "dados/tau_q.csv").read_bytes()).hexdigest(),
        "modelo": "Microsoft Quantum Resource Estimator local; SurfaceCode + RoundBasedFactory",
        "portas_T_por_rotacao": T_ROTACAO,
        "distancias_codigo": DISTANCIAS,
        "erro_fisico_maximo": ERRO_FISICO_MAXIMO,
        "gate_time_ns": 50, "measurement_time_ns": 100,
        "erros_fisicos": [1e-4, 1e-3],
        "escopo_orcamento": "Falha física/QEC/destilação; não inclui erro de estimação QAE, discretização ou síntese das rotações do modelo original.",
        "profundidade": "Escalonamentos condicionais de E3: serial ou somente preparações normais independentes em paralelo. Não são profundidades ótimas de um oráculo compilado.",
        "layout": "Footprint PSSPC do QRE; uma etapa de lattice surgery por camada T declarada, abrangendo todos os qubits de computação. Sem otimização adicional de routing.",
        "fabricas": "Número de cópias em paralelo escolhido pelo QRE para suprir estados T dentro da duração imposta pela profundidade.",
        "abstracao_fabricas": "O QRE usa demanda agregada e duração para dimensionar cópias; não se simulam arranque, filas internas, estoques de estados mágicos ou picos de consumo por camada.",
        "contagem": "QDK conta primitivas concretas de Toffoli (7 T/T-dagger) e somador Cuccaro (14b T/T-dagger); a composição original de E3 é preservada. Não houve síntese nem auditoria independente do oráculo completo.",
        "auxiliares": "À largura original adicionam-se ceil(log2(chamadas_grover)) qubits da AE canônica e n-1 qubits da iteração unária QROM; layout PSSPC e fábricas são posteriores.",
        "limitacoes": "A correspondência entre blocos analíticos e um circuito reversível completo ainda exige validação. Estes resultados não são uma previsão de hardware comercial nem validação empírica de velocidade.",
        "fontes": [
            "https://github.com/microsoft/qdk/wiki/QREv3",
            "https://github.com/microsoft/qdk/tree/main/samples/qre",
            "https://arxiv.org/abs/2211.07629",
            "https://doi.org/10.1103/PhysRevX.8.041015",
        ],
    }
    (raiz / "dados/recursos_premissas.json").write_text(json.dumps(premissas, indent=2, ensure_ascii=False) + "\n")
    return logicos, resultados


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--somente-logicos", action="store_true")
    argumentos = parser.parse_args()
    executar(fisicos=not argumentos.somente_logicos)
