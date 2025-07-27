"""Comandos para configuração do ambiente DevOps."""

import typer
from rich import print
from typing import Optional, List

from ..system.environment_manager import EnvironmentManager
from ..system.docker_installer import DockerInstaller
from ..system.installers.terraform_installer import TerraformInstaller
from ..system.installers.git_installer import GitInstaller
from ..config.constants import Tool, DEVOPS_TOOLS_CONFIG


def setup_environment(
    check_only: bool = typer.Option(False, "--check-only", help="Apenas verificar o ambiente atual"),
    required_only: bool = typer.Option(False, "--required-only", help="Instalar apenas ferramentas obrigatórias"),
    skip_docker: bool = typer.Option(False, "--skip-docker", help="Pular instalação do Docker"),
    force: bool = typer.Option(False, "--force", "-f", help="Forçar reinstalação de ferramentas"),
    tools: Optional[List[str]] = typer.Option(None, "--tools", "-t", help="Instalar apenas ferramentas específicas (ex: terraform,git)")
) -> None:
    """
    Configura o ambiente DevOps completo para o curso.
    
    Este comando verifica e instala todas as ferramentas necessárias:
    - Docker (obrigatório)
    - Git (obrigatório) 
    - Terraform (obrigatório)
    - Azure CLI (opcional)
    - AWS CLI v2 (opcional)
    - kubectl (opcional)
    - Ansible (opcional)
    - watch (opcional)
    """
    print(":rocket: [bold green]Setup do Ambiente DevOps[/bold green]")
    print()
    
    # Inicializar gerenciador
    env_manager = EnvironmentManager()
    
    # Modo apenas verificação
    if check_only:
        env_manager.show_status_report()
        return
    
    # Verificar status atual
    print(":mag: [bold blue]Verificando ambiente atual...[/bold blue]")
    env_manager.check_all_tools()
    env_manager.show_status_report()
    
    # Determinar ferramentas a instalar
    if tools:
        # Lista específica de ferramentas
        selected_tools = []
        for tool_name in tools:
            try:
                tool = Tool(tool_name.lower())
                selected_tools.append(tool)
            except ValueError:
                print(f":warning: [yellow]Ferramenta desconhecida: {tool_name}[/yellow]")
        
        if not selected_tools:
            print(":x: [red]Nenhuma ferramenta válida especificada[/red]")
            raise typer.Exit(1)
        
        tools_to_install = [t for t in selected_tools if not env_manager.tools_status.get(t, None) or not env_manager.tools_status[t].installed]
    
    elif required_only:
        # Apenas ferramentas obrigatórias
        tools_to_install = env_manager.get_missing_tools(only_required=True)
    
    else:
        # Todas as ferramentas não instaladas
        tools_to_install = env_manager.get_missing_tools(only_required=False)
    
    # Filtrar Docker se solicitado
    if skip_docker and Tool.DOCKER in tools_to_install:
        tools_to_install.remove(Tool.DOCKER)
        print(":information: [blue]Docker será pulado conforme solicitado[/blue]")
    
    # Verificar se há algo para instalar
    if not tools_to_install:
        print(":white_check_mark: [green]Todas as ferramentas selecionadas já estão instaladas![/green]")
        return
    
    # Mostrar plano de instalação
    print(f"\\n:wrench: [bold cyan]Plano de Instalação:[/bold cyan]")
    for tool in tools_to_install:
        config = DEVOPS_TOOLS_CONFIG[tool]
        required_text = "[red](obrigatória)[/red]" if config["required"] else "[yellow](opcional)[/yellow]"
        print(f"  • [blue]{config['name']}[/blue] {required_text} - {config['description']}")
    
    # Confirmar instalação
    if not force:
        print()
        confirm = typer.confirm("Deseja continuar com a instalação?")
        if not confirm:
            print(":x: [yellow]Instalação cancelada pelo usuário[/yellow]")
            raise typer.Exit(0)
    
    print("\\n:gear: [bold green]Iniciando instalação das ferramentas...[/bold green]")
    
    # Instalar ferramentas uma por vez
    success_count = 0
    for tool in tools_to_install:
        config = DEVOPS_TOOLS_CONFIG[tool]
        print(f"\\n:arrow_forward: [bold blue]Instalando {config['name']}...[/bold blue]")
        
        try:
            success = _install_tool(tool, env_manager.system_info, force)
            if success:
                print(f":white_check_mark: [green]{config['name']} instalado com sucesso![/green]")
                success_count += 1
            else:
                print(f":x: [red]Falha ao instalar {config['name']}[/red]")
        
        except Exception as e:
            print(f":x: [red]Erro ao instalar {config['name']}: {str(e)}[/red]")
    
    # Relatório final
    print(f"\\n:chart_with_upwards_trend: [bold cyan]Relatório de Instalação:[/bold cyan]")
    print(f"  • [green]Instaladas com sucesso:[/green] {success_count}")
    print(f"  • [red]Falharam:[/red] {len(tools_to_install) - success_count}")
    
    # Verificar ambiente final
    print("\\n:mag: [bold blue]Verificando ambiente após instalação...[/bold blue]")
    env_manager.check_all_tools()
    env_manager.show_status_report()
    
    # Status final
    if env_manager.is_environment_ready():
        print("\\n:party_popper: [bold green]Ambiente DevOps configurado com sucesso![/bold green]")
        print(":information: [blue]Você está pronto para o curso![/blue]")
    else:
        missing = env_manager.get_missing_tools(only_required=True)
        print(f"\\n:warning: [yellow]Ainda faltam algumas ferramentas obrigatórias: {[DEVOPS_TOOLS_CONFIG[t]['name'] for t in missing]}[/yellow]")
        print(":information: [blue]Execute novamente o comando para tentar instalar as ferramentas em falta[/blue]")


def environment_status() -> None:
    """Mostra o status atual de todas as ferramentas DevOps."""
    env_manager = EnvironmentManager()
    env_manager.show_status_report()


def _install_tool(tool: Tool, system_info, force: bool = False) -> bool:
    """
    Instala uma ferramenta específica.
    
    Args:
        tool: Ferramenta a ser instalada
        system_info: Informações do sistema
        force: Forçar reinstalação
        
    Returns:
        bool: True se a instalação foi bem-sucedida
    """
    try:
        if tool == Tool.DOCKER:
            # Docker já tem instalador dedicado
            docker_installer = DockerInstaller()
            return docker_installer.install(force=force, test_after_install=True)
        
        elif tool == Tool.GIT:
            return _install_git(system_info)
        
        elif tool == Tool.TERRAFORM:
            return _install_terraform(system_info)
        
        elif tool == Tool.AZURE_CLI:
            return _install_azure_cli(system_info)
        
        elif tool == Tool.AWS_CLI:
            return _install_aws_cli(system_info)
        
        elif tool == Tool.KUBECTL:
            return _install_kubectl(system_info)
        
        elif tool == Tool.ANSIBLE:
            return _install_ansible(system_info)
        
        elif tool == Tool.WATCH:
            return _install_watch(system_info)
        
        else:
            print(f":warning: [yellow]Instalador para {tool.value} não implementado ainda[/yellow]")
            return False
    
    except Exception as e:
        print(f":x: [red]Erro durante instalação de {tool.value}: {str(e)}[/red]")
        return False


def _install_git(system_info) -> bool:
    """Instala Git baseado no sistema operacional."""
    try:
        git_installer = GitInstaller(system_info)
        return git_installer.install()
    except Exception as e:
        print(f":x: [red]Erro durante instalação do Git: {str(e)}[/red]")
        return False


def _install_terraform(system_info) -> bool:
    """Instala Terraform baseado no sistema operacional."""
    try:
        terraform_installer = TerraformInstaller(system_info)
        return terraform_installer.install()
    except Exception as e:
        print(f":x: [red]Erro durante instalação do Terraform: {str(e)}[/red]")
        return False


def _install_azure_cli(system_info) -> bool:
    """Instala Azure CLI baseado no sistema operacional."""
    print(":information: [blue]Instalação do Azure CLI será implementada na próxima etapa[/blue]")
    return False


def _install_aws_cli(system_info) -> bool:
    """Instala AWS CLI v2 baseado no sistema operacional."""
    print(":information: [blue]Instalação do AWS CLI será implementada na próxima etapa[/blue]")
    return False


def _install_kubectl(system_info) -> bool:
    """Instala kubectl baseado no sistema operacional."""
    print(":information: [blue]Instalação do kubectl será implementada na próxima etapa[/blue]")
    return False


def _install_ansible(system_info) -> bool:
    """Instala Ansible baseado no sistema operacional."""
    print(":information: [blue]Instalação do Ansible será implementada na próxima etapa[/blue]")
    return False


def _install_watch(system_info) -> bool:
    """Instala watch baseado no sistema operacional."""
    print(":information: [blue]Instalação do watch será implementada na próxima etapa[/blue]")
    return False