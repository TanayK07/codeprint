$ErrorActionPreference = 'Stop'

Write-Host "Uninstalling CodePrint..." -ForegroundColor Yellow

try {
    # Find Python command
    $pythonCmd = $null
    $pythonCommands = @('python', 'python3', 'py')
    
    foreach ($cmd in $pythonCommands) {
        try {
            $result = & $cmd --version 2>&1
            if ($LASTEXITCODE -eq 0 -and $result -like "*Python*") {
                $pythonCmd = $cmd
                break
            }
        } catch {
            continue
        }
    }
    
    if ($pythonCmd) {
        Write-Host "Removing codeprintio package..." -ForegroundColor Cyan
        & $pythonCmd -m pip uninstall codeprintio -y
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "CodePrint uninstalled successfully!" -ForegroundColor Green
        } else {
            Write-Warning "pip uninstall failed with exit code $LASTEXITCODE"
        }
    } else {
        Write-Warning "Python not found. Manual cleanup may be required."
    }
    
} catch {
    Write-Warning "Uninstallation encountered an issue: $_"
    Write-Host "You may need to manually run: pip uninstall codeprintio" -ForegroundColor Cyan
}
