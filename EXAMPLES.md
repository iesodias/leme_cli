# 📚 Exemplos Práticos - CLI Terraform & Docker

## 🎯 Cenários Reais de Uso

### 1. 🏫 Professor Distribuindo para Alunos

```bash
# O que você (professor) faz:
# 1. Preparar o ambiente
pip install typer rich jinja2

# 2. Testar a CLI
python3 main.py system-info
python3 main.py install docker

# 3. Criar material de exemplo
python3 main.py new project --name aula-terraform --provider azure
python3 main.py new resource --type storage-account --provider azure --name exemplo-storage

# 4. Compartilhar com alunos
# - Enviar pasta completa do projeto
# - Instruir: "Execute 'python3 main.py install docker'"
```

### 2. 🎓 Aluno Recebendo o Projeto

```bash
# O que o aluno faz:
# 1. Instalar dependências (uma vez só)
pip install typer rich jinja2

# 2. Verificar sistema
python3 main.py system-info

# 3. Instalar Docker automaticamente
python3 main.py install docker

# 4. Verificar se está tudo funcionando
python3 main.py status

# 5. Começar a trabalhar!
python3 main.py new project --name meu-primeiro-projeto --provider azure
```

### 3. 🏢 Ambiente Corporativo

```bash
# Setup inicial para equipe
python3 main.py install docker
python3 main.py status

# Criar estrutura de projeto padrão
python3 main.py new project --name webapp-prod --provider azure
python3 main.py new resource --type storage-account --provider azure --name storage-prod
python3 main.py new resource --type virtual_machine --provider azure --name vm-app

# Inicializar todos os projetos
for dir in webapp-prod storage-prod vm-app; do
    python3 main.py run init $dir
    python3 main.py run validate $dir
done
```

## 🛠 Cenários por Sistema Operacional

### Ubuntu/Debian (incluindo WSL)

```bash
# Aluno no Ubuntu
# 1. Verificar sistema
python3 main.py system-info
# Output: Sistema Operacional: ubuntu, WSL: Não/Sim

# 2. Instalar Docker
python3 main.py install docker
# Instala via APT + repositório oficial Docker

# 3. Verificar instalação
python3 main.py status
# Mostra se Docker está funcionando

# 4. Criar projeto
python3 main.py new project --name lab1 --provider azure
cd lab1
python3 ../main.py run init .
```

### macOS (Intel/Apple Silicon)

```bash
# Aluno no Mac
# 1. Verificar sistema
python3 main.py system-info
# Output: Sistema Operacional: macos, Arquitetura: arm64/x86_64

# 2. Instalar Docker (instala Homebrew se necessário)
python3 main.py install docker
# Instala via Homebrew + Docker Desktop

# 3. Instruções pós-instalação
# CLI instrui: "Abra Docker Desktop manualmente"
open /Applications/Docker.app

# 4. Verificar
python3 main.py status
```

### CentOS/RHEL/Fedora

```bash
# Servidor corporativo
# 1. Como root ou sudo
python3 main.py install docker
# Fedora: usa DNF
# CentOS/RHEL: usa YUM

# 2. Configurar usuário
sudo usermod -aG docker $USER
newgrp docker

# 3. Testar
python3 main.py status
docker run hello-world
```

## 🎨 Cenários de Templates

### Projeto Web Application

```bash
# 1. Criar estrutura base
python3 main.py new project --name webapp-azure --provider azure
# Prompts:
# - Resource Group: rg-webapp-backend
# - Storage Account: sawebappbackend  
# - Container: tfstate

cd webapp-azure

# 2. Adicionar storage para app
python3 ../main.py new resource --type storage-account --provider azure --name webapp-storage
# Prompts:
# - Localização: East US
# - Nome curto: eus

# 3. Adicionar VM para aplicação
python3 ../main.py new resource --type virtual_machine --provider azure --name webapp-vm

# 4. Estrutura final:
# webapp-azure/        (projeto principal)
# webapp-storage/      (storage da aplicação)
# webapp-vm/          (VM da aplicação)
```

### Ambiente Multi-Tenant

```bash
# Cliente A
python3 main.py new project --name cliente-a --provider azure
python3 main.py new resource --type storage-account --provider azure --name storage-cliente-a

# Cliente B  
python3 main.py new project --name cliente-b --provider azure
python3 main.py new resource --type storage-account --provider azure --name storage-cliente-b

# Inicializar todos
for client in cliente-a cliente-b storage-cliente-a storage-cliente-b; do
    python3 main.py run init $client
done
```

## 🔄 Workflows Completos

### Workflow: Desenvolvimento → Staging → Produção

```bash
# 1. Ambiente de Desenvolvimento
python3 main.py new project --name app-dev --provider azure
cd app-dev
# Editar variables.tf: environment = "dev"
python3 ../main.py run init .
python3 ../main.py run plan .
python3 ../main.py run apply .

# 2. Ambiente de Staging
python3 main.py new project --name app-staging --provider azure
cd app-staging
# Editar variables.tf: environment = "staging"
python3 ../main.py run init .
python3 ../main.py run plan .

# 3. Ambiente de Produção
python3 main.py new project --name app-prod --provider azure
cd app-prod
# Editar variables.tf: environment = "prod"
python3 ../main.py run init .
python3 ../main.py run plan .
```

### Workflow: Teste e Limpeza

```bash
# 1. Criar ambiente de teste
python3 main.py new project --name teste-temporario --provider azure
python3 main.py run init teste-temporario
python3 main.py run apply teste-temporario

# 2. Executar testes (seus scripts)
# ... executar testes ...

# 3. Limpar recursos
python3 main.py run destroy teste-temporario
python3 main.py delete teste-temporario --force
```

## 🚨 Cenários de Solução de Problemas

### Problema: Docker não funciona no WSL

```bash
# 1. Verificar sistema
python3 main.py system-info
# Confirma: WSL: Sim

# 2. Verificar status
python3 main.py status
# Mostra erro de Docker

# 3. Soluções:
# Opção A: Docker Desktop no Windows
# Instalar Docker Desktop no Windows e habilitar WSL integration

# Opção B: Docker Engine no WSL
python3 main.py install docker --manual
# Seguir instruções manuais
```

### Problema: Terraform não encontrado

```bash
# 1. Tentar executar Terraform
python3 main.py run init meu-projeto
# Erro: terraform não encontrado

# 2. Instalar Terraform manualmente
# Ubuntu/Debian:
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# macOS:
brew install terraform

# 3. Verificar
terraform --version
```

### Problema: Permissões Docker no Linux

```bash
# 1. Sintoma
python3 main.py status
# Mostra: "Docker instalado mas não funciona"

# 2. Solução
sudo usermod -aG docker $USER
newgrp docker
# ou fazer logout/login

# 3. Testar
docker run hello-world
python3 main.py status
```

## 📊 Cenários de Monitoramento

### Verificação Diária

```bash
#!/bin/bash
# Script para verificação diária

echo "=== Status da CLI ==="
python3 main.py system-info
echo ""

echo "=== Status Docker ==="
python3 main.py status
echo ""

echo "=== Projetos Terraform ==="
for dir in */; do
    if [[ -f "$dir/main.tf" ]]; then
        echo "Validando $dir..."
        python3 main.py run validate "$dir"
    fi
done
```

### Relatório de Recursos

```bash
#!/bin/bash
# Gerar relatório de todos os projetos

echo "=== Relatório de Projetos ===" > relatorio.txt
date >> relatorio.txt
echo "" >> relatorio.txt

for dir in */; do
    if [[ -f "$dir/main.tf" ]]; then
        echo "=== $dir ===" >> relatorio.txt
        python3 main.py run plan "$dir" >> relatorio.txt 2>&1
        echo "" >> relatorio.txt
    fi
done
```

## 🎓 Cenários Educacionais

### Aula 1: Introdução

```bash
# Professor demonstra:
python3 main.py system-info
python3 main.py install docker
python3 main.py new module --name exemplo-simples

# Alunos praticam:
python3 main.py install docker
python3 main.py status
python3 main.py new module --name meu-primeiro-modulo
```

### Aula 2: Projeto Azure

```bash
# Professor cria template:
python3 main.py new project --name template-aula --provider azure

# Alunos criam projetos individuais:
python3 main.py new project --name projeto-aluno1 --provider azure
python3 main.py new project --name projeto-aluno2 --provider azure
```

### Aula 3: Storage Accounts

```bash
# Cada aluno cria seu storage:
python3 main.py new resource --type storage-account --provider azure --name storage-aluno1

# Inicializar e validar:
python3 main.py run init storage-aluno1
python3 main.py run validate storage-aluno1
python3 main.py run plan storage-aluno1
```

---

## 💡 Dicas Importantes

1. **Sempre verificar sistema primeiro**: `python3 main.py system-info`
2. **Status é seu amigo**: `python3 main.py status` resolve 80% dos problemas
3. **Instruções manuais como backup**: `python3 main.py install docker --manual`
4. **Teste sempre**: `python3 main.py run validate .` antes de apply
5. **Limpeza regular**: Use `--force` apenas quando necessário

**🎯 Estes exemplos cobrem os cenários mais comuns que você e seus alunos encontrarão!**