# Script de Instalação da CLI Leme para Windows
# Instala Python, dependências e configura a CLI automaticamente
# Suporte: Windows 10/11, Windows Server

param(
    [switch]$Force = $false
)

# Configurações
$CliName = "leme"
$CliVersion = "1.0.0"
$InstallDir = "$env:USERPROFILE\.leme"
$BinDir = "$env:USERPROFILE\.local\bin"

# Cores para output
function Write-Header {
    Write-Host "┌─────────────────────────────────────────────────────────────┐" -ForegroundColor Blue
    Write-Host "│                    🚀 Instalador CLI Leme                  │" -ForegroundColor Blue
    Write-Host "│          Terraform & Docker - Versão $CliVersion          │" -ForegroundColor Blue
    Write-Host "└─────────────────────────────────────────────────────────────┘" -ForegroundColor Blue
}

function Write-Step {
    param($Message)
    Write-Host "▶ $Message" -ForegroundColor Blue
}

function Write-Success {
    param($Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param($Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

# Verificar se está executando como administrador
function Test-Administrator {
    try {
        $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
        return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    } catch {
        # Se não conseguir verificar (ex: PowerShell Core no Linux/macOS), assumir que não é admin
        return $false
    }
}

# Detectar sistema Windows
function Get-WindowsInfo {
    try {
        # Tentar usar Get-CimInstance (Windows PowerShell)
        $osInfo = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction Stop
        $archInfo = Get-CimInstance -ClassName Win32_Processor -ErrorAction Stop
        
        return @{
            Version = $osInfo.Version
            Caption = $osInfo.Caption
            Architecture = $archInfo.Architecture
        }
    } catch {
        try {
            # Fallback para Get-WmiObject (compatibilidade)
            $osInfo = Get-WmiObject -Class Win32_OperatingSystem
            $archInfo = Get-WmiObject -Class Win32_Processor
            
            return @{
                Version = $osInfo.Version
                Caption = $osInfo.Caption
                Architecture = $archInfo.Architecture
            }
        } catch {
            # Fallback final usando variáveis de ambiente
            return @{
                Version = $env:OS
                Caption = "Windows $env:OS"
                Architecture = $env:PROCESSOR_ARCHITECTURE
            }
        }
    }
}

# Verificar Python
function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)\.(\d+)") {
            $major = [int]$matches[1]
            $minor = [int]$matches[2]
            
            if ($major -eq 3 -and $minor -ge 7) {
                Write-Success "Python $($matches[0]) encontrado"
                return $true
            } else {
                Write-Warning "Python $($matches[0]) encontrado, mas versão 3.7+ é necessária"
                return $false
            }
        }
    } catch {
        Write-Warning "Python não encontrado"
        return $false
    }
    return $false
}

# Instalar Python
function Install-Python {
    if (Test-Python) {
        return
    }
    
    Write-Step "Instalando Python 3..."
    
    # Verificar se winget está disponível
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        try {
            winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements
            Write-Success "Python instalado via winget"
        } catch {
            Write-Warning "Falha ao instalar via winget, tentando download direto..."
            Install-PythonDirect
        }
    } else {
        Install-PythonDirect
    }
    
    # Atualizar PATH para sessão atual
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
    
    # Verificar instalação
    if (-not (Test-Python)) {
        Write-Error-Custom "Falha ao instalar Python"
        exit 1
    }
}

# Instalar Python via download direto
function Install-PythonDirect {
    $pythonUrl = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    
    Write-Step "Baixando Python..."
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
    
    Write-Step "Instalando Python..."
    Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=0", "PrependPath=1", "Include_test=0" -Wait
    
    Remove-Item $pythonInstaller -Force
}

# Verificar pip
function Test-Pip {
    try {
        pip --version | Out-Null
        Write-Success "pip encontrado"
        return $true
    } catch {
        Write-Warning "pip não encontrado"
        return $false
    }
}

# Instalar pip se necessário
function Install-Pip {
    if (Test-Pip) {
        return
    }
    
    Write-Step "Instalando pip..."
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
}

# Criar diretórios
function New-Directories {
    Write-Step "Criando diretórios..."
    
    if (-not (Test-Path $InstallDir)) {
        New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    }
    
    if (-not (Test-Path $BinDir)) {
        New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
    }
    
    Write-Success "Diretórios criados"
}

# Instalar CLI
function Install-Cli {
    Write-Step "Instalando CLI Leme..."
    
    # Copiar arquivos (assumindo execução local)
    $sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    Copy-Item -Path "$sourceDir\*" -Destination $InstallDir -Recurse -Force -Exclude "install.ps1"
    
    Write-Success "Arquivos copiados para $InstallDir"
}

# Instalar dependências Python
function Install-Dependencies {
    Write-Step "Instalando dependências Python..."
    
    Set-Location $InstallDir
    python -m pip install --user typer rich jinja2
    
    Write-Success "Dependências instaladas"
}

# Criar executável
function New-Executable {
    Write-Step "Criando comando executável 'leme'..."
    
    # Criar script batch
    $batchContent = @"
@echo off
cd /d "$InstallDir"
python main.py %*
"@
    
    $batchPath = "$BinDir\leme.bat"
    $batchContent | Out-File -FilePath $batchPath -Encoding ASCII
    
    # Criar script PowerShell (alternativo)
    $psContent = @"
#!/usr/bin/env pwsh
Set-Location "$InstallDir"
python main.py @args
"@
    
    $psPath = "$BinDir\leme.ps1"
    $psContent | Out-File -FilePath $psPath -Encoding UTF8
    
    Write-Success "Comandos 'leme.bat' e 'leme.ps1' criados"
}

# Configurar PATH
function Set-PathEnvironment {
    Write-Step "Configurando PATH..."
    
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    
    if ($currentPath -notlike "*$BinDir*") {
        $newPath = "$currentPath;$BinDir"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        $env:PATH = "$env:PATH;$BinDir"
        Write-Success "PATH configurado"
    } else {
        Write-Success "PATH já configurado"
    }
}

# Testar instalação
function Test-Installation {
    Write-Step "Testando instalação..."
    
    # Atualizar PATH para teste
    $env:PATH = "$env:PATH;$BinDir"
    
    try {
        $testResult = & "$BinDir\leme.bat" --help 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "CLI Leme instalada e funcionando!"
        } else {
            Write-Error-Custom "CLI instalada mas com problemas"
            exit 1
        }
    } catch {
        Write-Error-Custom "Erro ao testar instalação: $_"
        exit 1
    }
}

# Mostrar informações finais
function Show-FinalInfo {
    Write-Host ""
    Write-Host "🎉 Instalação concluída com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Como usar:" -ForegroundColor Blue
    Write-Host "  1. Reinicie seu PowerShell/CMD"
    Write-Host "  2. Execute: leme --help"
    Write-Host "  3. Para instalar Docker: leme install docker"
    Write-Host "  4. Para criar projeto: leme new project --name meu-projeto --provider azure"
    Write-Host ""
    Write-Host "Documentação:" -ForegroundColor Blue
    Write-Host "  README: $InstallDir\README.md"
    Write-Host "  Guia rápido: $InstallDir\QUICKSTART.md"
    Write-Host "  Exemplos: $InstallDir\EXAMPLES.md"
    Write-Host ""
    Write-Host "Importante: Reinicie o terminal para usar o comando 'leme'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para usar no PowerShell também execute:" -ForegroundColor Blue
    Write-Host "  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
}

# Função principal
function Main {
    Write-Header
    
    Write-Step "Detectando sistema Windows..."
    $windowsInfo = Get-WindowsInfo
    Write-Success "Sistema: $($windowsInfo.Caption)"
    
    if (-not (Test-Administrator)) {
        Write-Warning "Executando sem privilégios de administrador"
        Write-Warning "Algumas funcionalidades podem requerer elevação"
    }
    
    Install-Python
    Install-Pip
    New-Directories
    Install-Cli
    Install-Dependencies
    New-Executable
    Set-PathEnvironment
    Test-Installation
    Show-FinalInfo
}

# Executar instalação
try {
    Main
} catch {
    Write-Error-Custom "Erro durante a instalação: $_"
    exit 1
}