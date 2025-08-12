const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

// Check if Python is installed
function checkPython() {
    const pythonCommands = ['python3', 'python'];
    
    for (const cmd of pythonCommands) {
        try {
            const result = spawn.sync(cmd, ['--version'], { 
                encoding: 'utf8',
                stdio: 'pipe' 
            });
            if (result.status === 0) {
                return cmd;
            }
        } catch (e) {
            continue;
        }
    }
    
    console.error('Error: Python 3.7+ is required but not found.');
    console.error('Please install Python from https://www.python.org/');
    process.exit(1);
}

// Main execution
function main() {
    const pythonCmd = checkPython();
    const scriptPath = path.join(__dirname, '..', 'src', 'gemini_scanner.py');
    
    // Pass all arguments to Python script
    const args = process.argv.slice(2);
    
    const child = spawn(pythonCmd, [scriptPath, ...args], {
        stdio: 'inherit',
        shell: false
    });
    
    child.on('exit', (code) => {
        process.exit(code);
    });
    
    child.on('error', (err) => {
        console.error('Failed to start scanner:', err);
        process.exit(1);
    });
}

if (require.main === module) {
    main();
}