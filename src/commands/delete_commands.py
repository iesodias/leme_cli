"""Comandos para exclusão de recursos."""

import shutil
from pathlib import Path
import typer
from rich import print

from ..config.validation import validate_directory_exists, ValidationError


def delete_project(project_path: Path, force: bool = False) -> None:
    """
    Apaga um diretório de projeto e todo o seu conteúdo de forma permanente.
    
    Args:
        project_path: Caminho para o diretório do projeto
        force: Forçar exclusão sem confirmação
    """
    try:
        # Validar se o diretório existe
        validate_directory_exists(project_path)
        
        print(f":warning: [bold yellow]Atenção:[/bold yellow] Esta ação é irreversível.")
        
        should_delete = force
        if not force:
            confirmed = typer.confirm(
                f"Você tem CERTEZA que quer apagar permanentemente o diretório '{project_path}' "
                "e todo o seu conteúdo?"
            )
            if not confirmed:
                print("Operação cancelada pelo usuário.")
                raise typer.Exit()
            should_delete = True
        
        if should_delete:
            shutil.rmtree(project_path)
            print(f":wastebasket: [bold green]Projeto '{project_path}' apagado com sucesso.[/bold green]")
            
    except ValidationError as e:
        print(f":x: [bold red]Erro:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f":x: [bold red]Erro ao apagar o diretório:[/bold red] {e}")
        raise typer.Exit(code=1)