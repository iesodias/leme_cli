#!/bin/bash

# Script de Desinstalação da CLI Leme
# Remove completamente a CLI e suas configurações

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

CLI_NAME="leme"
INSTALL_DIR="$HOME/.leme"
BIN_DIR="$HOME/.local/bin"

print_header() {
    echo -e "${RED}"
    echo "┌─────────────────────────────────────────────────────────────┐"
    echo "│                🗑️  Desinstalador CLI Leme                  │"
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

confirm_uninstall() {
    echo -e "${YELLOW}Esta ação removerá completamente a CLI Leme do seu sistema.${NC}"
    echo -e "${YELLOW}Isso inclui:${NC}"
    echo "  - Arquivos da CLI em $INSTALL_DIR"
    echo "  - Comando 'leme' em $BIN_DIR"
    echo "  - Configurações do PATH"
    echo ""
    read -p "Tem certeza que deseja continuar? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Desinstalação cancelada."
        exit 0
    fi
}

remove_files() {
    print_step "Removendo arquivos da CLI..."
    
    if [ -d "$INSTALL_DIR" ]; then
        rm -rf "$INSTALL_DIR"
        print_success "Diretório $INSTALL_DIR removido"
    else
        print_warning "Diretório $INSTALL_DIR não encontrado"
    fi
    
    if [ -f "$BIN_DIR/leme" ]; then
        rm -f "$BIN_DIR/leme"
        print_success "Comando 'leme' removido"
    else
        print_warning "Comando 'leme' não encontrado"
    fi
}

remove_path_config() {
    print_step "Removendo configuração do PATH..."
    
    # Detectar arquivos de configuração do shell
    for rc_file in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
        if [ -f "$rc_file" ]; then
            # Remover linhas relacionadas ao Leme
            sed -i.backup '/# CLI Leme/d' "$rc_file" 2>/dev/null || true
            sed -i.backup "\|$BIN_DIR|d" "$rc_file" 2>/dev/null || true
            rm -f "$rc_file.backup" 2>/dev/null || true
        fi
    done
    
    print_success "Configuração do PATH removida"
}

show_final_message() {
    echo ""
    echo -e "${GREEN}🎉 CLI Leme desinstalada com sucesso!${NC}"
    echo ""
    echo -e "${BLUE}Para completar a remoção:${NC}"
    echo "  1. Reinicie seu terminal"
    echo "  2. O comando 'leme' não estará mais disponível"
    echo ""
    echo -e "${YELLOW}Nota:${NC} As dependências Python (typer, rich, jinja2) não foram removidas"
    echo "      Elas podem ser usadas por outras aplicações"
}

main() {
    print_header
    confirm_uninstall
    remove_files
    remove_path_config
    show_final_message
}

main "$@"