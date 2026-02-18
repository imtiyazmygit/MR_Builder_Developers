"""
Unit tests for ConfigManager class
"""

import unittest
import sys
import os
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.manager = ConfigManager(self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_load_default_config(self):
        """Test loading default configuration."""
        config = self.manager.load_config()
        
        self.assertIsInstance(config, dict)
        self.assertIn('commit', config)
        self.assertIn('branch', config)
        self.assertIn('mr', config)
    
    def test_get_config_value(self):
        """Test getting configuration value."""
        value = self.manager.get('commit.max_subject_length')
        
        self.assertEqual(value, 72)
    
    def test_get_nested_config_value(self):
        """Test getting nested configuration value."""
        value = self.manager.get('branch.naming_pattern')
        
        self.assertEqual(value, 'feature/{description}')
    
    def test_get_nonexistent_key(self):
        """Test getting non-existent key returns default."""
        value = self.manager.get('nonexistent.key', 'default_value')
        
        self.assertEqual(value, 'default_value')
    
    def test_set_config_value(self):
        """Test setting configuration value."""
        self.manager.set('commit.max_subject_length', 80)
        value = self.manager.get('commit.max_subject_length')
        
        self.assertEqual(value, 80)
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        # Set a value
        self.manager.set('commit.max_subject_length', 90)
        
        # Save config
        success = self.manager.save_config()
        self.assertTrue(success)
        
        # Create new manager to load config
        new_manager = ConfigManager(self.test_dir)
        value = new_manager.get('commit.max_subject_length')
        
        self.assertEqual(value, 90)
    
    def test_show_config(self):
        """Test showing configuration as JSON."""
        config_str = self.manager.show_config()
        
        self.assertIsInstance(config_str, str)
        self.assertIn('commit', config_str)
        self.assertIn('branch', config_str)
    
    def test_init_config(self):
        """Test initializing configuration file."""
        success = self.manager.init_config()
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.manager.config_path))
        
        # Second init should fail
        success = self.manager.init_config()
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()
