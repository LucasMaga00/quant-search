"""As duas figuras do artigo: evidência de L(d) e exigência de throughput.

Execute após E1, E3 e E4: python codigo/figuras_artigo.py.
Os PDFs são vetoriais e os PNGs servem à inspeção. Nenhuma figura extrapola
retas de erro nem usa a carga genérica para definir a escala das curvas úteis.
"""

from __future__ import annotations

import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "quant-mpl-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, ScalarFormatter
import numpy as np
import pandas as pd

from cenarios_atraso import FORMAS, LeiAtraso, RAIZ, ROTULOS


CORES_CARGA = {"cholesky": "#006D8F", "fator unico": "#AE5227"}
CORES_L = {"potencia_ajustada": "#006D8F", "potencia_05": "#86518E",
           "potencia_1": "#AE5227", "degrau": "#48565F", "exponencial": "#427E50"}


def configurar_estilo(raiz):
    fonte = raiz / "codigo/fontes/texgyretermes-regular.otf"
    if not fonte.is_file():
        raise FileNotFoundError(f"Fonte TeX Gyre Termes ausente: {fonte}")
    font_manager.fontManager.addfont(str(fonte))
    nome = font_manager.FontProperties(fname=str(fonte)).get_name()
    plt.rcParams.update({
        "font.family": nome, "font.size": 10, "axes.labelsize": 11,
        "mathtext.fontset": "stix", "axes.spines.top": False,
        "axes.spines.right": False, "axes.linewidth": 0.65,
        "xtick.major.width": 0.65, "ytick.major.width": 0.65,
        "lines.linewidth": 1.6, "legend.frameon": False,
        "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.facecolor": "white",
        "axes.unicode_minus": True,
    })


def salvar(fig, raiz, nome):
    destino = raiz / "figuras"
    destino.mkdir(exist_ok=True)
    fig.savefig(destino / f"{nome}.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(destino / f"{nome}.png", dpi=180, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def tempos_classicos(tc, eps):
    """Usa tempos medidos; identifica a extrapolação do alvo 0,1%.

    A coluna eps permite consumir uma futura medição direta sem mudar a
    figura. Na ausência desse alvo, mantém a lei de erro explicitada em E1.
    """
    if "eps" in tc and np.isclose(tc.eps, eps).any():
        tabela = tc[np.isclose(tc.eps, eps)].copy()
    else:
        tabela = tc.copy()
        if "eps" in tabela:
            tabela = tabela[np.isclose(tabela.eps, 0.01)]
        tabela["tau_c_s"] *= (eps / 0.01) ** (1 / tabela.inclinacao_erro)
    return tabela.pivot(index="N", columns="metodo", values="tau_c_s")


def figura_taxa(raiz=RAIZ):
    tq = pd.read_csv(raiz / "dados/tau_q.csv")
    tc = pd.read_csv(raiz / "dados/tau_c.csv")
    tq = tq[tq.carga.isin(CORES_CARGA)]
    fig = plt.figure(figsize=(7.35, 4.9))
    grade = fig.add_gridspec(2, 2, height_ratios=[3.3, 1], hspace=0.10, wspace=0.15)
    superiores, inferiores = [], []
    taxas = []
    for coluna, eps in enumerate((0.01, 0.001)):
        ax = fig.add_subplot(grade[0, coluna], sharey=superiores[0] if superiores else None)
        baixo = fig.add_subplot(grade[1, coluna], sharex=ax)
        superiores.append(ax)
        inferiores.append(baixo)
        tempos = tempos_classicos(tc, eps)
        for carga, cor in CORES_CARGA.items():
            q = tq[np.isclose(tq.eps, eps) & (tq.carga == carga)].set_index("N")
            for metodo, estilo, marcador in (("mc", "-", "o"), ("qmc", "--", "s")):
                r = q.T_total / tempos.loc[q.index, metodo]
                taxas.extend(r)
                ax.plot(q.index, r, color=cor, linestyle=estilo,
                        marker=marcador, markersize=3.5, markeredgewidth=0.6,
                        markerfacecolor="white")
        for a in (ax, baixo):
            a.set_xscale("log", base=2)
            a.set_yscale("log")
            a.set_xlim(0.8, 650)
            a.set_xticks([1, 4, 16, 64, 256, 512])
            a.xaxis.set_major_formatter(ScalarFormatter())
            a.minorticks_off()
        ax.grid(axis="y", color="#DCE1E4", linewidth=0.5)
        ax.spines.bottom.set_visible(False)
        ax.tick_params(axis="x", bottom=False, labelbottom=False)
        baixo.spines.top.set_visible(False)
        baixo.set_ylim(3e3, 3e8)
        baixo.set_yticks([1e4, 1e6, 1e8])
        for taxa in (1e4, 1e6, 1e8):
            baixo.axhline(taxa, color="#727C82", linestyle=":", linewidth=0.8)
        alvo = "1%" if eps == 0.01 else "0,1%"
        letra = "a" if coluna == 0 else "b"
        baixo.set_xlabel(f"Número de ações, $N$\n({letra}) erro-alvo de {alvo}")
        if coluna == 0:
            ax.set_ylabel(r"Taxa de empate, $r^*$ (portas T/s)")
            baixo.set_ylabel("Hardware\n(portas T/s)", fontsize=9)
        else:
            ax.tick_params(axis="y", labelleft=False)
            baixo.tick_params(axis="y", labelleft=False)
        # Marcas do corte do eixo: as linhas de hardware não comprimem as
        # curvas da região relevante. Os valores estão rotulados à esquerda.
        d = 0.013
        ax.plot((-d, +d), (-d, +d), transform=ax.transAxes, color="#48565F", clip_on=False, lw=0.8)
        baixo.plot((-d, +d), (1-d, 1+d), transform=baixo.transAxes, color="#48565F", clip_on=False, lw=0.8)
    limite_baixo = 10 ** np.floor(np.log10(min(taxas)))
    limite_alto = 10 ** np.ceil(np.log10(max(taxas)))
    for ax in superiores:
        ax.set_ylim(limite_baixo / 1.8, limite_alto * 1.3)
    legenda = [Line2D([], [], color=CORES_CARGA[carga], linestyle=estilo,
                     marker=marcador, markersize=3.5, markerfacecolor="white",
                     label=f"{nome} · {ref}")
               for carga, nome in (("cholesky", "Cholesky"), ("fator unico", "Fator único"))
               for ref, estilo, marcador in (("MC", "-", "o"), ("QMC", "--", "s"))]
    fig.legend(handles=legenda, loc="lower center", bbox_to_anchor=(0.51, -0.035),
               ncol=2, columnspacing=2.3, handlelength=3)
    fig.subplots_adjust(bottom=0.23, top=0.98, left=0.11, right=0.99)
    salvar(fig, raiz, "taxa_empate")


def figura_atraso(raiz=RAIZ):
    # N=64 é uma única carteira e por isso recebe pontos, nunca boxplot.
    observado = pd.read_csv(raiz / "dados/backtest_L.csv")
    observado = observado[(observado.N == 64) & (observado.atraso_min > 0)]
    cb = pd.read_csv(raiz / "dados/backtest_c_beta.csv")
    p = cb[cb.N == 64][["c", "beta"]].median()
    leis = {forma: LeiAtraso(p.c, p.beta, forma) for forma in FORMAS}
    fig, eixos = plt.subplots(1, 2, figsize=(7.35, 3.8), gridspec_kw={"wspace": 0.25})
    subminuto, medido = eixos
    ds = np.geomspace(0.001, 60, 450)
    subminuto.set_facecolor("#F6F3ED")
    for forma in FORMAS:
        if forma == "degrau":
            subminuto.step([ds[0], 60], [0, leis[forma](60)], where="post",
                           color=CORES_L[forma], linestyle="--", label=ROTULOS[forma])
        else:
            subminuto.plot(ds, leis[forma](ds), color=CORES_L[forma],
                           label=ROTULOS[forma])
    subminuto.set_xscale("log")
    subminuto.set_xlim(0.001, 60)
    subminuto.set_ylim(-0.035 * leis["potencia_ajustada"](60),
                      1.08 * leis["potencia_ajustada"](60))
    subminuto.set_xticks([0.001, 0.1, 1, 10, 60])
    subminuto.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}".replace(".", ",")))
    subminuto.set_xlabel("Atraso, $d$ (s)\n(a) Extrapolação: sem observações")
    subminuto.set_ylabel(r"$L(d)$ (US\$/dia por US\$1 milhão de limite)")
    # O painel medido mostra a evidência e o ajuste original. As quatro formas
    # alternativas são cenários de subminuto, não novos ajustes aos dados.
    ds_medido = np.linspace(60, 1800, 350)
    medido.plot(ds_medido / 60, leis["potencia_ajustada"](ds_medido),
                color=CORES_L["potencia_ajustada"])
    medido.scatter(observado.atraso_min, observado.L, s=25,
                   color="#20292E", zorder=3, label="Dados medidos")
    medido.set_xlim(0, 31)
    medido.set_ylim(0, 1.12 * max(observado.L.max(), leis["potencia_ajustada"](1800)))
    medido.set_xticks([1, 5, 10, 20, 30])
    medido.set_xlabel("Atraso, $d$ (min)\n(b) Intervalo medido")
    for ax in eixos:
        ax.grid(axis="y", color="#DCE1E4", linewidth=0.5)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", ".")))
    handles, labels = subminuto.get_legend_handles_labels()
    h_medido, l_medido = medido.get_legend_handles_labels()
    fig.legend(handles + h_medido, labels + l_medido, loc="lower center",
               bbox_to_anchor=(0.51, -0.04), ncol=2, columnspacing=2.0,
               handlelength=2.8, fontsize=9)
    fig.subplots_adjust(bottom=0.33, top=0.98, left=0.10, right=0.99)
    salvar(fig, raiz, "custo_atraso")


def gerar_figuras(raiz=RAIZ):
    configurar_estilo(raiz)
    figura_taxa(raiz)
    figura_atraso(raiz)


if __name__ == "__main__":
    gerar_figuras()
    print("Figuras vetoriais e prévias geradas em figuras/taxa_empate e custo_atraso.")
