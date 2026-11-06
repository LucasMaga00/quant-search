"""Baixa da Alpaca os dados do backtest: contratos de opções (base para K) e barras de 1 minuto SIP
(consolidadas de todas as bolsas dos EUA). Chaves em .env (ALPACA_KEY, ALPACA_SECRET).

uv run --env-file .env codigo/baixar_dados.py   (a partir da raiz do repositório) 2024-11-01 2026-11-01 64
  -> dados/opcoes_por_acao.csv   contratos por ação, ordenados por open interest
  -> dados/barras_1m.csv.gz      barras de 1 minuto das 64 ações com mais open interest
"""
import csv, datetime, gzip, json, os, sys, urllib.parse, urllib.request
from pathlib import Path

INICIO, FIM, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
CABECALHO = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET"]}

# Candidatas: grandes empresas americanas com opções líquidas; o ranking abaixo escolhe as N com mais open interest
CANDIDATAS = """AAPL MSFT NVDA AMZN GOOGL META TSLA AVGO JPM LLY V UNH XOM MA JNJ PG HD COST ABBV WMT NFLX CRM BAC
ORCL CVX KO MRK AMD PEP ADBE TMO LIN ACN MCD CSCO ABT WFC DIS INTC IBM QCOM GE CAT VZ TXN AMGN PFE NOW INTU
CMCSA PM UBER GS MS T SPGI ISRG HON RTX UNP BKNG LOW NEE AMAT BA PLTR MU SBUX C BLK DE MDT GILD LMT SCHW AXP
PYPL MMM CVS MO SO DUK F GM COIN SHOP SNOW PANW CRWD ABNB COP NKE TGT""".split()


def paginas(url, params, chave):
    """Itera as páginas de um endpoint da Alpaca, seguindo next_page_token."""
    params = dict(params)
    while True:
        pedido = urllib.request.Request(f"{url}?{urllib.parse.urlencode(params)}", headers=CABECALHO)
        corpo = json.load(urllib.request.urlopen(pedido, timeout=60))
        yield corpo[chave]
        if not corpo.get("next_page_token"):
            return
        params["page_token"] = corpo["next_page_token"]


Path("dados").mkdir(exist_ok=True)
hoje = datetime.date.today()
resumo = []
for acao in CANDIDATAS:
    contratos = [c for pagina in paginas("https://paper-api.alpaca.markets/v2/options/contracts", {
        "underlying_symbols": acao, "status": "active", "limit": 10000,
        "expiration_date_gte": hoje.isoformat(), "expiration_date_lte": (hoje + datetime.timedelta(days=730)).isoformat(),
    }, "option_contracts") for c in pagina]
    oi = [int(c.get("open_interest") or 0) for c in contratos]
    resumo.append({"acao": acao, "contratos": len(oi), "com_oi": sum(x > 0 for x in oi),
                   "com_oi_1000": sum(x >= 1000 for x in oi), "oi_total": sum(oi)})
resumo.sort(key=lambda r: -r["oi_total"])
with open("dados/opcoes_por_acao.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(resumo[0]))
    w.writeheader()
    w.writerows(resumo)
acoes = [r["acao"] for r in resumo[:N]]
print("ações:", " ".join(acoes))

with gzip.open("dados/barras_1m.csv.gz", "wt", newline="") as f:
    w = csv.writer(f)
    w.writerow(["acao", "t", "o", "h", "l", "c", "v"])
    for pagina in paginas("https://data.alpaca.markets/v2/stocks/bars", {
        "symbols": ",".join(acoes), "timeframe": "1Min", "start": INICIO, "end": FIM,
        "feed": "sip", "adjustment": "split", "limit": 10000,
    }, "bars"):
        for acao, barras in pagina.items():
            w.writerows([acao, b["t"], b["o"], b["h"], b["l"], b["c"], b["v"]] for b in barras)
print("ok")
