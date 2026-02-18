"""
Unit tests for CommitFormatter class
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commit_formatter import CommitFormatter, CommitType


class TestCommitFormatter(unittest.TestCase):
    """Test cases for CommitFormatter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.formatter = CommitFormatter()
    
    def test_format_basic_commit(self):
        """Test basic commit message formatting."""
        message = self.formatter.format_commit_message(
            commit_type=CommitType.FEAT,
            scope=None,
            subject="add new feature"
        )
        
        self.assertEqual(message, "feat: add new feature")
    
    def test_format_commit_with_scope(self):
        """Test commit message with scope."""
        message = self.formatter.format_commit_message(
            commit_type=CommitType.FIX,
            scope="auth",
            subject="resolve login bug"
        )
        
        self.assertEqual(message, "fix(auth): resolve login bug")
    
    def test_format_commit_with_body(self):
        """Test commit message with body."""
        message = self.formatter.format_commit_message(
            commit_type=CommitType.FEAT,
            scope="api",
            subject="add endpoint",
            body="This is the body text"
        )
        
        self.assertIn("feat(api): add endpoint", message)
        self.assertIn("This is the body text", message)
    
    def test_format_breaking_change(self):
        """Test breaking change commit."""
        message = self.formatter.format_commit_message(
            commit_type=CommitType.FEAT,
            scope="api",
            subject="change response format",
            breaking=True
        )
        
        self.assertIn("feat(api)!", message)
        self.assertIn("BREAKING CHANGE:", message)
    
    def test_validate_valid_commit(self):
        """Test validation of valid commit."""
        message = "feat: add new feature"
        is_valid, errors = self.formatter.validate_commit_message(message)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_commit_with_scope(self):
        """Test validation of commit with scope."""
        message = "fix(auth): resolve bug"
        is_valid, errors = self.formatter.validate_commit_message(message)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_invalid_type(self):
        """Test validation with invalid type."""
        message = "invalid: some message"
        is_valid, errors = self.formatter.validate_commit_message(message)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_validate_subject_with_period(self):
        """Test validation of subject ending with period."""
        message = "feat: add feature."
        is_valid, errors = self.formatter.validate_commit_message(message)
        
        self.assertFalse(is_valid)
        self.assertTrue(any("period" in error.lower() for error in errors))
    
    def test_validate_subject_uppercase(self):
        """Test validation of subject starting with uppercase."""
        message = "feat: Add feature"
        is_valid, errors = self.formatter.validate_commit_message(message)
        
        self.assertFalse(is_valid)
        self.assertTrue(any("lowercase" in error.lower() for error in errors))
    
    def test_parse_commit_message(self):
        """Test parsing of commit message."""
        message = "feat(auth): add login\n\nDetailed body\n\nCloses #123"
        parsed = self.formatter.parse_commit_message(message)
        
        self.assertTrue(parsed['valid'])
        self.assertEqual(parsed['type'], 'feat')
        self.assertEqual(parsed['scope'], 'auth')
        self.assertEqual(parsed['subject'], 'add login')
    
    def test_wrap_text(self):
        """Test text wrapping."""
        long_text = "This is a very long line that should be wrapped at the maximum length specified"
        wrapped = self.formatter._wrap_text(long_text, 20)
        
        lines = wrapped.split('\n')
        for line in lines:
            self.assertLessEqual(len(line), 20)


if __name__ == '__main__':
    unittest.main()
