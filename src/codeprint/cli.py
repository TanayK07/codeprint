#!/usr/bin/env python3
"""
CodePrint - Enhanced Interactive CLI with Navigation
A powerful tool for creating AI-ready project snapshots
"""

import os
import sys
import json
import fnmatch
import argparse
import datetime
import subprocess
import platform
import hashlib
import concurrent.futures
from pathlib import Path
from typing import Dict, Set, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import shutil
import time

# For cross-platform clipboard support
CLIPBOARD_AVAILABLE = False
try:
    # Try platform-specific clipboard tools first
    if platform.system() == "Linux":
        # Check for xclip or xsel
        if shutil.which("xclip") or shutil.which("xsel"):
            CLIPBOARD_AVAILABLE = True
        else:
            try:
                import pyperclip
                CLIPBOARD_AVAILABLE = True
            except ImportError:
                pass
    elif platform.system() == "Darwin":  # macOS
        # macOS has pbcopy built-in
        CLIPBOARD_AVAILABLE = True
    elif platform.system() == "Windows":
        try:
            import pyperclip
            CLIPBOARD_AVAILABLE = True
        except ImportError:
            pass
except Exception:
    pass

# For colored output
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback for when colorama is not available
    class Fore:
        RED = GREEN = BLUE = YELLOW = CYAN = MAGENTA = WHITE = BLACK = ''
        RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''

# For tab completion
try:
    # Try Windows-specific readline
    if platform.system() == 'Windows':
        try:
            import pyreadline3 as readline
        except ImportError:
            try:
                import pyreadline as readline
            except ImportError:
                import readline
    else:
        import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

# Version
__version__ = "1.0.5"

# Compact ASCII Art Logo
ASCII_LOGO = """
╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║  ██████╗ ██████╗ ██████╗ ███████╗    ██████╗ ██████╗ ██╗███╗   ██╗████████╗  │  AI-Ready Code Snapshots v1.0.5  │  📋 Transform → AI Ready  ║
║ ██╔════╝██╔═══██╗██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██║████╗  ██║╚══██╔══╝  │ Cross-platform project scanner     │  🚀 Fast & Smart Detection ║
║ ██║     ██║   ██║██║  ██║█████╗      ██████╔╝██████╔╝██║██╔██╗ ██║   ██║     │ Perfect for ChatGPT, Claude & More │  ⚙️  Highly Configurable  ║
║ ██║     ██║   ██║██║  ██║██╔══╝      ██╔═══╝ ██╔══██╗██║██║╚██╗██║   ██║     │────────────────────────────────────│──────────────────────────║
║ ╚██████╗╚██████╔╝██████╔╝███████╗    ██║     ██║  ██║██║██║ ╚████║   ██║     │ Use: codeprint [options] [path]    │  Get started: --help      ║
║  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝     │════════════════════════════════════│══════════════════════════║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

class OutputFormat(Enum):
    TXT = "txt"
    MCP = "mcp"

class ProjectType(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    ANDROID = "android"
    IOS = "ios"
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"
    DOTNET = "dotnet"
    GO = "go"
    RUST = "rust"
    CPP = "cpp"
    RUBY = "ruby"
    PHP = "php"
    FLUTTER = "flutter"
    UNKNOWN = "unknown"

@dataclass
class ScannerConfig:
    """Configuration for the scanner"""
    output_format: OutputFormat = OutputFormat.TXT
    copy_to_clipboard: bool = False
    output_file: Optional[str] = None
    max_file_size: int = 1024 * 1024  # 1MB
    max_files: int = 500
    max_lines_per_file: int = 1000
    use_gitignore: bool = True
    auto_detect_project: bool = True
    show_progress: bool = True
    parallel_processing: bool = True
    ignore_dirs: Set[str] = field(default_factory=set)
    ignore_patterns: Set[str] = field(default_factory=set)
    include_hidden: bool = False
    verbose: bool = False
    interactive_mode: bool = False
    custom_ignore_dirs: Set[str] = field(default_factory=set)
    custom_ignore_files: Set[str] = field(default_factory=set)
    custom_ignore_extensions: Set[str] = field(default_factory=set)

def copy_to_clipboard(text: str) -> bool:
    """Cross-platform clipboard copy function"""
    try:
        system = platform.system()
        
        if system == "Linux":
            # Try xclip first
            if shutil.which("xclip"):
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], 
                                         stdin=subprocess.PIPE, text=True)
                process.communicate(input=text)
                return process.returncode == 0
            # Try xsel
            elif shutil.which("xsel"):
                process = subprocess.Popen(['xsel', '--clipboard', '--input'], 
                                         stdin=subprocess.PIPE, text=True)
                process.communicate(input=text)
                return process.returncode == 0
            # Fallback to pyperclip
            else:
                import pyperclip
                pyperclip.copy(text)
                return True
                
        elif system == "Darwin":  # macOS
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, text=True)
            process.communicate(input=text)
            return process.returncode == 0
            
        elif system == "Windows":
            import pyperclip
            pyperclip.copy(text)
            return True
            
    except Exception:
        return False
    
    return False

def setup_config_interactive():
    """Interactive setup for configuration"""
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║           CODEPRINT SETUP               ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Let's configure CodePrint for your needs!{Style.RESET_ALL}")
    
    # Ask if user wants to use defaults
    use_defaults = input(f"\n{Fore.GREEN}Use all default settings? (Y/n): {Style.RESET_ALL}").strip().lower()
    
    if use_defaults in ['y', 'yes', '']:
        print(f"{Fore.GREEN}✓ Using all default settings{Style.RESET_ALL}")
        config = ScannerConfig()
        save_user_config(config)
        return config
    
    print(f"\n{Fore.CYAN}Walking through configuration options...{Style.RESET_ALL}")
    config = ScannerConfig()
    
    # Output format
    print(f"\n{Fore.YELLOW}1. Output Format{Style.RESET_ALL}")
    print(f"   txt - Simple text format")
    print(f"   mcp - Markdown Context Pack format (better for AI)")
    format_choice = input(f"   Choose format (txt/mcp) [txt]: ").strip().lower()
    if format_choice == 'mcp':
        config.output_format = OutputFormat.MCP
    
    # Clipboard
    print(f"\n{Fore.YELLOW}2. Clipboard{Style.RESET_ALL}")
    clipboard_choice = input(f"   Copy output to clipboard automatically? (y/N): ").strip().lower()
    if clipboard_choice in ['y', 'yes']:
        config.copy_to_clipboard = True
    
    # Max files
    print(f"\n{Fore.YELLOW}3. Maximum Files{Style.RESET_ALL}")
    max_files_choice = input(f"   Maximum files to scan (500/unlimited): ").strip().lower()
    if max_files_choice in ['unlimited', 'u', 'no limit']:
        config.max_files = 999999
    elif max_files_choice.isdigit():
        config.max_files = int(max_files_choice)
    
    # Max file size
    print(f"\n{Fore.YELLOW}4. Maximum File Size{Style.RESET_ALL}")
    max_size_choice = input(f"   Maximum file size in KB (1024/unlimited): ").strip().lower()
    if max_size_choice in ['unlimited', 'u', 'no limit']:
        config.max_file_size = 999999 * 1024
    elif max_size_choice.isdigit():
        config.max_file_size = int(max_size_choice) * 1024
    
    # Max lines per file
    print(f"\n{Fore.YELLOW}5. Maximum Lines Per File{Style.RESET_ALL}")
    max_lines_choice = input(f"   Maximum lines per file (1000/unlimited): ").strip().lower()
    if max_lines_choice in ['unlimited', 'u', 'no limit']:
        config.max_lines_per_file = 999999
    elif max_lines_choice.isdigit():
        config.max_lines_per_file = int(max_lines_choice)
    
    # Use .gitignore
    print(f"\n{Fore.YELLOW}6. Respect .gitignore{Style.RESET_ALL}")
    gitignore_choice = input(f"   Respect .gitignore patterns? (Y/n): ").strip().lower()
    if gitignore_choice in ['n', 'no']:
        config.use_gitignore = False
    
    # Auto-detect project
    print(f"\n{Fore.YELLOW}7. Auto-detect Project Type{Style.RESET_ALL}")
    autodetect_choice = input(f"   Auto-detect project type? (Y/n): ").strip().lower()
    if autodetect_choice in ['n', 'no']:
        config.auto_detect_project = False
    
    # Include hidden files
    print(f"\n{Fore.YELLOW}8. Hidden Files{Style.RESET_ALL}")
    hidden_choice = input(f"   Include hidden files? (y/N): ").strip().lower()
    if hidden_choice in ['y', 'yes']:
        config.include_hidden = True
    
    print(f"\n{Fore.GREEN}✓ Configuration complete!{Style.RESET_ALL}")
    save_user_config(config)
    return config

def get_config_file_path():
    """Get the path to the configuration file"""
    if platform.system() == "Windows":
        config_dir = os.path.expanduser("~\\AppData\\Local\\CodePrint")
    else:
        config_dir = os.path.expanduser("~/.config/codeprint")
    
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")

def save_user_config(config: ScannerConfig):
    """Save user configuration to file"""
    config_data = {
        "output_format": config.output_format.value,
        "copy_to_clipboard": config.copy_to_clipboard,
        "max_file_size": config.max_file_size,
        "max_files": config.max_files,
        "max_lines_per_file": config.max_lines_per_file,
        "use_gitignore": config.use_gitignore,
        "auto_detect_project": config.auto_detect_project,
        "include_hidden": config.include_hidden,
    }
    
    try:
        config_path = get_config_file_path()
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        print(f"{Fore.GREEN}✓ Configuration saved to: {config_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.YELLOW}⚠ Could not save configuration: {e}{Style.RESET_ALL}")

def load_user_config() -> ScannerConfig:
    """Load user configuration from file"""
    config = ScannerConfig()
    
    try:
        config_path = get_config_file_path()
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            config.output_format = OutputFormat(config_data.get("output_format", "txt"))
            config.copy_to_clipboard = config_data.get("copy_to_clipboard", False)
            config.max_file_size = config_data.get("max_file_size", 1024 * 1024)
            config.max_files = config_data.get("max_files", 500)
            config.max_lines_per_file = config_data.get("max_lines_per_file", 1000)
            config.use_gitignore = config_data.get("use_gitignore", True)
            config.auto_detect_project = config_data.get("auto_detect_project", True)
            config.include_hidden = config_data.get("include_hidden", False)
    except Exception:
        pass
    
    return config

class ProjectDetector:
    """Detects project type based on files present"""
    
    @staticmethod
    def detect_project_type(path: Path) -> ProjectType:
        """Detect the project type based on characteristic files"""
        
        # Check for specific project files - order matters!
        checks = [
            # Flutter (check before Dart/Android)
            (['pubspec.yaml', 'lib/main.dart'], ProjectType.FLUTTER),
            # Android (check before general Java)
            (['build.gradle', 'AndroidManifest.xml'], ProjectType.ANDROID),
            (['gradle.properties', 'AndroidManifest.xml'], ProjectType.ANDROID),
            # iOS
            (['Podfile', '*.xcodeproj', '*.xcworkspace'], ProjectType.IOS),
            # React (check before general JavaScript)
            (['package.json', 'src/App.js'], ProjectType.REACT),
            (['package.json', 'src/App.jsx'], ProjectType.REACT),
            (['package.json', 'src/App.tsx'], ProjectType.REACT),
            # Vue
            (['vue.config.js'], ProjectType.VUE),
            (['nuxt.config.js'], ProjectType.VUE),
            # Angular
            (['angular.json'], ProjectType.ANGULAR),
            (['.angular-cli.json'], ProjectType.ANGULAR),
            # TypeScript (check before JavaScript)
            (['tsconfig.json'], ProjectType.TYPESCRIPT),
            # JavaScript/Node.js
            (['package.json'], ProjectType.JAVASCRIPT),
            # Python
            (['requirements.txt'], ProjectType.PYTHON),
            (['setup.py'], ProjectType.PYTHON),
            (['pyproject.toml'], ProjectType.PYTHON),
            (['Pipfile'], ProjectType.PYTHON),
            # Java
            (['pom.xml'], ProjectType.JAVA),
            (['build.gradle'], ProjectType.JAVA),
            # .NET
            (['*.csproj'], ProjectType.DOTNET),
            (['*.sln'], ProjectType.DOTNET),
            (['*.vbproj'], ProjectType.DOTNET),
            (['*.fsproj'], ProjectType.DOTNET),
            # Go
            (['go.mod'], ProjectType.GO),
            (['go.sum'], ProjectType.GO),
            # Rust
            (['Cargo.toml'], ProjectType.RUST),
            (['Cargo.lock'], ProjectType.RUST),
            # C++
            (['CMakeLists.txt'], ProjectType.CPP),
            (['Makefile'], ProjectType.CPP),
            (['*.cpp'], ProjectType.CPP),
            # Ruby
            (['Gemfile'], ProjectType.RUBY),
            (['Rakefile'], ProjectType.RUBY),
            # PHP
            (['composer.json'], ProjectType.PHP),
            (['composer.lock'], ProjectType.PHP),
        ]
        
        for patterns, project_type in checks:
            for pattern in patterns:
                if '*' in pattern:
                    if list(path.glob(pattern)):
                        return project_type
                else:
                    if (path / pattern).exists():
                        return project_type
        
        return ProjectType.UNKNOWN

    @staticmethod
    def should_ignore_xml(project_type: ProjectType, interactive: bool = True) -> bool:
        """Determine if XML files should be ignored for certain project types"""
        # Auto-ignore XML for certain project types
        auto_ignore_xml_projects = {
            ProjectType.ANDROID,  # Android XML files are often layout/config
        }
        
        if project_type in auto_ignore_xml_projects:
            if not interactive:
                return True
            # For Android, default to yes but allow override
            choice = input(f"\n{Fore.YELLOW}Android project detected. Skip XML files? (Y/n): {Style.RESET_ALL}").strip().lower()
            return choice not in ['n', 'no']
        
        # Ask for other project types that commonly have XML
        xml_common_projects = {
            ProjectType.JAVA,
            ProjectType.DOTNET,
        }
        
        if project_type in xml_common_projects and interactive:
            choice = input(f"\n{Fore.YELLOW}{project_type.value.title()} project detected. Skip XML files? (y/N): {Style.RESET_ALL}").strip().lower()
            return choice in ['y', 'yes']
        
        return False

    @staticmethod
    def get_recommended_ignore_patterns(project_type: ProjectType, interactive: bool = True) -> Tuple[Set[str], Set[str]]:
        """Get recommended ignore patterns with automatic XML handling"""
        # Get base patterns
        ignore_xml = ProjectDetector.should_ignore_xml(project_type, interactive)
        dirs, files = IgnorePatterns.get_ignore_patterns(project_type, ignore_xml)
        
        # Add any additional project-specific recommendations
        if project_type == ProjectType.ANDROID:
            # Additional Android-specific ignores
            files.update({
                'proguard-rules.pro',  # Obfuscation rules - often not needed for AI
                '*.jks', '*.keystore',  # Security files
            })
        elif project_type == ProjectType.PYTHON:
            # Additional Python-specific ignores
            dirs.update({
                '.pytest_cache',
                '.mypy_cache',
                '__pycache__',
            })
        
        return dirs, files
    

class IgnorePatterns:
    """Manages ignore patterns for different project types"""
    
    # Universal ignore patterns - Enhanced with more binary file types
    UNIVERSAL_IGNORE_DIRS = {
        # Version control
        '.git', '.svn', '.hg', '.bzr',
        # IDEs
        '.vscode', '.idea', '.vs', '.atom', '.sublime-text',
        # OS
        '.DS_Store', 'Thumbs.db', 'desktop.ini',
        # Temp
        'tmp', 'temp', 'cache', '.cache',
        # Logs
        'logs', '*.log',
        # Backups
        '*~', '*.bak', '*.backup', '*.old',
    }
    
    UNIVERSAL_IGNORE_FILES = {
        # Binary executables
        '*.exe', '*.dll', '*.so', '*.dylib', '*.a', '*.lib',
        '*.o', '*.obj', '*.pdb', '*.idb',
        
        # Archives and compressed files
        '*.zip', '*.tar', '*.gz', '*.bz2', '*.7z', '*.rar',
        '*.xz', '*.lz', '*.lzma', '*.cab', '*.msi', '*.pkg',
        
        # Images and graphics
        '*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.ico', '*.svg', '*.webp',
        '*.tiff', '*.tif', '*.raw', '*.cr2', '*.nef', '*.arw', '*.dng',
        '*.psd', '*.ai', '*.eps', '*.pdf',
        
        # Audio files
        '*.mp3', '*.wav', '*.flac', '*.ogg', '*.aac', '*.m4a', '*.wma',
        '*.opus', '*.ape', '*.ac3', '*.dts',
        
        # Video files
        '*.mp4', '*.avi', '*.mov', '*.wmv', '*.flv', '*.mkv', '*.webm',
        '*.m4v', '*.3gp', '*.mpg', '*.mpeg', '*.ts', '*.vob',
        
        # Documents (binary formats)
        '*.doc', '*.docx', '*.xls', '*.xlsx', '*.ppt', '*.pptx',
        '*.odt', '*.ods', '*.odp', '*.rtf',
        
        # Fonts
        '*.ttf', '*.otf', '*.woff', '*.woff2', '*.eot',
        
        # Databases
        '*.db', '*.sqlite', '*.sqlite3', '*.mdb', '*.accdb',
        
        # Data files (binary)
        '*.pkl', '*.pickle', '*.npy', '*.npz', '*.h5', '*.hdf5',
        '*.parquet', '*.feather', '*.arrow', '*.mat',
        
        # Certificates and keys
        '*.pem', '*.key', '*.crt', '*.cer', '*.p12', '*.pfx',
        '*.jks', '*.keystore',
        
        # OS files
        '.DS_Store', 'Thumbs.db', 'desktop.ini', '*.lnk',
        
        # Java/Android binaries
        '*.jar', '*.class', '*.dex', '*.apk', '*.aab', '*.aar',
        
        # Gradle files
        'gradlew', 'gradlew.bat', 'gradle-wrapper.jar',
        
        # iOS/macOS binaries
        '*.ipa', '*.app', '*.dmg',
        
        # .NET binaries
        '*.nupkg', '*.vsix',
        
        # Node.js
        '*.node',
        
        # Python binaries
        '*.pyd', '*.wheel',
        
        # Rust binaries
        '*.rlib',
        
        # Go binaries
        '*.test',
        
        # Other binary formats
        '*.bin', '*.dat', '*.dump', '*.img', '*.iso',
    }
    
    # Project-specific ignore patterns
    PROJECT_SPECIFIC = {
        ProjectType.PYTHON: {
            'dirs': {
                '__pycache__', '*.egg-info', '.pytest_cache', '.mypy_cache',
                '.tox', '.nox', '.coverage', 'htmlcov', '.hypothesis',
                'venv', 'env', '.venv', '.env', 'virtualenv',
                'build', 'dist', 'wheels', '.eggs',
            },
            'files': {
                '*.pyc', '*.pyo', '*.pyd', '.Python',
                '*.so', '*.egg', '*.egg-link',
                '.coverage', '*.cover', '.hypothesis',
                '*.mo', '*.pot',
            }
        },
        ProjectType.JAVASCRIPT: {
            'dirs': {
                'node_modules', 'bower_components', '.npm', '.yarn',
                'dist', 'build', 'out', '.next', '.nuxt',
                'coverage', '.nyc_output',
            },
            'files': {
                'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
                '*.min.js', '*.map',
            }
        },
        ProjectType.JAVA: {
            'dirs': {
                'target', 'build', 'out', 'bin',
                '.gradle', '.m2', '.settings',
            },
            'files': {
                '*.class', '*.jar', '*.war', '*.ear',
                '.classpath', '.project', '.factorypath',
                # XML files are often config files in Java - make optional
            }
        },
        ProjectType.ANDROID: {
            'dirs': {
                'build', '.gradle', '.idea', 'captures',
                '*.iml', 'local.properties', '.externalNativeBuild',
                '.cxx', '*.apk', '*.aab', '*.ap_', '*.dex',
            },
            'files': {
                '*.apk', '*.aab', '*.ap_', '*.dex', '*.so',
                'local.properties', '*.keystore', '*.jks',
                'gradlew', 'gradlew.bat', 'gradle-wrapper.jar',
                'gradle-wrapper.properties',
                # XML files should be excluded by default for Android
                '*.xml',  # Added here for Android projects
            }
        },
        ProjectType.DOTNET: {
            'dirs': {
                'bin', 'obj', 'packages', '.vs',
                'TestResults', '_ReSharper*',
            },
            'files': {
                '*.dll', '*.exe', '*.pdb', '*.user',
                '*.userosscache', '*.sln.docstates',
            }
        },
        ProjectType.GO: {
            'dirs': {
                'vendor', 'bin', 'pkg',
            },
            'files': {
                '*.exe', '*.test', '*.out',
            }
        },
        ProjectType.RUST: {
            'dirs': {
                'target', 'Cargo.lock',
            },
            'files': {
                '*.rs.bk', '*.pdb',
            }
        },
    }
    
    @classmethod
    def get_ignore_patterns(cls, project_type: ProjectType, ignore_xml: bool = False) -> Tuple[Set[str], Set[str]]:
        """Get ignore patterns for a specific project type"""
        dirs = cls.UNIVERSAL_IGNORE_DIRS.copy()
        files = cls.UNIVERSAL_IGNORE_FILES.copy()
        
        # Add XML ignore if requested
        if ignore_xml:
            files.add('*.xml')
        
        if project_type in cls.PROJECT_SPECIFIC:
            specific = cls.PROJECT_SPECIFIC[project_type]
            dirs.update(specific.get('dirs', set()))
            files.update(specific.get('files', set()))
        
        # For JavaScript-based frameworks, include JS patterns
        if project_type in [ProjectType.REACT, ProjectType.VUE, ProjectType.ANGULAR, ProjectType.TYPESCRIPT]:
            js_specific = cls.PROJECT_SPECIFIC[ProjectType.JAVASCRIPT]
            dirs.update(js_specific.get('dirs', set()))
            files.update(js_specific.get('files', set()))
        
        return dirs, files

    @classmethod
    def is_likely_binary(cls, file_path: Path) -> bool:
        """Check if a file is likely binary based on extension"""
        suffix = file_path.suffix.lower()
        binary_extensions = {
            # Extract just the extensions from UNIVERSAL_IGNORE_FILES
            ext for pattern in cls.UNIVERSAL_IGNORE_FILES 
            if pattern.startswith('*.')
            for ext in [pattern[1:]]  # Remove the '*'
        }
        return suffix in binary_extensions

class GitignoreParser:
    """Parse and apply .gitignore rules"""
    
    @staticmethod
    def parse_gitignore(gitignore_path: Path) -> Set[str]:
        """Parse a .gitignore file and return patterns"""
        patterns = set()
        
        if not gitignore_path.exists():
            return patterns
        
        try:
            with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if line and not line.startswith('#'):
                        patterns.add(line)
        except Exception:
            pass
        
        return patterns

class FastFileProcessor:
    """Fast parallel file processing with improved binary detection"""
    
    def __init__(self, config: ScannerConfig):
        self.config = config
        self.processed_files = 0
        self.total_size = 0
        
    def is_binary_file(self, file_path: Path) -> bool:
        """Check if a file is binary using multiple methods"""
        
        # Method 1: Check by extension first (fastest)
        if IgnorePatterns.is_likely_binary(file_path):
            return True
        
        # Method 2: Check file size - very large files are likely binary
        try:
            size = file_path.stat().st_size
            if size > 10 * 1024 * 1024:  # 10MB
                return True
        except:
            return True
            
        # Method 3: Sample-based binary detection (for small files)
        try:
            with open(file_path, 'rb') as f:
                # Read first 8192 bytes
                chunk = f.read(8192)
                if not chunk:
                    return False
                    
                # Check for null bytes (common in binary files)
                if b'\x00' in chunk:
                    return True
                    
                # Check for high percentage of non-printable characters
                printable_chars = sum(1 for byte in chunk if 32 <= byte <= 126 or byte in [9, 10, 13])
                if len(chunk) > 0 and (printable_chars / len(chunk)) < 0.75:
                    return True
                    
        except Exception:
            # If we can't read it, assume it's binary
            return True
            
        return False
        
    def should_ignore(self, path: Path, is_dir: bool = False) -> bool:
        """Check if a path should be ignored"""
        name = path.name
        
        # Check custom ignore patterns first
        if name in self.config.custom_ignore_dirs and is_dir:
            return True
        if name in self.config.custom_ignore_files and not is_dir:
            return True
        
        # Check custom extensions
        if not is_dir and path.suffix.lower() in self.config.custom_ignore_extensions:
            return True
        
        # Check if it's a binary file (not for directories)
        if not is_dir and self.is_binary_file(path):
            return True
        
        # Check directory patterns
        if is_dir:
            for pattern in self.config.ignore_dirs:
                if fnmatch.fnmatch(name, pattern) or name == pattern:
                    return True
        
        # Check file patterns
        for pattern in self.config.ignore_patterns:
            if fnmatch.fnmatch(name, pattern):
                return True
        
        # Check hidden files
        if not self.config.include_hidden and name.startswith('.'):
            return True
        
        return False
    
    def process_file(self, file_path: Path) -> Optional[Dict]:
        """Process a single file with better error handling"""
        try:
            # Check file size first
            size = file_path.stat().st_size
            if size > self.config.max_file_size:
                if self.config.verbose:
                    print(f"Skipping {file_path}: too large ({size/1024:.1f} KB)")
                return None
            
            # Check if binary
            if self.is_binary_file(file_path):
                if self.config.verbose:
                    print(f"Skipping {file_path}: binary file detected")
                return None
            
            # Try to read file
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Additional check for binary content after reading
                    if '\x00' in content:
                        if self.config.verbose:
                            print(f"Skipping {file_path}: null bytes detected")
                        return None
                    
                    lines = content.splitlines()
                    
                    # Truncate if needed
                    if len(lines) > self.config.max_lines_per_file:
                        content = '\n'.join(lines[:self.config.max_lines_per_file])
                        content += f"\n\n# [Truncated at {self.config.max_lines_per_file} lines]"
                    
                    return {
                        'path': file_path,
                        'content': content,
                        'size': size,
                        'lines': len(lines)
                    }
            except UnicodeDecodeError:
                if self.config.verbose:
                    print(f"Skipping {file_path}: encoding error")
                return None
            except Exception as e:
                if self.config.verbose:
                    print(f"Skipping {file_path}: read error - {e}")
                return None
                
        except Exception as e:
            if self.config.verbose:
                print(f"Error processing {file_path}: {e}")
            return None
    
    def scan_directory(self, root_path: Path) -> List[Dict]:
        """Scan directory for files with improved filtering"""
        files_to_process = []
        
        # Collect files
        try:
            for item in root_path.rglob('*'):
                if self.processed_files >= self.config.max_files:
                    break
                    
                if item.is_file():
                    # Check if should ignore
                    should_ignore = False
                    
                    # Check parent directories for ignore patterns
                    for parent in item.parents:
                        if self.should_ignore(parent, is_dir=True):
                            should_ignore = True
                            break
                    
                    if not should_ignore and not self.should_ignore(item):
                        files_to_process.append(item)
        except Exception as e:
            if self.config.verbose:
                print(f"Error scanning directory: {e}")
            return []
        
        # Process files in parallel if enabled
        results = []
        if self.config.parallel_processing:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(self.process_file, f) for f in files_to_process]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        if result:
                            results.append(result)
                            self.processed_files += 1
                            self.total_size += result['size']
                    except Exception as e:
                        if self.config.verbose:
                            print(f"Error in parallel processing: {e}")
        else:
            for file_path in files_to_process:
                try:
                    result = self.process_file(file_path)
                    if result:
                        results.append(result)
                        self.processed_files += 1
                        self.total_size += result['size']
                except Exception as e:
                    if self.config.verbose:
                        print(f"Error processing {file_path}: {e}")
        
        return results

class OutputGenerator:
    """Generate output in different formats"""
    
    @staticmethod
    def generate_txt(project_name: str, files: List[Dict], stats: Dict) -> str:
        """Generate TXT format output"""
        output = []
        output.append(f"Project Snapshot: {project_name}")
        output.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("=" * 60)
        output.append("")
        
        # Directory structure
        output.append("Directory Structure:")
        output.append("-" * 40)
        
        # Create a simple tree structure
        seen_dirs = set()
        for file_info in files:
            path = file_info['path']
            parts = path.relative_to(path.parent.parent).parts if path.parent.parent.exists() else path.parts
            for i in range(len(parts)):
                dir_path = '/'.join(parts[:i+1])
                if dir_path not in seen_dirs:
                    indent = "  " * i
                    is_file = i == len(parts) - 1
                    symbol = "📄" if is_file else "📁"
                    output.append(f"{indent}{symbol} {parts[i]}")
                    seen_dirs.add(dir_path)
        
        output.append("")
        output.append("=" * 60)
        output.append("File Contents:")
        output.append("=" * 60)
        output.append("")
        
        # File contents
        for file_info in files:
            path = file_info['path']
            output.append(f"--- File: {path.name} ---")
            output.append(file_info['content'])
            output.append("")
        
        # Statistics
        output.append("=" * 60)
        output.append("Statistics:")
        output.append(f"- Files processed: {stats['files_processed']}")
        output.append(f"- Total size: {stats['total_size'] / 1024:.2f} KB")
        output.append(f"- Project type: {stats['project_type']}")
        output.append("=" * 60)
        
        return '\n'.join(output)
    
    @staticmethod
    def generate_mcp(project_name: str, files: List[Dict], stats: Dict) -> str:
        """Generate MCP (Markdown Context Pack) format output"""
        output = []
        output.append(f"# {project_name}")
        output.append("")
        output.append(f"Project snapshot generated on {datetime.datetime.now().strftime('%Y-%m-%d')}.")
        output.append("")
        
        # Metadata
        output.append("```mcp-metadata")
        metadata = {
            "date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "num_files": stats['files_processed'],
            "total_size_kb": round(stats['total_size'] / 1024, 2),
            "project_type": stats['project_type'],
            "version": __version__
        }
        output.append(json.dumps(metadata, indent=2))
        output.append("```")
        output.append("")
        
        # Project structure
        output.append("## Project Structure")
        output.append("")
        output.append("```")
        
        # Create tree structure
        seen_dirs = set()
        for file_info in files:
            path = file_info['path']
            parts = path.relative_to(path.parent.parent).parts if path.parent.parent.exists() else path.parts
            for i in range(len(parts)):
                dir_path = '/'.join(parts[:i+1])
                if dir_path not in seen_dirs:
                    indent = "  " * i
                    is_file = i == len(parts) - 1
                    symbol = "" if is_file else "/"
                    output.append(f"{indent}{parts[i]}{symbol}")
                    seen_dirs.add(dir_path)
        
        output.append("```")
        output.append("")
        
        # Files by language
        output.append("## Files")
        output.append("")
        
        # Group files by extension
        files_by_ext = {}
        for file_info in files:
            ext = file_info['path'].suffix or '.txt'
            if ext not in files_by_ext:
                files_by_ext[ext] = []
            files_by_ext[ext].append(file_info)
        
        for ext, ext_files in sorted(files_by_ext.items()):
            lang = ext.lstrip('.') or 'text'
            if lang == 'py':
                lang = 'python'
            output.append(f"### {lang.upper()} Files")
            output.append("")
            
            for file_info in ext_files:
                output.append(f"#### {file_info['path'].name}")
                output.append("")
                output.append(f"```{lang}")
                output.append(file_info['content'])
                output.append("```")
                output.append("")
        
        # Summary
        output.append("## Summary")
        output.append("")
        output.append("### Statistics")
        output.append("")
        output.append(f"- Total files: {stats['files_processed']}")
        output.append(f"- Total size: {stats['total_size'] / 1024:.2f} KB")
        output.append(f"- Project type: {stats['project_type']}")
        output.append("")
        
        return '\n'.join(output)

class InteractiveCLI:
    """Interactive CLI mode with navigation"""
    
    def __init__(self, config: ScannerConfig):
        self.config = config
        self.current_dir = os.getcwd()
        self.scanner = ProjectScanner(config)
        
        # Setup tab completion if available
        if READLINE_AVAILABLE:
            self.setup_tab_completion()
    
    def setup_tab_completion(self):
        """Setup tab completion for paths"""
        def path_completer(text, state):
            # Get the current line
            line = readline.get_line_buffer()
            
            # Check if we're completing a cd command
            if line.startswith('cd '):
                # Get the partial path
                partial = line[3:].strip()
                
                # Get the directory to search
                if os.path.isabs(partial):
                    search_dir = os.path.dirname(partial) or '/'
                    prefix = os.path.basename(partial)
                else:
                    search_dir = self.current_dir
                    prefix = partial
                
                # Find matching directories
                try:
                    items = []
                    for item in os.listdir(search_dir):
                        if item.startswith(prefix) and os.path.isdir(os.path.join(search_dir, item)):
                            items.append(item + '/')
                    
                    if state < len(items):
                        return items[state]
                except:
                    pass
            
            return None
        
        readline.set_completer(path_completer)
        readline.parse_and_bind('tab: complete')
    
    def print_banner(self):
        """Print the interactive mode banner"""
        if COLORS_AVAILABLE:
            print(Fore.BLUE + Style.BRIGHT + ASCII_LOGO)
            print(Style.RESET_ALL)
        else:
            print(ASCII_LOGO)
        print()
    
    def print_help(self):
        """Print help for interactive mode"""
        help_text = f"""
{Fore.CYAN}Commands:{Style.RESET_ALL}
  {Fore.GREEN}ls{Style.RESET_ALL}              - List current directory contents
  {Fore.GREEN}cd <dir>{Style.RESET_ALL}        - Change directory (supports tab completion)
  {Fore.GREEN}cd <number>{Style.RESET_ALL}     - Change to directory by number from list
  {Fore.GREEN}scan [options]{Style.RESET_ALL}  - Generate snapshot with options
  {Fore.GREEN}pwd{Style.RESET_ALL}             - Show current directory path
  {Fore.GREEN}config{Style.RESET_ALL}          - Show current configuration
  {Fore.GREEN}config <key> <value>{Style.RESET_ALL} - Change configuration
  {Fore.GREEN}help{Style.RESET_ALL}            - Show this help message
  {Fore.GREEN}clear{Style.RESET_ALL}           - Clear the screen
  {Fore.GREEN}exit/quit{Style.RESET_ALL}       - Exit the program

{Fore.CYAN}Scan Options:{Style.RESET_ALL}
  {Fore.YELLOW}scan{Style.RESET_ALL}            - Scan with current settings
  {Fore.YELLOW}scan -f mcp{Style.RESET_ALL}     - Scan with MCP format
  {Fore.YELLOW}scan -f txt{Style.RESET_ALL}     - Scan with TXT format
  {Fore.YELLOW}scan -c{Style.RESET_ALL}         - Scan and copy to clipboard
  {Fore.YELLOW}scan -o file.txt{Style.RESET_ALL} - Scan to specific file
  {Fore.YELLOW}scan --no-gitignore{Style.RESET_ALL} - Ignore .gitignore patterns
  {Fore.YELLOW}scan --ignore dir1,file.ext{Style.RESET_ALL} - Ignore custom patterns

{Fore.CYAN}Configuration Keys:{Style.RESET_ALL}
  {Fore.YELLOW}format{Style.RESET_ALL}          - Output format (txt/mcp)
  {Fore.YELLOW}clipboard{Style.RESET_ALL}       - Copy to clipboard (true/false)
  {Fore.YELLOW}max-files{Style.RESET_ALL}       - Maximum files to scan
  {Fore.YELLOW}max-size{Style.RESET_ALL}        - Maximum file size (KB)
"""
        print(help_text)
    
    def list_directory(self):
        """List current directory contents"""
        print(f"\n{Fore.CYAN}Contents of {self.current_dir}:{Style.RESET_ALL}")
        print("-" * 60)
        
        try:
            items = list(Path(self.current_dir).iterdir())
            directories = sorted([item for item in items if item.is_dir()], key=lambda x: x.name.lower())
            files = sorted([item for item in items if item.is_file()], key=lambda x: x.name.lower())
            
            if directories:
                print(f"{Fore.YELLOW}Directories:{Style.RESET_ALL}")
                for i, directory in enumerate(directories, 1):
                    # Check if it's a git repo
                    is_git = (directory / '.git').exists()
                    git_marker = f" {Fore.GREEN}(git){Style.RESET_ALL}" if is_git else ""
                    
                    # Detect project type
                    project_type = ProjectDetector.detect_project_type(directory)
                    type_marker = f" {Fore.MAGENTA}[{project_type.value}]{Style.RESET_ALL}" if project_type != ProjectType.UNKNOWN else ""
                    
                    print(f"  {Fore.CYAN}{i:2d}.{Style.RESET_ALL} 📁 {directory.name}/{git_marker}{type_marker}")
            else:
                print(f"  {Fore.YELLOW}No directories found.{Style.RESET_ALL}")
            
            if files:
                print(f"\n{Fore.YELLOW}Files:{Style.RESET_ALL}")
                for i, file in enumerate(files[:10], len(directories) + 1):  # Show only first 10 files
                    size = file.stat().st_size
                    size_str = f"{size/1024:.1f} KB" if size > 1024 else f"{size} B"
                    print(f"  {Fore.CYAN}{i:2d}.{Style.RESET_ALL} 📄 {file.name} ({size_str})")
                
                if len(files) > 10:
                    print(f"  {Fore.YELLOW}... and {len(files) - 10} more files{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}Error listing directory: {e}{Style.RESET_ALL}")
        
        print("-" * 60)
    
    def change_directory(self, target: str):
        """Change to a new directory"""
        try:
            # Handle numeric selection
            if target.isdigit():
                items = sorted([d for d in Path(self.current_dir).iterdir() if d.is_dir()], 
                              key=lambda x: x.name.lower())
                index = int(target) - 1
                if 0 <= index < len(items):
                    target = str(items[index])
                else:
                    print(f"{Fore.RED}Invalid directory number{Style.RESET_ALL}")
                    return
            
            # Handle special paths
            if target == '~':
                target = str(Path.home())
            elif target == '..':
                target = str(Path(self.current_dir).parent)
            elif not os.path.isabs(target):
                target = str(Path(self.current_dir) / target)
            
            # Change directory
            target_path = Path(target).resolve()
            if target_path.is_dir():
                os.chdir(str(target_path))
                self.current_dir = os.getcwd()
                print(f"{Fore.GREEN}Changed to: {self.current_dir}{Style.RESET_ALL}")
                
                # Auto-detect project type
                project_type = ProjectDetector.detect_project_type(target_path)
                if project_type != ProjectType.UNKNOWN:
                    print(f"{Fore.MAGENTA}Detected project type: {project_type.value}{Style.RESET_ALL}")
                
                # Auto-list after changing
                self.list_directory()
            else:
                print(f"{Fore.RED}Not a valid directory: {target}{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}Error changing directory: {e}{Style.RESET_ALL}")
    
    def show_config(self):
        """Show current configuration"""
        print(f"\n{Fore.CYAN}Current Configuration:{Style.RESET_ALL}")
        print("-" * 40)
        print(f"  Format: {Fore.YELLOW}{self.config.output_format.value}{Style.RESET_ALL}")
        print(f"  Clipboard: {Fore.YELLOW}{self.config.copy_to_clipboard}{Style.RESET_ALL}")
        print(f"  Max files: {Fore.YELLOW}{self.config.max_files}{Style.RESET_ALL}")
        print(f"  Max file size: {Fore.YELLOW}{self.config.max_file_size // 1024} KB{Style.RESET_ALL}")
        print(f"  Max lines per file: {Fore.YELLOW}{self.config.max_lines_per_file}{Style.RESET_ALL}")
        print(f"  Use .gitignore: {Fore.YELLOW}{self.config.use_gitignore}{Style.RESET_ALL}")
        print(f"  Auto-detect project: {Fore.YELLOW}{self.config.auto_detect_project}{Style.RESET_ALL}")
        print(f"  Include hidden files: {Fore.YELLOW}{self.config.include_hidden}{Style.RESET_ALL}")
        print("-" * 40)
    
    def update_config(self, key: str, value: str):
        """Update configuration value"""
        try:
            if key == 'format':
                if value.lower() in ['txt', 'mcp']:
                    self.config.output_format = OutputFormat(value.lower())
                    print(f"{Fore.GREEN}Format set to: {value}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Invalid format. Use 'txt' or 'mcp'{Style.RESET_ALL}")
            
            elif key == 'clipboard':
                if value.lower() in ['true', 'false']:
                    self.config.copy_to_clipboard = value.lower() == 'true'
                    print(f"{Fore.GREEN}Clipboard copy set to: {value}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Invalid value. Use 'true' or 'false'{Style.RESET_ALL}")
            
            elif key == 'max-files':
                self.config.max_files = int(value)
                print(f"{Fore.GREEN}Max files set to: {value}{Style.RESET_ALL}")
            
            elif key == 'max-size':
                self.config.max_file_size = int(value) * 1024
                print(f"{Fore.GREEN}Max file size set to: {value} KB{Style.RESET_ALL}")
            
            elif key == 'max-lines':
                self.config.max_lines_per_file = int(value)
                print(f"{Fore.GREEN}Max lines per file set to: {value}{Style.RESET_ALL}")
            
            else:
                print(f"{Fore.RED}Unknown configuration key: {key}{Style.RESET_ALL}")
                print(f"Available keys: format, clipboard, max-files, max-size, max-lines")
        
        except ValueError:
            print(f"{Fore.RED}Invalid value for {key}{Style.RESET_ALL}")
    
    def scan_current_directory(self, args: List[str] = None):
        """Scan the current directory with optional arguments"""
        # Parse scan arguments
        if args:
            for i, arg in enumerate(args):
                if arg == '-f' and i + 1 < len(args):
                    format_value = args[i + 1]
                    if format_value in ['txt', 'mcp']:
                        self.config.output_format = OutputFormat(format_value)
                elif arg == '-c':
                    self.config.copy_to_clipboard = True
                elif arg == '-o' and i + 1 < len(args):
                    self.config.output_file = args[i + 1]
                elif arg == '--no-gitignore':
                    self.config.use_gitignore = False
                elif arg == '--ignore' and i + 1 < len(args):
                    ignore_items = args[i + 1].split(',')
                    for item in ignore_items:
                        item = item.strip()
                        if '.' in item and not item.startswith('.'):
                            self.config.custom_ignore_extensions.add(item)
                        elif item.endswith('/'):
                            self.config.custom_ignore_dirs.add(item.rstrip('/'))
                        else:
                            self.config.custom_ignore_files.add(item)
        
        # Perform scan
        project_path = Path(self.current_dir)
        output, stats = self.scanner.scan(project_path)
        self.scanner.save_output(output, self.config.output_file)
        
        # Reset temporary flags
        self.config.output_file = None
    
    def run(self):
        """Run the interactive CLI"""
        self.print_banner()
        self.print_help()
        self.list_directory()
        
        while True:
            try:
                # Show prompt with current directory
                prompt = f"\n{Fore.CYAN}[{Path(self.current_dir).name}]{Style.RESET_ALL} {Fore.GREEN}>{Style.RESET_ALL} "
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Parse command
                parts = user_input.split()
                command = parts[0].lower()
                
                # Handle commands
                if command in ['exit', 'quit', 'q']:
                    print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                    break
                
                elif command == 'ls':
                    self.list_directory()
                
                elif command == 'pwd':
                    print(f"{Fore.GREEN}Current directory: {self.current_dir}{Style.RESET_ALL}")
                
                elif command == 'cd' and len(parts) > 1:
                    target = ' '.join(parts[1:])
                    self.change_directory(target)
                
                elif command == 'scan':
                    self.scan_current_directory(parts[1:] if len(parts) > 1 else None)
                
                elif command == 'config':
                    if len(parts) == 1:
                        self.show_config()
                    elif len(parts) >= 3:
                        key = parts[1]
                        value = ' '.join(parts[2:])
                        self.update_config(key, value)
                    else:
                        print(f"{Fore.RED}Usage: config <key> <value>{Style.RESET_ALL}")
                
                elif command == 'help':
                    self.print_help()
                
                elif command == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.print_banner()
                
                else:
                    print(f"{Fore.RED}Unknown command: {command}{Style.RESET_ALL}")
                    print(f"Type 'help' for available commands")
            
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'exit' to quit{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

class ProjectScanner:
    """Main scanner class"""
    
    def __init__(self, config: ScannerConfig):
        self.config = config
        
    def print_banner(self):
        """Print colorful ASCII banner"""
        if COLORS_AVAILABLE:
            print(Fore.BLUE + Style.BRIGHT + ASCII_LOGO)
            print(Style.RESET_ALL)
        else:
            print(ASCII_LOGO)
        print()
    
    def setup_ignore_patterns(self, project_path: Path, project_type: ProjectType):
        """Setup ignore patterns based on project type and gitignore"""
        # Ask about XML files for certain project types
        ignore_xml = False
        if not self.config.interactive_mode:
            ignore_xml = ProjectDetector.should_ignore_xml(project_type)
        
        # Get project-specific patterns
        dirs, files = IgnorePatterns.get_ignore_patterns(project_type, ignore_xml)
        self.config.ignore_dirs.update(dirs)
        self.config.ignore_patterns.update(files)
        
        # Parse .gitignore if enabled
        if self.config.use_gitignore:
            gitignore_path = project_path / '.gitignore'
            gitignore_patterns = GitignoreParser.parse_gitignore(gitignore_path)
            self.config.ignore_patterns.update(gitignore_patterns)
    
    def scan(self, path: Path) -> Tuple[str, Dict]:
        """Scan a project directory"""
        start_time = time.time()
        
        # Detect project type
        project_type = ProjectType.UNKNOWN
        if self.config.auto_detect_project:
            project_type = ProjectDetector.detect_project_type(path)
            if self.config.verbose or self.config.interactive_mode:
                print(f"{Fore.GREEN}✓ Detected project type: {project_type.value}{Style.RESET_ALL}")
        
        # Setup ignore patterns
        self.setup_ignore_patterns(path, project_type)
        
        # Process files
        processor = FastFileProcessor(self.config)
        if self.config.show_progress:
            print(f"{Fore.YELLOW}⏳ Scanning directory...{Style.RESET_ALL}")
        
        files = processor.scan_directory(path)
        
        # Generate statistics
        stats = {
            'files_processed': processor.processed_files,
            'total_size': processor.total_size,
            'project_type': project_type.value,
            'scan_time': time.time() - start_time
        }
        
        # Generate output
        project_name = path.name
        if self.config.output_format == OutputFormat.MCP:
            output = OutputGenerator.generate_mcp(project_name, files, stats)
        else:
            output = OutputGenerator.generate_txt(project_name, files, stats)
        
        if self.config.show_progress:
            print(f"{Fore.GREEN}✓ Scan complete in {stats['scan_time']:.2f}s{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  📁 Files processed: {stats['files_processed']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  💾 Total size: {stats['total_size'] / 1024:.2f} KB{Style.RESET_ALL}")
        
        return output, stats
    
    def save_output(self, output: str, output_file: Optional[str] = None):
        """Save output to file and/or clipboard"""
        
        # Determine output filename
        if not output_file:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            ext = self.config.output_format.value
            output_file = f"project_snapshot_{timestamp}.{ext}"
        
        # Save to file
        output_path = Path(output_file)
        output_path.write_text(output, encoding='utf-8')
        print(f"{Fore.GREEN}✓ Output saved to: {output_path.absolute()}{Style.RESET_ALL}")
        
        # Copy to clipboard if requested
        if self.config.copy_to_clipboard:
            if CLIPBOARD_AVAILABLE:
                try:
                    success = copy_to_clipboard(output)
                    if success:
                        print(f"{Fore.GREEN}✓ Output copied to clipboard{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}⚠ Could not copy to clipboard{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠ Could not copy to clipboard: {e}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠ Clipboard functionality not available{Style.RESET_ALL}")
                system = platform.system()
                if system == "Linux":
                    print(f"{Fore.CYAN}Install clipboard support: sudo apt install xclip{Style.RESET_ALL}")
                elif system == "Windows":
                    print(f"{Fore.CYAN}Install clipboard support: pip install pyperclip{Style.RESET_ALL}")

def parse_ignore_argument(ignore_arg: str, config: ScannerConfig):
    """Parse the --ignore argument and update config"""
    items = ignore_arg.split(',')
    for item in items:
        item = item.strip()
        if item.startswith('.') and len(item) > 1:  # File extension
            config.custom_ignore_extensions.add(item)
        elif item.endswith('/'):  # Directory
            config.custom_ignore_dirs.add(item.rstrip('/'))
        elif '.' in item and not item.startswith('.'):  # File with extension
            config.custom_ignore_extensions.add('.' + item.split('.')[-1])
        else:  # File or directory name
            config.custom_ignore_files.add(item)
            config.custom_ignore_dirs.add(item)

def install_clipboard_dependencies():
    """Install clipboard dependencies based on OS"""
    system = platform.system()
    
    if system == "Linux":
        print(f"{Fore.YELLOW}Installing clipboard support for Linux...{Style.RESET_ALL}")
        try:
            # Try to install xclip
            subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'xclip'], check=True, capture_output=True)
            print(f"{Fore.GREEN}✓ xclip installed successfully{Style.RESET_ALL}")
            return True
        except:
            try:
                # Fallback to pip
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyperclip'], check=True)
                print(f"{Fore.GREEN}✓ pyperclip installed successfully{Style.RESET_ALL}")
                return True
            except:
                print(f"{Fore.RED}✗ Could not install clipboard support{Style.RESET_ALL}")
                return False
    
    elif system == "Windows":
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyperclip'], check=True)
            print(f"{Fore.GREEN}✓ pyperclip installed successfully{Style.RESET_ALL}")
            return True
        except:
            print(f"{Fore.RED}✗ Could not install clipboard support{Style.RESET_ALL}")
            return False
    
    else:  # macOS
        print(f"{Fore.GREEN}✓ Clipboard support is built-in on macOS{Style.RESET_ALL}")
        return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='CodePrint - AI-ready project snapshots',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  codeprint                          # Scan current directory
  codeprint /path/to/project         # Scan specific directory
  codeprint -f mcp -c                # MCP format + clipboard
  codeprint --ignore "*.log,temp/"   # Ignore logs and temp directory
  codeprint --setup                  # Run setup configuration
  codeprint -i                       # Interactive mode
        """
    )
    
    parser.add_argument('path', nargs='?', default='.', help='Path to scan (default: current directory)')
    parser.add_argument('-f', '--format', choices=['txt', 'mcp'], help='Output format')
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('-c', '--clipboard', action='store_true', help='Copy to clipboard')
    parser.add_argument('--max-file-size', type=int, help='Maximum file size in KB')
    parser.add_argument('--max-files', type=int, help='Maximum number of files')
    parser.add_argument('--max-lines', type=int, help='Maximum lines per file')
    parser.add_argument('--include-hidden', action='store_true', help='Include hidden files')
    parser.add_argument('--no-gitignore', action='store_true', help='Ignore .gitignore patterns')
    parser.add_argument('--no-auto-detect', action='store_true', help='Disable project type detection')
    parser.add_argument('--no-progress', action='store_true', help='Disable progress output')
    parser.add_argument('--no-parallel', action='store_true', help='Disable parallel processing')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--setup', action='store_true', help='Run setup configuration')
    parser.add_argument('--ignore', help='Comma-separated list of files/dirs/extensions to ignore')
    parser.add_argument('--install-clipboard', action='store_true', help='Install clipboard dependencies')
    
    args = parser.parse_args()
    
    # Handle special commands
    if args.install_clipboard:
        install_clipboard_dependencies()
        return
    
    if args.setup:
        setup_config_interactive()
        return
    
    # Load configuration
    config = load_user_config()
    
    # Override with command line arguments
    if args.format:
        config.output_format = OutputFormat(args.format)
    if args.clipboard:
        config.copy_to_clipboard = True
    if args.output:
        config.output_file = args.output
    if args.max_file_size:
        config.max_file_size = args.max_file_size * 1024
    if args.max_files:
        config.max_files = args.max_files
    if args.max_lines:
        config.max_lines_per_file = args.max_lines
    if args.include_hidden:
        config.include_hidden = True
    if args.no_gitignore:
        config.use_gitignore = False
    if args.no_auto_detect:
        config.auto_detect_project = False
    if args.no_progress:
        config.show_progress = False
    if args.no_parallel:
        config.parallel_processing = False
    if args.verbose:
        config.verbose = True
    if args.interactive:
        config.interactive_mode = True
    if args.ignore:
        parse_ignore_argument(args.ignore, config)
    
    # Interactive mode
    if args.interactive:
        cli = InteractiveCLI(config)
        cli.run()
        return
    
    # Create scanner
    scanner = ProjectScanner(config)
    
    # Show banner if not in quiet mode
    if config.show_progress and not args.no_progress:
        scanner.print_banner()
    
    # Scan project
    try:
        project_path = Path(args.path).resolve()
        if not project_path.exists():
            print(f"{Fore.RED}Error: Path does not exist: {args.path}{Style.RESET_ALL}")
            sys.exit(1)
        
        if not project_path.is_dir():
            print(f"{Fore.RED}Error: Path is not a directory: {args.path}{Style.RESET_ALL}")
            sys.exit(1)
        
        output, stats = scanner.scan(project_path)
        scanner.save_output(output, config.output_file)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Scan interrupted{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        if config.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()