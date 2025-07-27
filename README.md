# CLI Leme - DevOps Environment Toolkit

Uma CLI completa para configuração de ambiente DevOps, geração de projetos Infrastructure as Code (IaC) com Terraform, e instalação automática de ferramentas essenciais como Docker, Git, Terraform, Azure CLI, AWS CLI v2, kubectl, Ansible e watch.

## Índice

- [Setup Rápido](#setup-rápido)
- [Teste em Container](#teste-em-container)
- [Instalação](#instalação)
- [Ambiente DevOps](#ambiente-devops)
- [Comandos Principais](#comandos-principais)
- [Criando Projetos](#criando-projetos)
- [Gerenciando Recursos](#gerenciando-recursos)
- [Executando Terraform](#executando-terraform)
- [Exemplos Práticos](#exemplos-práticos)
- [Sistemas Suportados](#sistemas-suportados)
- [Solução de Problemas](#solução-de-problemas)
- [Desinstalação](#desinstalação)

## Setup Rápido

### Para Estudantes/Iniciantes
```bash
# 1. Clone/baixe o projeto
git clone https://github.com/iesodias/leme_cli.git
cd leme_cli

# 2. Instale dependências
pip install rich typer jinja2

# 3. Configure ambiente DevOps completo
python3 main.py setup-environment

# 4. Verifique instalação
python3 main.py environment-status
```

### Para Professores/Cursos
```bash
# Setup completo em um comando
python3 main.py setup-environment --required-only --force

# Verificar que tudo foi instalado
python3 main.py environment-status
```

## Teste em Container

**Teste a CLI sem afetar seu sistema!**

### Método 1: Teste Rápido
```bash
# Build da imagem de teste
docker build -f Dockerfile.test -t leme-test .

# Teste básico da CLI
docker run --rm leme-test python3 /app/main.py --help

# Teste status do ambiente
docker run --rm leme-test python3 /app/main.py environment-status

# Teste instalação completa (Git + Terraform)
docker run --rm leme-test python3 /app/main.py setup-environment --tools git,terraform --force
```

### Método 2: Container Interativo
```bash
# Entre no container para testes manuais
docker run -it --rm leme-test bash

# Dentro do container:
python3 /app/main.py setup-environment --help
python3 /app/main.py environment-status
python3 /app/main.py setup-environment --check-only
```

### Dockerfile de Teste
O projeto inclui um `Dockerfile.test` que cria um ambiente Ubuntu 22.04 limpo com:
- Python 3.10
- Dependências da CLI (rich, typer, jinja2)
- Ferramentas básicas (curl, wget, unzip, sudo)

**Perfeito para:**
- Testar a CLI antes de instalar no seu sistema
- Validar instaladores em Ubuntu/Debian
- Demonstrações em aulas/workshops
- CI/CD e testes automatizados

## Instalação

### Método Recomendado (Um Comando)

A CLI Leme pode ser instalada automaticamente em qualquer sistema. O script detecta seu sistema operacional, instala Python se necessário, e configura tudo automaticamente.

#### Linux / macOS / WSL

```bash
curl -sSL https://raw.githubusercontent.com/iesodias/leme_cli/main/install.sh | bash
```

#### Windows (PowerShell)

```powershell
iwr -useb https://raw.githubusercontent.com/iesodias/leme_cli/main/install.ps1 | iex
```

#### Instalação Local (Para Desenvolvimento)

Se você baixou o projeto localmente:

```bash
# Linux/macOS/WSL
chmod +x install.sh
./install.sh

# Windows (PowerShell como Administrador)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install.ps1
```

### Verificando a Instalação

Após a instalação, reinicie seu terminal e execute:

```bash
leme --help
```

Se funcionar, você está pronto!

## Instalação Manual

Caso prefira instalar manualmente ou o script automático não funcione:

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

### Passos Manuais

```bash
# 1. Clone ou baixe o projeto
cd leme_cli

# 2. Instale as dependências necessárias
pip install typer rich jinja2

# 3. Torne o script executável (Linux/macOS)
chmod +x main.py

# 4. Execute a CLI
python3 main.py --help
```

### Criando Comando Global (Manual)

```bash
# Linux/macOS
echo 'alias leme="python3 $(pwd)/main.py"' >> ~/.bashrc
source ~/.bashrc

# Windows (adicionar ao PATH ou criar leme.bat)
# Criar leme.bat em uma pasta do PATH
echo @python "%~dp0main.py" %* > leme.bat
```

## Ambiente DevOps

### Setup Completo do Ambiente

A CLI Leme pode configurar automaticamente um ambiente DevOps completo com todas as ferramentas necessárias.

#### Ferramentas Instaladas Automaticamente:
- **Docker** - Containerização 
- **Git** - Controle de versão
- **Terraform** - Infrastructure as Code
- **Azure CLI** - Interface Azure (opcional)
- **AWS CLI v2** - Interface AWS (opcional)  
- **kubectl** - Cliente Kubernetes (opcional)
- **Ansible** - Automação de configuração (opcional)
- **watch** - Monitoramento de comandos (pré-instalado na maioria dos sistemas)

### Comandos de Ambiente

#### Status do Ambiente
```bash
# Ver status de todas as ferramentas
python3 main.py environment-status

# Informações detalhadas do sistema
python3 main.py system-info
```

#### Setup Automático
```bash
# Instalar TODAS as ferramentas
python3 main.py setup-environment

# Instalar apenas ferramentas obrigatórias (Docker, Git, Terraform)
python3 main.py setup-environment --required-only

# Instalar ferramentas específicas
python3 main.py setup-environment --tools git,terraform,docker

# Apenas verificar status (não instalar)
python3 main.py setup-environment --check-only

# Forçar reinstalação (sem perguntas)
python3 main.py setup-environment --force

# Pular Docker (útil em ambientes onde Docker já existe)
python3 main.py setup-environment --skip-docker
```

#### Exemplos de Uso

**Para Curso/Workshop:**
```bash
# Setup básico para aula
python3 main.py setup-environment --required-only --force

# Verificar que alunos têm tudo instalado
python3 main.py environment-status
```

**Para Desenvolvimento:**
```bash
# Setup completo para desenvolvedor
python3 main.py setup-environment --tools git,terraform,docker,kubectl,azure-cli

# Verificar instalação
python3 main.py environment-status
```

**Para CI/CD:**
```bash
# Apenas verificar ferramentas (em pipelines)
python3 main.py setup-environment --check-only
```

### Detecção Automática

A CLI detecta automaticamente:
- **Sistema Operacional**: Ubuntu, Debian, CentOS, RHEL, Fedora, macOS, Windows, WSL
- **Arquitetura**: x86_64, ARM64/aarch64  
- **Gerenciador de Pacotes**: apt, yum, dnf, homebrew
- **Versões Instaladas**: De todas as ferramentas DevOps

### Instalação Inteligente

Cada ferramenta tem múltiplos métodos de instalação com fallbacks:

**Git:**
- Ubuntu/Debian: `apt install git`
- macOS: Xcode Command Line Tools ou Homebrew
- CentOS/RHEL: `yum install git`

**Terraform:**
- Repositório oficial HashiCorp (preferido)
- Download direto de binário (fallback)
- Homebrew no macOS

**Docker:**
- Repositório oficial Docker (preferido)
- Gerenciadores de pacote do sistema (fallback)

### Relatório Detalhado

```bash
python3 main.py environment-status
```

Mostra:
- Ferramentas instaladas (com versões)
- Ferramentas em falta
- Resumo estatístico
- Ferramentas obrigatórias em falta
- Sugestões de próximos passos

## Comandos Principais

### Ajuda Geral
```bash
python3 main.py --help
```

### Informações do Sistema
```bash
# Ver informações detalhadas do sistema
python3 main.py system-info

# Verificar status das ferramentas instaladas
python3 main.py status
```

## Criando Projetos

### 1. Criar Novo Projeto

#### Projeto Azure
```bash
python3 main.py new project --name meu-projeto-azure --provider azure
```

Durante a criação, você será solicitado a fornecer:
- Nome do Resource Group para o backend
- Nome do Storage Account para o backend
- Nome do Container no Storage Account (padrão: tfstate)

#### Projeto AWS
```bash
python3 main.py new project --name meu-projeto-aws --provider aws
```

Durante a criação, você será solicitado a fornecer:
- Região da AWS (padrão: us-east-1)
- Nome do bucket S3 para o backend

### 2. Criar Módulo Reutilizável
```bash
python3 main.py new module --name meu-modulo
```

### 3. Criar Recurso Específico

#### Storage Account (Azure)
```bash
python3 main.py new resource --type storage-account --provider azure --name minha-storage
```

Durante a criação, você será solicitado a fornecer:
- Localização/região do Azure (padrão: East US)
- Nome curto da localização (padrão: eus)

#### Virtual Machine (Azure)
```bash
python3 main.py new resource --type virtual_machine --provider azure --name minha-vm
```

## Gerenciando Projetos

### Deletar Projeto
```bash
# Com confirmação
python3 main.py delete caminho/para/projeto

# Forçar exclusão sem confirmação
python3 main.py delete caminho/para/projeto --force
```

## Instalação de Ferramentas

### Docker

#### Instalação Automática
```bash
# Instalar Docker automaticamente
python3 main.py install docker
```

#### Opções Avançadas
```bash
# Apenas verificar se está instalado
python3 main.py install docker --check-only

# Ver instruções para instalação manual
python3 main.py install docker --manual

# Forçar reinstalação
python3 main.py install docker --force

# Instalar sem testar após instalação
python3 main.py install docker --no-test
```

#### Remoção do Docker
```bash
python3 main.py uninstall-docker
```

## Executando Terraform

### Comandos Disponíveis
```bash
# Inicializar projeto Terraform
python3 main.py run init caminho/para/projeto

# Validar configuração
python3 main.py run validate caminho/para/projeto

# Gerar plano de execução
python3 main.py run plan caminho/para/projeto

# Aplicar mudanças
python3 main.py run apply caminho/para/projeto

# Destruir recursos
python3 main.py run destroy caminho/para/projeto
```

## Exemplos Práticos

### Exemplo 1: Criando um Projeto Azure Completo

```bash
# 1. Instalar Docker (se necessário)
python3 main.py install docker

# 2. Verificar status
python3 main.py status

# 3. Criar projeto Azure
python3 main.py new project --name webapp-azure --provider azure
# Responder prompts:
# - Resource Group: rg-webapp-backend
# - Storage Account: sawebappbackend
# - Container: tfstate

# 4. Acessar o projeto
cd webapp-azure

# 5. Inicializar Terraform
python3 ../main.py run init .

# 6. Validar configuração
python3 ../main.py run validate .

# 7. Ver plano de execução
python3 ../main.py run plan .
```

### Exemplo 2: Criando Storage Account Azure

```bash
# 1. Criar módulo de storage account
python3 main.py new resource --type storage-account --provider azure --name storage-producao
# Responder prompts:
# - Localização: East US
# - Nome curto: eus

# 2. Acessar o módulo
cd storage-producao

# 3. Inicializar e validar
python3 ../main.py run init .
python3 ../main.py run validate .
```

### Exemplo 3: Workflow Completo

```bash
# 1. Ver informações do sistema
python3 main.py system-info

# 2. Instalar Docker se necessário
python3 main.py install docker --check-only

# 3. Criar projeto
python3 main.py new project --name meu-app --provider azure

# 4. Criar recursos adicionais
python3 main.py new resource --type storage-account --provider azure --name app-storage

# 5. Executar Terraform nos projetos
python3 main.py run init meu-app
python3 main.py run validate meu-app
python3 main.py run plan meu-app

# 6. Limpar recursos de teste
python3 main.py delete app-storage --force
```

## Sistemas Suportados

### Ferramentas DevOps Suportadas

| Ferramenta | Ubuntu/Debian | CentOS/RHEL | Fedora | macOS | Método de Instalação |
|------------|---------------|-------------|--------|-------|---------------------|
| **Docker** | Suportado | Suportado | Suportado | Suportado | Repositório oficial + fallbacks |
| **Git** | Suportado | Suportado | Suportado | Suportado | Gerenciador de pacotes |
| **Terraform** | Suportado | Suportado | Suportado | Suportado | Repositório HashiCorp + binário |
| **Azure CLI** | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento |
| **AWS CLI v2** | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento |
| **kubectl** | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento |
| **Ansible** | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento | Em desenvolvimento |
| **watch** | Suportado | Suportado | Suportado | Suportado | Pré-instalado |

### Sistemas Testados

| Sistema | Versão | Arquitetura | Status | Notas |
|---------|--------|-------------|--------|-------|
| Ubuntu | 22.04 LTS | x86_64, ARM64 | Testado | Ambiente principal de desenvolvimento |
| Ubuntu | 20.04 LTS | x86_64, ARM64 | Testado | Compatibilidade verificada |
| Debian | 11+ | x86_64, ARM64 | Testado | Instalação via APT |
| WSL Ubuntu | 22.04 | x86_64 | Testado | Windows Subsystem for Linux |
| macOS | 12+ | Intel, Apple Silicon | Beta | Homebrew como método principal |
| CentOS | 7, 8 | x86_64 | Beta | YUM + repositórios oficiais |
| RHEL | 8+ | x86_64 | Beta | YUM + repositórios oficiais |
| Fedora | 35+ | x86_64 | Beta | DNF + repositórios oficiais |

### Detecção Automática

A CLI detecta automaticamente:
- **Sistema Operacional**: Ubuntu, Debian, macOS, CentOS, RHEL, Fedora, Windows, WSL
- **Arquitetura**: x86_64, ARM64/aarch64, amd64
- **Ambiente**: WSL (Windows Subsystem for Linux)
- **Gerenciador de Pacotes**: apt, yum, dnf, homebrew
- **Versões**: Sistema operacional e ferramentas instaladas

### Container Docker (Teste)

**Ambiente de teste validado:**
- **Base**: Ubuntu 22.04 LTS
- **Arquitetura**: ARM64 (Apple Silicon) e x86_64
- **Python**: 3.10
- **Dependências**: rich, typer, jinja2 pré-instaladas
- **Ferramentas**: curl, wget, unzip, sudo pré-instaladas

**Uso do container de teste:**
```bash
# Build e teste básico
docker build -f Dockerfile.test -t leme-test .
docker run --rm leme-test python3 /app/main.py environment-status

# Teste instalação completa
docker run --rm leme-test python3 /app/main.py setup-environment --tools git,terraform --force
```

## Solução de Problemas

### Docker não está funcionando após instalação

```bash
# Verificar status
python3 main.py status

# No Linux: Fazer logout/login para aplicar permissões
# ou executar:
sudo systemctl start docker
sudo usermod -aG docker $USER

# No macOS: Abrir Docker Desktop manualmente
open /Applications/Docker.app
```

### Terraform não encontrado

```bash
# Verificar se Terraform está instalado
terraform --version

# Se não estiver, instalar manualmente:
# Ubuntu/Debian:
sudo apt update && sudo apt install terraform

# macOS:
brew install terraform
```

### Problemas com WSL

```bash
# Verificar se está no WSL
python3 main.py system-info

# No WSL, garantir que Docker Desktop está rodando no Windows
# ou instalar Docker Engine diretamente no WSL
```

### Erro de permissões no Linux

```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Fazer logout/login ou executar:
newgrp docker

# Testar Docker
docker run hello-world
```

## Estrutura de Arquivos Gerados

### Projeto Azure
```
meu-projeto/
├── main.tf          # Resource Group principal
├── variables.tf     # Variáveis do projeto
├── outputs.tf       # Outputs do projeto
├── providers.tf     # Configuração do provider Azure
├── backend.tf       # Configuração do backend remoto
└── .gitignore       # Arquivos ignorados pelo Git
```

### Módulo/Recurso
```
meu-recurso/
├── main.tf          # Definição do recurso
├── variables.tf     # Variáveis do módulo
├── outputs.tf       # Outputs do módulo
└── providers.tf     # Provider necessário
```

## Tags e Convenções

### Nomenclatura Padrão

- **Resource Groups**: `rg-{nome-projeto}-{ambiente}`
- **Storage Accounts**: `st{nomeprojeto}{sufixo}`
- **Tags padrão**:
  - `Project`: Nome do projeto
  - `Environment`: dev/staging/prod
  - `ManagedBy`: Terraform

### Variáveis Comuns

- `location`: Região do Azure
- `location_short`: Sigla da região (ex: eus, wus)
- `environment`: Ambiente de deployment
- `common_tags`: Tags aplicadas a todos recursos

## Personalização

### Adicionando Novos Providers

1. Criar templates em `templates/providers/{novo-provider}/`
2. Atualizar `src/config/constants.py`
3. Implementar lógica específica em comandos

### Adicionando Novos Recursos

1. Criar templates em `templates/providers/{provider}/resource/{novo-recurso}/`
2. Atualizar enum `ResourceType`
3. Testar criação com CLI

## Suporte

### Comandos de Diagnóstico

```bash
# Informações completas do sistema
python3 main.py system-info

# Status de todas ferramentas
python3 main.py status

# Instruções manuais do Docker
python3 main.py install docker --manual

# Ajuda de comandos específicos
python3 main.py new --help
python3 main.py install --help
python3 main.py run --help
```

### Logs e Debug

- A CLI mostra output em tempo real dos comandos
- Erros são exibidos com cores para fácil identificação
- Use `--help` em qualquer comando para ver opções disponíveis

---

## Resumo Rápido

### Para Estudantes
```bash
# 1. Setup inicial
git clone https://github.com/iesodias/leme_cli.git
cd leme_cli
pip install rich typer jinja2

# 2. Configurar ambiente DevOps
python3 main.py setup-environment

# 3. Verificar instalação
python3 main.py environment-status

# 4. Criar projeto Terraform
python3 main.py new project --name meu-app --provider azure

# 5. Executar Terraform
python3 main.py run init meu-app
python3 main.py run plan meu-app
```

### Para Professores/Cursos
```bash
# Setup rápido para workshop
python3 main.py setup-environment --required-only --force
python3 main.py environment-status

# Validar instalação de alunos
python3 main.py setup-environment --check-only
```

### Para Teste (Docker)
```bash
# Testar sem afetar o sistema
docker build -f Dockerfile.test -t leme-test .
docker run --rm leme-test python3 /app/main.py setup-environment --tools git,terraform --force
```

## Desinstalação

### Remoção Automática

#### Linux/macOS/WSL
```bash
curl -sSL https://raw.githubusercontent.com/iesodias/leme_cli/main/uninstall.sh | bash
```

#### Remoção Manual

```bash
# Remover arquivos
rm -rf ~/.leme
rm -f ~/.local/bin/leme

# Limpar PATH (editar manualmente)
nano ~/.bashrc  # ou ~/.zshrc
# Remover linhas relacionadas ao Leme

# Reiniciar terminal
```

#### Windows
```powershell
# Remover diretórios
Remove-Item -Recurse -Force "$env:USERPROFILE\.leme"
Remove-Item -Force "$env:USERPROFILE\.local\bin\leme.bat"
Remove-Item -Force "$env:USERPROFILE\.local\bin\leme.ps1"

# Remover do PATH manualmente via:
# Configurações > Sistema > Sobre > Configurações avançadas do sistema > Variáveis de ambiente
```

---

## Para Professores

### Distribuindo para Alunos

1. **Compartilhe apenas uma linha:**
   ```bash
   curl -sSL https://install.leme.dev | bash
   ```

2. **Alunos executam e pronto!** 
   - Instala Python automaticamente
   - Configura todas as dependências
   - Disponibiliza comando `leme`

3. **Primeiro comando:**
   ```bash
   leme install docker
   leme new project --name meu-primeiro-projeto --provider azure
   ```

### Verificação em Massa
```bash
# Script para verificar instalação dos alunos
leme system-info
leme status
```

---

**Sua CLI Leme está pronta para usar! Divirta-se criando projetos de infraestrutura!**