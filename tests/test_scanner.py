import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

from gemini_scanner.scanner import ProjectScanner
from gemini_scanner.cli import ScannerConfig, OutputFormat

class TestProjectScanner:
    """Test suite for ProjectScanner"""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        
        # Create sample project structure
        Path(temp_dir, "src").mkdir()
        Path(temp_dir, "src", "main.py").write_text("def main():\n    print('Hello')")
        Path(temp_dir, "src", "utils.py").write_text("def helper():\n    pass")
        Path(temp_dir, "README.md").write_text("# Test Project")
        Path(temp_dir, "requirements.txt").write_text("pytest>=7.0.0")
        Path(temp_dir, ".gitignore").write_text("*.pyc\n__pycache__/")
        
        # Create some files to ignore
        Path(temp_dir, "build").mkdir()
        Path(temp_dir, "build", "output.exe").write_bytes(b"binary")
        Path(temp_dir, "__pycache__").mkdir()
        Path(temp_dir, "__pycache__", "cache.pyc").write_bytes(b"cache")
        
        yield Path(temp_dir)
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def scanner_config(self):
        """Create a default scanner configuration"""
        return ScannerConfig(
            output_format=OutputFormat.TXT,
            copy_to_clipboard=False,
            max_file_size=1024 * 1024,
            max_files=100,
            use_gitignore=True,
            auto_detect_project=True,
            show_progress=False,
            parallel_processing=False
        )
    
    def test_scanner_initialization(self, scanner_config):
        """Test scanner initialization"""
        scanner = ProjectScanner(scanner_config)
        assert scanner.config == scanner_config
    
    def test_scan_project(self, temp_project, scanner_config):
        """Test scanning a project"""
        scanner = ProjectScanner(scanner_config)
        output, stats = scanner.scan(temp_project)
        
        assert output is not None
        assert stats['files_processed'] > 0
        assert stats['project_type'] == 'python'
        assert 'main.py' in output
        assert 'utils.py' in output
        assert 'README.md' in output
    
    def test_ignore_patterns(self, temp_project, scanner_config):
        """Test that ignore patterns work correctly"""
        scanner = ProjectScanner(scanner_config)
        output, stats = scanner.scan(temp_project)
        
        # Check that ignored files are not in output
        assert 'output.exe' not in output
        assert 'cache.pyc' not in output
        assert '__pycache__' not in output
    
    def test_output_formats(self, temp_project, scanner_config):
        """Test different output formats"""
        # Test TXT format
        scanner_config.output_format = OutputFormat.TXT
        scanner = ProjectScanner(scanner_config)
        txt_output, _ = scanner.scan(temp_project)
        assert "Project Snapshot" in txt_output
        assert "File Contents:" in txt_output
        
        # Test MCP format
        scanner_config.output_format = OutputFormat.MCP
        scanner = ProjectScanner(scanner_config)
        mcp_output, _ = scanner.scan(temp_project)
        assert "# Test Project" in mcp_output or "# temp" in mcp_output
        assert "```mcp-metadata" in mcp_output
        assert "## Project Structure" in mcp_output
    
    @patch('pyperclip.copy')
    def test_clipboard_copy(self, mock_copy, temp_project, scanner_config):
        """Test clipboard functionality"""
        scanner_config.copy_to_clipboard = True
        scanner = ProjectScanner(scanner_config)
        output, _ = scanner.scan(temp_project)
        
        # Save output should trigger clipboard copy
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            scanner.save_output(output, f.name)
        
        # Check that pyperclip.copy was called
        mock_copy.assert_called_once_with(output)
    
    def test_max_file_size_limit(self, temp_project, scanner_config):
        """Test max file size limit"""
        # Create a large file
        large_file = temp_project / "large.txt"
        large_file.write_text("x" * (2 * 1024 * 1024))  # 2MB file
        
        scanner_config.max_file_size = 1024 * 1024  # 1MB limit
        scanner = ProjectScanner(scanner_config)
        output, stats = scanner.scan(temp_project)
        
        # Large file should not be included
        assert "large.txt" not in output
    
    def test_max_files_limit(self, temp_project, scanner_config):
        """Test max files limit"""
        # Create many files
        for i in range(10):
            Path(temp_project, f"file{i}.txt").write_text(f"content {i}")
        
        scanner_config.max_files = 5
        scanner = ProjectScanner(scanner_config)
        output, stats = scanner.scan(temp_project)
        
        assert stats['files_processed'] <= 5

