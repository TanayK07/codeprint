# 🚀 CodePrint

[![PyPI version](https://badge.fury.io/py/codeprintio.svg)](https://badge.fury.io/py/codeprintio)
[![npm version](https://badge.fury.io/js/codeprintio.svg)](https://badge.fury.io/js/codeprintio)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-blue)](https://github.com/Tanayk07/codeprint)

A blazing-fast, cross-platform CLI tool that creates comprehensive AI-ready snapshots of your codebase. Perfect for use with ChatGPT, Claude, Gemini, and other AI assistants.

<div align="center">
  <img src="docs/demo.gif" alt="CodePrint Demo" width="600">
</div>

## ✨ Features

- 🚀 **Lightning Fast**: Parallel processing for rapid scanning
- 🎯 **Smart Detection**: Automatically detects project type and applies appropriate filters
- 📋 **Multiple Formats**: Outputs in TXT or MCP (Markdown Context Pack) format
- 📎 **Clipboard Ready**: Option to copy output directly to clipboard
- 🔍 **Gitignore Support**: Respects `.gitignore` patterns
- 🎨 **Beautiful CLI**: Colorful ASCII art and progress indicators
- 🌍 **Cross-Platform**: Works on Windows, macOS, Linux, Git Bash, and more
- 🧠 **AI-Optimized**: Perfect for prompt engineering with any AI assistant

## 📦 Installation

### Quick Install (Recommended)

#### Using the universal installer:

**Linux/macOS:**
```bash
curl -sSL https://raw.githubusercontent.com/Tanayk07/codeprint/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://raw.githubusercontent.com/Tanayk07/codeprint/main/install.ps1 | iex
```

### Package Managers

#### pip (Python)
```bash
pip install codeprintio
```

#### npm (Node.js)
```bash
npm install -g codeprintio
```

#### Homebrew (macOS)
```bash
brew tap Tanayk07/codeprint
brew install codeprintio
```

#### Chocolatey (Windows)
```powershell
choco install codeprintio
```

#### WinGet (Windows)
```powershell
winget install codeprintio
```

#### Snap (Linux)
```bash
sudo sudo snap install codeprintio
```

#### APT (Debian/Ubuntu)
```bash
sudo add-apt-repository ppa:Tanayk07/codeprint
sudo apt update
sudo sudo apt install codeprintio
```

## 🚀 Quick Start

### Basic Usage

Scan current directory and save to file:
```bash
codeprint
```

Scan with specific format:
```bash
codeprint -f mcp  # Generate MCP format
codeprint -f txt  # Generate TXT format (default)
```

Copy to clipboard automatically:
```bash
codeprint -c
```

### Advanced Usage

```bash
# Scan specific directory
codeprint -p /path/to/project

# Custom output file
codeprint -o my_snapshot.txt

# Include hidden files
codeprint --include-hidden

# Set custom limits
codeprint --max-files 1000 --max-file-size 2048 --max-lines 2000

# Disable automatic project detection
codeprint --no-auto-detect

# Disable gitignore patterns
codeprint --no-gitignore

# Verbose output
codeprint -v
```

## 🎯 Project Type Detection

CodePrint automatically detects your project type and applies appropriate ignore patterns:

| Project Type | Detection Files | Auto-Ignored |
|-------------|----------------|--------------|
| Python | `requirements.txt`, `setup.py`, `pyproject.toml` | `__pycache__`, `*.pyc`, `venv/`, `.egg-info/` |
| JavaScript | `package.json` | `node_modules/`, `dist/`, `*.min.js` |
| TypeScript | `tsconfig.json` | `node_modules/`, `dist/`, `*.d.ts` |
| Java | `pom.xml`, `build.gradle` | `target/`, `*.class`, `.gradle/` |
| Android | `AndroidManifest.xml`, `gradle.properties` | `build/`, `*.apk`, `*.aab` |
| iOS | `Podfile`, `*.xcodeproj` | `Pods/`, `*.ipa`, `DerivedData/` |
| React | `package.json` + React files | `node_modules/`, `build/`, `.next/` |
| .NET | `*.csproj`, `*.sln` | `bin/`, `obj/`, `packages/` |
| Go | `go.mod` | `vendor/`, `*.exe` |
| Rust | `Cargo.toml` | `target/`, `Cargo.lock` |
| Flutter | `pubspec.yaml` | `build/`, `.dart_tool/` |

## 📋 Output Formats

### TXT Format
Simple text format with file contents and directory structure. Perfect for quick sharing.

### MCP Format (Markdown Context Pack)
Structured markdown format with metadata, syntax highlighting, and better organization. Ideal for AI assistants.

## ⚙️ Configuration

### Command-Line Flags

| Flag | Description | Default |
|------|-------------|---------|
| `-f, --format` | Output format (txt/mcp) | txt |
| `-o, --output` | Output file name | auto-generated |
| `-c, --clipboard` | Copy to clipboard | false |
| `-p, --path` | Path to scan | current directory |
| `--max-file-size` | Max file size (KB) | 1024 |
| `--max-files` | Max number of files | 500 |
| `--max-lines` | Max lines per file | 1000 |
| `--include-hidden` | Include hidden files | false |
| `--no-gitignore` | Ignore .gitignore patterns | false |
| `--no-auto-detect` | Disable project type detection | false |
| `--no-progress` | Disable progress output | false |
| `--no-parallel` | Disable parallel processing | false |
| `-v, --verbose` | Verbose output | false |

### Environment Variables

```bash
export GEMINI_DEFAULT_FORMAT=mcp
export GEMINI_CLIPBOARD=true
export GEMINI_MAX_FILES=1000
```

## 🔧 Development

### Building from Source

```bash
# Clone the repository
git clone https://github.com/Tanayk07/codeprint.git
cd codeprint

# Install dependencies
pip install -r requirements.txt

# Run locally
python src/codeprint.py

# Run tests
pytest tests/

# Build distributions
python setup.py sdist bdist_wheel
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📈 Performance

CodePrint is optimized for speed:

- **Parallel Processing**: Utilizes multiple threads for file processing
- **Smart Filtering**: Skips binary and large files automatically
- **Efficient Memory Usage**: Streams large files instead of loading entirely
- **Fast Pattern Matching**: Uses optimized fnmatch for ignore patterns

Benchmark results (on a typical React project):
- Files scanned: 500
- Time taken: ~2 seconds
- Memory usage: < 50MB

## 🛡️ Security

- Never includes sensitive files (keys, certificates, .env files)
- Respects .gitignore patterns by default
- No network requests or data collection
- Open source and auditable

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for better AI context management
- ASCII art generated with [pyfiglet](https://github.com/pwaller/pyfiglet)
- Colored output powered by [colorama](https://github.com/tartley/colorama)

## 🐛 Troubleshooting

### Common Issues

**Python not found:**
- Ensure Python 3.7+ is installed
- Add Python to your PATH

**Clipboard not working:**
- Install `pyperclip`: `pip install pyperclip`
- On Linux, install `xclip` or `xsel`

**Colors not showing:**
- Install `colorama`: `pip install colorama`
- On Windows, enable ANSI colors in terminal

## 📧 Contact

- GitHub: [@Tanayk07](https://github.com/Tanayk07)
- Email: tkedia7@gmail.com

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Tanayk07/codeprint&type=Date)](https://star-history.com/#Tanayk07/codeprint&Date)

---

<div align="center">
Made with ❤️ for the AI community
</div>