"""Comandos para execução do Terraform."""

from pathlib import Path
import typer
from rich import print

from ..config.constants import TerraformAction
from ..config.validation import validate_directory_exists, ValidationError
from ..terraform.terraform_runner import TerraformRunner


def run_terraform_command(action: TerraformAction, project_path: Path) -> None:
    """
    Executa um comando Terraform dentro do diretório de um projeto.
    
    Args:
        action: Comando do Terraform a ser executado
        project_path: Caminho para o projeto Terraform
    """
    try:
        # Validar se o diretório existe
        validate_directory_exists(project_path)
        
        # Verificar se existem arquivos Terraform
        terraform_runner = TerraformRunner()
        if not terraform_runner.check_terraform_files(project_path):
            print(f":warning: [yellow]Aviso:[/yellow] Nenhum arquivo .tf encontrado em '{project_path}'")
            if not typer.confirm("Deseja continuar mesmo assim?"):
                raise typer.Exit()
        
        # Executar comando
        terraform_runner.run_command(action, project_path)
        
    except ValidationError as e:
        print(f":x: [bold red]Erro:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f":x: [bold red]Erro inesperado:[/bold red] {e}")
        raise typer.Exit(code=1)