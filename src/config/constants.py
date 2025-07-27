"""Constantes e configurações da aplicação."""

import enum
from pathlib import Path


class Provider(str, enum.Enum):
    """Provedores de nuvem suportados."""
    AWS = "aws"
    AZURE = "azure"


class TerraformAction(str, enum.Enum):
    """Comandos do Terraform suportados."""
    INIT = "init"
    VALIDATE = "validate"
    PLAN = "plan"
    APPLY = "apply"
    DESTROY = "destroy"


class ResourceType(str, enum.Enum):
    """Tipos de recursos suportados."""
    STORAGE_ACCOUNT = "storage-account"
    VIRTUAL_MACHINE = "virtual_machine"


class Tool(str, enum.Enum):
    """Ferramentas que podem ser instaladas."""
    DOCKER = "docker"
    TERRAFORM = "terraform"
    ANSIBLE = "ansible"
    AZURE_CLI = "az"
    AWS_CLI = "aws"
    GIT = "git"
    KUBECTL = "kubectl"
    WATCH = "watch"


# Configurações de paths
BASE_PATH = Path(__file__).parent.parent.parent
TEMPLATES_PATH = BASE_PATH / "templates"
SRC_PATH = BASE_PATH / "src"

# Configurações de templates
TEMPLATE_FILES = {
    "main": "main.tf",
    "variables": "variables.tf", 
    "outputs": "outputs.tf",
    "providers": "providers.tf",
    "backend": "backend.tf",
    "gitignore": ".gitignore"
}

# Mapeamento de templates por provider
PROVIDER_TEMPLATES = {
    Provider.AWS: {
        "backend": "s3_backend.tf.j2",
        "provider": "aws_provider.tf.j2"
    },
    Provider.AZURE: {
        "backend": "azurerm_backend.tf.j2", 
        "provider": "provider.tf.j2"
    }
}

# Configurações padrão
DEFAULT_CONFIG = {
    "aws": {
        "region": "us-east-1"
    },
    "azure": {
        "location": "East US",
        "location_short": "eus",
        "container": "tfstate"
    }
}

# Configurações das ferramentas DevOps
DEVOPS_TOOLS_CONFIG = {
    Tool.DOCKER: {
        "name": "Docker",
        "description": "Plataforma de containerização",
        "check_command": ["docker", "--version"],
        "priority": 1,
        "required": True
    },
    Tool.GIT: {
        "name": "Git",
        "description": "Sistema de controle de versão",
        "check_command": ["git", "--version"],
        "priority": 2,
        "required": True
    },
    Tool.TERRAFORM: {
        "name": "Terraform",
        "description": "Infrastructure as Code",
        "check_command": ["terraform", "--version"],
        "priority": 3,
        "required": True
    },
    Tool.AZURE_CLI: {
        "name": "Azure CLI",
        "description": "Interface de linha de comando da Azure",
        "check_command": ["az", "--version"],
        "priority": 4,
        "required": False
    },
    Tool.AWS_CLI: {
        "name": "AWS CLI v2",
        "description": "Interface de linha de comando da AWS",
        "check_command": ["aws", "--version"],
        "priority": 5,
        "required": False
    },
    Tool.KUBECTL: {
        "name": "kubectl",
        "description": "Cliente para Kubernetes",
        "check_command": ["kubectl", "version", "--client"],
        "priority": 6,
        "required": False
    },
    Tool.ANSIBLE: {
        "name": "Ansible",
        "description": "Automação e gerenciamento de configuração",
        "check_command": ["ansible", "--version"],
        "priority": 7,
        "required": False
    },
    Tool.WATCH: {
        "name": "watch",
        "description": "Executa comandos periodicamente",
        "check_command": ["watch", "--version"],
        "priority": 8,
        "required": False
    }
}