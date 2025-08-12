import pytest
from gemini_scanner.output import OutputGenerator
from pathlib import Path

class TestOutputGenerator:
    """Test suite for OutputGenerator"""
    
    @pytest.fixture
    def sample_files(self):
        """Create sample file data"""
        return [
            {
                'path': Path('src/main.py'),
                'content': 'def main():\n    print("Hello")',
                'size': 32,
                'lines': 2
            },
            {
                'path': Path('README.md'),
                'content': '# Test Project',
                'size': 14,
                'lines': 1
            }
        ]
    
    @pytest.fixture
    def sample_stats(self):
        """Create sample statistics"""
        return {
            'files_processed': 2,
            'total_size': 46,
            'project_type': 'python',
            'scan_time': 1.5
        }
    
    def test_generate_txt_output(self, sample_files, sample_stats):
        """Test TXT format generation"""
        output = OutputGenerator.generate_txt('TestProject', sample_files, sample_stats)
        
        assert 'Project Snapshot: TestProject' in output
        assert 'Directory Structure:' in output
        assert 'File Contents:' in output
        assert 'main.py' in output
        assert 'README.md' in output
        assert 'def main():' in output
        assert '# Test Project' in output
        assert 'Statistics:' in output
        assert 'Files processed: 2' in output
    
    def test_generate_mcp_output(self, sample_files, sample_stats):
        """Test MCP format generation"""
        output = OutputGenerator.generate_mcp('TestProject', sample_files, sample_stats)
        
        assert '# TestProject' in output
        assert '```mcp-metadata' in output
        assert '"num_files": 2' in output
        assert '## Project Structure' in output
        assert '## Files' in output
        assert '```python' in output
        assert 'def main():' in output
        assert '## Summary' in output
