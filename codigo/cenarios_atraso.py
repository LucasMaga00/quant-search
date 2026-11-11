"""E4: cenários condicionais para o valor econômico de reduzir a latência.

Não estima o comportamento de L abaixo de um minuto. Compara as formas
solicitadas na avaliação, mantendo uma âncora comum no intervalo observado.
Execute da raiz: python codigo/cenarios_atraso.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import brentq


RAIZ = Path(__file__).resolve().parents[1]
RECALCULOS_DIA = 390
PREGAO_S = 390 * 60
LIMITE_MESA_MILHOES = 100.0
PRECO_CLASSICO_S = 0.10 / 3600
# Uma meta hipotética, sem pressupor que preços comerciais NISQ se apliquem
# a um computador tolerante a falhas. Não é uma previsão de preço de hardware.
PRECO_META_S = 1.60
TAXAS_T = (1e4, 1e6, 1e8)
FORMAS = ("potencia_ajustada", "potencia_05", "potencia_1", "degrau", "exponencial")
ROTULOS = {
    "potencia_ajustada": r"Potência ajustada ($\beta$ estimado)",
    "potencia_05": r"Potência, $\beta=0{,}5$",
    "potencia_1": r"Potência, $\beta=1$",
    "degrau": "Degraus de 60 s",
    "exponencial": "Exponencial saturante",
}


@dataclass(frozen=True)
class LeiAtraso:
    """L em US$/dia por US$1 milhão de limite; atraso em segundos.

    A = c 60^beta é comum a todas as formas. A exponencial também coincide
    com a potência ajustada em 1.800 s. O degrau é contínuo à direita:
    A floor(d/60)^beta, portanto não cobra atrasos menores que 60 s.
    """

    c: float
    beta: float
    forma: str = "potencia_ajustada"

    def __post_init__(self):
        if self.c <= 0 or not 0 < self.beta < 1:
            raise ValueError("A calibração exige c>0 e 0<beta<1.")
        if self.forma not in FORMAS:
            raise ValueError(f"Forma desconhecida: {self.forma}")

    @property
    def ancora_60(self) -> float:
        return self.c * 60**self.beta

    @property
    def escala_exponencial_s(self) -> float:
        # A razão varia monotonicamente de 1 a 30 quando a escala cresce.
        alvo = 30**self.beta
        return float(np.exp(brentq(
            lambda log_s: np.expm1(-1800 / np.exp(log_s))
            / np.expm1(-60 / np.exp(log_s)) - alvo,
            np.log(0.01), np.log(1e9),
        )))

    def __call__(self, atraso_s):
        d = np.asarray(atraso_s, dtype=float)
        if np.any(d < 0):
            raise ValueError("Atraso não pode ser negativo.")
        if self.forma == "potencia_ajustada":
            return self.c * d**self.beta
        if self.forma == "potencia_05":
            return self.ancora_60 * (d / 60) ** 0.5
        if self.forma == "potencia_1":
            return self.ancora_60 * d / 60
        if self.forma == "degrau":
            return self.ancora_60 * np.floor(d / 60) ** self.beta
        s = self.escala_exponencial_s
        return self.ancora_60 * np.expm1(-d / s) / np.expm1(-60 / s)


def equilibrio(tc, T, lei, limite=LIMITE_MESA_MILHOES):
    """Teto e metas condicionais, sem atribuir um preço comercial ao FTQC.

    r*=T/tc é uma exigência de throughput médio; não substitui o tempo
    físico estimado em E3 com profundidade e fábricas de estados mágicos.
    X nos cenários sem capacidade de recálculo por minuto é apenas um valor
    formal do modelo; a coluna de viabilidade identifica essa restrição.
    A taxa-meta é inf{r>=r*: p*(r)>=preço-meta}, não a raiz de uma igualdade:
    no cenário degrau o preço-limite pode ultrapassar a meta num salto.
    """
    Cc = tc * PRECO_CLASSICO_S
    custo = lambda atraso: float(lei(atraso)) * limite / RECALCULOS_DIA
    teto = custo(tc)
    r_star = T / tc
    preco = lambda taxa: (Cc + teto - custo(T / taxa)) * taxa / T
    # Para r>=r*, X(r)>=C_c>0; como L é não decrescente, p*(r) é monótono.
    # O custo clássico positivo garante um limite superior factível, inclusive
    # no cenário degrau. Bisseção pela desigualdade mantém lo não factível e
    # hi factível, mesmo se houver saltos (brentq não oferece essa garantia).
    escala = 2.0
    while preco(r_star * escala) < PRECO_META_S and escala < 1e14:
        escala *= 2
    if preco(r_star * escala) < PRECO_META_S:
        raise RuntimeError("Não foi encontrado limite superior factível para a taxa-meta.")
    lo, hi = r_star, r_star * escala
    if preco(lo) >= PRECO_META_S:
        hi = lo
    else:
        for _ in range(128):
            meio = np.sqrt(lo) * np.sqrt(hi)
            if meio <= lo or meio >= hi:
                break
            if preco(meio) >= PRECO_META_S:
                hi = meio
            else:
                lo = meio
            if hi / lo - 1 <= 1e-12:
                break
    r_meta = hi
    saida = {
        "C_c": Cc, "teto_dR": teto, "X_max": Cc + teto,
        "limite_milhoes": limite, "cadencia_alvo_s": 60,
        "L_tau_c_fora_intervalo_medido": bool(tc < 60 or tc > 1800),
        "p_T_max": (Cc + teto) / T, "r_estrela": r_star,
        "preco_meta_usd_s": PRECO_META_S, "r_meta_preco": r_meta,
        "r_meta_limite_inferior": lo,
        "preco_no_r_meta_usd_s": preco(r_meta),
        "preco_no_limite_inferior_usd_s": preco(lo),
        "r_meta_sobre_r_estrela": r_meta / r_star,
        "ganho_anual_max_condicional": teto * RECALCULOS_DIA * 252,
    }
    for r in TAXAS_T:
        tau = T / r
        sufixo = f"{r:.0e}"
        saida[f"tau_q_s_{sufixo}"] = tau
        saida[f"L_tau_q_fora_intervalo_medido_{sufixo}"] = bool(tau < 60 or tau > 1800)
        saida[f"X_{sufixo}"] = Cc + teto - custo(tau)
        saida[f"recalculo_1min_viavel_{sufixo}"] = bool(tau <= 60)
        saida[f"termina_no_pregao_{sufixo}"] = bool(tau <= PREGAO_S)
    return saida


def validar_formas(lei_base):
    """Verificações da calibração e dos limites, não ajuste aos subminutos."""
    grade = np.r_[0.0, np.geomspace(1e-4, 1e6, 400)]
    for forma in FORMAS:
        lei = LeiAtraso(lei_base.c, lei_base.beta, forma)
        valores = lei(grade)
        if lei(0) != 0 or np.any(np.diff(valores) < -1e-9):
            raise AssertionError(f"L(0) ou monotonicidade inválidos: {forma}")
        np.testing.assert_allclose(lei(60), lei_base(60), rtol=1e-12)
    np.testing.assert_allclose(
        LeiAtraso(lei_base.c, lei_base.beta, "exponencial")(1800),
        lei_base(1800), rtol=1e-10,
    )


def gerar_saidas(raiz=RAIZ):
    tq = pd.read_csv(raiz / "dados/tau_q.csv")
    tq = tq[tq["carga"] != "generica"]
    cb = pd.read_csv(raiz / "dados/backtest_c_beta.csv")
    parametros = cb.groupby("N")[["c", "beta", "c_es", "beta_es"]].median()
    linhas, calibracao = [], []
    for N, p in parametros.iterrows():
        base = LeiAtraso(p.c, p.beta)
        validar_formas(base)
        calibracao.append({
            "N": N, "c": p.c, "beta": p.beta, "ancora_60_usd_dia": base(60),
            "ancora_1800_usd_dia": base(1800),
            "escala_exponencial_s": base.escala_exponencial_s,
            "limiar_degrau_s": 60,
        })
    for _, r in tq.iterrows():
        N = int(r.N)
        p = parametros.loc[min(N, 64)]
        for forma in FORMAS:
            lei = LeiAtraso(p.c, p.beta, forma)
            linhas.append({
                "N": N, "eps": r.eps, "carga": r.carga, "forma_L": forma,
                "natureza_resultado": "cenario_condicional",
                "N_calibracao_L": min(N, 64),
                "tau_c_s": r.tau_c_s, "T_q": r.T_total,
                **equilibrio(r.tau_c_s, r.T_total, lei),
            })
    cenarios = pd.DataFrame(linhas)
    cenarios.to_csv(raiz / "dados/cenarios_forma_L.csv", index=False)
    base = cenarios[cenarios.forma_L == "potencia_ajustada"].copy()
    base.to_csv(raiz / "dados/equilibrio.csv", index=False)
    pd.DataFrame(calibracao).to_csv(raiz / "dados/calibracao_formas_L.csv", index=False)

    sensibilidade = []
    selecao = tq[(tq.eps == 0.01) & (tq.carga == "fator unico")].set_index("N")
    for N in (8, 32, 64):
        tc, T = selecao.loc[N, ["tau_c_s", "T_total"]]
        p = parametros.loc[N]
        casos = {"perda media, mediana": (p.c, p.beta, 100.0),
                 "ES 97,5%, mediana": (p.c_es, p.beta_es, 100.0)}
        g = cb[cb.N == N].dropna(subset=["c", "beta"])
        if len(g) > 1:
            tetos = g.c * tc**g.beta
            for q in (0.25, 0.75):
                i = (tetos - tetos.quantile(q)).abs().idxmin()
                casos[f"carteira quartil {q:.0%}"] = (g.loc[i, "c"], g.loc[i, "beta"], 100.0)
        for limite in (1.0, 10.0, 1000.0):
            casos[f"limite US$ {limite:g} milhoes"] = (p.c, p.beta, limite)
        for nome, (c, beta, limite) in casos.items():
            sensibilidade.append({
                "N": N, "caso": nome, "forma_L": "potencia_ajustada",
                "natureza_resultado": "cenario_condicional", "limite_milhoes": limite,
                **equilibrio(tc, T, LeiAtraso(c, beta), limite),
            })
    pd.DataFrame(sensibilidade).to_csv(raiz / "dados/sensibilidade.csv", index=False)
    return base, cenarios


if __name__ == "__main__":
    base, cenarios = gerar_saidas()
    print("E4: cenários condicionais calculados; preço-meta hipotético de US$1,60/s.")
    print(cenarios[(cenarios.N == 64) & (cenarios.eps == 0.01)
                   & (cenarios.carga == "fator unico")]
          [["forma_L", "X_max", "r_meta_sobre_r_estrela"]].to_string(index=False))
