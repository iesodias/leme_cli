#!/usr/bin/env python3

import typer
from rich import print
from typing import Optional

from src.commands.install_commands import install_docker, uninstall_docker, check_docker_status, system_info, install_azure_cli, install_aws_cli
from src.commands.environment_commands import setup_environment, environment_status

# --- Configuração da Aplicação ---
app = typer.Typer(
    help="CLI para configuração automática de ambiente DevOps.",
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


install_app = typer.Typer(help="Instala ferramentas necessárias (Docker, etc).")
app.add_typer(install_app, name="install")

# --- Comandos da CLI ---


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


@install_app.command("azure-cli")
def install_azure_cli_command(
    force: bool = typer.Option(False, "--force", "-f", help="Forçar reinstalação mesmo se já estiver instalado"),
    manual: bool = typer.Option(False, "--manual", help="Mostrar instruções para instalação manual")
):
    """Instala o Azure CLI automaticamente baseado no sistema operacional."""
    install_azure_cli(force, manual)


@install_app.command("aws-cli")
def install_aws_cli_command(
    force: bool = typer.Option(False, "--force", "-f", help="Forçar reinstalação mesmo se já estiver instalado"),
    manual: bool = typer.Option(False, "--manual", help="Mostrar instruções para instalação manual")
):
    """Instala o AWS CLI v2 automaticamente baseado no sistema operacional."""
    install_aws_cli(force, manual)


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
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Perguntar para cada ferramenta se deseja instalar"),
    tools: Optional[str] = typer.Option(None, "--tools", "-t", help="Instalar apenas ferramentas específicas (ex: git,docker)")
):
    """Configura o ambiente DevOps completo para o curso."""
    tools_list = tools.split(',') if tools else None
    setup_environment(check_only, required_only, skip_docker, force, interactive, tools_list)


@app.command("environment-status") 
def environment_status_command():
    """Mostra o status detalhado de todas as ferramentas DevOps."""
    environment_status()


if __name__ == "__main__":
    app()
