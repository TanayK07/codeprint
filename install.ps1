param(
    [string]$InstallMethod = "auto"
)

$ErrorActionPreference = "Stop"

function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Green "========================================"
Write-ColorOutput Green "     Gemini Scanner Installer"
Write-ColorOutput Green "========================================"
Write-Output ""

# Check for Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $python) {
    Write-ColorOutput Red "Error: Python is not installed."
    Write-Output "Please install Python 3.7+ from https://www.python.org/"
    exit 1
}

Write-Output "Python found at: $($python.Path)"

# Determine installation method
if ($InstallMethod -eq "auto") {
    # Check for package managers
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    $choco = Get-Command choco -ErrorAction SilentlyContinue
    
    if ($winget) {
        $InstallMethod = "winget"
    } elseif ($choco) {
        $InstallMethod = "chocolatey"
    } else {
        $InstallMethod = "pip"
    }
}

Write-Output "Installation method: $InstallMethod"
Write-Output ""

switch ($InstallMethod) {
    "winget" {
        Write-ColorOutput Green "Installing via WinGet..."
        winget install gemini-scanner
    }
    "chocolatey" {
        Write-ColorOutput Green "Installing via Chocolatey..."
        choco install gemini-scanner -y
    }
    "pip" {
        Write-ColorOutput Green "Installing via pip..."
        & $python.Path -m pip install gemini-scanner
    }
    default {
        Write-ColorOutput Red "Unknown installation method: $InstallMethod"
        exit 1
    }
}

Write-Output ""
Write-ColorOutput Green "✅ Installation complete!"
Write-Output "Run 'gemini --help' to get started."