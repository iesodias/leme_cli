#!/usr/bin/env python3

import typer
from rich import print
from pathlib import Path
from typing import Optional

from src.config.constants import TerraformAction
from src.commands.new_commands import create_project, create_module, create_resource
from src.commands.delete_commands import delete_project
from src.commands.terraform_commands import run_terraform_command
from src.commands.install_commands import install_docker, uninstall_docker, check_docker_status, system_info
from src.commands.environment_commands import setup_environment, environment_status

# --- Configuração da Aplicação ---
app = typer.Typer(
    help="CLI para gerar, gerenciar e executar projetos e recursos de IaC com Terraform.",
    add_completion=False,
    add_help_option=False
)

# --- Callback Principal para Opções Globais ---
@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    help: Optional[bool] = typer.Option(
        None,
        "--help",
        "-h",
        is_eager=True,
        help="Mostra esta mensagem de ajuda e sai.",
        show_default=False
    )
):
    """
    Callback principal para gerenciar opções globais como --help.
    Se nenhum comando for passado, mostra a ajuda.
    """
    if help:
        typer.echo(ctx.get_help())
        raise typer.Exit()
    
    if ctx.invoked_subcommand is None:
        print("[bold yellow]Nenhum comando especificado. Use --help para ver as opções.[/bold yellow]")
        typer.echo(ctx.get_help())
        raise typer.Exit()


# Cria sub-apps para agrupar comandos
new_app = typer.Typer(help="Cria um novo projeto, módulo ou recurso.")
app.add_typer(new_app, name="new")

install_app = typer.Typer(help="Instala ferramentas necessárias (Docker, etc).")
app.add_typer(install_app, name="install")

# --- Comandos da CLI ---

@new_app.command("project")
def new_project(
    name: str = typer.Option(..., "--name", "-n", help="O nome do projeto."),
    provider: str = typer.Option(..., "--provider", "-p", help="O provedor de nuvem: 'aws' ou 'azure'."),
    path: str = typer.Option(".", "--path", help="Diretório onde criar o projeto (padrão: diretório atual).")
):
    """
    Cria a estrutura de um novo projeto Terraform para um provedor específico.
    """
    create_project(name, provider, path)


@new_app.command("module")
def new_module(
    name: str = typer.Option(..., "--name", "-n", help="O nome do módulo."),
    path: str = typer.Option(".", "--path", help="Diretório onde criar o módulo (padrão: diretório atual).")
):
    """Cria a estrutura de um novo módulo Terraform reutilizável."""
    create_module(name, path)


@new_app.command("resource")
def new_resource(
    resource_type: str = typer.Option(..., "--type", "-t", help="Tipo do recurso a ser criado (ex: storage-account, virtual_machine)."),
    provider: str = typer.Option(..., "--provider", "-p", help="O provedor de nuvem: 'aws' ou 'azure'."),
    name: str = typer.Option(..., "--name", "-n", help="O nome para o módulo do recurso (será o nome da pasta)."),
    path: str = typer.Option(".", "--path", help="Diretório onde criar o recurso (padrão: diretório atual).")
):
    """Cria um módulo Terraform para um recurso específico."""
    create_resource(resource_type, provider, name, path)


@app.command("delete")
def delete_project_command(
    project_path: Path = typer.Argument(
        ...,
        help="O caminho para o diretório do projeto que será apagado.",
        exists=True, file_okay=False, dir_okay=True, resolve_path=True,
    ),
    force: bool = typer.Option(
        False, "--force", "-f",
        help="Forçar a exclusão sem pedir confirmação. USE COM CUIDADO!",
    )
):
    """Apaga um diretório de projeto e todo o seu conteúdo de forma permanente."""
    delete_project(project_path, force)


@app.command("run")
def run_terraform(
    action: TerraformAction = typer.Argument(..., help="Comando do Terraform a ser executado."),
    project_path: Path = typer.Argument(
        ...,
        help="Caminho para o projeto Terraform.",
        exists=True, file_okay=False, dir_okay=True, resolve_path=True,
    )
):
    """Executa um comando Terraform dentro do diretório de um projeto."""
    run_terraform_command(action, project_path)


# --- Comandos de Instalação ---

@install_app.command("docker")
def install_docker_command(
    check_only: bool = typer.Option(False, "--check-only", help="Apenas verificar se o Docker está instalado"),
    force: bool = typer.Option(False, "--force", "-f", help="Forçar reinstalação mesmo se já estiver instalado"),
    manual: bool = typer.Option(False, "--manual", help="Mostrar instruções para instalação manual"),
    no_test: bool = typer.Option(False, "--no-test", help="Não testar a instalação após completar")
):
    """Instala o Docker automaticamente baseado no sistema operacional."""
    install_docker(check_only, force, manual, no_test)


@app.command("status")
def status_command():
    """Verifica o status das ferramentas instaladas."""
    check_docker_status()


@app.command("system-info")
def system_info_command():
    """Mostra informações detalhadas do sistema operacional."""
    system_info()


@app.command("uninstall-docker")
def uninstall_docker_command():
    """Remove o Docker do sistema."""
    uninstall_docker()


@app.command("setup-environment")
def setup_environment_command(
    check_only: bool = typer.Option(False, "--check-only", help="Apenas verificar o ambiente atual"),
    required_only: bool = typer.Option(False, "--required-only", help="Instalar apenas ferramentas obrigatórias"),
    skip_docker: bool = typer.Option(False, "--skip-docker", help="Pular instalação do Docker"),
    force: bool = typer.Option(False, "--force", "-f", help="Forçar reinstalação de ferramentas"),
    tools: Optional[str] = typer.Option(None, "--tools", "-t", help="Instalar apenas ferramentas específicas (ex: terraform,git)")
):
    """Configura o ambiente DevOps completo para o curso."""
    tools_list = tools.split(',') if tools else None
    setup_environment(check_only, required_only, skip_docker, force, tools_list)


@app.command("environment-status") 
def environment_status_command():
    """Mostra o status detalhado de todas as ferramentas DevOps."""
    environment_status()


if __name__ == "__main__":
    app()
