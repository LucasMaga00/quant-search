# Proposta inicial de pesquisa

## 1. Título provisório

Custo de equilíbrio da estimação quântica de amplitude no recálculo intradiário do VaR de carteiras de opções

## 2. Problema de pesquisa

Mesas de operações com opções acompanham o risco da carteira ao longo do pregão. O VaR 99% de 1 dia mede a perda que a carteira pode sofrer em um dia, mas pode ser recalculado muitas vezes durante o pregão, a cada movimento relevante do mercado. Como o valor das opções não varia linearmente com o preço das ações, esse cálculo costuma ser feito por simulação de Monte Carlo. Enquanto ele não termina, a mesa decide com uma estimativa de risco defasada, e um limite de risco estourado só é percebido, e protegido com hedge, depois que a perda já cresceu.

A estimação quântica de amplitude precisa de menos amostras que o Monte Carlo clássico para atingir o mesmo erro, o que abre a possibilidade de recalcular o VaR mais rápido [4](https://doi.org/10.1038/s41534-019-0130-6). A vantagem vem da precisão, e o tamanho da carteira trabalha contra ela: para cada ação adicionada, o circuito precisa carregar mais uma dimensão da distribuição de preços, e essa carga consome qubits e portas. Além disso, o tempo de resposta depende do hardware, da correção de erros, da fila e da rede, e a execução quântica custa mais que a clássica [2](https://doi.org/10.1109/JPROC.2025.3574102), [3](https://doi.org/10.22331/q-2021-06-01-463).

O problema investigado tem duas partes. A primeira é saber até quantas ações na carteira a estimação quântica de amplitude ainda calcula o VaR mais rápido que o Monte Carlo clássico, considerando a carga dos dados. A segunda é saber quanto vale, em dinheiro, recalcular o VaR mais cedo, e qual custo a execução quântica precisa atingir para que esse valor cubra a diferença de custo. A literatura estima recursos e tempos de execução, mas não diz quanto vale ter a estimativa de risco um segundo antes. Este trabalho mede esse valor com um modelo de decaimento calibrado em dados históricos.

Neste trabalho, há **viabilidade técnica** para uma carteira de N ações quando a estimação quântica de amplitude entrega o VaR com o mesmo erro do método clássico em menos tempo. Há **viabilidade econômica** quando o ganho obtido por recalcular o VaR mais cedo supera o custo adicional da execução quântica. O **custo de equilíbrio** X(N) é o custo máximo por execução quântica que mantém essa condição para uma carteira de N ações. A **ampliação do acesso** é tratada como a trajetória do custo de acesso à computação quântica, por serviços em nuvem ou infraestrutura própria, em direção a X(N).

## 3. Pergunta de pesquisa

**Para uma carteira de opções sobre N ações cujo VaR 99% de 1 dia é recalculado ao longo do pregão, quanto a execução quântica precisa custar para que o ganho de recalcular mais rápido cubra a diferença de custo em relação ao Monte Carlo clássico, e até qual N essa vantagem existe?**

## 4. Objetivo geral

Estimar, em função do número de ações N, o custo de equilíbrio a partir do qual o recálculo intradiário do VaR 99% de 1 dia de uma carteira de opções por estimação quântica de amplitude se torna economicamente vantajoso em relação ao Monte Carlo clássico, e projetar em que horizonte esse custo pode ser atingido.

## 5. Objetivos específicos

1. Implementar o cálculo do VaR 99% de 1 dia de uma carteira de opções sobre N ações por Monte Carlo clássico, quasi-Monte Carlo e estimação quântica de amplitude, com o mesmo erro-alvo.
2. Medir em simulador, para valores pequenos de N, os qubits, as portas e a profundidade do circuito quântico, separando a carga da distribuição do restante, e extrapolar esses recursos para valores maiores de N.
3. Estimar os tempos de resposta clássico e quântico em função de N, incluindo fila e rede, e os custos de cada execução.
4. Calibrar o modelo de decaimento com um backtest do recálculo intradiário do VaR e do hedge em dados históricos, simulando diferentes atrasos.
5. Calcular X(N), identificar a faixa de N em que há vantagem de tempo e analisar a sensibilidade dos resultados às premissas.
6. Projetar, em cenários de evolução do hardware, dos custos de acesso e dos métodos clássicos, quando o custo quântico pode atingir X(N), incluindo cenários em que isso não ocorre no horizonte considerado.

## 6. Hipóteses

**H1:** Existe um número de ações N* acima do qual o tempo de carga da distribuição faz a estimação quântica de amplitude levar tanto ou mais tempo que o Monte Carlo clássico para atingir o mesmo erro, de modo que a vantagem de tempo e o ganho do recálculo mais rápido desaparecem.

**H0:** Na faixa de N testada, a estimação quântica de amplitude é mais rápida que o Monte Carlo clássico para todo N.

O valor de N* depende do cenário de hardware, e por isso a hipótese será testada em cada cenário. A análise não pressupõe que a computação quântica se tornará economicamente vantajosa no período investigado. Se nenhum cenário mostrar viabilidade, esse também é um resultado válido.

## 7. Resumo inicial

A estimação quântica de amplitude precisa de menos amostras que o Monte Carlo clássico para atingir o mesmo erro, o que poderia acelerar o recálculo intradiário do VaR de carteiras de opções. A execução quântica, porém, custa mais, e o circuito que carrega a distribuição de preços cresce com o número de ações. Este trabalho investiga, em função do número de ações N, quanto a execução quântica precisa custar para que o ganho de recalcular o VaR 99% de 1 dia mais rápido cubra essa diferença de custo. O VaR será calculado por Monte Carlo, quasi-Monte Carlo e estimação quântica de amplitude com o mesmo erro, e os recursos do circuito quântico, com a carga separada do restante, serão medidos em simulador para N pequeno e extrapolados. O valor de recalcular mais cedo será estimado por um modelo de decaimento, com o valor da informação instantânea e a meia-vida da estimativa de risco como parâmetros, calibrado por um backtest com atrasos simulados. O resultado é a curva do custo de equilíbrio X(N), a faixa de N em que há vantagem de tempo e uma projeção condicional de quando o custo quântico pode atingir X(N). Por se tratar de uma proposta inicial, ainda não há resultados.

**Palavras-chave:** computação quântica; estimação quântica de amplitude; Value at Risk; carteira de opções; custo de equilíbrio.

## 8. Abstract inicial

Quantum amplitude estimation needs fewer samples than classical Monte Carlo to reach the same error, which could speed up intraday recalculation of the VaR of option portfolios. Quantum execution, however, costs more, and the circuit that loads the price distribution grows with the number of stocks. This study investigates, as a function of the number of stocks N, how much quantum execution must cost for the gain from recalculating the 1-day 99% VaR faster to cover that cost difference. VaR will be computed by Monte Carlo, quasi-Monte Carlo, and quantum amplitude estimation at the same error, and the resources of the quantum circuit, with data loading separated from the rest, will be measured in a simulator for small N and extrapolated. The value of recalculating earlier will be estimated with a decay model, parameterized by the value of instantaneous information and the half-life of the risk estimate, and calibrated through a backtest with simulated delays. The outputs are the break-even cost curve X(N), the range of N with a time advantage, and a conditional projection of when quantum cost may reach X(N). As this is an initial research proposal, it reports no findings.

**Keywords:** quantum computing; quantum amplitude estimation; Value at Risk; option portfolio; break-even cost.

## 9. Introdução

A literatura sobre computação quântica para finanças examina como algoritmos quânticos poderiam contribuir para modelagem estocástica, otimização e aprendizado de máquina. A revisão de Herman et al. (2023) apresenta aplicações e limitações dessas abordagens e inclui a análise de risco por simulação entre elas [1](https://doi.org/10.1038/s42254-023-00603-1).

Woerner e Egger (2019) propõem usar a estimação quântica de amplitude para calcular *Value at Risk* e *Conditional Value at Risk*. O algoritmo converge mais rápido que a simulação de Monte Carlo clássica: para um erro-alvo eps, o número de amostras cai da ordem de 1/eps^2 para a ordem de 1/eps. Os autores representam a distribuição de incerteza com um circuito de carga e discutem como a convergência se relaciona com a profundidade do circuito [4](https://doi.org/10.1038/s41534-019-0130-6). O custo desse circuito de carga cresce com o número de variáveis de risco, que, numa carteira de opções, inclui uma variável por ação.

Chakrabarti et al. (2021) estimam os recursos necessários para obter vantagem quântica na precificação de derivativos e identificam obstáculos de implementação. O estudo mostra que a viabilidade depende do número de qubits lógicos, da profundidade dos circuitos e do tempo de execução, e não pode ser inferida apenas da complexidade assintótica do algoritmo [3](https://doi.org/10.22331/q-2021-06-01-463). O modelo de Choi, Moses e Thompson (2025) chega a uma conclusão parecida em termos gerais: reduzir o número de operações não garante menor tempo de solução, porque o resultado depende da combinação entre algoritmo, hardware e escala do problema [2](https://doi.org/10.1109/JPROC.2025.3574102). Mejia et al. (2025), em um preprint, apresentam uma ferramenta que compara vantagem econômica quântica sob premissas variáveis de hardware, correção de erros, custos e algoritmos, sem fixar uma data única que valha para qualquer aplicação [5](https://doi.org/10.48550/arXiv.2508.21031).

Esses trabalhos medem tempo, qubits e profundidade de circuito, mas não convertem uma resposta mais rápida em retorno financeiro, e não medem como a carga dos dados limita a vantagem quando a carteira cresce. Em uma mesa de opções, uma estimativa de risco perde valor conforme o mercado se move: quanto mais tarde o VaR atualizado chega, mais tarde vem o hedge.

Este trabalho compara o recálculo intradiário do VaR 99% de 1 dia de uma carteira de opções por estimação quântica de amplitude e por métodos clássicos, em função do número de ações, e converte a diferença de tempo em ganho financeiro com um modelo de decaimento calibrado em dados históricos. As contribuições pretendidas são:

1. a medição da parcela de recursos do circuito quântico gasta na carga da distribuição em função do número de ações, para o cálculo do VaR de carteiras de opções;
2. um modelo que converte o tempo de recálculo do VaR em ganho financeiro, com parâmetros calibrados por backtest;
3. a curva do custo de equilíbrio X(N) e a faixa de N em que existe vantagem de tempo, com uma projeção condicional de quando o custo quântico pode atingir X(N);
4. código e dados em repositório público, para que os resultados possam ser reproduzidos.

## 10. Modelo proposto

Para uma carteira de N ações, o valor de uma estimativa de risco cai com o tempo que se leva para obtê-la:

```
V(tau) = V0 * exp(-lambda * tau),    lambda = ln(2) / h

dR(N) = V0 * ( exp(-lambda * tau_q(N)) - exp(-lambda * tau_c(N)) )

Adoção vantajosa quando:   dR(N) > C_q(N) - C_c(N)
Custo de equilíbrio:       X(N) = C_c(N) + dR(N)
```

Os termos do modelo são:

- V0: valor de ter o VaR atualizado instantaneamente, em reais por recálculo;
- h: meia-vida da estimativa de risco, o tempo em que ela perde metade do valor;
- tau_c(N) e tau_q(N): tempo total até o VaR no método clássico e no quântico, somando cálculo, fila e rede, para o mesmo erro-alvo; tau_q(N) inclui a carga da distribuição;
- C_c(N) e C_q(N): custo de uma execução em cada plataforma;
- dR(N): ganho por recálculo obtido com a resposta quântica;
- X(N): custo máximo por execução quântica que ainda torna a adoção vantajosa.

Para os valores de N em que tau_q(N) é maior ou igual a tau_c(N), dR(N) é nulo ou negativo, e a execução quântica só compensaria se custasse menos que a clássica. O menor N em que isso acontece é o N* da hipótese H1.

## 11. Metodologia

A pesquisa combina implementação em simulador, um backtest de calibração e análise de cenários.

1. Cálculo do VaR: os preços das ações serão modelados por movimento browniano geométrico correlacionado, e a carteira terá opções europeias sobre essas ações. O VaR 99% de 1 dia será calculado por Monte Carlo, por quasi-Monte Carlo e por estimação quântica de amplitude, com o mesmo erro-alvo. Para caber no circuito, a perda da carteira em função dos preços será aproximada por funções lineares por partes, e o erro dessa aproximação será medido contra a reavaliação completa no método clássico.
2. Recursos quânticos: o circuito será implementado no Qiskit e executado no simulador Aer para N pequeno, limitado pela memória disponível. Para cada N, serão registrados qubits, portas e profundidade, separando a carga da distribuição do restante. O crescimento desses recursos com N será ajustado e extrapolado para valores maiores. Os resultados serão sempre identificados como simulador ideal, simulador com ruído ou estimativa de recursos.
3. Tempos e custos: tau_c(N) virá da execução dos métodos clássicos em hardware documentado. tau_q(N) virá dos recursos medidos, convertidos em tempo por premissas de velocidade de hardware tiradas da literatura [3](https://doi.org/10.22331/q-2021-06-01-463), mais fila e latência de rede. C_c(N) e C_q(N) virão de preços publicados de serviços em nuvem.
4. Backtest de calibração: o recálculo intradiário do VaR e o hedge disparado por estouro de limite serão simulados sobre dados históricos de ações e opções, com diferentes atrasos entre o movimento do mercado e o VaR atualizado. A fonte dos dados será definida conforme disponibilidade e custo. O ajuste de uma exponencial ao resultado do hedge em função do atraso fornecerá V0 e h.
5. Custo de equilíbrio e cenários: com os parâmetros calibrados, o modelo calculará X(N) e N*. A análise de sensibilidade variará h, V0, o erro-alvo e as premissas de hardware. Cenários de evolução do hardware quântico, dos custos de acesso e dos métodos clássicos indicarão quando C_q(N) pode ficar abaixo de X(N), com resultados condicionais às premissas de cada cenário.

As variáveis independentes são o número de ações N, o método (Monte Carlo, quasi-Monte Carlo ou estimação quântica de amplitude), o erro-alvo e o cenário de hardware. As variáveis dependentes são os recursos do circuito, a parcela gasta na carga, tau_c(N), tau_q(N), dR(N) e X(N). Ficam fixos o modelo de preços, a composição da carteira por ação, o nível de confiança de 99%, o horizonte de 1 dia, o período dos dados históricos e as versões de software. Como a estimação quântica de amplitude e o Monte Carlo são aleatórios, cada configuração será repetida com várias sementes, e os resultados serão apresentados com média e desvio padrão.

A referência clássica é o melhor método razoável para uma carteira não linear. Monte Carlo e quasi-Monte Carlo serão ajustados com o mesmo esforço dado ao método quântico. O VaR paramétrico fica de fora porque supõe uma carteira linear.

Se os dados históricos não estiverem disponíveis, V0 e h serão tratados como premissas, e a análise de sensibilidade passará a ser o resultado principal. Se o simulador não comportar valores de N suficientes para ajustar o crescimento dos recursos, a extrapolação usará estimativas analíticas do custo do circuito de carga.

## 12. Ameaças à validade

- Validade interna: as premissas de velocidade do hardware quântico determinam tau_q(N). Por isso, cada resultado será apresentado junto com o cenário de hardware que o produziu.
- Validade externa: a calibração de V0 e h vale para a estratégia de hedge e o período testados. Outras mesas e outros períodos podem ter meias-vidas diferentes, e a análise de sensibilidade indicará o quanto X(N) muda nesses casos.
- Validade de construto: a aproximação linear por partes pode alterar o VaR calculado no circuito. O erro dessa aproximação será reportado junto com os resultados.
- Validade de conclusão: a extrapolação dos recursos para N maior depende de poucos pontos medidos em simulador. O ajuste será apresentado com seu intervalo de confiança.

## Referências

1. HERMAN, Dylan; GOOGIN, Cody; LIU, Xiaoyuan; SUN, Yue; GALDA, Alexey; SAFRO, Ilya; PISTOIA, Marco; ALEXEEV, Yuri. Quantum computing for finance. *Nature Reviews Physics*, v. 5, p. 450-465, 2023. [DOI: 10.1038/s42254-023-00603-1](https://doi.org/10.1038/s42254-023-00603-1).

2. CHOI, Sukwoong; MOSES, William S.; THOMPSON, Neil. The Quantum Tortoise and the Classical Hare: When Will Quantum Computers Outpace Classical Ones and When Will They Be Left Behind? *Proceedings of the IEEE*, v. 113, n. 2, p. 113-124, 2025. [DOI: 10.1109/JPROC.2025.3574102](https://doi.org/10.1109/JPROC.2025.3574102).

3. CHAKRABARTI, Shouvanik; KRISHNAKUMAR, Rajiv; MAZZOLA, Guglielmo; STAMATOPOULOS, Nikitas; WOERNER, Stefan; ZENG, William J. A Threshold for Quantum Advantage in Derivative Pricing. *Quantum*, v. 5, art. 463, 2021. [DOI: 10.22331/q-2021-06-01-463](https://doi.org/10.22331/q-2021-06-01-463).

4. WOERNER, Stefan; EGGER, Daniel J. Quantum risk analysis. *npj Quantum Information*, v. 5, art. 15, 2019. [DOI: 10.1038/s41534-019-0130-6](https://doi.org/10.1038/s41534-019-0130-6).

5. MEJIA, Frederick; GUNDLACH, Hans; LYNCH, Jayson; DUKATZ, Carl; LUCAS, Andrew; CRANE, Eleanor; SHUKLA, Prashant; THOMPSON, Neil. Introducing the Quantum Economic Advantage Online Calculator. *arXiv*, 2508.21031, 2025. **Preprint**; utilizado como referência metodológica complementar. [DOI: 10.48550/arXiv.2508.21031](https://doi.org/10.48550/arXiv.2508.21031).
