#!/usr/bin/env node
const { spawn, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

// Check if Python is installed - Windows/Git Bash compatible
function checkPython() {
    const pythonCommands = ['python', 'python3', 'py'];
    
    for (const cmd of pythonCommands) {
        try {
            // Use spawnSync with proper options for Windows/Git Bash
            const result = spawnSync(cmd, ['--version'], { 
                encoding: 'utf8',
                stdio: 'pipe',
                shell: true,
                windowsHide: true
            });
            
            // Check if command succeeded
            if (result.status === 0 || (result.stdout && result.stdout.includes('Python'))) {
                console.log(`Found Python: ${cmd}`);
                return cmd;
            }
        } catch (e) {
            // Continue to next command
            continue;
        }
    }
    
    console.error('Error: Python 3.7+ is required but not found.');
    console.error('Please install Python from https://www.python.org/');
    console.error('Available Python commands tried: python, python3, py');
    process.exit(1);
}

// Main execution
function main() {
    const pythonCmd = checkPython();
    
    // Try to find the Python script
    const possiblePaths = [
        path.join(__dirname, '..', 'src', 'codeprint', 'cli.py'),
        path.join(__dirname, '..', 'codeprint', 'cli.py')
    ];
    
    let scriptPath = null;
    for (const p of possiblePaths) {
        if (fs.existsSync(p)) {
            scriptPath = p;
            console.log(`Found script: ${scriptPath}`);
            break;
        }
    }
    
    if (!scriptPath) {
        // Fallback: try to run via pip-installed command
        console.log('Python script not found in package, trying pip-installed version...');
        
        // Try different command names
        const commands = ['codeprint', 'codeprintio', 'codep'];
        for (const cmd of commands) {
            try {
                const child = spawn(cmd, process.argv.slice(2), {
                    stdio: 'inherit',
                    shell: true,
                    windowsHide: true
                });
                
                child.on('exit', (code) => process.exit(code || 0));
                child.on('error', (err) => {
                    console.log(`Command ${cmd} failed, trying next...`);
                });
                return;
            } catch (e) {
                continue;
            }
        }
        
        console.error('Could not find codeprint. Install via: pip install codeprintio');
        process.exit(1);
    }
    
    // Run the Python script
    const args = process.argv.slice(2);
    console.log(`Running: ${pythonCmd} ${scriptPath} ${args.join(' ')}`);
    
    const child = spawn(pythonCmd, [scriptPath, ...args], {
        stdio: 'inherit',
        shell: true,
        windowsHide: true
    });
    
    child.on('exit', (code) => process.exit(code || 0));
    child.on('error', (err) => {
        console.error('Failed to start scanner:', err);
        process.exit(1);
    });
}

if (require.main === module) {
    main();
}