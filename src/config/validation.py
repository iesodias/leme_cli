"""Módulo de validação e verificações."""

import shutil
from pathlib import Path
from typing import List, Optional
from jinja2 import Environment

from .constants import Provider, ResourceType, TEMPLATES_PATH


class ValidationError(Exception):
    """Exceção customizada para erros de validação."""
    pass


def validate_terraform_installed() -> None:
    """Verifica se o Terraform está instalado no sistema."""
    if not shutil.which("terraform"):
        raise ValidationError(
            "O comando 'terraform' não foi encontrado no seu sistema. "
            "Por favor, instale o Terraform e garanta que ele esteja no seu PATH."
        )


def validate_provider(provider: str) -> Provider:
    """Valida se o provider é suportado."""
    try:
        return Provider(provider.lower())
    except ValueError:
        supported = ", ".join([p.value for p in Provider])
        raise ValidationError(
            f"Provedor '{provider}' não é suportado. "
            f"Provedores suportados: {supported}"
        )


def validate_resource_type(resource_type: str, provider: Provider) -> ResourceType:
    """Valida se o tipo de recurso é suportado para o provider."""
    try:
        resource_enum = ResourceType(resource_type.lower())
    except ValueError:
        supported = ", ".join([r.value for r in ResourceType])
        raise ValidationError(
            f"Tipo de recurso '{resource_type}' não é suportado. "
            f"Tipos suportados: {supported}"
        )
    
    # Verificar se o template existe para este provider/recurso
    template_path = TEMPLATES_PATH / "providers" / provider.value / "resource" / resource_enum.value
    if not template_path.is_dir():
        raise ValidationError(
            f"Recurso do tipo '{resource_type}' não é suportado para o provedor '{provider.value}'"
        )
    
    return resource_enum


def validate_directory_not_exists(path: Path) -> None:
    """Verifica se o diretório não existe."""
    if path.exists():
        raise ValidationError(f"O diretório '{path}' já existe.")


def validate_directory_exists(path: Path) -> None:
    """Verifica se o diretório existe."""
    if not path.exists():
        raise ValidationError(f"O diretório '{path}' não existe.")
    if not path.is_dir():
        raise ValidationError(f"'{path}' não é um diretório.")


def validate_template_exists(template_path: str, jinja_env: Environment) -> None:
    """Verifica se um template existe."""
    try:
        jinja_env.get_template(template_path)
    except Exception:
        raise ValidationError(f"Template '{template_path}' não encontrado.")


def validate_required_templates(provider: Provider, is_project: bool = False) -> List[str]:
    """Valida se todos os templates necessários existem para um provider."""
    missing_templates = []
    
    base_path = f"providers/{provider.value}"
    
    if is_project:
        template_path = f"{base_path}/project"
        required_files = ["main.tf.j2", "variables.tf.j2", "outputs.tf.j2", "provider.tf.j2"]
    else:
        template_path = f"{base_path}"
        required_files = ["provider.tf.j2"]
    
    for file in required_files:
        full_path = TEMPLATES_PATH / template_path / file
        if not full_path.exists():
            missing_templates.append(f"{template_path}/{file}")
    
    return missing_templates


def validate_project_name(name: str) -> None:
    """Valida o nome do projeto."""
    if not name:
        raise ValidationError("Nome do projeto não pode estar vazio.")
    
    if not name.replace("-", "").replace("_", "").isalnum():
        raise ValidationError(
            "Nome do projeto deve conter apenas letras, números, hífens e underscores."
        )


def validate_template_variables(template_data: dict, required_vars: List[str]) -> None:
    """Valida se todas as variáveis necessárias estão presentes."""
    missing_vars = [var for var in required_vars if var not in template_data]
    if missing_vars:
        raise ValidationError(
            f"Variáveis obrigatórias faltando: {', '.join(missing_vars)}"
        )