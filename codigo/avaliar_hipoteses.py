"""Avalia as hipóteses reformuladas no artigo, sem cláusula de confirmação trivial.

H1: inclinação de log(r*)~log(N), 8<=N<=512 e erro1%, maior em
Cholesky que em fator único, nas referências MC e QMC.
H2: r*>1e8 em todos os N, erros e cargas por aritmética, em cada referência.
"""
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]


def avaliar(raiz=RAIZ):
    tc = pd.read_csv(raiz / 'dados/tau_c.csv')
    tq = pd.read_csv(raiz / 'dados/tau_q.csv')
    tq = tq[tq.carga.isin(['cholesky', 'fator unico'])]
    linhas = []
    for metodo in ('mc', 'qmc'):
        tempos = tc[tc.metodo == metodo].set_index('N')
        taxas = []
        for eps in (0.01, 0.001):
            q = tq[np.isclose(tq.eps, eps)].copy()
            t = tempos.loc[q.N, 'tau_c_s'].to_numpy()
            if not np.isclose(eps, 0.01):
                t = t * (eps / 0.01) ** (1 / tempos.loc[q.N, 'inclinacao_erro'].to_numpy())
            q['r_referencia'] = q.T_total.to_numpy() / t
            taxas.append(q)
        taxas = pd.concat(taxas)
        coeficientes = {}
        for carga in ('cholesky', 'fator unico'):
            q = taxas[np.isclose(taxas.eps, 0.01) & (taxas.N >= 8) & (taxas.carga == carga)]
            coeficientes[carga] = np.polyfit(np.log(q.N), np.log(q.r_referencia), 1)[0]
        linhas.append({'hipotese': 'H1', 'referencia': metodo,
                       'inclinacao_cholesky': coeficientes['cholesky'],
                       'inclinacao_fator_unico': coeficientes['fator unico'],
                       'minimo_r_estrela': np.nan, 'contraexemplos': np.nan,
                       'satisfeita_no_modelo': coeficientes['cholesky'] > coeficientes['fator unico']})
        contraexemplos = int((taxas.r_referencia <= 1e8).sum())
        linhas.append({'hipotese': 'H2', 'referencia': metodo,
                       'inclinacao_cholesky': np.nan, 'inclinacao_fator_unico': np.nan,
                       'minimo_r_estrela': taxas.r_referencia.min(),
                       'contraexemplos': contraexemplos,
                       'satisfeita_no_modelo': contraexemplos == 0})
    resultado = pd.DataFrame(linhas)
    resultado.to_csv(raiz / 'dados/hipoteses.csv', index=False)
    return resultado


if __name__ == '__main__':
    print(avaliar().to_string(index=False))
