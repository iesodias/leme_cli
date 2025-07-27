"""Instalador do Terraform para diferentes sistemas operacionais."""

import subprocess
import os
import tempfile
import tarfile
import zipfile
from pathlib import Path
from typing import Optional, List
from rich import print

from .base_installer import BaseInstaller
from ..system_detector import SystemInfo, OperatingSystem


class TerraformInstaller(BaseInstaller):
    """Instalador especializado para Terraform."""
    
    def __init__(self, system_info: SystemInfo):
        """
        Inicializa o instalador do Terraform.
        
        Args:
            system_info: Informações do sistema operacional
        """
        super().__init__(system_info)
        self.tool_name = "Terraform"
        self.version = "1.7.1"  # Versão estável mais recente
        
    def is_installed(self) -> bool:
        """
        Verifica se o Terraform está instalado.
        
        Returns:
            bool: True se o Terraform estiver instalado
        """
        try:
            result = subprocess.run(
                ["terraform", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def get_installed_version(self) -> Optional[str]:
        """
        Obtém a versão instalada do Terraform.
        
        Returns:
            Optional[str]: Versão instalada ou None
        """
        try:
            result = subprocess.run(
                ["terraform", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                # Terraform v1.7.1
                first_line = result.stdout.strip().split('\n')[0]
                if "Terraform" in first_line:
                    return first_line.replace("Terraform", "").strip()
            return None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
    
    def install(self) -> bool:
        """
        Instala o Terraform baseado no sistema operacional.
        
        Returns:
            bool: True se a instalação foi bem-sucedida
        """
        print(f":gear: [blue]Instalando {self.tool_name}...[/blue]")
        
        try:
            if self.system_info.os_type == OperatingSystem.MACOS:
                return self._install_macos()
            
            elif self.system_info.os_type in [
                OperatingSystem.UBUNTU, OperatingSystem.WSL_UBUNTU,
                OperatingSystem.DEBIAN, OperatingSystem.WSL_DEBIAN
            ]:
                return self._install_ubuntu()
            
            elif self.system_info.os_type in [
                OperatingSystem.CENTOS, OperatingSystem.RHEL, OperatingSystem.FEDORA
            ]:
                return self._install_redhat()
            
            else:
                print(f":warning: [yellow]Sistema {self.system_info.os_type.value} não suportado para instalação automática do Terraform[/yellow]")
                return self._show_manual_instructions()
        
        except Exception as e:
            print(f":x: [red]Erro durante instalação do Terraform: {str(e)}[/red]")
            return False
    
    def _install_macos(self) -> bool:
        """Instala Terraform no macOS."""
        print(":apple: [blue]Detectado macOS - usando Homebrew[/blue]")
        
        # Verificar se Homebrew está disponível
        if not self._check_homebrew():
            print(":warning: [yellow]Homebrew não encontrado, tentando instalação manual[/yellow]")
            return self._install_manual_binary()
        
        try:
            # Instalar via Homebrew
            print(":beer: [blue]Instalando Terraform via Homebrew...[/blue]")
            result = subprocess.run(
                ["brew", "install", "terraform"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print(":white_check_mark: [green]Terraform instalado via Homebrew![/green]")
                return True
            else:
                print(f":warning: [yellow]Falha no Homebrew: {result.stderr}[/yellow]")
                return self._install_manual_binary()
        
        except subprocess.TimeoutExpired:
            print(":warning: [yellow]Timeout do Homebrew, tentando instalação manual[/yellow]")
            return self._install_manual_binary()
    
    def _install_ubuntu(self) -> bool:
        """Instala Terraform no Ubuntu/Debian."""
        print(":gear: [blue]Detectado Ubuntu/Debian - usando repositório oficial[/blue]")
        
        try:
            # Método 1: Tentar repositório oficial HashiCorp
            if self._install_ubuntu_repo():
                return True
            
            # Método 2: Fallback para instalação manual
            print(":information: [blue]Tentando instalação manual...[/blue]")
            return self._install_manual_binary()
        
        except Exception as e:
            print(f":warning: [yellow]Erro no método de repositório: {str(e)}[/yellow]")
            return self._install_manual_binary()
    
    def _install_ubuntu_repo(self) -> bool:
        """Instala via repositório oficial do HashiCorp."""
        try:
            # Adicionar chave GPG do HashiCorp
            print(":key: [blue]Adicionando chave GPG do HashiCorp...[/blue]")
            subprocess.run([
                "wget", "-O-", "https://apt.releases.hashicorp.com/gpg"
            ], check=True, capture_output=True)
            
            subprocess.run([
                "sudo", "gpg", "--dearmor", "-o", "/usr/share/keyrings/hashicorp-archive-keyring.gpg"
            ], input=subprocess.PIPE, check=True)
            
            # Adicionar repositório
            print(":package: [blue]Adicionando repositório HashiCorp...[/blue]")
            distro = self._get_ubuntu_codename()
            repo_line = f"deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com {distro} main"
            
            subprocess.run([
                "echo", repo_line, "|", "sudo", "tee", "/etc/apt/sources.list.d/hashicorp.list"
            ], shell=True, check=True)
            
            # Atualizar e instalar
            print(":arrows_counterclockwise: [blue]Atualizando repositórios...[/blue]")
            subprocess.run(["sudo", "apt", "update"], check=True, capture_output=True)
            
            print(":package: [blue]Instalando Terraform...[/blue]")
            subprocess.run(["sudo", "apt", "install", "-y", "terraform"], check=True)
            
            print(":white_check_mark: [green]Terraform instalado via repositório oficial![/green]")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f":warning: [yellow]Falha no repositório oficial: {e}[/yellow]")
            return False
    
    def _install_redhat(self) -> bool:
        """Instala Terraform no CentOS/RHEL/Fedora."""
        print(":gear: [blue]Detectado sistema RedHat - usando repositório oficial[/blue]")
        
        try:
            # Determinar gerenciador de pacotes
            if self.system_info.os_type == OperatingSystem.FEDORA:
                pkg_manager = "dnf"
            else:
                pkg_manager = "yum"
            
            # Adicionar repositório HashiCorp
            print(":package: [blue]Adicionando repositório HashiCorp...[/blue]")
            subprocess.run([
                "sudo", pkg_manager, "install", "-y", "yum-utils"
            ], check=True)
            
            subprocess.run([
                "sudo", pkg_manager, "config-manager", "--add-repo",
                "https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo"
            ], check=True)
            
            # Instalar Terraform
            print(":package: [blue]Instalando Terraform...[/blue]")
            subprocess.run([
                "sudo", pkg_manager, "install", "-y", "terraform"
            ], check=True)
            
            print(":white_check_mark: [green]Terraform instalado via repositório oficial![/green]")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f":warning: [yellow]Falha no repositório: {e}[/yellow]")
            return self._install_manual_binary()
    
    def _install_manual_binary(self) -> bool:
        """Instala Terraform baixando o binário diretamente."""
        print(":download: [blue]Instalação manual - baixando binário...[/blue]")
        
        try:
            # Determinar arquitetura e URL
            arch = self._get_architecture()
            os_name = self._get_os_name()
            
            if not arch or not os_name:
                print(":x: [red]Não foi possível determinar arquitetura/OS[/red]")
                return False
            
            url = f"https://releases.hashicorp.com/terraform/{self.version}/terraform_{self.version}_{os_name}_{arch}.zip"
            
            # Baixar arquivo
            print(f":arrow_down: [blue]Baixando {url}...[/blue]")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                zip_file = temp_path / "terraform.zip"
                
                # Download
                result = subprocess.run([
                    "curl", "-L", "-o", str(zip_file), url
                ], capture_output=True)
                
                if result.returncode != 0:
                    print(":x: [red]Falha no download[/red]")
                    return False
                
                # Extrair
                print(":package: [blue]Extraindo arquivo...[/blue]")
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)
                
                # Instalar binário
                terraform_bin = temp_path / "terraform"
                if not terraform_bin.exists():
                    print(":x: [red]Binário do Terraform não encontrado no arquivo[/red]")
                    return False
                
                # Tornar executável
                terraform_bin.chmod(0o755)
                
                # Mover para local do sistema
                if os_name == "darwin":  # macOS
                    install_path = Path("/usr/local/bin/terraform")
                else:  # Linux
                    install_path = Path("/usr/local/bin/terraform")
                
                # Instalar (pode precisar de sudo)
                try:
                    subprocess.run([
                        "sudo", "cp", str(terraform_bin), str(install_path)
                    ], check=True)
                    
                    subprocess.run([
                        "sudo", "chmod", "755", str(install_path)
                    ], check=True)
                    
                except subprocess.CalledProcessError:
                    # Tentar sem sudo (se usuário tiver permissões)
                    try:
                        subprocess.run([
                            "cp", str(terraform_bin), str(install_path)
                        ], check=True)
                    except subprocess.CalledProcessError:
                        print(":x: [red]Falha ao instalar binário (sem permissões)[/red]")
                        return False
                
                print(":white_check_mark: [green]Terraform instalado manualmente![/green]")
                return True
        
        except Exception as e:
            print(f":x: [red]Erro na instalação manual: {str(e)}[/red]")
            return False
    
    def _get_architecture(self) -> Optional[str]:
        """Retorna a arquitetura para download."""
        arch_map = {
            "x86_64": "amd64",
            "amd64": "amd64",
            "arm64": "arm64",
            "aarch64": "arm64"
        }
        return arch_map.get(self.system_info.architecture.lower())
    
    def _get_os_name(self) -> Optional[str]:
        """Retorna o nome do OS para download."""
        if self.system_info.os_type == OperatingSystem.MACOS:
            return "darwin"
        elif self.system_info.os_type in [
            OperatingSystem.UBUNTU, OperatingSystem.WSL_UBUNTU,
            OperatingSystem.DEBIAN, OperatingSystem.WSL_DEBIAN,
            OperatingSystem.CENTOS, OperatingSystem.RHEL,
            OperatingSystem.FEDORA
        ]:
            return "linux"
        return None
    
    def _get_ubuntu_codename(self) -> str:
        """Obtém o codename da distribuição Ubuntu."""
        try:
            result = subprocess.run([
                "lsb_release", "-cs"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        # Fallback baseado na versão
        version_map = {
            "22.04": "jammy",
            "20.04": "focal", 
            "18.04": "bionic"
        }
        return version_map.get(self.system_info.os_version, "jammy")
    
    def _check_homebrew(self) -> bool:
        """Verifica se o Homebrew está instalado."""
        try:
            subprocess.run(["brew", "--version"], capture_output=True, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False
    
    def _show_manual_instructions(self) -> bool:
        """Mostra instruções para instalação manual."""
        print(":information_source: [cyan]Instruções para instalação manual do Terraform:[/cyan]")
        print()
        print("1. Acesse: https://www.terraform.io/downloads")
        print("2. Baixe a versão para seu sistema operacional")
        print("3. Extraia o arquivo e mova o binário para um diretório no PATH")
        print("4. Exemplo Linux/macOS:")
        print("   sudo mv terraform /usr/local/bin/")
        print("   sudo chmod +x /usr/local/bin/terraform")
        print()
        return False
    
    def get_install_commands(self) -> List[str]:
        """
        Retorna lista de comandos para instalação manual.
        
        Returns:
            List[str]: Lista de comandos
        """
        if self.system_info.os_type == OperatingSystem.MACOS:
            return [
                "# Via Homebrew (recomendado)",
                "brew install terraform",
                "",
                "# Ou instalação manual:",
                f"curl -LO https://releases.hashicorp.com/terraform/{self.version}/terraform_{self.version}_darwin_arm64.zip",
                "unzip terraform_*.zip",
                "sudo mv terraform /usr/local/bin/",
                "sudo chmod +x /usr/local/bin/terraform"
            ]
        
        elif self.system_info.os_type in [
            OperatingSystem.UBUNTU, OperatingSystem.WSL_UBUNTU,
            OperatingSystem.DEBIAN, OperatingSystem.WSL_DEBIAN
        ]:
            return [
                "# Via repositório oficial HashiCorp",
                "wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg",
                f"echo 'deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com {self._get_ubuntu_codename()} main' | sudo tee /etc/apt/sources.list.d/hashicorp.list",
                "sudo apt update",
                "sudo apt install terraform"
            ]
        
        elif self.system_info.os_type in [
            OperatingSystem.CENTOS, OperatingSystem.RHEL, OperatingSystem.FEDORA
        ]:
            pkg_manager = "dnf" if self.system_info.os_type == OperatingSystem.FEDORA else "yum"
            return [
                f"# Via repositório oficial HashiCorp",
                f"sudo {pkg_manager} install -y yum-utils",
                f"sudo {pkg_manager} config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo",
                f"sudo {pkg_manager} install terraform"
            ]
        
        else:
            return [
                "# Instalação manual",
                "1. Acesse: https://www.terraform.io/downloads",
                "2. Baixe a versão para seu sistema operacional",
                "3. Extraia o arquivo e mova o binário para um diretório no PATH",
                "4. Exemplo: sudo mv terraform /usr/local/bin/"
            ]

    def uninstall(self) -> bool:
        """
        Remove o Terraform do sistema.
        
        Returns:
            bool: True se a remoção foi bem-sucedida
        """
        print(f":wastebasket: [blue]Removendo {self.tool_name}...[/blue]")
        
        try:
            if self.system_info.os_type == OperatingSystem.MACOS:
                # Tentar remover via Homebrew primeiro
                try:
                    subprocess.run(["brew", "uninstall", "terraform"], check=True)
                    print(":white_check_mark: [green]Terraform removido via Homebrew![/green]")
                    return True
                except subprocess.CalledProcessError:
                    pass
            
            elif self.system_info.os_type in [
                OperatingSystem.UBUNTU, OperatingSystem.WSL_UBUNTU,
                OperatingSystem.DEBIAN, OperatingSystem.WSL_DEBIAN
            ]:
                try:
                    subprocess.run(["sudo", "apt", "remove", "-y", "terraform"], check=True)
                    print(":white_check_mark: [green]Terraform removido via apt![/green]")
                    return True
                except subprocess.CalledProcessError:
                    pass
            
            elif self.system_info.os_type in [
                OperatingSystem.CENTOS, OperatingSystem.RHEL, OperatingSystem.FEDORA
            ]:
                pkg_manager = "dnf" if self.system_info.os_type == OperatingSystem.FEDORA else "yum"
                try:
                    subprocess.run(["sudo", pkg_manager, "remove", "-y", "terraform"], check=True)
                    print(":white_check_mark: [green]Terraform removido via {pkg_manager}![/green]")
                    return True
                except subprocess.CalledProcessError:
                    pass
            
            # Fallback: remover binário manual
            for path in ["/usr/local/bin/terraform", "/usr/bin/terraform"]:
                if Path(path).exists():
                    try:
                        subprocess.run(["sudo", "rm", path], check=True)
                        print(f":white_check_mark: [green]Terraform removido de {path}![/green]")
                        return True
                    except subprocess.CalledProcessError:
                        continue
            
            print(":x: [red]Terraform não encontrado para remoção[/red]")
            return False
        
        except Exception as e:
            print(f":x: [red]Erro ao remover Terraform: {str(e)}[/red]")
            return False