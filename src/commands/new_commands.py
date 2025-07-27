"""Comandos para criação de novos recursos."""

from pathlib import Path
from typing import Dict, Any
import typer
from rich import print

from ..config.constants import Provider, ResourceType
from ..config.validation import (
    validate_provider, validate_resource_type, validate_directory_not_exists,
    validate_project_name, ValidationError
)
from ..templates.template_manager import TemplateManager


def create_project(name: str, provider: str) -> None:
    """
    Cria a estrutura de um novo projeto Terraform para um provedor específico.
    
    Args:
        name: Nome do projeto
        provider: Provedor de nuvem (aws ou azure)
    """
    try:
        # Validações
        validate_project_name(name)
        provider_enum = validate_provider(provider)
        project_path = Path(name)
        validate_directory_not_exists(project_path)
        
        print(f":construction: Criando projeto [bold green]{name}[/bold green] para o provedor [bold blue]{provider_enum.value}[/bold blue]...")
        
        # Preparar dados do template
        template_data = {"project_name": name}
        template_manager = TemplateManager()
        
        # Coletar informações específicas do provider
        if provider_enum == Provider.AWS:
            template_data.update(_collect_aws_config())
        elif provider_enum == Provider.AZURE:
            template_data.update(_collect_azure_config())
        
        # Validar templates antes de criar
        missing_templates = template_manager.validate_all_templates(provider_enum)
        if missing_templates:
            print(f":warning: [yellow]Aviso:[/yellow] Alguns templates estão faltando: {', '.join(missing_templates)}")
        
        # Gerar arquivos do projeto
        template_manager.render_project_files(provider_enum, template_data, project_path)
        
        print(f"\\n:rocket: Projeto [bold green]{name}[/bold green] criado com sucesso!")
        print(f"Acesse o diretório com: [bold cyan]cd {name}[/bold cyan]")
        
    except ValidationError as e:
        print(f":x: [bold red]Erro:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f":x: [bold red]Erro inesperado:[/bold red] {e}")
        raise typer.Exit(code=1)


def create_module(name: str) -> None:
    """
    Cria a estrutura de um novo módulo Terraform reutilizável.
    
    Args:
        name: Nome do módulo
    """
    try:
        validate_project_name(name)
        module_path = Path(name)
        validate_directory_not_exists(module_path)
        
        print(f":package: Criando módulo [bold blue]{name}[/bold blue]...")
        
        template_manager = TemplateManager()
        template_manager.render_module_files(module_path)
        
        print(f"\\n:sparkles: Módulo [bold blue]{name}[/bold blue] criado com sucesso!")
        
    except ValidationError as e:
        print(f":x: [bold red]Erro:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f":x: [bold red]Erro inesperado:[/bold red] {e}")
        raise typer.Exit(code=1)


def create_resource(resource_type: str, provider: str, name: str) -> None:
    """
    Cria um módulo Terraform para um recurso específico.
    
    Args:
        resource_type: Tipo do recurso (ex: storage-account, virtual_machine)
        provider: Provedor de nuvem (aws ou azure) 
        name: Nome para o módulo do recurso
    """
    try:
        # Validações
        validate_project_name(name)
        provider_enum = validate_provider(provider)
        resource_enum = validate_resource_type(resource_type, provider_enum)
        resource_path = Path(name)
        validate_directory_not_exists(resource_path)
        
        print(f":sparkles: Criando recurso [bold yellow]{resource_enum.value}[/bold yellow] para [bold blue]{provider_enum.value}[/bold blue] em [bold green]./{name}/[/bold green]...")
        
        # Preparar dados do template
        template_data = {"resource_name": name}
        
        # Coletar informações específicas do provider
        if provider_enum == Provider.AZURE:
            template_data.update(_collect_azure_resource_config())
        
        # Validar templates
        template_manager = TemplateManager()
        missing_templates = template_manager.validate_all_templates(provider_enum, resource_enum.value)
        if missing_templates:
            print(f":warning: [yellow]Aviso:[/yellow] Alguns templates estão faltando: {', '.join(missing_templates)}")
        
        # Gerar arquivos do recurso
        template_manager.render_resource_files(provider_enum, resource_enum.value, template_data, resource_path)
        
        print(f"\\n:rocket: Módulo de recurso [bold green]{name}[/bold green] criado com sucesso!")
        
    except ValidationError as e:
        print(f":x: [bold red]Erro:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f":x: [bold red]Erro inesperado:[/bold red] {e}")
        raise typer.Exit(code=1)


def _collect_aws_config() -> Dict[str, Any]:
    """Coleta configurações específicas da AWS."""
    aws_region = typer.prompt("Qual a região da AWS?", default="us-east-1")
    s3_bucket = typer.prompt("Qual o nome do bucket S3 para o backend?")
    
    return {
        "aws_region": aws_region,
        "bucket_name": s3_bucket
    }


def _collect_azure_config() -> Dict[str, Any]:
    """Coleta configurações específicas do Azure."""
    resource_group = typer.prompt("Qual o nome do Resource Group para o backend?")
    storage_account = typer.prompt("Qual o nome do Storage Account para o backend?")
    container = typer.prompt("Qual o nome do Container no Storage Account?", default="tfstate")
    
    return {
        "resource_group_name": resource_group,
        "storage_account_name": storage_account,
        "container_name": container
    }


def _collect_azure_resource_config() -> Dict[str, Any]:
    """Coleta configurações para recursos do Azure."""
    location = typer.prompt("Qual a localização/região do Azure?", default="East US")
    location_short = typer.prompt("Qual o nome curto da localização (ex: 'eus' para East US)?", default="eus")
    
    return {
        "location": location,
        "location_short": location_short
    }