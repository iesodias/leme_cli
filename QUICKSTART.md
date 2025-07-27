# ⚡ Guia Rápido - CLI Terraform & Docker

## 🚀 Setup em 30 segundos

```bash
# 1. Instalar dependências
pip install typer rich jinja2

# 2. Verificar CLI
python3 main.py --help

# 3. Instalar Docker automaticamente
python3 main.py install docker
```

## 📋 Comandos Essenciais

### 🔍 Verificar Sistema
```bash
python3 main.py system-info    # Info do sistema
python3 main.py status         # Status ferramentas
```

### 🏗 Criar Projetos
```bash
# Projeto Azure
python3 main.py new project --name MEU-PROJETO --provider azure

# Projeto AWS  
python3 main.py new project --name MEU-PROJETO --provider aws

# Módulo reutilizável
python3 main.py new module --name MEU-MODULO
```

### 🎯 Criar Recursos
```bash
# Storage Account Azure
python3 main.py new resource --type storage-account --provider azure --name NOME

# Virtual Machine Azure
python3 main.py new resource --type virtual_machine --provider azure --name NOME
```

### ⚡ Terraform
```bash
python3 main.py run init PASTA      # Inicializar
python3 main.py run validate PASTA  # Validar
python3 main.py run plan PASTA      # Planejar
python3 main.py run apply PASTA     # Aplicar
python3 main.py run destroy PASTA   # Destruir
```

### 🐳 Docker
```bash
python3 main.py install docker           # Instalar
python3 main.py install docker --check-only  # Só verificar
python3 main.py install docker --manual     # Instruções manuais
python3 main.py uninstall-docker           # Remover
```

### 🗑 Limpeza
```bash
python3 main.py delete PASTA        # Com confirmação
python3 main.py delete PASTA --force # Sem confirmação
```

## 🎯 Workflow Típico

```bash
# 1. Setup inicial
python3 main.py install docker
python3 main.py status

# 2. Criar projeto
python3 main.py new project --name webapp --provider azure

# 3. Trabalhar com Terraform
cd webapp
python3 ../main.py run init .
python3 ../main.py run validate .
python3 ../main.py run plan .

# 4. Criar recursos adicionais
cd ..
python3 main.py new resource --type storage-account --provider azure --name storage

# 5. Limpar
python3 main.py delete storage --force
```

## 🖥 Sistemas Suportados

| OS | Status | Comando |
|----|--------|---------|
| Ubuntu/Debian | ✅ | `apt` + Docker repo |
| WSL | ✅ | `apt` + Docker repo |
| macOS | ✅ | `brew` + Docker Desktop |
| CentOS/RHEL | ✅ | `yum` + Docker repo |
| Fedora | ✅ | `dnf` + Docker repo |

## 🚨 Solução Rápida de Problemas

```bash
# Docker não funciona?
python3 main.py status
sudo systemctl start docker     # Linux
open /Applications/Docker.app   # macOS

# Terraform não encontrado?
brew install terraform  # macOS
sudo apt install terraform  # Ubuntu

# Permissões no Linux?
sudo usermod -aG docker $USER
# Fazer logout/login

# Ver instruções manuais?
python3 main.py install docker --manual
```

## 📁 Estrutura Gerada

```
meu-projeto/
├── main.tf       # Código principal
├── variables.tf  # Variáveis
├── outputs.tf    # Outputs
├── providers.tf  # Providers
├── backend.tf    # Backend remoto
└── .gitignore    # Git ignore
```

## 🏷 Convenções

- **Projects**: `projeto-nome`
- **Resource Groups**: `rg-projeto-ambiente`
- **Storage**: `stprojeto{sufixo}`
- **Tags**: Project, Environment, ManagedBy

## 🆘 Ajuda Rápida

```bash
python3 main.py --help
python3 main.py COMANDO --help
python3 main.py new --help
python3 main.py install --help
```

---

**💡 Dica**: Use `python3 main.py status` sempre que algo não funcionar!