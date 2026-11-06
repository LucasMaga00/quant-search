"""Carteira sintética comum aos notebooks: por ação, 5 straddles vendidos (K = 10) com hedge de delta.

Parâmetros iguais para todas as ações; o tempo de cálculo depende de N, K e M, não de quais ações.
"""
import numpy as np
from scipy.special import ndtr, ndtri
from scipy.stats import qmc

S0 = 100.0      # preço inicial
SIGMA = 0.25    # volatilidade anual
RHO = 0.3       # correlação entre cada par de ações
R = 0.04        # taxa livre de risco anual
VENC = 0.25     # vencimento das opções, em anos
DT = 1 / 252    # horizonte do VaR: 1 dia útil
ALPHA = 0.99
STRIKES = np.array([0.90, 0.95, 1.00, 1.05, 1.10])  # 5 straddles por ação: K = 10
K = 2 * len(STRIKES)
BLOCO = 4096    # cenários reavaliados por vez, para limitar a memória


def montar_carteira(N):
    """Retorna (ativo, strike, call, qtd) por opção e acoes (quantidade de cada ação no hedge)."""
    ativo = np.repeat(np.arange(N), K)
    strike = np.tile(np.repeat(S0 * STRIKES, 2), N)
    call = np.tile([True, False], N * len(STRIKES))
    qtd = -np.ones(N * K)
    d1 = (np.log(1 / STRIKES) + (R + SIGMA**2 / 2) * VENC) / (SIGMA * np.sqrt(VENC))
    acoes = np.full(N, (2 * ndtr(d1) - 1).sum())   # zera o delta dos straddles vendidos
    return ativo, strike, call, qtd, acoes


def black_scholes(S, K_, T, call):
    d1 = (np.log(S / K_) + (R + SIGMA**2 / 2) * T) / (SIGMA * np.sqrt(T))
    d2 = d1 - SIGMA * np.sqrt(T)
    preco_call = S * ndtr(d1) - K_ * np.exp(-R * T) * ndtr(d2)
    return np.where(call, preco_call, preco_call - S + K_ * np.exp(-R * T))  # put pela paridade


def normais(M, N, metodo, semente):
    if metodo == "mc":
        return np.random.default_rng(semente).standard_normal((M, N))
    u = qmc.Sobol(d=N, scramble=True, seed=semente).random(M)
    return ndtri(np.clip(u, 1e-10, 1 - 1e-10))   # o Sobol pode gerar 0 exato, que viraria -inf


def preco_em_1_dia(z):
    """Preço da ação em 1 dia para um choque normal padrão z."""
    return S0 * np.exp((R - SIGMA**2 / 2) * DT + SIGMA * np.sqrt(DT) * z)


def perdas(N, M, metodo, semente, carteira):
    """Perda da carteira em 1 dia em M cenários, com reavaliação completa das N x K opções."""
    ativo, strike, call, qtd, acoes = carteira
    C = np.full((N, N), RHO)
    np.fill_diagonal(C, 1.0)
    Z = normais(M, N, metodo, semente) @ np.linalg.cholesky(C).T
    v0 = black_scholes(S0, strike, VENC, call) @ qtd + acoes.sum() * S0
    perda = np.empty(M)
    for i in range(0, M, BLOCO):
        S1 = preco_em_1_dia(Z[i:i + BLOCO])
        perda[i:i + BLOCO] = v0 - (black_scholes(S1[:, ativo], strike, VENC - DT, call) @ qtd + S1 @ acoes)
    return perda


def calcular_var(N, M, metodo, semente, carteira):
    return np.quantile(perdas(N, M, metodo, semente, carteira), ALPHA)


def perda_por_acao(z):
    """Perda do bloco de uma ação (K opções e hedge) para choques normais padrão z da ação."""
    ativo, strike, call, qtd, acoes = montar_carteira(1)
    S1 = preco_em_1_dia(np.asarray(z, dtype=float))[..., None]
    v0 = black_scholes(S0, strike, VENC, call) @ qtd + acoes[0] * S0
    return v0 - (black_scholes(S1, strike, VENC - DT, call) @ qtd + S1[..., 0] * acoes[0])


if __name__ == "__main__":
    # a soma das perdas por ação reproduz a reavaliação completa (a carteira é separável por ação)
    N, M = 3, 1000
    car = montar_carteira(N)
    C = np.full((N, N), RHO)
    np.fill_diagonal(C, 1.0)
    Z = normais(M, N, "mc", 0) @ np.linalg.cholesky(C).T
    assert np.allclose(perdas(N, M, "mc", 0, car), perda_por_acao(Z).sum(1))
    print("ok")
