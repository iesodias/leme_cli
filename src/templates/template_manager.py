"""Gerenciador de templates Jinja2."""

from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from rich import print

from ..config.constants import (
    Provider, TEMPLATES_PATH, TEMPLATE_FILES, 
    PROVIDER_TEMPLATES, DEFAULT_CONFIG
)
from ..config.validation import (
    ValidationError, validate_template_exists, 
    validate_template_variables
)


class TemplateManager:
    """Gerenciador de templates para geração de código Terraform."""
    
    def __init__(self):
        """Inicializa o gerenciador de templates."""
        self.jinja_env = Environment(
            loader=FileSystemLoader(TEMPLATES_PATH), 
            trim_blocks=True
        )
    
    def render_project_files(
        self, 
        provider: Provider, 
        template_data: Dict[str, Any], 
        project_path: Path
    ) -> None:
        """Renderiza todos os arquivos de um projeto."""
        files_to_generate = self._get_project_template_mapping(provider, template_data)
        
        # Adicionar gitignore comum
        files_to_generate["common/gitignore.j2"] = TEMPLATE_FILES["gitignore"]
        
        # Criar diretório do projeto
        project_path.mkdir(exist_ok=True)
        
        # Renderizar cada arquivo
        for template_name, output_filename in files_to_generate.items():
            self._render_file(template_name, template_data, project_path / output_filename)
    
    def render_resource_files(
        self, 
        provider: Provider, 
        resource_type: str,
        template_data: Dict[str, Any], 
        resource_path: Path
    ) -> None:
        """Renderiza arquivos de um recurso específico."""
        resource_path.mkdir(exist_ok=True)
        
        # Templates básicos do recurso
        base_template_path = f"providers/{provider.value}/resource/{resource_type}"
        resource_files = {
            f"{base_template_path}/main.tf.j2": TEMPLATE_FILES["main"],
            f"{base_template_path}/variables.tf.j2": TEMPLATE_FILES["variables"], 
            f"{base_template_path}/outputs.tf.j2": TEMPLATE_FILES["outputs"]
        }
        
        # Renderizar arquivos do recurso
        for template_name, output_filename in resource_files.items():
            self._render_file(template_name, template_data, resource_path / output_filename)
        
        # Adicionar provider
        provider_template = f"providers/{provider.value}/project/provider.tf.j2"
        self._render_file(provider_template, template_data, resource_path / TEMPLATE_FILES["providers"])
    
    def render_module_files(self, module_path: Path) -> None:
        """Cria arquivos vazios para um módulo."""
        module_path.mkdir(exist_ok=True)
        
        empty_files = [
            TEMPLATE_FILES["main"],
            TEMPLATE_FILES["variables"], 
            TEMPLATE_FILES["outputs"]
        ]
        
        for filename in empty_files:
            file_path = module_path / filename
            file_path.touch()
            print(f"  [green]✓[/green] Arquivo '{filename}' criado.")
    
    def _render_file(self, template_name: str, template_data: Dict[str, Any], output_path: Path) -> None:
        """Renderiza um arquivo específico."""
        try:
            template = self.jinja_env.get_template(template_name)
            rendered_content = template.render(template_data)
            output_path.write_text(rendered_content)
            print(f"  [green]✓[/green] Arquivo '{output_path.name}' criado.")
        except TemplateNotFound:
            print(f"  [yellow]![/yellow] Template '{template_name}' não encontrado. Pulando.")
        except Exception as e:
            print(f"  [red]✗[/red] Erro ao renderizar '{template_name}': {e}")
    
    def _get_project_template_mapping(self, provider: Provider, template_data: Dict[str, Any]) -> Dict[str, str]:
        """Retorna o mapeamento de templates para arquivos de projeto."""
        base_template_path = f"providers/{provider.value}/project"
        
        files_mapping = {
            f"{base_template_path}/main.tf.j2": TEMPLATE_FILES["main"],
            f"{base_template_path}/variables.tf.j2": TEMPLATE_FILES["variables"],
            f"{base_template_path}/outputs.tf.j2": TEMPLATE_FILES["outputs"],
            f"{base_template_path}/provider.tf.j2": TEMPLATE_FILES["providers"]
        }
        
        # Adicionar backend específico do provider
        if provider == Provider.AWS:
            files_mapping[f"{base_template_path}/s3_backend.tf.j2"] = TEMPLATE_FILES["backend"]
        elif provider == Provider.AZURE:
            files_mapping[f"{base_template_path}/azurerm_backend.tf.j2"] = TEMPLATE_FILES["backend"]
        
        return files_mapping
    
    def get_template_variables_for_provider(self, provider: Provider) -> Dict[str, Any]:
        """Retorna as variáveis padrão para um provider."""
        return DEFAULT_CONFIG.get(provider.value, {})
    
    def validate_all_templates(self, provider: Provider, resource_type: str = None) -> List[str]:
        """Valida se todos os templates necessários existem."""
        missing_templates = []
        
        # Validar templates de projeto
        project_templates = [
            f"providers/{provider.value}/project/main.tf.j2",
            f"providers/{provider.value}/project/variables.tf.j2", 
            f"providers/{provider.value}/project/outputs.tf.j2",
            f"providers/{provider.value}/project/provider.tf.j2"
        ]
        
        for template in project_templates:
            try:
                validate_template_exists(template, self.jinja_env)
            except ValidationError:
                missing_templates.append(template)
        
        # Validar templates de recurso se especificado
        if resource_type:
            resource_templates = [
                f"providers/{provider.value}/resource/{resource_type}/main.tf.j2",
                f"providers/{provider.value}/resource/{resource_type}/variables.tf.j2",
                f"providers/{provider.value}/resource/{resource_type}/outputs.tf.j2"
            ]
            
            for template in resource_templates:
                try:
                    validate_template_exists(template, self.jinja_env)
                except ValidationError:
                    missing_templates.append(template)
        
        return missing_templates