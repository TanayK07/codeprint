import pytest
from cli import IgnorePatterns, GitignoreParser
from cli import ProjectType
from pathlib import Path
import tempfile


class TestIgnorePatterns:
    """Test suite for IgnorePatterns"""
    
    def test_get_python_patterns(self):
        """Test Python-specific ignore patterns"""
        dirs, files = IgnorePatterns.get_ignore_patterns(ProjectType.PYTHON)
        
        assert '__pycache__' in dirs
        assert 'venv' in dirs
        assert '*.pyc' in files
        assert '*.pyo' in files
    
    def test_get_javascript_patterns(self):
        """Test JavaScript-specific ignore patterns"""
        dirs, files = IgnorePatterns.get_ignore_patterns(ProjectType.JAVASCRIPT)
        
        assert 'node_modules' in dirs
        assert 'dist' in dirs
        assert '*.min.js' in files
    
    def test_universal_patterns_included(self):
        """Test that universal patterns are always included"""
        dirs, files = IgnorePatterns.get_ignore_patterns(ProjectType.UNKNOWN)
        
        # Check universal dirs
        assert '.git' in dirs
        assert '.vscode' in dirs
        
        # Check universal files
        assert '*.exe' in files
        assert '*.jpg' in files
        assert '*.db' in files
        assert '*.pkl' in files

class TestGitignoreParser:
    """Test suite for GitignoreParser"""
    
    def test_parse_gitignore(self):
        """Test parsing .gitignore file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.gitignore', delete=False) as f:
            f.write("# Comment\n")
            f.write("*.pyc\n")
            f.write("__pycache__/\n")
            f.write("\n")  # Empty line
            f.write("dist/\n")
            f.name
            
        gitignore_path = Path(f.name)
        patterns = GitignoreParser.parse_gitignore(gitignore_path)
        
        assert '*.pyc' in patterns
        assert '__pycache__/' in patterns
        assert 'dist/' in patterns
        assert '# Comment' not in patterns  # Comments should be excluded
        
        gitignore_path.unlink()
    
    def test_parse_nonexistent_gitignore(self):
        """Test parsing non-existent .gitignore file"""
        patterns = GitignoreParser.parse_gitignore(Path('/nonexistent/.gitignore'))
        assert patterns == set()