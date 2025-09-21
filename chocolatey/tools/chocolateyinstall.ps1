$ErrorActionPreference = 'Stop'

$packageName = 'codeprintio'
$packageVersion = '1.0.7'

Write-Host "Installing CodePrint v$packageVersion..." -ForegroundColor Green

try {
    # Check if Python is available
    $pythonCmd = $null
    $pythonCommands = @('python', 'python3', 'py')
    
    foreach ($cmd in $pythonCommands) {
        try {
            $result = & $cmd --version 2>&1
            if ($LASTEXITCODE -eq 0 -and $result -like "*Python*") {
                $pythonCmd = $cmd
                Write-Host "Found Python: $cmd" -ForegroundColor Cyan
                break
            }
        } catch {
            continue
        }
    }
    
    if (-not $pythonCmd) {
        Write-Error "Python 3.7+ is required but not found. Please install Python from https://www.python.org/"
        throw "Python not found"
    }
    
    # Upgrade pip first
    Write-Host "Upgrading pip..." -ForegroundColor Cyan
    & $pythonCmd -m pip install --upgrade pip
    
    # Install codeprintio
    Write-Host "Installing codeprintio via pip..." -ForegroundColor Cyan
    & $pythonCmd -m pip install codeprintio==$packageVersion
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "CodePrint installed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Usage:" -ForegroundColor Yellow
        Write-Host "  codeprint --help          # Show all options"
        Write-Host "  codeprint                 # Scan current directory"
        Write-Host "  codeprint -f mcp -c       # MCP format + clipboard"
        Write-Host ""
        Write-Host "Documentation: https://github.com/Tanayk07/codeprint#readme" -ForegroundColor Cyan
    } else {
        throw "pip install failed with exit code $LASTEXITCODE"
    }
    
} catch {
    Write-Error "Installation failed: $_"
    throw
}
