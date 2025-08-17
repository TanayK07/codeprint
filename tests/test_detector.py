
# tests/test_detector.py
import pytest
from pathlib import Path
import tempfile
import shutil

import sys
sys.path.insert(0, 'src/codeprint')
from cli import ProjectDetector, ProjectType

class TestProjectDetector:
    """Test suite for ProjectDetector"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_detect_python_project(self, temp_dir):
        """Test Python project detection"""
        (temp_dir / "requirements.txt").touch()
        assert ProjectDetector.detect_project_type(temp_dir) == ProjectType.PYTHON
        
        # Test with setup.py
        (temp_dir / "requirements.txt").unlink()
        (temp_dir / "setup.py").touch()
        assert ProjectDetector.detect_project_type(temp_dir) == ProjectType.PYTHON
    
    def test_detect_javascript_project(self, temp_dir):
        """Test JavaScript project detection"""
        (temp_dir / "package.json").touch()
        assert ProjectDetector.detect_project_type(temp_dir) == ProjectType.JAVASCRIPT
    
    def test_detect_typescript_project(self, temp_dir):
        """Test TypeScript project detection"""
        (temp_dir / "tsconfig.json").touch()
        assert ProjectDetector.detect_project_type(temp_dir) == ProjectType.TYPESCRIPT
    
    def test_detect_java_project(self, temp_dir):
        """Test Java project detection"""
        (temp_dir / "pom.xml").touch()
        assert ProjectDetector.detect_project_type(temp_dir) == ProjectType.JAVA
        
        # Test with build.gradle
        (temp_dir / "pom.xml").unlink()
        (temp_dir / "build.gradle").touch()
        result = ProjectDetector.detect_project_type(temp_dir)
        assert result in [ProjectType.JAVA, ProjectType.ANDROID] 
           
    def test_detect_android_project(self, temp_dir):
        """Test Android project detection"""
        (temp_dir / "AndroidManifest.xml").touch()
        assert ProjectDetector.detect_project_type(temp_dir) == ProjectType.ANDROID
    
    def test_detect_go_project(self, temp_dir):
        """Test Go project detection"""
        (temp_dir / "go.mod").touch()
        assert ProjectDetector.detect_project_type(temp_dir) == ProjectType.GO
    
    def test_detect_rust_project(self, temp_dir):
        """Test Rust project detection"""
        (temp_dir / "Cargo.toml").touch()
        assert ProjectDetector.detect_project_type(temp_dir) == ProjectType.RUST
    
    def test_detect_unknown_project(self, temp_dir):
        """Test unknown project type"""
        (temp_dir / "random.txt").touch()
        assert ProjectDetector.detect_project_type(temp_dir) == ProjectType.UNKNOWN
        