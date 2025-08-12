const { exec } = require('child_process');
const os = require('os');

console.log('📦 Installing Python dependencies...');

// Determine the Python command
const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

// Install required Python packages
exec(`${pythonCmd} -m pip install colorama pyperclip`, (error, stdout, stderr) => {
    if (error) {
        console.warn('⚠️  Could not install Python dependencies automatically.');
        console.log('Please run manually: pip install colorama pyperclip');
        return;
    }
    console.log('✅ Python dependencies installed successfully!');
});