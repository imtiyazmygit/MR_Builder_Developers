"""
Unit tests for MRBuilder class
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mr_builder import MRBuilder


class TestMRBuilder(unittest.TestCase):
    """Test cases for MRBuilder class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.builder = MRBuilder()
    
    def test_generate_mr_description_basic(self):
        """Test basic MR description generation."""
        description = self.builder.generate_mr_description(
            title="Test MR",
            changes=["Change 1", "Change 2"]
        )
        
        self.assertIn("Test MR", description)
        self.assertIn("Change 1", description)
        self.assertIn("Change 2", description)
        self.assertIn("## Changes", description)
    
    def test_generate_mr_description_with_issues(self):
        """Test MR description with issue references."""
        description = self.builder.generate_mr_description(
            title="Test MR",
            changes=["Change 1"],
            issue_refs=["#123", "#456"]
        )
        
        self.assertIn("## Related Issues", description)
        self.assertIn("#123", description)
        self.assertIn("#456", description)
    
    def test_validate_mr_requirements(self):
        """Test MR validation."""
        validations = self.builder.validate_mr_requirements()
        
        self.assertIsInstance(validations, dict)
        self.assertIn('has_description', validations)
        self.assertIn('has_tests', validations)
        self.assertIn('no_merge_conflicts', validations)
    
    def test_suggest_reviewers(self):
        """Test reviewer suggestions."""
        files = ["src/test.py", "docs/README.md", "src/app.js"]
        reviewers = self.builder.suggest_reviewers(files)
        
        self.assertIsInstance(reviewers, list)
        self.assertIn("python-team", reviewers)
        self.assertIn("docs-team", reviewers)
        self.assertIn("frontend-team", reviewers)
    
    def test_get_mr_checklist(self):
        """Test checklist generation."""
        checklist = self.builder.get_mr_checklist()
        
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 0)
        self.assertTrue(all(isinstance(item, str) for item in checklist))
    
    def test_format_checklist(self):
        """Test checklist formatting."""
        items = ["Item 1", "Item 2", "Item 3"]
        checked = [True, False, True]
        
        formatted = self.builder.format_checklist(items, checked)
        
        self.assertIn("- [x] Item 1", formatted)
        self.assertIn("- [ ] Item 2", formatted)
        self.assertIn("- [x] Item 3", formatted)
    
    def test_format_checklist_default_unchecked(self):
        """Test checklist formatting with default unchecked state."""
        items = ["Item 1", "Item 2"]
        formatted = self.builder.format_checklist(items)
        
        self.assertIn("- [ ] Item 1", formatted)
        self.assertIn("- [ ] Item 2", formatted)


if __name__ == '__main__':
    unittest.main()
