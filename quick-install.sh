#!/bin/bash
# CLI Leme DevOps - Instalação Rápida
# Autor: Seu Nome
# Versão: 1.0.0-beta

set -e

echo "CLI Leme DevOps - Setup Rápido"
echo "================================"

# Função para detectar sistema operacional
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt &> /dev/null; then
            echo "ubuntu"
        elif command -v yum &> /dev/null; then
            echo "centos"
        elif command -v dnf &> /dev/null; then
            echo "fedora"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python 3 não encontrado."
    echo ""
    echo "Instalando Python automaticamente..."
    
    case $OS in
        "ubuntu")
            sudo apt update && sudo apt install -y python3 python3-pip
            ;;
        "centos")
            sudo yum install -y python3 python3-pip
            ;;
        "fedora")
            sudo dnf install -y python3 python3-pip
            ;;
        "macos")
            if command -v brew &> /dev/null; then
                brew install python3
            else
                echo "Por favor instale Homebrew primeiro:"
                echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
                exit 1
            fi
            ;;
        *)
            echo "Sistema não suportado. Instale Python 3.7+ manualmente."
            exit 1
            ;;
    esac
fi

# Verificar se pip está disponível e instalar se necessário
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "pip não encontrado. Instalando..."
    
    case $OS in
        "ubuntu")
            sudo apt update && sudo apt install -y python3-pip
            ;;
        "centos")
            sudo yum install -y python3-pip
            ;;
        "fedora")
            sudo dnf install -y python3-pip
            ;;
        "macos")
            if command -v brew &> /dev/null; then
                brew install python3
            else
                echo "ERRO: Não foi possível instalar pip no macOS"
                exit 1
            fi
            ;;
        *)
            echo "ERRO: Não foi possível instalar pip automaticamente"
            echo "Por favor instale manualmente: sudo apt install python3-pip"
            exit 1
            ;;
    esac
fi

# Usar pip3 se disponível, senão pip
PIP_CMD="pip3"
if ! command -v pip3 &> /dev/null; then
    PIP_CMD="pip"
fi

echo "Verificando Python..."
python3 --version || (echo "ERRO: Erro ao verificar Python" && exit 1)

echo "Instalando dependências Python..."
$PIP_CMD install rich typer jinja2 || (echo "ERRO: Erro ao instalar dependências" && exit 1)

echo "SUCESSO: Dependências instaladas com sucesso!"
echo ""
echo "Próximos passos:"
echo "1. Execute: python3 main.py --help"
echo "2. Configure ambiente: python3 main.py setup-environment"
echo "3. Verifique status: python3 main.py environment-status"
echo ""
echo "Para ajuda completa, veja o README.md"
echo "Para testar em container: docker build -f Dockerfile.test -t leme-test ."
echo ""
echo "CLI Leme DevOps pronta para usar!"