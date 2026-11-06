# Computação quântica no setor financeiro

Pesquisa acadêmica sobre o custo de equilíbrio da estimação quântica de amplitude no recálculo intradiário do VaR 99% de 1 dia de carteiras de opções, em função do número de ações na carteira. O [artigo](artigo.md) traz pergunta, hipóteses, modelo, metodologia e os resultados dos quatro experimentos.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| [`artigo.md`](artigo.md) | o artigo |
| [`referencias.bib`](referencias.bib) | referências em BibTeX |
| [`figuras/`](figuras) | figuras do artigo, gravadas pelos notebooks |
| [`codigo/carteira.py`](codigo/carteira.py) | carteira sintética e precificação, comum aos notebooks 1 e 3 |
| [`codigo/baixar_dados.py`](codigo/baixar_dados.py) | download dos dados de mercado da Alpaca, usados no notebook 2 |
| [`codigo/1_var_classico.ipynb`](codigo/1_var_classico.ipynb) | E1: VaR por Monte Carlo e quasi-Monte Carlo, mede tau_c(N) |
| [`codigo/2_backtest.ipynb`](codigo/2_backtest.ipynb) | E2: backtest do custo do atraso, estima c e beta de L(d) = c * d^beta |
| [`codigo/3_var_quantico.ipynb`](codigo/3_var_quantico.ipynb) | E3: modelo de recursos quânticos, estima T_q(N) e a taxa de portas T de empate |
| [`codigo/4_equilibrio.ipynb`](codigo/4_equilibrio.ipynb) | E4: custo de equilíbrio, combina os três experimentos |
| [`dados/`](dados) | saídas dos notebooks em CSV; as barras de 1 minuto e `dados/b3/` ficam fora do git |

## Como rodar

Na raiz do repositório:

```
uv run --with-requirements requirements.txt jupyter lab
```

Sem `uv`: `pip install -r requirements.txt` e `jupyter lab`. Os notebooks ficam em `codigo/` e rodam na ordem do número; cada um lê as saídas dos anteriores em `dados/`.

1. `codigo/1_var_classico.ipynb`: cerca de 8 minutos, grava `dados/tau_c.csv`.
2. `codigo/baixar_dados.py`: precisa de um `.env` na raiz com `ALPACA_KEY` e `ALPACA_SECRET` (conta grátis da Alpaca). Leva cerca de 80 minutos e grava `dados/barras_1m.csv.gz`.
   ```
   uv run --env-file .env codigo/baixar_dados.py 2024-11-01 2026-11-01 64
   ```
3. `codigo/2_backtest.ipynb`: cerca de 4 minutos, grava `dados/backtest_L.csv` e `dados/backtest_c_beta.csv`.
4. `codigo/3_var_quantico.ipynb`: cerca de 30 segundos, grava `dados/tau_q.csv`.
5. `codigo/4_equilibrio.ipynb`: segundos, grava `dados/equilibrio.csv`.
