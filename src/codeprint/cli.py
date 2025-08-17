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
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

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
__version__ = "1.0.0"

# ASCII Art Logo
ASCII_LOGO = """
╔═══════════════════════════════════════════════════════════════╗
║   ██████╗ ██████╗ ██████╗ ███████╗                          ║
║  ██╔════╝██╔═══██╗██╔══██╗██╔════╝                          ║
║  ██║     ██║   ██║██║  ██║█████╗                            ║
║  ██║     ██║   ██║██║  ██║██╔══╝                            ║
║  ╚██████╗╚██████╔╝██████╔╝███████╗                          ║
║   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝                          ║
║  ██████╗ ██████╗ ██╗███╗   ██╗████████╗                     ║
║  ██╔══██╗██╔══██╗██║████╗  ██║██║████╗  ██║   ██║           ║
║  ██████╔╝██████╔╝██║██╔██╗ ██║   ██║                        ║
║  ██╔═══╝ ██╔══██╗██║██║╚██╗██║   ██║                        ║
║  ██║     ██║  ██║██║██║ ╚████║   ██║                        ║
║  ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝                        ║
╚═══════════════════════════════════════════════════════════════╝
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

class ProjectDetector:
    """Detects project type based on files present"""
    
    @staticmethod
    def detect_project_type(path: Path) -> ProjectType:
        """Detect the project type based on characteristic files"""
        
        # Check for specific project files
        checks = [
             # Java BEFORE Android (so build.gradle is detected as Java first)
            (['pom.xml', 'build.gradle'], ProjectType.JAVA),
            # Android
            (['build.gradle', 'AndroidManifest.xml', 'gradle.properties'], ProjectType.ANDROID),
            # iOS
            (['Podfile', '*.xcodeproj', '*.xcworkspace'], ProjectType.IOS),
            # Flutter
            (['pubspec.yaml', 'lib/main.dart'], ProjectType.FLUTTER),
            # Python
            (['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'], ProjectType.PYTHON),
            # Node.js/JavaScript
            (['package.json'], ProjectType.JAVASCRIPT),
            # TypeScript
            (['tsconfig.json'], ProjectType.TYPESCRIPT),
            # React
            (['package.json', 'src/App.js', 'src/App.jsx', 'src/App.tsx'], ProjectType.REACT),
            # Vue
            (['vue.config.js', 'nuxt.config.js'], ProjectType.VUE),
            # Angular
            (['angular.json', '.angular-cli.json'], ProjectType.ANGULAR),
            # Java
            (['pom.xml', 'build.gradle'], ProjectType.JAVA),
            # .NET
            (['*.csproj', '*.sln', '*.vbproj', '*.fsproj'], ProjectType.DOTNET),
            # Go
            (['go.mod', 'go.sum'], ProjectType.GO),
            # Rust
            (['Cargo.toml', 'Cargo.lock'], ProjectType.RUST),
            # C++
            (['CMakeLists.txt', 'Makefile', '*.cpp'], ProjectType.CPP),
            # Ruby
            (['Gemfile', 'Rakefile'], ProjectType.RUBY),
            # PHP
            (['composer.json', 'composer.lock'], ProjectType.PHP),
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

class IgnorePatterns:
    """Manages ignore patterns for different project types"""
    
    # Universal ignore patterns
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
        # Binary files
        '*.exe', '*.dll', '*.so', '*.dylib', '*.a', '*.lib',
        '*.o', '*.obj', '*.pdb', '*.idb',
        # Archives
        '*.zip', '*.tar', '*.gz', '*.bz2', '*.7z', '*.rar',
        # Media
        '*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.ico', '*.svg',
        '*.mp3', '*.mp4', '*.avi', '*.mov', '*.wmv', '*.flv',
        '*.wav', '*.flac', '*.ogg',
        # Documents
        '*.pdf', '*.doc', '*.docx', '*.xls', '*.xlsx', '*.ppt', '*.pptx',
        # Databases
        '*.db', '*.sqlite', '*.sqlite3', '*.mdb', '*.accdb',
        # Data files
        '*.pkl', '*.pickle', '*.npy', '*.npz', '*.h5', '*.hdf5',
        '*.parquet', '*.feather', '*.arrow',
        # Certificates and keys
        '*.pem', '*.key', '*.crt', '*.cer', '*.p12', '*.pfx',
        # OS files
        '.DS_Store', 'Thumbs.db', 'desktop.ini', '*.lnk',
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
    def get_ignore_patterns(cls, project_type: ProjectType) -> Tuple[Set[str], Set[str]]:
        """Get ignore patterns for a specific project type"""
        dirs = cls.UNIVERSAL_IGNORE_DIRS.copy()
        files = cls.UNIVERSAL_IGNORE_FILES.copy()
        
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
    """Fast parallel file processing"""
    
    def __init__(self, config: ScannerConfig):
        self.config = config
        self.processed_files = 0
        self.total_size = 0
        
    def should_ignore(self, path: Path, is_dir: bool = False) -> bool:
        """Check if a path should be ignored"""
        name = path.name
        
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
        """Process a single file"""
        try:
            # Check file size
            size = file_path.stat().st_size
            if size > self.config.max_file_size:
                return None
            
            # Try to read file
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
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
            except Exception:
                return None
                
        except Exception:
            return None
    
    def scan_directory(self, root_path: Path) -> List[Dict]:
        """Scan directory for files"""
        files_to_process = []
        
        # Collect files
        for item in root_path.rglob('*'):
            if self.processed_files >= self.config.max_files:
                break
                
            if item.is_file():
                # Check if should ignore
                should_ignore = False
                for parent in item.parents:
                    if self.should_ignore(parent, is_dir=True):
                        should_ignore = True
                        break
                
                if not should_ignore and not self.should_ignore(item):
                    files_to_process.append(item)
        
        # Process files in parallel if enabled
        results = []
        if self.config.parallel_processing:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(self.process_file, f) for f in files_to_process]
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        results.append(result)
                        self.processed_files += 1
                        self.total_size += result['size']
        else:
            for file_path in files_to_process:
                result = self.process_file(file_path)
                if result:
                    results.append(result)
                    self.processed_files += 1
                    self.total_size += result['size']
        
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
            lines = ASCII_LOGO.split('\n')
            colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA]
            for i, line in enumerate(lines):
                color = colors[i % len(colors)]
                print(color + Style.BRIGHT + line)
            
            print(Fore.WHITE + Style.BRIGHT + f"  CodePrint v{__version__} - Interactive Mode")
            print(Fore.CYAN + "  📋 Navigate and scan any project directory")
            print(Style.RESET_ALL)
        else:
            print(ASCII_LOGO)
            print(f"  CodePrint v{__version__} - Interactive Mode")
            print("  Navigate and scan any project directory")
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
            # Gradient effect for the banner
            lines = ASCII_LOGO.split('\n')
            colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA]
            for i, line in enumerate(lines):
                color = colors[i % len(colors)]
                print(color + Style.BRIGHT + line)
            
            # Print info
            print(Fore.WHITE + Style.BRIGHT + "  AI-Ready Code Snapshots v" + __version__)
            print(Fore.CYAN + "  📋 Transform code into AI-ready snapshots")
            print(Style.RESET_ALL)
        else:
            print(ASCII_LOGO)
            print(f"  Project Scanner v{__version__}")
            print("  Transform code into AI-ready snapshots")
        print()
    
    def setup_ignore_patterns(self, project_path: Path, project_type: ProjectType):
        """Setup ignore patterns based on project type and gitignore"""
        # Get project-specific patterns
        dirs, files = IgnorePatterns.get_ignore_patterns(project_type)
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
                    pyperclip.copy(output)
                    print(f"{Fore.GREEN}✓ Output copied to clipboard{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠ Could not copy to clipboard: {e}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠ Clipboard functionality not available (install pyperclip){Style.RESET_ALL}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="CodePrint - Create AI-ready project snapshots",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  codeprint                    # Start interactive mode
  codeprint -i                 # Explicitly start interactive mode
  codeprint .                  # Scan current directory
  codeprint /path/to/project   # Scan specific directory
  codeprint -f mcp -c          # Scan with MCP format and copy to clipboard
  codeprint --help             # Show all options
        """
    )
    
    # Add interactive mode flag
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Start in interactive mode with directory navigation'
    )
    
    # Path argument (optional)
    parser.add_argument(
        'path',
        nargs='?',
        default=None,
        help='Path to scan (if not provided, starts interactive mode)'
    )
    
    # Output format options
    parser.add_argument(
        '-f', '--format',
        choices=['txt', 'mcp'],
        default='txt',
        help='Output format (default: txt)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file name'
    )
    
    parser.add_argument(
        '-c', '--clipboard',
        action='store_true',
        help='Copy output to clipboard'
    )
    
    # Scan options
    parser.add_argument(
        '--no-gitignore',
        action='store_true',
        help='Do not use .gitignore patterns'
    )
    
    parser.add_argument(
        '--no-auto-detect',
        action='store_true',
        help='Do not auto-detect project type'
    )
    
    parser.add_argument(
        '--include-hidden',
        action='store_true',
        help='Include hidden files'
    )
    
    # Limits
    parser.add_argument(
        '--max-file-size',
        type=int,
        default=1024,
        help='Maximum file size in KB (default: 1024)'
    )
    
    parser.add_argument(
        '--max-files',
        type=int,
        default=500,
        help='Maximum number of files (default: 500)'
    )
    
    parser.add_argument(
        '--max-lines',
        type=int,
        default=1000,
        help='Maximum lines per file (default: 1000)'
    )
    
    # Other options
    parser.add_argument(
        '--no-progress',
        action='store_true',
        help='Disable progress output'
    )
    
    parser.add_argument(
        '--no-parallel',
        action='store_true',
        help='Disable parallel processing'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    args = parser.parse_args()
    
    # Create configuration
    config = ScannerConfig(
        output_format=OutputFormat(args.format),
        copy_to_clipboard=args.clipboard,
        output_file=args.output,
        max_file_size=args.max_file_size * 1024,
        max_files=args.max_files,
        max_lines_per_file=args.max_lines,
        use_gitignore=not args.no_gitignore,
        auto_detect_project=not args.no_auto_detect,
        show_progress=not args.no_progress,
        parallel_processing=not args.no_parallel,
        include_hidden=args.include_hidden,
        verbose=args.verbose,
        interactive_mode=args.interactive or (args.path is None)
    )
    
    # Check if we should start interactive mode
    if config.interactive_mode:
        # Start interactive CLI
        interactive_cli = InteractiveCLI(config)
        interactive_cli.run()
    else:
        # Direct scan mode
        scanner = ProjectScanner(config)
        scanner.print_banner()
        
        # Determine path to scan
        if args.path:
            if args.path == '.':
                project_path = Path.cwd()
            else:
                project_path = Path(args.path).resolve()
        else:
            project_path = Path.cwd()
        
        if not project_path.exists():
            print(f"{Fore.RED}✗ Path does not exist: {project_path}{Style.RESET_ALL}")
            sys.exit(1)
        
        try:
            output, stats = scanner.scan(project_path)
            scanner.save_output(output, config.output_file)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠ Scan interrupted by user{Style.RESET_ALL}")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
            if config.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    main()
    