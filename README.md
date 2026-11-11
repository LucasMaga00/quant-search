# Computação quântica no setor financeiro

Pesquisa sobre a taxa agregada de portas T necessária para empatar com Monte Carlo e quasi-Monte Carlo, e sobre o teto econômico condicional ao custo de receber o VaR antes. O ganho subminuto é tratado como cenário, pois os dados de mercado têm frequência de um minuto.

O artigo está em [LaTeX no modelo IEEE](artigo.tex), com [PDF para revisão](output/pdf/artigo.pdf). A [versão Markdown](artigo.md) está sincronizada nesta revisão.

## Ambiente e execução

Python 3.12 e dependências com versões fixadas em `requirements.txt`:

```bash
uv run --python 3.12 --with-requirements requirements.txt jupyter lab
```

Alternativamente, crie um ambiente virtual com Python 3.12, execute `pip install -r requirements.txt` e abra `jupyter lab`. Os notebooks ficam em `codigo/` e rodam na ordem 1 a 4. A calibração de E1 pode levar vários minutos; os tempos do artigo vêm da reavaliação completa, com uma thread nas bibliotecas numéricas.

| Etapa | Código | Resultados |
|---|---|---|
| E1: calibração e tempo clássico | `codigo/1_var_classico.ipynb`, `codigo/e1_validacao.py` | `dados/tau_c.csv` e diagnósticos de validação de M |
| E2: backtest observado | `codigo/2_backtest.ipynb` | `dados/backtest_L.csv`, `dados/backtest_c_beta.csv` |
| E3: contagem lógica e estimativa física | `codigo/3_var_quantico.ipynb`, `codigo/recursos_tolerantes_falhas.py` | `dados/tau_q.csv`, recursos lógicos/físicos e premissas |
| Hipóteses reformuladas | `codigo/avaliar_hipoteses.py` | `dados/hipoteses.csv` |
| E4: formas do custo do atraso | `codigo/4_equilibrio.ipynb`, `codigo/cenarios_atraso.py` | `dados/cenarios_forma_L.csv`, `dados/equilibrio.csv`, `dados/sensibilidade.csv` |
| Duas figuras do artigo | `codigo/figuras_artigo.py` | `figuras/custo_atraso.pdf`, `figuras/taxa_empate.pdf` e prévias PNG |

E1 usa cache apenas para as avaliações de erro; os tempos são medidos novamente em série. O erro-alvo de 1% é validado entre 50 sementes. Os tempos clássicos de 0,1% continuam extrapolados e são identificados separadamente.

E3 executa o Microsoft QDK QRE **localmente**, sem Azure, conta ou serviço pago. O estimador recebe os blocos lógicos e dois escalonamentos declarados; calcula duração, correção de erros, qubits físicos e fábricas de estados mágicos em paralelo. Ele não comprova a síntese de um oráculo financeiro completo. O orçamento de falha física é separado dos erros algorítmicos.

O backtest usa VaR delta-gama; o benchmark de tempo usa reavaliação completa. A justificativa e o limite dessa transferência estão no artigo e no notebook E2. As análises monetárias são condicionais a essa aproximação, à regra de corte e à forma de L(d). A referência de US$1,60/s é uma meta hipotética de preço, sem cotação de hardware tolerante a falhas.

## Dados de mercado

Os CSVs derivados já estão no repositório. Para executar E2 desde os preços brutos, é necessário `dados/barras_1m.csv.gz`, que não é versionado. O download usa as credenciais locais `ALPACA_KEY` e `ALPACA_SECRET`, conforme os termos do provedor:

```bash
uv run --env-file .env codigo/baixar_dados.py 2024-11-01 2026-11-01 64
```

O download pode levar cerca de 80 minutos e requer acesso ao feed SIP correspondente. O script consulta o ranking de open interest no momento da execução, portanto uma nova coleta pode mudar o universo de ações. Esta revisão preserva os CSVs derivados da coleta original.

Depois de E1/E3, E4 e as figuras podem ser regenerados sem baixar preços:

```bash
uv run --with-requirements requirements.txt python codigo/cenarios_atraso.py
uv run --with-requirements requirements.txt python codigo/figuras_artigo.py
```

## LaTeX e PDF IEEE

`artigo.tex`, `referencias.bib` e as duas figuras PDF são suficientes para a edição no Overleaf. Selecione XeLaTeX e mantenha a estrutura `figuras/`. A classe usada é `IEEEtran` em modo `conference`; o evento específico pode exigir opções adicionais.

Para compilar localmente com Tectonic 0.17.0 ou latexmk/XeLaTeX:

```bash
python codigo/compilar_artigo.py
```

O PDF é gravado em `output/pdf/artigo.pdf`. O compilador pode precisar baixar pacotes LaTeX na primeira execução. Para indicar um executável fora do PATH, use `--tectonic /caminho/para/tectonic`.

O script de compilação não reescreve a fonte LaTeX. Se a edição for feita em Markdown, a conversão explícita para IEEE usa Pandoc 3.13:

```bash
python codigo/gerar_latex.py --pandoc /caminho/para/pandoc
python codigo/compilar_artigo.py
```

Essa conversão sobrescreve `artigo.tex`; alterações diretas em LaTeX devem ser preservadas antes de usá-la. A fonte TeX Gyre Termes das figuras e sua licença estão em `codigo/fontes/`.
