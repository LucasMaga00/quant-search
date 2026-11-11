"""Gera a fonte IEEE editável a partir da versão Markdown sincronizada.

Requer Pandoc 3.13. A compilação posterior usa apenas artigo.tex e
referencias.bib; não precisa de Pandoc nem de Python no Overleaf.
"""
from pathlib import Path
import argparse
import re
import shutil
import subprocess

RAIZ = Path(__file__).resolve().parents[1]
CHAVES = [
    'jorion2007var', 'glasserman2003montecarlo', 'brassard2002qae',
    'montanaro2015montecarlo', 'rebentrost2018finance', 'stamatopoulos2020option',
    'woerner2019risk', 'chakrabarti2021threshold', 'herbert2021groverrudolph',
    'choi2025tortoise', 'bcbs2019frtb', 'grover2002superpositions',
    'carreravazquez2021stateprep', 'babbush2018qrom', 'cuccaro2004adder',
    'babbush2021quadratic', 'beverland2022requirements', 'nielsen2010quantum',
    'ross2016gridsynth', 'moallemi2013latency', 'herman2023finance',
    'egger2021credit', 'stamatopoulos2022marketrisk', 'mejia2025calculator',
    'alpaca2026marketdata', 'ibm2026pricing', 'aws2026ec2pricing',
    'stamatopoulos2024risk', 'iaconis2024normal', 'xie2025gaussian', 'microsoft2026qre',
]
PREAMBULO = r'''% Fonte IEEE para revisão dos autores. Compilar com XeLaTeX ou Tectonic.
\documentclass[conference,a4paper]{IEEEtran}
\usepackage[T1]{fontenc}
\usepackage[brazil,english]{babel}
\usepackage{newtxtext,newtxmath}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{booktabs,array,calc}
\usepackage{placeins,stfloats}
\usepackage{url}
\usepackage[hidelinks]{hyperref}
\urlstyle{same}
\IEEEtriggeratref{26}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\pandocbounded}[1]{#1}
\setlength{\emergencystretch}{1.5em}
\title{@@TITLE@@}
\author{\IEEEauthorblockN{Arthur Bretas, Lucas Magalhães e Henrique Botti}
\IEEEauthorblockA{Inteli, Instituto de Tecnologia e Liderança\\
Orientação: Erinaldo Fonseca e Bryan Ferreira}}
\begin{document}
\selectlanguage{brazil}
\maketitle
\renewcommand{\abstractname}{Resumo}
\begin{abstract}
@@RESUMO@@
\end{abstract}
\begin{IEEEkeywords}
@@KEYWORDS_PT@@
\end{IEEEkeywords}
\selectlanguage{english}
\renewcommand{\abstractname}{Abstract}
\begin{abstract}
@@ABSTRACT@@
\end{abstract}
\begin{IEEEkeywords}
@@KEYWORDS_EN@@
\end{IEEEkeywords}
\selectlanguage{brazil}
'''


def gerar(pandoc):
    texto = (RAIZ / 'artigo.md').read_text()
    titulo = texto.splitlines()[0][2:]
    def trecho(inicio, fim):
        return texto.split(inicio, 1)[1].split(fim, 1)[0].strip()
    resumo = trecho('## Resumo', '**Palavras-chave:**')
    abstract = trecho('## Abstract', '**Keywords:**')
    palavras_pt = trecho('**Palavras-chave:**', '## Abstract')
    palavras_en = trecho('**Keywords:**', '## 1. Introdução')
    corpo = '## 1. Introdução' + texto.split('## 1. Introdução', 1)[1]
    corpo = corpo.split('## Referências', 1)[0]

    def referencias(t):
        return re.sub(r'\[\[(\d+)\]\]\([^)]*\)',
                      lambda m: r'\cite{' + CHAVES[int(m[1])-1] + '}', t)

    def converter(t):
        return subprocess.run([pandoc, '--from=markdown+tex_math_dollars+raw_tex',
                               '--to=latex', '--shift-heading-level=-1', '--wrap=none'],
                              input=referencias(t), text=True, capture_output=True,
                              check=True).stdout.strip()

    corpo = corpo.replace('### 4.2 Cenários econômicos', '### 4.2 Cenários econômicos {#cenarios-economicos}')
    corpo = corpo.replace('### 8.4 Estimativa tolerante a falhas', '### 8.4 Estimativa tolerante a falhas {#estimativa-tolerante-falhas}')
    corpo = corpo.replace('Seção 4.2', r'Seção \ref{cenarios-economicos}')
    corpo = corpo.replace('Seção 8.4', r'Seção \ref{estimativa-tolerante-falhas}')
    # A classe IEEE numera seções e subseções, evitando numeração duplicada.
    corpo = re.sub(r'^(#{2,3})\s+\d+(?:\.\d+)*\.?\s+', r'\1 ', corpo, flags=re.M)
    # As figuras centrais ocupam duas colunas; os PDFs são vetoriais.
    corpo = re.sub(r'!\[[^\]]*\]\(figuras/([^)]*)\.png\)\s*\n\s*\*Figura (\d+): ([^\n]+)\*',
                   lambda m: '\n' + r'\begin{figure*}[!t]'+'\n'+r'\centering'+'\n'+
                   r'\includegraphics[width=\textwidth]{figuras/'+m[1]+'.pdf}\n'+
                   r'\caption{'+converter(m[3])+r'}\label{fig:'+m[1]+r'}'+'\n'+
                   r'\end{figure*}'+'\n', corpo, flags=re.S)
    latex = converter(corpo)
    # Pandoc emite longtable, incompatível com as duas colunas IEEE. Cada
    # tabela cabe em uma página e passa a ser um float de largura dupla.
    tabelas = iter([
        'Trabalhos relacionados e limites para a pergunta de pesquisa.',
        'Entradas e saídas dos quatro experimentos.',
        'Parâmetros e premissas experimentais.',
        'Métricas técnicas e econômicas.',
        r'VaR clássico com erro-alvo de 1\%: calibração e tempo medido.',
        'Custo do atraso observado entre 1 e 30 minutos.',
        r'Recursos lógicos e taxa agregada de empate para erro de 1\%.',
        'Estimativa física condicional ao escalonamento lógico.',
        'Tetos econômicos condicionais à forma do custo do atraso.',
        'Arquivos e etapas para reprodução.',
    ])
    contador = 0
    def tabela(m):
        nonlocal contador
        contador += 1
        conteudo = m[1]
        abertura = re.match(r'\[\]\{(.*?)\}\s*\\toprule\\noalign\{\}', conteudo, re.S)
        if not abertura:
            raise ValueError('Formato de tabela inesperado; revise a conversão Pandoc.')
        spec = abertura[1].replace('\\linewidth', '\\textwidth')
        linhas = conteudo[abertura.end():]
        linhas = linhas.replace('\\endhead\n\\bottomrule\\noalign{}\n\\endlastfoot', '')
        # Paths podem quebrar nos separadores, inclusive em colunas estreitas.
        linhas = re.sub(r'\\texttt\{([^}]+)\}',
                        lambda x: r'\path{'+x[1].replace(r'\_', '_')+'}', linhas)
        caption = next(tabelas, f'Informações para reprodução ({contador}).')
        return (r'\begin{table*}[!tb]'+'\n'+r'\caption{'+caption+r'}\label{tab:'+str(contador)+'}\n'+
                r'\centering\footnotesize\setlength{\tabcolsep}{4pt}'+'\n'+
                r'\renewcommand{\arraystretch}{1.12}'+'\n'+r'\begin{tabular}{'+spec+'}\n'+
                r'\toprule'+'\n'+linhas+r'\bottomrule'+'\n'+r'\end{tabular}'+'\n'+r'\end{table*}')
    latex = re.sub(r'\{\\def\\LTcaptype\{none\}[^\n]*\n\\begin\{longtable\}(.*?)\\end\{longtable\}\s*\}',
                   tabela, latex, flags=re.S)
    latex = re.sub(r'\\texttt\{([^}]+)\}', lambda m: r'\path{' + m[1].replace(r'\_', '_') + '}' if '/' in m[1] else m[0], latex)
    latex = re.sub(r'Tabela (\d+)', lambda m: r'Tabela~\ref{tab:' + m[1] + '}', latex)
    latex = latex.replace('Tabelas 2 e 3', r'Tabelas~\ref{tab:2} e~\ref{tab:3}')
    latex = re.sub(r'(?<![\w\\])(\d+(?:[,.]\d+)?) (s|ns|min|h)(?=[.,;:\s)])', r'\1~\2', latex)
    # \\tag preserva a numeração das equações na versão Markdown sincronizada.
    inicio = PREAMBULO
    for chave, valor in {'TITLE': titulo, 'RESUMO': resumo, 'ABSTRACT': abstract,
                         'KEYWORDS_PT': palavras_pt, 'KEYWORDS_EN': palavras_en}.items():
        inicio = inicio.replace('@@'+chave+'@@', converter(valor))
    final = '\n\\FloatBarrier\n\\bibliographystyle{IEEEtran}\n\\bibliography{referencias}\n\\end{document}\n'
    (RAIZ / 'artigo.tex').write_text(inicio+'\n'+latex+'\n'+final)
    print(f'artigo.tex: {contador} tabelas convertidas para o modelo IEEE.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pandoc', default=shutil.which('pandoc'))
    args = parser.parse_args()
    if not args.pandoc:
        parser.error('Instale Pandoc 3.13 ou informe --pandoc /caminho/para/pandoc.')
    gerar(args.pandoc)
