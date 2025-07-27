"""Módulo para executar comandos do Terraform."""

import subprocess
from pathlib import Path
from typing import Optional
from rich import print

from ..config.constants import TerraformAction
from ..config.validation import validate_terraform_installed, ValidationError


class TerraformRunner:
    """Executor de comandos Terraform."""
    
    def __init__(self):
        """Inicializa o executor do Terraform."""
        validate_terraform_installed()
    
    def run_command(self, action: TerraformAction, project_path: Path, extra_args: Optional[list] = None) -> int:
        """
        Executa um comando Terraform no diretório especificado.
        
        Args:
            action: Ação do Terraform a ser executada
            project_path: Caminho do projeto Terraform
            extra_args: Argumentos adicionais para o comando
            
        Returns:
            Código de retorno do comando
            
        Raises:
            ValidationError: Se o comando falhar
        """
        if not project_path.exists() or not project_path.is_dir():
            raise ValidationError(f"Diretório do projeto '{project_path}' não existe ou não é válido.")
        
        print(f":gear: Executando [bold blue]terraform {action.value}[/bold blue] no diretório [bold green]{project_path}[/bold green]...")
        print("-" * 40)
        
        command = ["terraform", action.value]
        if extra_args:
            command.extend(extra_args)
        
        try:
            process = subprocess.Popen(
                command,
                cwd=project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # Mostrar output em tempo real
            for line in iter(process.stdout.readline, ''):
                print(line.rstrip())
            
            return_code = process.wait()
            
            print("-" * 40)
            
            if return_code == 0:
                print(f":white_check_mark: [bold green]Comando 'terraform {action.value}' executado com sucesso![/bold green]")
            else:
                print(f":x: [bold red]Comando 'terraform {action.value}' falhou com código de saída {return_code}.[/bold red]")
                raise ValidationError(f"Terraform {action.value} falhou com código {return_code}")
            
            return return_code
            
        except FileNotFoundError:
            raise ValidationError("Terraform não está instalado ou não está no PATH.")
        except Exception as e:
            raise ValidationError(f"Erro inesperado ao executar terraform {action.value}: {e}")
    
    def run_init(self, project_path: Path) -> int:
        """Executa terraform init."""
        return self.run_command(TerraformAction.INIT, project_path)
    
    def run_validate(self, project_path: Path) -> int:
        """Executa terraform validate."""
        return self.run_command(TerraformAction.VALIDATE, project_path)
    
    def run_plan(self, project_path: Path, var_file: Optional[str] = None) -> int:
        """Executa terraform plan."""
        extra_args = []
        if var_file:
            extra_args.extend(["-var-file", var_file])
        return self.run_command(TerraformAction.PLAN, project_path, extra_args)
    
    def run_apply(self, project_path: Path, var_file: Optional[str] = None, auto_approve: bool = False) -> int:
        """Executa terraform apply."""
        extra_args = []
        if var_file:
            extra_args.extend(["-var-file", var_file])
        if auto_approve:
            extra_args.append("-auto-approve")
        return self.run_command(TerraformAction.APPLY, project_path, extra_args)
    
    def run_destroy(self, project_path: Path, var_file: Optional[str] = None, auto_approve: bool = False) -> int:
        """Executa terraform destroy."""
        extra_args = []
        if var_file:
            extra_args.extend(["-var-file", var_file])
        if auto_approve:
            extra_args.append("-auto-approve")
        return self.run_command(TerraformAction.DESTROY, project_path, extra_args)
    
    @staticmethod
    def check_terraform_files(project_path: Path) -> bool:
        """Verifica se existem arquivos Terraform no diretório."""
        tf_files = list(project_path.glob("*.tf"))
        return len(tf_files) > 0