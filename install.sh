#!/bin/bash

set -e

REPO="https://github.com/Tanayk07/codeprint"
VERSION="2.0.0"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

# Install using pip
install_pip() {
    echo -e "${GREEN}Installing via pip...${NC}"
    pip install codeprintio
}

# Install using npm
install_npm() {
    echo -e "${GREEN}Installing via npm...${NC}"
    npm install -g codeprintio
}

# Install on macOS
install_macos() {
    if command -v brew &> /dev/null; then
        echo -e "${GREEN}Installing via Homebrew...${NC}"
        brew tap Tanayk07/codeprint
        brew install codeprintio
    else
        install_pip
    fi
}

# Install on Linux
install_linux() {
    if command -v apt &> /dev/null; then
        echo -e "${GREEN}Installing on Debian/Ubuntu...${NC}"
        sudo apt update
        sudo apt install -y python3 python3-pip
        install_pip
    elif command -v yum &> /dev/null; then
        echo -e "${GREEN}Installing on RedHat/CentOS...${NC}"
        sudo yum install -y python3 python3-pip
        install_pip
    elif command -v snap &> /dev/null; then
        echo -e "${GREEN}Installing via Snap...${NC}"
        sudo sudo snap install codeprintio
    else
        install_pip
    fi
}

# Install on Windows
install_windows() {
    if command -v choco &> /dev/null; then
        echo -e "${GREEN}Installing via Chocolatey...${NC}"
        choco install codeprintio
    elif command -v winget &> /dev/null; then
        echo -e "${GREEN}Installing via WinGet...${NC}"
        winget install codeprintio
    else
        install_pip
    fi
}

# Main installation
main() {
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}     CodePrint Installer${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    
    OS=$(detect_os)
    PYTHON=$(check_python)
    
    if [ -z "$PYTHON" ]; then
        echo -e "${RED}Error: Python is not installed.${NC}"
        echo "Please install Python 3.7+ from https://www.python.org/"
        exit 1
    fi
    
    echo -e "Detected OS: ${YELLOW}$OS${NC}"
    echo -e "Python command: ${YELLOW}$PYTHON${NC}"
    echo ""
    
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
            echo -e "${YELLOW}Unknown OS. Attempting pip installation...${NC}"
            install_pip
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}✅ Installation complete!${NC}"
    echo -e "Run ${YELLOW}codeprint --help${NC} to get started."
}

# Run main function
main