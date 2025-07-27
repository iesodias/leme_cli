# 🎓 Guia para Professores - CLI Leme DevOps

## 🎯 Objetivo
Este guia ajuda professores a usar a CLI Leme em cursos, workshops e aulas de DevOps/IaC.

## ⚡ Setup Rápido para Aula

### Preparação (5 minutos antes da aula):

```bash
# 1. Teste você mesmo primeiro
git clone https://github.com/SEU_USUARIO/leme-devops.git
cd leme-devops
./quick-install.sh
python3 main.py setup-environment --check-only

# 2. Se tudo estiver ok, compartilhe com alunos
```

### Instruções para Alunos (compartilhe via chat/email):

```bash
# Método 1: Instalação Direta (confiando no professor)
git clone https://github.com/SEU_USUARIO/leme-devops.git
cd leme-devops
./quick-install.sh
python3 main.py setup-environment --required-only --force

# Método 2: Teste Seguro Primeiro (recomendado)
git clone https://github.com/SEU_USUARIO/leme-devops.git
cd leme-devops
docker build -f Dockerfile.test -t leme-test .
docker run --rm leme-test python3 /app/main.py environment-status
# Se funcionar no container, instalar no sistema real
```

## 🧪 Cenários de Aula

### Cenário 1: Workshop DevOps Básico
**Duração: 2-3 horas**
**Objetivo: Configurar ambiente completo**

```bash
# Professor demonstra:
python3 main.py system-info
python3 main.py environment-status

# Alunos executam junto:
python3 main.py setup-environment --required-only --force

# Todos verificam juntos:
python3 main.py environment-status

# Resultado esperado: Docker ✅, Git ✅, Terraform ✅
```

### Cenário 2: Curso Infrastructure as Code
**Duração: 8+ horas (várias aulas)**
**Objetivo: Ambiente + projetos práticos**

```bash
# Aula 1: Setup ambiente
python3 main.py setup-environment
python3 main.py environment-status

# Aula 2: Primeiro projeto
python3 main.py new project --name workshop-azure --provider azure
cd workshop-azure
python3 ../main.py run init .
python3 ../main.py run plan .

# Aula 3: Recursos específicos
python3 main.py new resource --type storage-account --provider azure --name demo-storage
```

### Cenário 3: Demonstração Rápida
**Duração: 30 minutos**
**Objetivo: Mostrar capacidades**

```bash
# 1. Status atual (antes)
python3 main.py environment-status

# 2. Instalação automática
python3 main.py setup-environment --tools git,terraform --force

# 3. Status após instalação
python3 main.py environment-status

# 4. Criação de projeto simples
python3 main.py new project --name demo --provider azure
```

## 🔧 Comandos Úteis para Aula

### Verificação de Ambiente
```bash
# Ver quem tem o que instalado
python3 main.py environment-status

# Informações do sistema de cada aluno
python3 main.py system-info

# Apenas verificar sem instalar (diagnóstico)
python3 main.py setup-environment --check-only
```

### Instalação Progressiva
```bash
# Apenas ferramentas obrigatórias
python3 main.py setup-environment --required-only

# Adicionar ferramentas específicas depois
python3 main.py setup-environment --tools azure-cli,kubectl

# Pular Docker se já tiver
python3 main.py setup-environment --skip-docker
```

### Resolução de Problemas
```bash
# Ver ajuda de comandos específicos
python3 main.py setup-environment --help
python3 main.py environment-status --help

# Forçar reinstalação se algo falhou
python3 main.py setup-environment --force

# Verificar se Docker funciona
docker run hello-world
```

## 📋 Checklist para Professores

### Antes da Aula:
- [ ] Testar a CLI no seu sistema
- [ ] Testar em container Docker
- [ ] Preparar instruções de instalação
- [ ] Ter backup dos comandos principais
- [ ] Testar criação de projeto Terraform

### Durante a Aula:
- [ ] Compartilhar link do repositório
- [ ] Executar comandos junto com alunos
- [ ] Verificar que todos têm ambiente configurado
- [ ] Ajudar com problemas de instalação
- [ ] Demonstrar comandos principais

### Após a Aula:
- [ ] Coletar feedback dos alunos
- [ ] Documentar problemas encontrados
- [ ] Compartilhar recursos adicionais
- [ ] Preparar exercícios para casa

## 🚨 Problemas Comuns e Soluções

### Problema: Python não instalado
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# macOS
brew install python3

# Windows
# Download from python.org
```

### Problema: Permissões Docker
```bash
# Linux: adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
# Reiniciar terminal ou logout/login

# macOS: abrir Docker Desktop
open /Applications/Docker.app
```

### Problema: Terraform não encontrado
```bash
# Verificar se foi instalado
terraform --version

# Se não, instalação manual:
# Ubuntu/Debian
sudo apt install terraform

# macOS
brew install terraform
```

### Problema: Dependências Python
```bash
# Reinstalar dependências
pip3 install --upgrade rich typer jinja2

# Ou usar requirements.txt
pip3 install -r requirements.txt
```

## 💡 Dicas Pedagógicas

### Para Workshops Presenciais:
1. **Teste previamente** em diferentes sistemas
2. **Tenha backup manual** dos comandos importantes
3. **Use container Docker** para demonstração segura
4. **Prepare USBs** com o projeto para quem não tem internet

### Para Aulas Online:
1. **Compartilhe tela** durante instalação
2. **Use breakout rooms** para ajudar individualmente
3. **Grave a sessão** para revisão posterior
4. **Tenha chat/fórum** para dúvidas assíncronas

### Para Cursos Longos:
1. **Valide ambiente** no início de cada aula
2. **Crie exercícios incrementais** com a CLI
3. **Encourage feedback** dos alunos
4. **Mantenha-se atualizado** com novas versões

## 📚 Recursos Adicionais

### Links Úteis:
- [README.md](./README.md) - Documentação completa
- [DISTRIBUTION_PLAN.md](./DISTRIBUTION_PLAN.md) - Plano de distribuição
- [Dockerfile.test](./Dockerfile.test) - Container de teste

### Comandos de Emergência:
```bash
# Ajuda geral
python3 main.py --help

# Ajuda de comando específico
python3 main.py setup-environment --help

# Informações do sistema
python3 main.py system-info

# Status detalhado
python3 main.py environment-status
```

### Exemplo de Email para Alunos:
```
Assunto: Setup Ambiente DevOps - CLI Leme

Olá pessoal!

Para nossa aula de Infrastructure as Code, precisamos configurar algumas ferramentas.

1. Baixem a CLI: https://github.com/SEU_USUARIO/leme-devops
2. Sigam o README.md na seção "Setup Rápido"
3. Executem: python3 main.py setup-environment
4. Verifiquem: python3 main.py environment-status

Qualquer problema, me procurem!

Abraços,
Professor(a)
```

---

## 🎯 Objetivos de Aprendizado

Após usar a CLI Leme, alunos devem conseguir:
- ✅ Configurar ambiente DevOps automaticamente
- ✅ Criar projetos Infrastructure as Code
- ✅ Executar comandos Terraform básicos
- ✅ Entender conceitos de IaC e DevOps
- ✅ Usar Docker, Git, Terraform em projetos reais

**🎉 Boa aula!**