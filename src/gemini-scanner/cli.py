#!/usr/bin/env python3
"""
Project Scanner - Enhanced Cross-Platform Edition
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

# Version
__version__ = "2.0.0"

# ASCII Art Logo
ASCII_LOGO = """
╔═══════════════════════════════════════════════════════════════╗
║  ██████╗ ███████╗███╗   ███╗██╗███╗   ██╗██╗                ║
║ ██╔════╝ ██╔════╝████╗ ████║██║████╗  ██║██║                ║
║ ██║  ███╗█████╗  ██╔████╔██║██║██╔██╗ ██║██║                ║
║ ██║   ██║██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║                ║
║ ╚██████╔╝███████╗██║ ╚═╝ ██║██║██║ ╚████║██║                ║
║  ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝                ║
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

class ProjectDetector:
    """Detects project type based on files present"""
    
    @staticmethod
    def detect_project_type(path: Path) -> ProjectType:
        """Detect the project type based on characteristic files"""
        
        # Check for specific project files
        checks = [
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
            print(Fore.WHITE + Style.BRIGHT + "  Project Scanner for Prompt Engineering v" + __version__)
            print(Fore.CYAN + "  📋 Creating AI-ready snapshots of your codebase")
            print(Style.RESET_ALL)
        else:
            print(ASCII_LOGO)
            print(f"  Project Scanner v{__version__}")
            print("  Creating AI-ready snapshots of your codebase")
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
            if self.config.verbose:
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
        description="Project Scanner - Create AI-ready project snapshots",
        formatter_class=argparse.RawDescriptionHelpFormatter
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
        '-p', '--path',
        default='.',
        help='Path to scan (default: current directory)'
    )
    
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
        verbose=args.verbose
    )
    
    # Create scanner
    scanner = ProjectScanner(config)
    
    # Print banner
    scanner.print_banner()
    
    # Scan project
    try:
        project_path = Path(args.path).resolve()
        if not project_path.exists():
            print(f"{Fore.RED}✗ Path does not exist: {project_path}{Style.RESET_ALL}")
            sys.exit(1)
        
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
    