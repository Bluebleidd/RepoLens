import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from scanner import get_project_context
from analyzer import analyze_code

app = typer.Typer()
console = Console()

@app.command()
def audit(path: str = typer.Argument(..., help="Ścieżka do folderu z projektem")):
    """
    RepoLens: Przeprowadza audyt architektoniczny wskazanego projektu.
    """
    console.print(Panel.fit(f"[bold cyan]RepoLens[/bold cyan] analyzing: [yellow]{path}[/yellow]", border_style="cyan"))

    with console.status("[bold green]Skanowanie plików...[/bold green]", spinner="dots"):
        try:
            context = get_project_context(path)
            file_count = context.count("File: ")
            console.print(f"[green]✓[/green] Załadowano kontekst: {file_count} plików.")
        except Exception as e:
            console.print(f"[bold red]Błąd skanowania:[/bold red] {e}")
            return
        
    with console.status("[bold purple]Gemini analizuje architekturę i szuka błędów...[/bold purple]", spinner="earth"):
        try:
            report = analyze_code(context)
        except Exception as e:
            console.print(f"[bold red]Błąd API:[/bold red] {e}")
            return

    console.print("\n[bold]--- RAPORT REPOLENS ---[/bold]\n")
    console.print(Markdown(report))
    
    save_path = "AUDIT_REPORT.md"
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(report)
    console.print(f"\n[bold blue]Raport zapisano w pliku: {save_path}[/bold blue]")

if __name__ == "__main__":
    app()