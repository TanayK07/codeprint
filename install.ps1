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

function Print-Banner {
    Write-ColorOutput Blue "╔════════════════════════════════════════════════════════════════╗"
    Write-ColorOutput Blue "║               🚀 CODEPRINT INSTALLER v1.0.1                   ║"
    Write-ColorOutput Blue "║           AI-Ready Code Snapshots for Any Project             ║"
    Write-ColorOutput Blue "╚════════════════════════════════════════════════════════════════╝"
    Write-Output ""
}

function Install-ClipboardSupport {
    Write-ColorOutput Yellow "📋 Setting up clipboard support for Windows..."
    
    try {
        # Try to install pyperclip
        Write-ColorOutput Cyan "Installing pyperclip for clipboard support..."
        & python -m pip install pyperclip
        Write-ColorOutput Green "✓ Clipboard support installed"
        return $true
    }
    catch {
        Write-ColorOutput Yellow "⚠ Could not install clipboard support automatically"
        Write-ColorOutput Cyan "You can install it later with: pip install pyperclip"
        return $false
    }
}

function Test-PythonInstallation {
    # Check for Python
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        $python = Get-Command python3 -ErrorAction SilentlyContinue
    }

    if (-not $python) {
        Write-ColorOutput Red "❌ Python is not installed."
        Write-Output "Please install Python 3.7+ from https://www.python.org/"
        return $null
    }

    Write-Output "🐍 Python found at: $($python.Path)"
    return $python
}

function Install-CodePrint {
    param($InstallMethod, $PythonCmd)
    
    switch ($InstallMethod) {
        "winget" {
            Write-ColorOutput Green "📦 Installing via WinGet..."
            winget install codeprint
        }
        "chocolatey" {
            Write-ColorOutput Green "🍫 Installing via Chocolatey..."
            choco install codeprint -y
        }
        "pip" {
            Write-ColorOutput Green "📦 Installing via pip..."
            & $PythonCmd.Path -m pip install --upgrade pip
            & $PythonCmd.Path -m pip install codeprint
        }
        default {
            Write-ColorOutput Red "❌ Unknown installation method: $InstallMethod"
            exit 1
        }
    }
}

function Run-PostInstallSetup {
    Write-ColorOutput Cyan "🔧 Running post-installation setup..."
    
    # Check if codeprint is available
    $codeprint = Get-Command codeprint -ErrorAction SilentlyContinue
    if ($codeprint) {
        try {
            & codeprint --setup
        }
        catch {
            Write-ColorOutput Yellow "⚠ Could not run automatic setup"
            Write-ColorOutput Cyan "You can run setup later with: codeprint --setup"
        }
    }
    else {
        Write-ColorOutput Yellow "⚠ Could not find codeprint command"
        Write-ColorOutput Cyan "You may need to restart your terminal or add to PATH"
        Write-ColorOutput Cyan "Then run: codeprint --setup"
    }
}

function Show-CompletionMessage {
    Write-Output ""
    Write-ColorOutput Blue "╔════════════════════════════════════════════════════════════════╗"
    Write-ColorOutput Blue "║                     🎉 READY TO USE! 🎉                       ║"
    Write-ColorOutput Blue "╚════════════════════════════════════════════════════════════════╝"
    Write-Output ""
    Write-ColorOutput Cyan "📚 Getting Started:"
    Write-ColorOutput Yellow "   codeprint --help          # Show all options"
    Write-ColorOutput Yellow "   codeprint                 # Scan current directory"
    Write-ColorOutput Yellow "   codeprint -i              # Interactive mode"
    Write-ColorOutput Yellow "   codeprint -f mcp -c       # MCP format + clipboard"
    Write-Output ""
    Write-ColorOutput Cyan "💡 Pro Tips:"
    Write-Output "   • Use --ignore to exclude files/directories"
    Write-Output "   • MCP format works great with AI assistants"
    Write-Output "   • Interactive mode provides a file browser"
    Write-Output ""
    Write-ColorOutput Green "🌟 Happy coding with CodePrint!"
}

# Main execution
Print-Banner

# Test Python installation
$python = Test-PythonInstallation
if (-not $python) {
    exit 1
}

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

Write-Output "📋 Installation method: $InstallMethod"
Write-Output ""

# Install clipboard support
$clipboardSuccess = Install-ClipboardSupport
Write-Output ""

# Install CodePrint
try {
    Install-CodePrint -InstallMethod $InstallMethod -PythonCmd $python
    Write-ColorOutput Green "✅ Installation complete!"
}
catch {
    Write-ColorOutput Red "❌ Installation failed: $_"
    exit 1
}

# Run post-install setup
Write-Output ""
Run-PostInstallSetup

# Show completion message
Show-CompletionMessage