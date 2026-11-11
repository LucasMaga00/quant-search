"""Compila a fonte LaTeX revisável; execute a partir de qualquer diretório.

Requer Tectonic 0.17.0 (ou uma instalação LaTeX com latexmk e XeLaTeX).
Nenhum conteúdo do artigo é regenerado ou sobrescrito por este comando.
"""
from pathlib import Path
import argparse
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tectonic", default=shutil.which("tectonic"))
    args = parser.parse_args()
    raiz = Path(__file__).resolve().parents[1]
    saida = raiz / "output" / "pdf"
    saida.mkdir(parents=True, exist_ok=True)
    if args.tectonic:
        cmd = [args.tectonic, "--untrusted", "--keep-logs", "--outdir", str(saida), "artigo.tex"]
    elif shutil.which("latexmk"):
        cmd = ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error",
               f"-outdir={saida}", "artigo.tex"]
    else:
        parser.error("Instale Tectonic 0.17.0 ou latexmk/XeLaTeX; também é possível compilar no Overleaf.")
    subprocess.run(cmd, cwd=raiz, check=True)
    print(saida / "artigo.pdf")


if __name__ == "__main__":
    main()
