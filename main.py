import os
import typer
from pathlib import Path
from rich.console import Console
from dotenv import load_dotenv

from app.scanner import get_project_context
from app.analyzer import analyze_code

load_dotenv()

app = typer.Typer()
console = Console()

@app.command()
def main(
    path: str = typer.Argument(..., help="Path to the project folder to analyze."),
    model: str = typer.Option(None, "--model", "-m", help="Gemini model to use. Overrides GEMINI_MODEL env var."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Scan files and generate a preview without calling API."),
):
    target_model = model or os.getenv("GEMINI_MODEL")

    if not target_model:
        console.print("\n[bold red]❌ ERROR: No Gemini model specified![/bold red]")
        console.print("You must either:")
        console.print(" 1. Set [bold yellow]GEMINI_MODEL[/bold yellow] in your [bold blue].env[/bold blue] file.")
        console.print(" 2. Or use the [bold yellow]--model[/bold yellow] option in the terminal.")
        raise typer.Exit(code=1)

    project_path = Path(path)
    
    if not project_path.exists():
        console.print(f"[bold red]Error:[/bold red] Path '{path}' does not exist.")
        raise typer.Exit(code=1)

    repo_name = project_path.resolve().name
    output_dir = Path("reports") 
    output_dir.mkdir(parents=True, exist_ok=True)

    report_num = 1
    while True:
        candidate_name = f"{repo_name}_report_{report_num}.md"
        candidate_path = output_dir / candidate_name
        
        if not candidate_path.exists():
            save_path = candidate_path
            break
        report_num += 1

    with console.status(f"[bold green]Scanning files in {repo_name}...[/bold green]", spinner="dots"):
        try:
            context = get_project_context(str(project_path))
            console.print(f"✓ Loaded context from: {project_path}")
        except Exception as e:
            console.print(f"[bold red]Scanning failed:[/bold red] {e}")
            raise typer.Exit(code=1)

    if dry_run:
        console.print("[yellow]Dry Run mode: Skipping AI analysis.[/yellow]")
        console.print(f"Target Model: {target_model}")
        console.print(f"Context length: {len(context)} characters.")
        console.print(f"Next report would be saved to: {save_path}")
        return
    
    with console.status(f"[bold purple]Gemini ({target_model}) is analyzing {repo_name}...[/bold purple]", spinner="earth"):
        try:
            report = analyze_code(context, model=target_model)
        except Exception as e:
            console.print(f"[bold red]Analysis failed:[/bold red] {e}")
            raise typer.Exit(code=1)

    try:
        save_path.write_text(report, encoding="utf-8")
        console.print(f"\n[bold blue]Report saved to file: {save_path.resolve()}[/bold blue]")
    except Exception as e:
        console.print(f"[bold red]Failed to save report:[/bold red] {e}")

if __name__ == "__main__":
    app()