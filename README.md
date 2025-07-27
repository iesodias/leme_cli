# CLI Leme DevOps - Configuração Automática de Ambiente

🚀 **Configuração automática do seu ambiente DevOps em 3 comandos**

Esta CLI instala e configura automaticamente todas as ferramentas necessárias para o curso:

## ✅ Ferramentas Instaladas

### 🔧 **Obrigatórias** (instaladas automaticamente)
- **Docker** - Para containerização e ambientes isolados
- **Git** - Para controle de versão de código

### ☁️ **Opcionais** (você escolhe)
- **AWS CLI v2** - Interface de linha de comando da Amazon Web Services
- **Azure CLI** - Interface de linha de comando do Microsoft Azure
- **kubectl** - Gerenciamento de clusters Kubernetes
- **Ansible** - Automação de configuração e deploy
- **watch** - Monitoramento de comandos em tempo real

## 🚀 Instalação Rápida (3 Comandos)

### Para Alunos - Configuração Completa

```bash
# 1. Baixar a CLI
git clone https://github.com/iesodias/leme_cli.git
cd leme_cli

# 2. Instalar dependências automaticamente  
./quick-install.sh

# 3. Configurar ambiente DevOps completo
python3 main.py setup-environment
```

**Pronto!** 🎉 Agora você tem Docker, Git e todas as ferramentas configuradas.

### ✅ Verificar se funcionou

```bash
# Ver o status de todas as ferramentas
python3 main.py environment-status

# Testar o Docker
docker run hello-world

# Ver versões instaladas
docker --version
git --version
```

### Se o script automático não funcionar

#### No Windows:
1. Baixar e instalar Python de https://python.org
2. Instalar Git de https://git-scm.com
3. Abrir terminal e executar:
```bash
git clone https://github.com/iesodias/leme_cli.git
cd leme_cli
pip install rich typer jinja2
python main.py setup-environment
```

#### Instalação manual (qualquer sistema):
```bash
git clone https://github.com/iesodias/leme_cli.git
cd leme_cli
pip install rich typer jinja2
python3 main.py setup-environment
```

## 🛠️ Comandos Úteis para Alunos

### 📦 Instalar Ferramentas Individuais

```bash
# Instalar Docker isoladamente
python3 main.py install docker

# Instalar AWS CLI v2
python3 main.py install aws-cli

# Instalar Azure CLI  
python3 main.py install azure-cli
```

### ⚙️ Configurações Avançadas

```bash
# Instalar apenas ferramentas obrigatórias (Docker + Git)
python3 main.py setup-environment --required-only

# Instalar ferramentas específicas
python3 main.py setup-environment --tools docker,git,aws-cli

# Forçar reinstalação (se algo deu errado)
python3 main.py setup-environment --force

# Pular Docker (se já tiver instalado)
python3 main.py setup-environment --skip-docker
```

### 🔍 Verificar Status

```bash
# Ver todas as ferramentas instaladas
python3 main.py environment-status

# Ver informações do seu sistema operacional
python3 main.py system-info

# Verificar apenas Docker
python3 main.py install docker --check-only
```


## Teste Seguro (Recomendado)

Antes de instalar no seu sistema, teste em um container Docker:

```bash
# 1. Construir container de teste
docker build -f Dockerfile.test -t leme-test .

# 2. Testar a CLI
docker run --rm leme-test python3 /app/main.py environment-status

# 3. Testar instalação
docker run --rm leme-test python3 /app/main.py setup-environment --tools git,docker --force
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

#### Linux - Problema de permissões (mais comum):
```bash
# 1. Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# 2. Aplicar as mudanças (escolha uma opção):
newgrp docker        # Opção A: Nova sessão de grupo
# OU
logout/login         # Opção B: Logout e login novamente  
# OU
sudo reboot          # Opção C: Reiniciar sistema

# 3. Testar se funcionou
docker run hello-world
```

#### Linux - Docker daemon não está rodando:
```bash
# Iniciar Docker daemon
sudo systemctl start docker
sudo systemctl enable docker

# Verificar status
sudo systemctl status docker
```

#### macOS - Docker Desktop não está rodando:
```bash
# Abrir Docker Desktop
open /Applications/Docker.app

# Ou verificar se está instalado
ls /Applications/Docker.app
```

### Erro "permission denied" no Docker
```bash
# Verificar se usuário está no grupo docker
groups | grep docker

# Se não estiver, adicionar:
sudo usermod -aG docker $USER
newgrp docker

# Verificar novamente
groups | grep docker

# Testar Docker
docker run hello-world
```


## 💻 Sistemas Suportados

| Sistema Operacional | Status | Ferramentas Suportadas |
|---------------------|--------|------------------------|
| **Ubuntu 20.04+** | ✅ Totalmente Testado | Docker, Git, AWS CLI, Azure CLI |
| **Debian 11+** | ✅ Totalmente Testado | Docker, Git, AWS CLI, Azure CLI |
| **macOS 12+** | ✅ Funcional | Docker, Git, AWS CLI, Azure CLI |
| **WSL Ubuntu** | ✅ Testado | Docker, Git, AWS CLI, Azure CLI |
| **CentOS/RHEL 7+** | ⚠️ Funcional | Docker, Git, AWS CLI, Azure CLI |
| **Fedora 35+** | ⚠️ Funcional | Docker, Git, AWS CLI, Azure CLI |

### 🔧 Métodos de Instalação Automática

- **Ubuntu/Debian**: Repositórios oficiais via `apt`
- **macOS**: Homebrew + instaladores oficiais
- **CentOS/RHEL/Fedora**: Repositórios oficiais via `yum`/`dnf`
- **Arquiteturas**: x86_64 (Intel/AMD) e ARM64 (Apple Silicon/ARM)


## 📚 Guia Passo a Passo para Alunos

### 🥇 **PRIMEIRA VEZ** - Configuração Inicial

```bash
# 1. Clonar o repositório
git clone https://github.com/iesodias/leme_cli.git
cd leme_cli

# 2. Instalar dependências
./quick-install.sh

# 3. Configurar ambiente completo
python3 main.py setup-environment

# 4. Verificar se funcionou
python3 main.py environment-status
```

### 🔄 **USO DIÁRIO** - Comandos Úteis

```bash
# Verificar status das ferramentas
python3 main.py environment-status

# Instalar ferramenta específica se precisar
python3 main.py install azure-cli
python3 main.py install aws-cli

# Verificar versões instaladas
docker --version
git --version
aws --version    # Se instalou AWS CLI
az --version     # Se instalou Azure CLI
```

### 🧪 **TESTAR INSTALAÇÃO**

```bash
# Testar Docker
docker run hello-world

# Testar Git (configurar se for primeira vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
git --version

# Testar AWS CLI (se instalou)
aws --version

# Testar Azure CLI (se instalou)  
az --version
```

## 🆘 Solução de Problemas Rápida

### ❌ **Erro: "Python não encontrado"**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# macOS
brew install python3

# Windows - Baixar de python.org
```

### ❌ **Erro: "Docker não funciona"**
```bash
# 1. Verificar se Docker está rodando
docker --version

# 2. Adicionar usuário ao grupo docker (Linux)
sudo usermod -aG docker $USER
newgrp docker

# 3. Testar novamente
docker run hello-world
```

### ❌ **Erro: "Permission denied"**
```bash
# Verificar permissões e tentar novamente
python3 main.py setup-environment --force
```

### 💡 **Comandos de Diagnóstico**

```bash
# Ver informações do sistema
python3 main.py system-info

# Ver status detalhado de todas as ferramentas
python3 main.py environment-status

# Ajuda geral
python3 main.py --help

# Ajuda para comandos específicos
python3 main.py setup-environment --help
python3 main.py install --help
```

## 📞 Suporte

**Se nada funcionar:**

1. **Primeiro**: `python3 main.py environment-status`
2. **Depois**: `python3 main.py setup-environment --force`
3. **Por último**: Abrir issue no GitHub com a saída do comando `python3 main.py system-info`

---

## 📋 Resumo - Cola para Alunos

```bash
# ⬇️ BAIXAR E INSTALAR (primeira vez)
git clone https://github.com/iesodias/leme_cli.git
cd leme_cli
./quick-install.sh
python3 main.py setup-environment

# ✅ VERIFICAR SE FUNCIONOU
python3 main.py environment-status
docker run hello-world

# 🔧 COMANDOS ÚTEIS
python3 main.py install docker        # Docker isolado
python3 main.py install aws-cli       # AWS CLI
python3 main.py install azure-cli     # Azure CLI
python3 main.py setup-environment --force    # Forçar reinstalação
```

**🎯 A CLI detecta seu sistema automaticamente e instala tudo corretamente!**