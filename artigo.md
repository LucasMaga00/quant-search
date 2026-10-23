# Proposta inicial de pesquisa

## 1. Título provisório

Viabilidade técnica e econômica da computação quântica no setor financeiro: condições de adoção e cenários de ampliação do acesso

## 2. Problema de pesquisa

A computação quântica tem sido investigada como alternativa para problemas financeiros que envolvem otimização, modelagem de incertezas e processamento numérico. Entre as aplicações discutidas na literatura estão a otimização de carteiras, a análise de risco e a precificação de ativos e derivativos. Entretanto, a possibilidade de executar um algoritmo quântico ou demonstrar uma vantagem em sua complexidade não estabelece, por si só, que sua adoção seja economicamente vantajosa para uma organização financeira [1](https://doi.org/10.1038/s42254-023-00603-1), [2](https://doi.org/10.1109/JPROC.2025.3574102).

O problema investigado consiste em estabelecer como relacionar requisitos técnicos, custos de utilização e benefícios potenciais dessas aplicações, utilizando métodos clássicos como referência. Essa avaliação deverá considerar o tamanho do problema, a precisão exigida, o tempo total de processamento e os recursos necessários para obter resultados confiáveis. Estimativas de recursos para precificação de derivativos ilustram a importância de avaliar a implementação completa, além do ganho algorítmico esperado [3](https://doi.org/10.22331/q-2021-06-01-463).

Neste trabalho, a **viabilidade técnica** será entendida como a capacidade de executar uma aplicação com a precisão e o prazo exigidos. A **viabilidade econômica** será avaliada pelo benefício incremental líquido da adoção em comparação com uma solução clássica adequada, considerando os custos adicionais envolvidos. Esse benefício poderá decorrer de redução de despesas computacionais, menor tempo de processamento ou melhoria mensurável na qualidade da solução. Ganhos de desempenho não serão automaticamente interpretados como aumento de lucro.

A **ampliação do acesso**, associada à ideia de democratização da tecnologia, será tratada inicialmente por indicadores como custo de utilização, disponibilidade de recursos por serviços em nuvem e necessidade de infraestrutura própria. Esses indicadores serão analisados como possíveis facilitadores da adoção, sem pressupor acesso universal ou benefício econômico garantido.

## 3. Pergunta de pesquisa

**Em quais condições técnicas e econômicas a computação quântica pode se tornar viável para aplicações no setor financeiro, em comparação com métodos clássicos, e como diferentes cenários de evolução tecnológica e ampliação do acesso podem influenciar essa viabilidade ao longo do tempo?**

## 4. Objetivo geral

Investigar as condições técnicas e econômicas para a viabilidade da computação quântica no setor financeiro, considerando seus potenciais benefícios em relação aos métodos clássicos e cenários de ampliação do acesso à tecnologia.

## 5. Objetivos específicos

1. Mapear aplicações financeiras investigadas na literatura, com atenção inicial à otimização de carteiras, à análise de risco e à precificação de ativos e derivativos, para selecionar um recorte de aprofundamento.
2. Identificar os métodos clássicos de referência e os benefícios potenciais atribuídos às abordagens quânticas, distinguindo propostas teóricas, simulações, experimentos em hardware e estimativas de recursos.
3. Levantar requisitos técnicos e componentes de custo relevantes para as aplicações selecionadas, incluindo preparação de dados, execução, tratamento de erros e integração com recursos clássicos, conforme a disponibilidade de evidências.
4. Definir critérios de comparação que relacionem custo total, tempo de processamento, precisão e qualidade da solução, indicando quando houver dados suficientes para estimar benefícios monetários.
5. Construir cenários de evolução tecnológica e de custos de acesso, examinando sua influência sobre os possíveis limites de viabilidade e, quando os dados permitirem, sobre os horizontes temporais de adoção.
6. Analisar as limitações e a sensibilidade das estimativas às premissas adotadas, incluindo a possibilidade de não identificar viabilidade no horizonte considerado.

## 6. Hipótese

Nesta etapa, não se estabelece uma hipótese formal, pois a pesquisa tem caráter exploratório e ainda não foram selecionados a aplicação específica, as variáveis e o modelo de comparação. A formulação de uma hipótese testável será reavaliada após essa delimitação.

A análise será conduzida sem pressupor que a computação quântica necessariamente se tornará economicamente vantajosa no período investigado. A ausência de viabilidade nos cenários examinados também constituirá um resultado válido.

## 7. Resumo inicial

A computação quântica tem motivado pesquisas sobre aplicações no setor financeiro, mas a identificação de possíveis ganhos computacionais exige avaliação conjunta de requisitos técnicos e custos de adoção. Este trabalho tem como objetivo investigar as condições técnicas e econômicas para a viabilidade da computação quântica nesse setor, considerando benefícios potenciais em relação aos métodos clássicos e cenários de ampliação do acesso à tecnologia. Propõe-se uma pesquisa exploratória baseada em revisão da literatura e análise de cenários, com atenção inicial à otimização de carteiras, à análise de risco e à precificação de ativos e derivativos. A revisão orientará a seleção de um recorte e o levantamento de indicadores de custo total, tempo de processamento, precisão e qualidade das soluções. A ampliação do acesso será examinada por fatores como custo de utilização, disponibilidade de recursos em nuvem e necessidade de infraestrutura própria. Quando houver dados suficientes, serão estimados limites de viabilidade e horizontes temporais condicionados a premissas explícitas. A contribuição pretendida consiste em organizar critérios para avaliar a adoção da tecnologia, distinguindo potencial algorítmico, execução prática e benefício econômico. Por se tratar de uma proposta inicial, ainda não são apresentados resultados ou conclusões sobre a viabilidade das aplicações.

**Palavras-chave:** computação quântica; setor financeiro; viabilidade econômica; vantagem quântica; análise de cenários.

## 8. Abstract inicial

Quantum computing has motivated research into financial applications, but assessing potential computational gains requires considering technical requirements and adoption costs together. This study aims to investigate the technical and economic conditions under which quantum computing may become viable in the financial sector, considering potential benefits over classical methods and scenarios of broader access to the technology. An exploratory study based on a literature review and scenario analysis is proposed, initially focusing on portfolio optimization, risk analysis, and asset and derivative pricing. The review will guide the selection of a narrower scope and the identification of indicators for total cost, processing time, accuracy, and solution quality. Broader access will be examined through factors such as usage costs, cloud resource availability, and the need for dedicated infrastructure. Where sufficient data are available, feasibility thresholds and time horizons will be estimated under explicit assumptions. The intended contribution is to organize criteria for assessing technology adoption while distinguishing algorithmic potential, practical execution, and economic benefit. As this is an initial research proposal, no findings or conclusions about application viability are reported.

**Keywords:** quantum computing; financial sector; economic viability; quantum advantage; scenario analysis.

## 9. Introdução

A resolução de problemas financeiros envolve métodos computacionais para representar incertezas, avaliar instrumentos e selecionar decisões sob restrições. A literatura sobre computação quântica para finanças examina como algoritmos quânticos poderiam contribuir para essas tarefas, especialmente em modelagem estocástica, otimização e aprendizado de máquina. A revisão de Herman et al. (2023) apresenta aplicações e limitações dessas abordagens e fornece uma base para investigar sua utilidade em problemas financeiros [1](https://doi.org/10.1038/s42254-023-00603-1).

Entre as propostas existentes, Woerner e Egger (2019) apresentam o uso da estimação quântica de amplitude na avaliação de risco e na precificação de instrumentos financeiros. O estudo aborda medidas como *Value at Risk* e *Conditional Value at Risk* e discute a relação entre a convergência do algoritmo e a profundidade do circuito. Seus resultados oferecem fundamento para examinar ganhos algorítmicos potenciais em tarefas tradicionalmente tratadas com simulações de Monte Carlo, sem estabelecer, por si só, a rentabilidade de sua adoção em operações financeiras [4](https://doi.org/10.1038/s41534-019-0130-6).

A passagem de uma proposta algorítmica para uma aplicação útil exige avaliar os recursos necessários para executá-la. Chakrabarti et al. (2021) estimam recursos para casos de precificação de derivativos e identificam obstáculos de implementação que afetam a possibilidade de obter vantagem quântica. O estudo evidencia a relevância de considerar requisitos de qubits lógicos, profundidade de circuitos e tempo de execução, em vez de inferir viabilidade apenas a partir da complexidade assintótica de um algoritmo [3](https://doi.org/10.22331/q-2021-06-01-463).

Essa distinção também aparece no modelo de Choi, Moses e Thompson (2025), que relaciona a eficiência dos algoritmos às diferenças de velocidade entre sistemas clássicos e quânticos. Nessa perspectiva, uma redução no número de operações não assegura menor tempo de solução: o resultado depende da combinação entre algoritmo, hardware e escala do problema. A comparação precisa, portanto, utilizar uma alternativa clássica adequada ao caso analisado [2](https://doi.org/10.1109/JPROC.2025.3574102).

No plano econômico, o interesse desta pesquisa está no benefício incremental obtido por uma organização ao adotar uma abordagem quântica. Para o recorte a ser selecionado, propõe-se examinar os custos de acesso e integração e os possíveis benefícios operacionais em condições comparáveis de precisão e qualidade. Essa definição permite investigar situações em que uma execução mais rápida gera valor, mas exige que a relação entre desempenho e benefício monetário seja demonstrada ou explicitada como premissa. Na ausência desses dados, a comparação será limitada a indicadores de custo e desempenho, sem afirmar um retorno financeiro efetivo.

A estimativa de quando essas condições poderão ser satisfeitas também requer explicitar incertezas. Mejia et al. (2025), em um preprint, apresentam uma ferramenta de análise de vantagem econômica quântica que permite variar premissas sobre hardware, correção de erros, conectividade, custos e algoritmos. O trabalho mostra uma forma de estruturar comparações condicionais, em vez de adotar uma data única e independente das características da aplicação [5](https://doi.org/10.48550/arXiv.2508.21031).

Neste artigo, a ampliação do acesso será examinada como possível mudança nas condições de adoção, considerando custos de utilização, disponibilidade de serviços em nuvem e necessidade de infraestrutura própria. Esses fatores serão tratados como dimensões de análise, e sua evolução não será presumida como suficiente para garantir viabilidade. Também deverão ser consideradas melhorias dos métodos clássicos, para que os cenários não comparem uma tecnologia quântica em evolução com uma referência clássica artificialmente estática.

Diante desse contexto, o objetivo deste trabalho é investigar as condições técnicas e econômicas para a viabilidade da computação quântica no setor financeiro, considerando seus potenciais benefícios em relação aos métodos clássicos e cenários de ampliação do acesso à tecnologia. Inicialmente, serão consideradas a otimização de carteiras, a análise de risco e a precificação de ativos e derivativos como áreas candidatas. A seleção de uma aplicação para aprofundamento dependerá da disponibilidade de evidências comparáveis e da possibilidade de delimitar critérios verificáveis.

Para atingir esse objetivo, propõe-se uma revisão da literatura seguida de análise de cenários. A revisão deverá registrar as fontes consultadas, os critérios de seleção e as premissas dos estudos incluídos, distinguindo evidências experimentais de projeções. A análise de cenários deverá variar parâmetros de desempenho, custo e acesso de forma documentada, incluindo análise de sensibilidade e cenários em que a viabilidade não seja atingida. Eventuais estimativas temporais serão apresentadas como resultados condicionais, restritos às aplicações e às premissas examinadas. A contribuição pretendida é organizar uma avaliação fundamentada das condições de adoção, que possa ser refinada ao longo da pesquisa.

## Referências

1. HERMAN, Dylan; GOOGIN, Cody; LIU, Xiaoyuan; SUN, Yue; GALDA, Alexey; SAFRO, Ilya; PISTOIA, Marco; ALEXEEV, Yuri. Quantum computing for finance. *Nature Reviews Physics*, v. 5, p. 450–465, 2023. [DOI: 10.1038/s42254-023-00603-1](https://doi.org/10.1038/s42254-023-00603-1).

2. CHOI, Sukwoong; MOSES, William S.; THOMPSON, Neil. The Quantum Tortoise and the Classical Hare: When Will Quantum Computers Outpace Classical Ones and When Will They Be Left Behind? *Proceedings of the IEEE*, v. 113, n. 2, p. 113–124, 2025. [DOI: 10.1109/JPROC.2025.3574102](https://doi.org/10.1109/JPROC.2025.3574102).

3. CHAKRABARTI, Shouvanik; KRISHNAKUMAR, Rajiv; MAZZOLA, Guglielmo; STAMATOPOULOS, Nikitas; WOERNER, Stefan; ZENG, William J. A Threshold for Quantum Advantage in Derivative Pricing. *Quantum*, v. 5, art. 463, 2021. [DOI: 10.22331/q-2021-06-01-463](https://doi.org/10.22331/q-2021-06-01-463).

4. WOERNER, Stefan; EGGER, Daniel J. Quantum risk analysis. *npj Quantum Information*, v. 5, art. 15, 2019. [DOI: 10.1038/s41534-019-0130-6](https://doi.org/10.1038/s41534-019-0130-6).

5. MEJIA, Frederick; GUNDLACH, Hans; LYNCH, Jayson; DUKATZ, Carl; LUCAS, Andrew; CRANE, Eleanor; SHUKLA, Prashant; THOMPSON, Neil. Introducing the Quantum Economic Advantage Online Calculator. *arXiv*, 2508.21031, 2025. **Preprint**; utilizado como referência metodológica complementar. [DOI: 10.48550/arXiv.2508.21031](https://doi.org/10.48550/arXiv.2508.21031).
