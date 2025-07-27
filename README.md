# CLI Leme - Configuração Automática de Ambiente DevOps

Ferramenta para configurar automaticamente seu ambiente de desenvolvimento DevOps com todas as ferramentas necessárias para o curso.

## O que esta CLI faz

A CLI Leme instala e configura automaticamente:
- **Docker** - Para containerização
- **Git** - Para controle de versão  
- **Terraform** - Para Infrastructure as Code
- **Outras ferramentas** - Azure CLI, AWS CLI v2, kubectl, Ansible (opcionais)

## Instalação e Uso

### Passo 1: Baixar a CLI
```bash
git clone https://github.com/iesodias/leme_cli.git
cd leme_cli
```

### Passo 2: Instalar dependências
```bash
pip install rich typer jinja2
```

### Passo 3: Configurar seu ambiente
```bash
python3 main.py setup-environment
```

### Passo 4: Verificar se tudo foi instalado
```bash
python3 main.py environment-status
```

## Comandos Principais

### Configurar ambiente completo
```bash
# Instalar todas as ferramentas automaticamente
python3 main.py setup-environment

# Instalar apenas ferramentas obrigatórias (Docker, Git, Terraform)
python3 main.py setup-environment --required-only

# Instalar ferramentas específicas
python3 main.py setup-environment --tools git,terraform,docker

# Forçar instalação sem perguntas
python3 main.py setup-environment --force
```

### Verificar status das ferramentas
```bash
# Ver quais ferramentas estão instaladas
python3 main.py environment-status

# Ver informações do seu sistema
python3 main.py system-info
```

### Trabalhar com projetos Terraform
```bash
# Criar um novo projeto Azure
python3 main.py new project --name meu-projeto --provider azure

# Criar um projeto AWS
python3 main.py new project --name meu-projeto --provider aws

# Executar comandos Terraform
python3 main.py run init meu-projeto
python3 main.py run plan meu-projeto
python3 main.py run apply meu-projeto
```

## Teste Seguro (Recomendado)

Antes de instalar no seu sistema, teste em um container Docker:

```bash
# 1. Construir container de teste
docker build -f Dockerfile.test -t leme-test .

# 2. Testar a CLI
docker run --rm leme-test python3 /app/main.py environment-status

# 3. Testar instalação
docker run --rm leme-test python3 /app/main.py setup-environment --tools git,terraform --force
```

## Solução de Problemas

### Python não encontrado
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# macOS
brew install python3

# Windows
# Baixar de python.org
```

### Docker não funciona após instalação
```bash
# Linux: Reiniciar terminal ou executar
sudo systemctl start docker
sudo usermod -aG docker $USER
# Depois fazer logout/login

# macOS: Abrir Docker Desktop
open /Applications/Docker.app
```

### Permissões negadas
```bash
# Linux: Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Testar
docker run hello-world
```

### Terraform não encontrado
```bash
# Verificar instalação
terraform --version

# Se não estiver instalado, executar novamente
python3 main.py setup-environment --tools terraform --force
```

## Sistemas Suportados

| Sistema | Status | Método |
|---------|--------|--------|
| Ubuntu 20.04+ | Testado | apt + repositórios oficiais |
| Debian 11+ | Testado | apt + repositórios oficiais |
| macOS 12+ | Funcional | Homebrew |
| WSL Ubuntu | Testado | apt + repositórios oficiais |
| CentOS/RHEL | Funcional | yum/dnf + repositórios oficiais |
| Fedora | Funcional | dnf + repositórios oficiais |

## Estrutura dos Projetos Criados

### Projeto Azure
```
meu-projeto/
├── main.tf          # Configuração principal
├── variables.tf     # Variáveis do projeto
├── outputs.tf       # Saídas do projeto
├── providers.tf     # Configuração do Azure
├── backend.tf       # Backend remoto
└── .gitignore       # Arquivos ignorados
```

### Projeto AWS
```
meu-projeto/
├── main.tf          # Configuração principal
├── variables.tf     # Variáveis do projeto
├── outputs.tf       # Saídas do projeto
├── providers.tf     # Configuração da AWS
├── backend.tf       # Backend S3
└── .gitignore       # Arquivos ignorados
```

## Workflow Recomendado

### 1. Configuração inicial (primeira vez)
```bash
git clone https://github.com/iesodias/leme_cli.git
cd leme_cli
pip install rich typer jinja2
python3 main.py setup-environment
python3 main.py environment-status
```

### 2. Criar seu primeiro projeto
```bash
# Azure
python3 main.py new project --name meu-primeiro-projeto --provider azure

# AWS
python3 main.py new project --name meu-primeiro-projeto --provider aws
```

### 3. Trabalhar com Terraform
```bash
cd meu-primeiro-projeto
python3 ../main.py run init .
python3 ../main.py run validate .
python3 ../main.py run plan .
```

### 4. Aplicar mudanças (quando estiver pronto)
```bash
python3 ../main.py run apply .
```

## Comandos de Ajuda

```bash
# Ajuda geral
python3 main.py --help

# Ajuda para comandos específicos
python3 main.py setup-environment --help
python3 main.py new --help
python3 main.py run --help
```

## Resumo dos Comandos Essenciais

```bash
# Setup inicial
git clone https://github.com/iesodias/leme_cli.git
cd leme_cli
pip install rich typer jinja2

# Configurar ambiente
python3 main.py setup-environment

# Verificar instalação
python3 main.py environment-status

# Criar projeto
python3 main.py new project --name workshop --provider azure

# Trabalhar com Terraform
cd workshop
python3 ../main.py run init .
python3 ../main.py run plan .
```

## Suporte

Se encontrar problemas:

1. **Verifique o status**: `python3 main.py environment-status`
2. **Veja informações do sistema**: `python3 main.py system-info`  
3. **Tente forçar reinstalação**: `python3 main.py setup-environment --force`
4. **Use o container de teste**: `docker build -f Dockerfile.test -t leme-test .`

A CLI detecta automaticamente seu sistema operacional e escolhe o melhor método de instalação para cada ferramenta.