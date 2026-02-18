"""
Unit tests for BranchManager class
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.branch_manager import BranchManager


class TestBranchManager(unittest.TestCase):
    """Test cases for BranchManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = BranchManager()
    
    def test_suggest_branch_name_simple(self):
        """Test simple branch name suggestion."""
        branch = self.manager.suggest_branch_name(
            description="add user profile"
        )
        
        self.assertEqual(branch, "feature/add-user-profile")
    
    def test_suggest_branch_name_with_issue(self):
        """Test branch name suggestion with issue number."""
        branch = self.manager.suggest_branch_name(
            issue_number=123,
            description="fix login bug"
        )
        
        self.assertEqual(branch, "feature/issue-123-fix-login-bug")
    
    def test_suggest_branch_name_special_chars(self):
        """Test branch name with special characters."""
        branch = self.manager.suggest_branch_name(
            description="Add User's Profile (NEW!)"
        )
        
        # Should remove special characters and normalize
        self.assertNotIn("'", branch)
        self.assertNotIn("(", branch)
        self.assertNotIn(")", branch)
        self.assertNotIn("!", branch)
        self.assertTrue(branch.startswith("feature/"))
    
    def test_get_branch_naming_conventions(self):
        """Test getting branch naming conventions."""
        conventions = self.manager.get_branch_naming_conventions()
        
        self.assertIsInstance(conventions, dict)
        self.assertIn('feature', conventions)
        self.assertIn('bugfix', conventions)
        self.assertIn('hotfix', conventions)
    
    def test_get_current_branch(self):
        """Test getting current branch."""
        branch = self.manager.get_current_branch()
        
        # Should return a string or None if not in a git repo
        self.assertTrue(branch is None or isinstance(branch, str))
    
    def test_get_branch_info(self):
        """Test getting branch information."""
        info = self.manager.get_branch_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('current_branch', info)
        self.assertIn('local_branches', info)
        self.assertIn('remote_branches', info)


if __name__ == '__main__':
    unittest.main()
