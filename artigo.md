# Proposta inicial de pesquisa

## 1. Título provisório

Viabilidade técnica e econômica da computação quântica no setor financeiro: condições de adoção e cenários de ampliação do acesso

## 2. Problema de pesquisa

A computação quântica tem sido investigada como alternativa para problemas financeiros de otimização, modelagem de incertezas e processamento numérico. A literatura discute, entre outras aplicações, a otimização de carteiras, a análise de risco e a precificação de ativos e derivativos. Executar um algoritmo quântico, ou demonstrar que ele tem complexidade menor, não basta para mostrar que adotá-lo compensa economicamente para uma organização financeira [1](https://doi.org/10.1038/s42254-023-00603-1), [2](https://doi.org/10.1109/JPROC.2025.3574102).

O problema investigado é como relacionar requisitos técnicos, custos de utilização e benefícios potenciais dessas aplicações, tendo métodos clássicos como referência. A avaliação deve considerar o tamanho do problema, a precisão exigida, o tempo total de processamento e os recursos necessários para obter resultados confiáveis. As estimativas de recursos para precificação de derivativos mostram por que é preciso avaliar a implementação completa, além do ganho algorítmico esperado [3](https://doi.org/10.22331/q-2021-06-01-463).

Neste trabalho, **viabilidade técnica** é a capacidade de executar uma aplicação com a precisão e o prazo exigidos. A **viabilidade econômica** será medida pelo benefício incremental líquido da adoção em relação a uma solução clássica adequada, descontados os custos adicionais. Esse benefício pode vir de despesas computacionais menores, de menor tempo de processamento ou de uma melhoria mensurável na qualidade da solução. Um ganho de desempenho não será tratado automaticamente como aumento de lucro.

A **ampliação do acesso**, associada à ideia de democratização da tecnologia, será analisada inicialmente por três indicadores: custo de utilização, disponibilidade de recursos em serviços de nuvem e necessidade de infraestrutura própria. Esses indicadores entram como possíveis facilitadores da adoção, sem pressupor acesso universal nem benefício econômico garantido.

## 3. Pergunta de pesquisa

**Em quais condições técnicas e econômicas a computação quântica pode se tornar viável para aplicações no setor financeiro, em comparação com métodos clássicos, e como diferentes cenários de evolução tecnológica e ampliação do acesso podem influenciar essa viabilidade ao longo do tempo?**

## 4. Objetivo geral

Investigar as condições técnicas e econômicas para a viabilidade da computação quântica no setor financeiro, considerando seus potenciais benefícios em relação aos métodos clássicos e cenários de ampliação do acesso à tecnologia.

## 5. Objetivos específicos

1. Mapear as aplicações financeiras investigadas na literatura, começando pela otimização de carteiras, pela análise de risco e pela precificação de ativos e derivativos, para escolher um recorte de aprofundamento.
2. Identificar os métodos clássicos de referência e os benefícios atribuídos às abordagens quânticas, separando propostas teóricas, simulações, experimentos em hardware e estimativas de recursos.
3. Levantar os requisitos técnicos e os componentes de custo das aplicações selecionadas, incluindo preparação de dados, execução, tratamento de erros e integração com recursos clássicos, conforme as evidências disponíveis.
4. Definir critérios de comparação que relacionem custo total, tempo de processamento, precisão e qualidade da solução, indicando os casos em que há dados suficientes para estimar benefícios monetários.
5. Construir cenários de evolução tecnológica e de custos de acesso e examinar como eles afetam os limites de viabilidade e, quando os dados permitirem, os horizontes temporais de adoção.
6. Analisar as limitações das estimativas e sua sensibilidade às premissas adotadas, incluindo a possibilidade de não haver viabilidade no horizonte considerado.

## 6. Hipótese

Nesta etapa não há hipótese formal. A pesquisa é exploratória, e a aplicação específica, as variáveis e o modelo de comparação ainda não foram escolhidos. Uma hipótese testável será formulada depois dessa delimitação.

A análise não pressupõe que a computação quântica se tornará economicamente vantajosa no período investigado. Se os cenários examinados não mostrarem viabilidade, esse também é um resultado válido.

## 7. Resumo inicial

A computação quântica tem motivado pesquisas sobre aplicações no setor financeiro, mas identificar possíveis ganhos computacionais exige avaliar, em conjunto, requisitos técnicos e custos de adoção. Este trabalho investiga as condições técnicas e econômicas para a viabilidade da computação quântica nesse setor, considerando benefícios potenciais em relação aos métodos clássicos e cenários de ampliação do acesso à tecnologia. Propõe-se uma pesquisa exploratória baseada em revisão da literatura e análise de cenários, começando pela otimização de carteiras, pela análise de risco e pela precificação de ativos e derivativos. A revisão orientará a escolha de um recorte e o levantamento de indicadores de custo total, tempo de processamento, precisão e qualidade das soluções. A ampliação do acesso será examinada por fatores como custo de utilização, disponibilidade de recursos em nuvem e necessidade de infraestrutura própria. Quando houver dados suficientes, serão estimados limites de viabilidade e horizontes temporais condicionados a premissas explícitas. A contribuição pretendida é um conjunto de critérios para avaliar a adoção da tecnologia que separe potencial algorítmico, execução prática e benefício econômico. Por se tratar de uma proposta inicial, ainda não há resultados nem conclusões sobre a viabilidade das aplicações.

**Palavras-chave:** computação quântica; setor financeiro; viabilidade econômica; vantagem quântica; análise de cenários.

## 8. Abstract inicial

Quantum computing has motivated research into financial applications, but assessing potential computational gains requires weighing technical requirements and adoption costs together. This study investigates the technical and economic conditions under which quantum computing may become viable in the financial sector, considering potential benefits over classical methods and scenarios of broader access to the technology. The study is exploratory, based on a literature review and scenario analysis, and starts with portfolio optimization, risk analysis, and asset and derivative pricing. The review will guide the choice of a narrower scope and the collection of indicators for total cost, processing time, accuracy, and solution quality. Broader access will be examined through usage costs, cloud resource availability, and the need for dedicated infrastructure. Where data allow, feasibility thresholds and time horizons will be estimated under explicit assumptions. The intended contribution is a set of criteria for assessing adoption that separates algorithmic potential, practical execution, and economic benefit. As this is an initial research proposal, it reports no findings or conclusions about application viability.

**Keywords:** quantum computing; financial sector; economic viability; quantum advantage; scenario analysis.

## 9. Introdução

Problemas financeiros exigem métodos computacionais para representar incertezas, avaliar instrumentos e tomar decisões sob restrições. A literatura sobre computação quântica para finanças examina como algoritmos quânticos poderiam contribuir para essas tarefas, especialmente em modelagem estocástica, otimização e aprendizado de máquina. A revisão de Herman et al. (2023) apresenta aplicações e limitações dessas abordagens e é usada aqui como base para examinar sua utilidade em problemas financeiros [1](https://doi.org/10.1038/s42254-023-00603-1).

Woerner e Egger (2019) propõem usar a estimação quântica de amplitude na avaliação de risco e na precificação de instrumentos financeiros. O estudo trata de medidas como *Value at Risk* e *Conditional Value at Risk* e discute a relação entre a convergência do algoritmo e a profundidade do circuito. Os resultados permitem examinar ganhos algorítmicos em tarefas tradicionalmente resolvidas com simulação de Monte Carlo, mas não mostram, por si só, que adotar a técnica em operações financeiras seja rentável [4](https://doi.org/10.1038/s41534-019-0130-6).

Para passar de uma proposta algorítmica a uma aplicação útil, é preciso estimar os recursos necessários para executá-la. Chakrabarti et al. (2021) fazem essa estimativa para casos de precificação de derivativos e identificam obstáculos de implementação que afetam a possibilidade de vantagem quântica. O estudo mostra que a viabilidade depende do número de qubits lógicos, da profundidade dos circuitos e do tempo de execução, e não pode ser inferida apenas da complexidade assintótica do algoritmo [3](https://doi.org/10.22331/q-2021-06-01-463).

A mesma distinção aparece no modelo de Choi, Moses e Thompson (2025), que relaciona a eficiência dos algoritmos às diferenças de velocidade entre sistemas clássicos e quânticos. Nesse modelo, reduzir o número de operações não garante menor tempo de solução, pois o resultado depende da combinação entre algoritmo, hardware e escala do problema. Por isso, a comparação deve usar uma alternativa clássica adequada ao caso analisado [2](https://doi.org/10.1109/JPROC.2025.3574102).

No plano econômico, esta pesquisa se interessa pelo benefício incremental que uma organização obtém ao adotar uma abordagem quântica. Para o recorte escolhido, serão examinados os custos de acesso e integração e os possíveis benefícios operacionais, com precisão e qualidade comparáveis. Essa definição admite casos em que uma execução mais rápida gera valor, desde que a relação entre desempenho e benefício monetário seja demonstrada ou declarada como premissa. Sem esses dados, a comparação ficará restrita a indicadores de custo e desempenho e não afirmará retorno financeiro efetivo.

Estimar quando essas condições poderão ser satisfeitas também exige explicitar as incertezas. Mejia et al. (2025), em um preprint, apresentam uma ferramenta de análise de vantagem econômica quântica que permite variar premissas sobre hardware, correção de erros, conectividade, custos e algoritmos. A ferramenta estrutura comparações condicionais, sem fixar uma data única que valha para qualquer aplicação [5](https://doi.org/10.48550/arXiv.2508.21031).

Neste artigo, a ampliação do acesso será examinada como possível mudança nas condições de adoção, a partir dos custos de utilização, da disponibilidade de serviços em nuvem e da necessidade de infraestrutura própria. Esses fatores são dimensões de análise, e não se presume que sua evolução baste para garantir viabilidade. Os cenários também incluirão melhorias dos métodos clássicos, para não comparar uma tecnologia quântica em evolução com uma referência clássica artificialmente estática.

O objetivo deste trabalho é, portanto, investigar as condições técnicas e econômicas para a viabilidade da computação quântica no setor financeiro, considerando seus potenciais benefícios em relação aos métodos clássicos e cenários de ampliação do acesso à tecnologia. As áreas candidatas iniciais são a otimização de carteiras, a análise de risco e a precificação de ativos e derivativos. A aplicação escolhida para aprofundamento dependerá da existência de evidências comparáveis e da possibilidade de definir critérios verificáveis.

O trabalho combina uma revisão da literatura com análise de cenários. A revisão registrará as fontes consultadas, os critérios de seleção e as premissas dos estudos incluídos, separando evidências experimentais de projeções. A análise de cenários variará parâmetros de desempenho, custo e acesso de forma documentada, com análise de sensibilidade e cenários em que a viabilidade não é atingida. Estimativas temporais, se houver, serão apresentadas como resultados condicionais, válidos apenas para as aplicações e premissas examinadas. A contribuição pretendida é uma avaliação fundamentada das condições de adoção, a ser refinada ao longo da pesquisa.

## Referências

1. HERMAN, Dylan; GOOGIN, Cody; LIU, Xiaoyuan; SUN, Yue; GALDA, Alexey; SAFRO, Ilya; PISTOIA, Marco; ALEXEEV, Yuri. Quantum computing for finance. *Nature Reviews Physics*, v. 5, p. 450-465, 2023. [DOI: 10.1038/s42254-023-00603-1](https://doi.org/10.1038/s42254-023-00603-1).

2. CHOI, Sukwoong; MOSES, William S.; THOMPSON, Neil. The Quantum Tortoise and the Classical Hare: When Will Quantum Computers Outpace Classical Ones and When Will They Be Left Behind? *Proceedings of the IEEE*, v. 113, n. 2, p. 113-124, 2025. [DOI: 10.1109/JPROC.2025.3574102](https://doi.org/10.1109/JPROC.2025.3574102).

3. CHAKRABARTI, Shouvanik; KRISHNAKUMAR, Rajiv; MAZZOLA, Guglielmo; STAMATOPOULOS, Nikitas; WOERNER, Stefan; ZENG, William J. A Threshold for Quantum Advantage in Derivative Pricing. *Quantum*, v. 5, art. 463, 2021. [DOI: 10.22331/q-2021-06-01-463](https://doi.org/10.22331/q-2021-06-01-463).

4. WOERNER, Stefan; EGGER, Daniel J. Quantum risk analysis. *npj Quantum Information*, v. 5, art. 15, 2019. [DOI: 10.1038/s41534-019-0130-6](https://doi.org/10.1038/s41534-019-0130-6).

5. MEJIA, Frederick; GUNDLACH, Hans; LYNCH, Jayson; DUKATZ, Carl; LUCAS, Andrew; CRANE, Eleanor; SHUKLA, Prashant; THOMPSON, Neil. Introducing the Quantum Economic Advantage Online Calculator. *arXiv*, 2508.21031, 2025. **Preprint**; utilizado como referência metodológica complementar. [DOI: 10.48550/arXiv.2508.21031](https://doi.org/10.48550/arXiv.2508.21031).
