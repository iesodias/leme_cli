#!/bin/bash

# Script de Instalação da CLI Leme
# Instala Python, dependências e configura a CLI automaticamente
# Suporte: Ubuntu, Debian, macOS, CentOS, Fedora, WSL

set -e  # Parar em qualquer erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Informações da CLI
CLI_NAME="leme"
CLI_VERSION="1.0.0"
INSTALL_DIR="$HOME/.leme"
BIN_DIR="$HOME/.local/bin"
REPO_URL="https://github.com/SEU_USUARIO/leme"  # Substituir pelo seu repositório

# Funções de output
print_header() {
    echo -e "${BLUE}"
    echo "┌─────────────────────────────────────────────────────────────┐"
    echo "│                    🚀 Instalador CLI Leme                  │"
    echo "│          Terraform & Docker - Versão $CLI_VERSION          │"
    echo "└─────────────────────────────────────────────────────────────┘"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Detectar sistema operacional
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$ID
            OS_VERSION=$VERSION_ID
        else
            OS="unknown"
        fi
        
        # Verificar WSL
        if grep -q Microsoft /proc/version 2>/dev/null; then
            WSL=true
        else
            WSL=false
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        OS="macos"
        OS_VERSION=$(sw_vers -productVersion)
        WSL=false
    else
        OS="unknown"
        WSL=false
    fi
    
    ARCH=$(uname -m)
}

# Verificar se Python está instalado
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 7 ]; then
            PYTHON_OK=true
            print_success "Python $PYTHON_VERSION encontrado"
        else
            PYTHON_OK=false
            print_warning "Python $PYTHON_VERSION encontrado, mas versão 3.7+ é necessária"
        fi
    else
        PYTHON_OK=false
        print_warning "Python 3 não encontrado"
    fi
}

# Instalar Python baseado no sistema
install_python() {
    if [ "$PYTHON_OK" = true ]; then
        return 0
    fi
    
    print_step "Instalando Python 3..."
    
    case $OS in
        ubuntu|debian)
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv
            ;;
        centos|rhel)
            sudo yum install -y python3 python3-pip
            ;;
        fedora)
            sudo dnf install -y python3 python3-pip
            ;;
        macos)
            if command -v brew &> /dev/null; then
                brew install python3
            else
                print_error "Homebrew não encontrado. Instale manualmente: https://brew.sh"
                exit 1
            fi
            ;;
        *)
            print_error "Sistema operacional não suportado: $OS"
            print_warning "Por favor, instale Python 3.7+ manualmente"
            exit 1
            ;;
    esac
    
    # Verificar instalação
    if command -v python3 &> /dev/null; then
        print_success "Python 3 instalado com sucesso"
    else
        print_error "Falha ao instalar Python 3"
        exit 1
    fi
}

# Verificar e instalar pip
check_install_pip() {
    if command -v pip3 &> /dev/null; then
        print_success "pip3 encontrado"
    else
        print_step "Instalando pip..."
        case $OS in
            ubuntu|debian)
                sudo apt install -y python3-pip
                ;;
            centos|rhel|fedora)
                # pip já deve estar instalado com python3
                python3 -m ensurepip --default-pip
                ;;
            macos)
                # pip já vem com Python do Homebrew
                python3 -m ensurepip --default-pip
                ;;
        esac
    fi
}

# Criar diretórios necessários
create_directories() {
    print_step "Criando diretórios..."
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"
    print_success "Diretórios criados"
}

# Baixar e instalar CLI
install_cli() {
    print_step "Baixando CLI Leme..."
    
    # Para desenvolvimento local, copiar arquivos
    if [ -d "$(dirname "$0")" ]; then
        cp -r "$(dirname "$0")"/* "$INSTALL_DIR/"
        print_success "Arquivos copiados para $INSTALL_DIR"
    else
        # Para instalação remota (futuro)
        print_error "Modo remoto não implementado ainda"
        exit 1
    fi
}

# Instalar dependências Python
install_dependencies() {
    print_step "Instalando dependências Python..."
    
    cd "$INSTALL_DIR"
    python3 -m pip install --user typer rich jinja2
    
    print_success "Dependências instaladas"
}

# Criar script executável
create_executable() {
    print_step "Criando comando executável 'leme'..."
    
    cat > "$BIN_DIR/leme" << EOF
#!/bin/bash
# CLI Leme - Terraform & Docker Tool
cd "$INSTALL_DIR"
python3 main.py "\$@"
EOF
    
    chmod +x "$BIN_DIR/leme"
    print_success "Comando 'leme' criado"
}

# Configurar PATH
setup_path() {
    print_step "Configurando PATH..."
    
    # Detectar shell
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    
    # Adicionar ao PATH se não estiver
    if ! echo "$PATH" | grep -q "$BIN_DIR"; then
        echo "" >> "$SHELL_RC"
        echo "# CLI Leme" >> "$SHELL_RC"
        echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$SHELL_RC"
        print_success "PATH configurado em $SHELL_RC"
    else
        print_success "PATH já configurado"
    fi
}

# Testar instalação
test_installation() {
    print_step "Testando instalação..."
    
    # Adicionar temporariamente ao PATH para teste
    export PATH="$PATH:$BIN_DIR"
    
    if command -v leme &> /dev/null; then
        # Testar comando básico
        if leme --help &> /dev/null; then
            print_success "CLI Leme instalada e funcionando!"
        else
            print_error "CLI instalada mas com problemas"
            exit 1
        fi
    else
        print_error "Comando 'leme' não encontrado"
        exit 1
    fi
}

# Mostrar informações finais
show_final_info() {
    echo ""
    echo -e "${GREEN}🎉 Instalação concluída com sucesso!${NC}"
    echo ""
    echo -e "${BLUE}Como usar:${NC}"
    echo "  1. Reinicie seu terminal ou execute: source ~/.bashrc"
    echo "  2. Execute: leme --help"
    echo "  3. Para instalar Docker: leme install docker"
    echo "  4. Para criar projeto: leme new project --name meu-projeto --provider azure"
    echo ""
    echo -e "${BLUE}Documentação:${NC}"
    echo "  README: $INSTALL_DIR/README.md"
    echo "  Guia rápido: $INSTALL_DIR/QUICKSTART.md"
    echo "  Exemplos: $INSTALL_DIR/EXAMPLES.md"
    echo ""
    echo -e "${YELLOW}Importante:${NC} Reinicie o terminal para usar o comando 'leme'"
}

# Função principal
main() {
    print_header
    
    print_step "Detectando sistema..."
    detect_os
    print_success "Sistema: $OS $OS_VERSION ($ARCH)"
    if [ "$WSL" = true ]; then
        print_success "WSL detectado"
    fi
    
    check_python
    install_python
    check_install_pip
    create_directories
    install_cli
    install_dependencies
    create_executable
    setup_path
    test_installation
    show_final_info
}

# Executar instalação
main "$@"