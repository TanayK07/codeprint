from setuptools import setup, find_packages
import sys
import platform
import subprocess
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def install_platform_dependencies():
    """Install platform-specific clipboard dependencies"""
    system = platform.system()
    
    print(f"Setting up clipboard support for {system}...")
    
    if system == "Linux":
        try:
            # Check if xclip is available
            subprocess.run(['which', 'xclip'], check=True, capture_output=True)
            print("✓ xclip already installed")
        except subprocess.CalledProcessError:
            print("Installing xclip for clipboard support...")
            try:
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', '-y', 'xclip'], check=True)
                print("✓ xclip installed successfully")
            except subprocess.CalledProcessError:
                print("⚠ Could not install xclip automatically. Install manually: sudo apt install xclip")
    
    elif system == "Darwin":  # macOS
        print("✓ Clipboard support is built-in on macOS")
    
    elif system == "Windows":
        print("✓ Windows clipboard support via pyperclip")

class PostInstallCommand:
    """Post-installation setup"""
    
    def run(self):
        print("\n" + "="*60)
        print("🚀 CodePrint Installation Complete!")
        print("="*60)
        
        # Install platform dependencies
        install_platform_dependencies()
        
        print("\n📋 CodePrint Setup")
        print("-"*30)
        
        # Ask if user wants to run setup
        try:
            choice = input("Would you like to configure CodePrint now? (Y/n): ").strip().lower()
            if choice not in ['n', 'no']:
                print("\nRunning setup configuration...")
                from codeprint.cli import setup_config_interactive
                setup_config_interactive()
            else:
                print("You can run setup later with: codeprint --setup")
        except (EOFError, KeyboardInterrupt):
            print("\nYou can run setup later with: codeprint --setup")
        
        print(f"\n✅ Ready to use!")
        print("Get started with: codeprint --help")
        print("Interactive mode: codeprint -i")

# Define base dependencies
base_deps = [
    "colorama>=0.4.4",
]

# Platform-specific dependencies
if platform.system() == "Windows":
    base_deps.append("pyperclip>=1.8.2")
elif platform.system() == "Linux":
    # Try to use system xclip, fallback to pyperclip
    base_deps.append("pyperclip>=1.8.2")

setup(
    name="codeprint",
    version="1.0.1",
    author="Tanay Kedia",
    description="AI-ready code snapshots for any project with enhanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tanayk07/codeprint",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Documentation",
        "Topic :: Utilities",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires=">=3.7",
    install_requires=base_deps,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "all": [
            "pyperclip>=1.8.2",  # For full clipboard support
        ],
    },
    entry_points={
        "console_scripts": [
            "codeprint=codeprint.cli:main",
            "codep=codeprint.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)