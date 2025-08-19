#!/bin/bash

set -e

REPO="https://github.com/Tanayk07/codeprint"
VERSION="1.0.1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Banner
print_banner() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║               🚀 CODEPRINT INSTALLER v1.0.1                   ║${NC}"
    echo -e "${BLUE}║           AI-Ready Code Snapshots for Any Project             ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Check for Python
check_python() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        echo "python"
    else
        echo ""
    fi
}

# Install clipboard dependencies
install_clipboard_deps() {
    local os=$1
    echo -e "${YELLOW}📋 Setting up clipboard support...${NC}"
    
    case $os in
        linux)
            if command -v apt &> /dev/null; then
                echo -e "${CYAN}Installing xclip for clipboard support...${NC}"
                sudo apt update && sudo apt install -y xclip
            elif command -v yum &> /dev/null; then
                echo -e "${CYAN}Installing xclip for clipboard support...${NC}"
                sudo yum install -y xclip
            elif command -v dnf &> /dev/null; then
                echo -e "${CYAN}Installing xclip for clipboard support...${NC}"
                sudo dnf install -y xclip
            elif command -v pacman &> /dev/null; then
                echo -e "${CYAN}Installing xclip for clipboard support...${NC}"
                sudo pacman -S --noconfirm xclip
            else
                echo -e "${YELLOW}⚠  Could not auto-install clipboard support${NC}"
                echo -e "   Install manually: sudo apt install xclip (or equivalent)"
            fi
            ;;
        macos)
            echo -e "${GREEN}✓ Clipboard support built-in on macOS${NC}"
            ;;
        windows)
            echo -e "${CYAN}Installing pyperclip for clipboard support...${NC}"
            pip install pyperclip
            ;;
    esac
}

# Install using pip
install_pip() {
    local python_cmd=$1
    echo -e "${GREEN}📦 Installing via pip...${NC}"
    $python_cmd -m pip install --upgrade pip
    $python_cmd -m pip install codeprint
}

# Install using npm
install_npm() {
    echo -e "${GREEN}📦 Installing via npm...${NC}"
    npm install -g codeprint
}

# Install on macOS
install_macos() {
    if command -v brew &> /dev/null; then
        echo -e "${GREEN}🍺 Installing via Homebrew...${NC}"
        brew tap Tanayk07/codeprint
        brew install codeprint
    else
        local python_cmd=$(check_python)
        if [ -n "$python_cmd" ]; then
            install_pip $python_cmd
        else
            echo -e "${RED}❌ Python not found. Please install Python first.${NC}"
            exit 1
        fi
    fi
}

# Install on Linux
install_linux() {
    local python_cmd=$(check_python)
    
    if [ -z "$python_cmd" ]; then
        echo -e "${YELLOW}🐍 Installing Python...${NC}"
        if command -v apt &> /dev/null; then
            sudo apt update
            sudo apt install -y python3 python3-pip
            python_cmd="python3"
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip
            python_cmd="python3"
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3 python3-pip
            python_cmd="python3"
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm python python-pip
            python_cmd="python3"
        else
            echo -e "${RED}❌ Could not install Python automatically${NC}"
            exit 1
        fi
    fi
    
    # Check for snap
    if command -v snap &> /dev/null; then
        echo -e "${CYAN}Do you want to install via Snap? (y/N): ${NC}"
        read -r use_snap
        if [[ $use_snap =~ ^[Yy]$ ]]; then
            echo -e "${GREEN}📦 Installing via Snap...${NC}"
            sudo snap install codeprint
            return
        fi
    fi
    
    install_pip $python_cmd
}

# Install on Windows
install_windows() {
    if command -v choco &> /dev/null; then
        echo -e "${GREEN}🍫 Installing via Chocolatey...${NC}"
        choco install codeprint
    elif command -v winget &> /dev/null; then
        echo -e "${GREEN}📦 Installing via WinGet...${NC}"
        winget install codeprint
    else
        local python_cmd=$(check_python)
        if [ -n "$python_cmd" ]; then
            install_pip $python_cmd
        else
            echo -e "${RED}❌ Python not found. Please install Python first.${NC}"
            exit 1
        fi
    fi
}

# Run post-install setup
run_post_install() {
    echo -e "\n${CYAN}🔧 Running post-installation setup...${NC}"
    
    # Try to run setup
    if command -v codeprint &> /dev/null; then
        codeprint --setup
    else
        echo -e "${YELLOW}⚠  Could not find codeprint command${NC}"
        echo -e "   You may need to restart your terminal or add to PATH"
        echo -e "   Then run: ${CYAN}codeprint --setup${NC}"
    fi
}

# Main installation
main() {
    print_banner
    
    OS=$(detect_os)
    PYTHON=$(check_python)
    
    echo -e "🖥️  Detected OS: ${YELLOW}$OS${NC}"
    
    if [ "$OS" != "macos" ] && [ -z "$PYTHON" ]; then
        echo -e "${RED}❌ Python is not installed.${NC}"
        echo -e "Please install Python 3.7+ from https://www.python.org/"
        exit 1
    fi
    
    if [ -n "$PYTHON" ]; then
        echo -e "🐍 Python command: ${YELLOW}$PYTHON${NC}"
    fi
    echo ""
    
    # Install clipboard dependencies first
    install_clipboard_deps $OS
    echo ""
    
    # Install based on OS
    case $OS in
        macos)
            install_macos
            ;;
        linux)
            install_linux
            ;;
        windows)
            install_windows
            ;;
        *)
            echo -e "${YELLOW}⚠  Unknown OS. Attempting pip installation...${NC}"
            if [ -n "$PYTHON" ]; then
                install_pip $PYTHON
            else
                echo -e "${RED}❌ Cannot install without Python${NC}"
                exit 1
            fi
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}✅ Installation complete!${NC}"
    
    # Run post-install setup
    run_post_install
    
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                     🎉 READY TO USE! 🎉                       ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}📚 Getting Started:${NC}"
    echo -e "   ${YELLOW}codeprint --help${NC}          # Show all options"
    echo -e "   ${YELLOW}codeprint${NC}                 # Scan current directory"
    echo -e "   ${YELLOW}codeprint -i${NC}              # Interactive mode"
    echo -e "   ${YELLOW}codeprint -f mcp -c${NC}       # MCP format + clipboard"
    echo ""
    echo -e "${CYAN}💡 Pro Tips:${NC}"
    echo -e "   • Use ${YELLOW}--ignore${NC} to exclude files/directories"
    echo -e "   • MCP format works great with AI assistants"
    echo -e "   • Interactive mode provides a file browser"
    echo ""
    echo -e "${GREEN}🌟 Happy coding with CodePrint!${NC}"
}

# Run main function
main