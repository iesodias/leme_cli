#!/bin/bash
# CLI Leme DevOps - Instalação Rápida
# Autor: Seu Nome
# Versão: 1.0.0-beta

set -e

echo "CLI Leme DevOps - Setup Rápido"
echo "================================"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python 3 não encontrado. Por favor instale Python 3.7+ primeiro."
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   macOS: brew install python3"
    exit 1
fi

# Verificar se pip está disponível
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "ERRO: pip não encontrado. Por favor instale pip primeiro."
    echo "   Ubuntu/Debian: sudo apt install python3-pip"
    exit 1
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