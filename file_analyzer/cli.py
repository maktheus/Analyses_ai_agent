import os
import typer
from rich.console import Console
from rich.progress import Progress
from pathlib import Path
from typing import Optional
from .indexer import FileIndexer
from .analyzer import FileAnalyzer

app = typer.Typer(help="File Analyzer Agent - Análise de arquivos usando modelos locais")
console = Console()

@app.command()
def analyze(
    path: str = typer.Argument(..., help="Caminho para os arquivos a serem analisados"),
    model: str = typer.Option("mistral", help="Modelo a ser usado para análise"),
    index_path: Optional[str] = typer.Option(None, help="Caminho para salvar/carregar o índice"),
    verbose: bool = typer.Option(False, help="Modo verboso")
):
    """
    Analisa arquivos usando um modelo local de linguagem.
    """
    try:
        path = Path(path)
        if not path.exists():
            console.print(f"[red]Erro: O caminho {path} não existe[/red]")
            raise typer.Exit(1)

        analyzer = FileAnalyzer(
            model_name=model,
            index_path=index_path,
            verbose=verbose
        )

        with Progress() as progress:
            task = progress.add_task("[cyan]Analisando arquivos...", total=None)
            results = analyzer.analyze_directory(path)
            progress.update(task, completed=True)

        console.print("\n[green]Análise concluída![/green]")
        console.print("\nResultados:")
        for result in results:
            console.print(f"\n[blue]{result['file']}[/blue]")
            console.print(result['analysis'])

    except Exception as e:
        console.print(f"[red]Erro durante a análise: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def index(
    path: str = typer.Argument(..., help="Caminho para os arquivos a serem indexados"),
    index_path: Optional[str] = typer.Option(None, help="Caminho para salvar o índice"),
    verbose: bool = typer.Option(False, help="Modo verboso")
):
    """
    Cria um índice dos arquivos para análise posterior.
    """
    try:
        path = Path(path)
        if not path.exists():
            console.print(f"[red]Erro: O caminho {path} não existe[/red]")
            raise typer.Exit(1)

        indexer = FileIndexer(
            index_path=index_path,
            verbose=verbose
        )

        with Progress() as progress:
            task = progress.add_task("[cyan]Indexando arquivos...", total=None)
            indexer.index_directory(path)
            progress.update(task, completed=True)

        console.print("[green]Indexação concluída com sucesso![/green]")

    except Exception as e:
        console.print(f"[red]Erro durante a indexação: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 