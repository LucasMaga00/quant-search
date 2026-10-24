# Proposta inicial de pesquisa

## 1. Título provisório

Custo de equilíbrio da estimação quântica de amplitude no recálculo intradiário do VaR de carteiras de opções

## 2. Problema de pesquisa

Mesas de opções recalculam o VaR 99% de 1 dia ao longo do pregão, a cada movimento relevante do mercado. Como o valor das opções não é linear no preço das ações, o cálculo costuma ser feito por Monte Carlo. Enquanto ele roda, a mesa decide com uma estimativa defasada, e um limite de risco estourado só é percebido, e protegido com hedge, depois que a perda cresceu.

A estimação quântica de amplitude atinge o mesmo erro com menos amostras, o que poderia acelerar esse recálculo [4](https://doi.org/10.1038/s41534-019-0130-6). Por outro lado, cada ação adicionada é mais uma dimensão da distribuição que o circuito precisa carregar, e a execução quântica custa mais e depende de hardware, correção de erros, fila e rede [2](https://doi.org/10.1109/JPROC.2025.3574102), [3](https://doi.org/10.22331/q-2021-06-01-463). A literatura estima recursos e tempos, mas não diz quanto vale, em dinheiro, ter o VaR um segundo antes.

Neste trabalho, há **viabilidade técnica** quando a estimação quântica entrega o VaR com o mesmo erro do método clássico em menos tempo, e **viabilidade econômica** quando o ganho de recalcular mais cedo supera o custo adicional. O **custo de equilíbrio** X(N) é o maior custo por execução quântica que mantém essa condição para uma carteira de N ações. A **ampliação do acesso** é a trajetória do custo quântico, em nuvem ou infraestrutura própria, em direção a X(N).

## 3. Pergunta de pesquisa

**Para uma carteira de opções sobre N ações cujo VaR 99% de 1 dia é recalculado ao longo do pregão, quanto a execução quântica precisa custar para que o ganho de recalcular mais rápido cubra a diferença de custo em relação ao Monte Carlo clássico, e até qual N essa vantagem existe?**

## 4. Objetivo geral

Estimar a curva de custo de equilíbrio X(N) do recálculo intradiário do VaR de uma carteira de opções por estimação quântica de amplitude, em relação ao Monte Carlo clássico, e projetar quando o custo quântico pode atingi-la.

## 5. Objetivos específicos

1. Calcular o VaR por Monte Carlo, quasi-Monte Carlo e estimação quântica de amplitude com o mesmo erro-alvo.
2. Medir em simulador os recursos do circuito para N pequeno, separando a carga da distribuição, e extrapolar para N maior.
3. Estimar tempos e custos de execução clássicos e quânticos em função de N.
4. Calibrar o modelo de decaimento com um backtest do recálculo do VaR e do hedge, com atrasos simulados.
5. Calcular X(N) e N* e analisar a sensibilidade às premissas.
6. Projetar, em cenários, quando o custo quântico atinge X(N), incluindo cenários em que isso não ocorre no horizonte considerado.

## 6. Hipóteses

**H1:** Existe um N* acima do qual a carga da distribuição faz a estimação quântica de amplitude levar tanto ou mais tempo que o Monte Carlo clássico para o mesmo erro, eliminando o ganho do recálculo mais rápido.

**H0:** A estimação quântica de amplitude é mais rápida que o Monte Carlo clássico em toda a faixa de N testada.

Como N* depende do cenário de hardware, a hipótese será testada em cada cenário. Se nenhum deles mostrar viabilidade, esse também é um resultado válido.

## 7. Resumo inicial

A estimação quântica de amplitude atinge o mesmo erro do Monte Carlo com menos amostras, o que poderia acelerar o recálculo intradiário do VaR de carteiras de opções. A execução quântica, porém, custa mais, e o circuito que carrega a distribuição de preços cresce com o número de ações N. Este trabalho estima quanto a execução quântica precisa custar, em função de N, para que o ganho de recalcular o VaR 99% de 1 dia mais rápido cubra essa diferença. Os recursos do circuito serão medidos em simulador para N pequeno e extrapolados, e o valor de recalcular mais cedo virá de um modelo de decaimento calibrado por backtest. Os resultados esperados são a curva de custo de equilíbrio X(N), a faixa de N com vantagem de tempo e uma projeção condicional de quando o custo quântico pode atingir essa curva. Por se tratar de uma proposta inicial, ainda não há resultados.

**Palavras-chave:** computação quântica; estimação quântica de amplitude; Value at Risk; carteira de opções; custo de equilíbrio.

## 8. Abstract inicial

Quantum amplitude estimation reaches the same error as Monte Carlo with fewer samples, which could speed up intraday recalculation of the VaR of option portfolios. Quantum execution, however, costs more, and the circuit that loads the price distribution grows with the number of stocks N. This study estimates how much quantum execution must cost, as a function of N, for the gain from recalculating the 1-day 99% VaR faster to cover that difference. Circuit resources will be measured in a simulator for small N and extrapolated, and the value of recalculating earlier will come from a decay model calibrated by backtest. The expected outputs are the break-even cost curve X(N), the range of N with a time advantage, and a conditional projection of when quantum cost may reach that curve. As this is an initial research proposal, it reports no findings.

**Keywords:** quantum computing; quantum amplitude estimation; Value at Risk; option portfolio; break-even cost.

## 9. Introdução

Herman et al. (2023) revisam aplicações da computação quântica em finanças, entre elas a análise de risco por simulação [1](https://doi.org/10.1038/s42254-023-00603-1). Woerner e Egger (2019) usam a estimação quântica de amplitude para calcular *Value at Risk* e *Conditional Value at Risk*: para um erro-alvo eps, o número de amostras cai da ordem de 1/eps^2 para a ordem de 1/eps. Os autores carregam a distribuição de incerteza com um circuito dedicado [4](https://doi.org/10.1038/s41534-019-0130-6). Numa carteira de opções, esse circuito cresce com o número de ações, porque cada ação é uma variável de risco.

Chakrabarti et al. (2021) mostram, para a precificação de derivativos, que a vantagem quântica depende do número de qubits lógicos, da profundidade dos circuitos e do tempo de execução, e não apenas da complexidade assintótica [3](https://doi.org/10.22331/q-2021-06-01-463). Choi, Moses e Thompson (2025) chegam a uma conclusão parecida: menos operações não garantem menos tempo, porque o resultado depende de algoritmo, hardware e escala do problema [2](https://doi.org/10.1109/JPROC.2025.3574102). Mejia et al. (2025), em um preprint, comparam vantagem econômica quântica sob premissas variáveis de hardware, custos e algoritmos, sem fixar uma data única [5](https://doi.org/10.48550/arXiv.2508.21031).

Esses trabalhos não convertem uma resposta mais rápida em retorno financeiro, nem medem como a carga dos dados limita a vantagem quando a carteira cresce. Este trabalho mede as duas coisas no recálculo intradiário do VaR de carteiras de opções. As contribuições pretendidas são:

1. a parcela dos recursos do circuito quântico gasta na carga da distribuição, em função de N;
2. um modelo, calibrado por backtest, que converte o tempo de recálculo do VaR em ganho financeiro;
3. a curva X(N), a faixa de N com vantagem de tempo e uma projeção condicional de quando o custo quântico atinge essa curva;
4. código e dados em repositório público.

## 10. Modelo proposto

O valor de uma estimativa de risco cai com o tempo que se leva para obtê-la:

```
V(tau) = V0 * exp(-lambda * tau),    lambda = ln(2) / h

dR(N) = V0 * ( exp(-lambda * tau_q(N)) - exp(-lambda * tau_c(N)) )

Adoção vantajosa quando:   dR(N) > C_q(N) - C_c(N)
Custo de equilíbrio:       X(N) = C_c(N) + dR(N)
```

- V0: valor de ter o VaR atualizado instantaneamente, em reais por recálculo;
- h: meia-vida da estimativa de risco;
- tau_c(N) e tau_q(N): tempo até o VaR, com o mesmo erro, somando cálculo, fila e rede; tau_q(N) inclui a carga da distribuição;
- C_c(N) e C_q(N): custo de uma execução em cada plataforma;
- dR(N): ganho por recálculo com a resposta quântica.

Quando tau_q(N) é maior ou igual a tau_c(N), dR(N) é nulo ou negativo, e o quântico só compensaria se custasse menos que o clássico. O menor N em que isso acontece é o N* da hipótese H1.

## 11. Metodologia

1. Cálculo do VaR: as ações seguem movimento browniano geométrico correlacionado, e a carteira tem opções europeias sobre elas. O VaR é calculado por Monte Carlo, quasi-Monte Carlo e estimação quântica de amplitude com o mesmo erro-alvo. No circuito, a perda é aproximada por funções lineares por partes, e o erro dessa aproximação é medido contra a reavaliação completa.
2. Recursos quânticos: o circuito é implementado no Qiskit e executado no simulador Aer para N pequeno. Para cada N, registram-se qubits, portas e profundidade, com a carga separada do restante, e o crescimento é extrapolado para N maior. Cada resultado indica se veio de simulador ideal, simulador com ruído ou estimativa de recursos.
3. Tempos e custos: tau_c(N) é medido em hardware documentado; tau_q(N) sai dos recursos medidos, convertidos por premissas de velocidade de hardware da literatura [3](https://doi.org/10.22331/q-2021-06-01-463), mais fila e rede. C_c(N) e C_q(N) vêm de preços publicados de serviços em nuvem.
4. Backtest de calibração: o recálculo do VaR e o hedge disparado por estouro de limite são simulados sobre dados históricos de ações e opções, com fonte a definir, variando o atraso entre o movimento do mercado e o VaR atualizado. O ajuste de uma exponencial ao resultado em função do atraso fornece V0 e h.
5. Custo de equilíbrio e cenários: com V0 e h calibrados, calculam-se X(N) e N*, com sensibilidade a h, V0, erro-alvo e premissas de hardware. Cenários de evolução do hardware, dos custos de acesso e dos métodos clássicos indicam quando C_q(N) pode ficar abaixo de X(N).

As variáveis independentes são N, o método, o erro-alvo e o cenário de hardware. As dependentes são os recursos do circuito, a parcela gasta na carga, tau_c(N), tau_q(N), dR(N) e X(N). Ficam fixos o modelo de preços, a composição da carteira por ação, o nível de 99%, o horizonte de 1 dia, o período dos dados e as versões de software. Cada configuração é repetida com várias sementes, e os resultados são apresentados com média e desvio padrão.

As referências clássicas são o Monte Carlo e o quasi-Monte Carlo, ajustados com o mesmo esforço dado ao método quântico. O VaR paramétrico fica de fora porque supõe uma carteira linear.

Se os dados históricos não estiverem disponíveis, V0 e h viram premissas e a análise de sensibilidade passa a ser o resultado principal. Se o simulador não comportar valores de N suficientes, a extrapolação usará estimativas analíticas do custo do circuito de carga.

## 12. Ameaças à validade

- Interna: tau_q(N) depende das premissas de velocidade do hardware, por isso cada resultado é apresentado com o cenário que o produziu.
- Externa: V0 e h valem para a estratégia de hedge e o período testados; a análise de sensibilidade mostra quanto X(N) muda fora deles.
- Construto: a aproximação linear por partes pode alterar o VaR do circuito, e o erro dela é reportado junto com os resultados.
- Conclusão: a extrapolação para N maior depende de poucos pontos medidos em simulador, e o ajuste é apresentado com intervalo de confiança.

## Referências

1. HERMAN, Dylan; GOOGIN, Cody; LIU, Xiaoyuan; SUN, Yue; GALDA, Alexey; SAFRO, Ilya; PISTOIA, Marco; ALEXEEV, Yuri. Quantum computing for finance. *Nature Reviews Physics*, v. 5, p. 450-465, 2023. [DOI: 10.1038/s42254-023-00603-1](https://doi.org/10.1038/s42254-023-00603-1).

2. CHOI, Sukwoong; MOSES, William S.; THOMPSON, Neil. The Quantum Tortoise and the Classical Hare: When Will Quantum Computers Outpace Classical Ones and When Will They Be Left Behind? *Proceedings of the IEEE*, v. 113, n. 2, p. 113-124, 2025. [DOI: 10.1109/JPROC.2025.3574102](https://doi.org/10.1109/JPROC.2025.3574102).

3. CHAKRABARTI, Shouvanik; KRISHNAKUMAR, Rajiv; MAZZOLA, Guglielmo; STAMATOPOULOS, Nikitas; WOERNER, Stefan; ZENG, William J. A Threshold for Quantum Advantage in Derivative Pricing. *Quantum*, v. 5, art. 463, 2021. [DOI: 10.22331/q-2021-06-01-463](https://doi.org/10.22331/q-2021-06-01-463).

4. WOERNER, Stefan; EGGER, Daniel J. Quantum risk analysis. *npj Quantum Information*, v. 5, art. 15, 2019. [DOI: 10.1038/s41534-019-0130-6](https://doi.org/10.1038/s41534-019-0130-6).

5. MEJIA, Frederick; GUNDLACH, Hans; LYNCH, Jayson; DUKATZ, Carl; LUCAS, Andrew; CRANE, Eleanor; SHUKLA, Prashant; THOMPSON, Neil. Introducing the Quantum Economic Advantage Online Calculator. *arXiv*, 2508.21031, 2025. **Preprint**; utilizado como referência metodológica complementar. [DOI: 10.48550/arXiv.2508.21031](https://doi.org/10.48550/arXiv.2508.21031).
