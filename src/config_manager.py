"""
Configuration Manager - Handles loading and saving configuration
"""

import json
import os
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration for MR Builder."""
    
    DEFAULT_CONFIG = {
        "commit": {
            "max_subject_length": 72,
            "max_body_line_length": 100,
            "allowed_types": ["feat", "fix", "docs", "style", "refactor", "test", "chore", "perf", "ci", "build"]
        },
        "branch": {
            "naming_pattern": "feature/{description}",
            "include_issue_number": True
        },
        "mr": {
            "default_reviewers": [],
            "required_labels": [],
            "checklist_items": [
                "Code follows project style guidelines",
                "All tests pass",
                "Documentation is updated",
                "No debug code or console logs",
                "Changes are backward compatible",
                "Security considerations addressed",
                "Performance impact evaluated"
            ]
        }
    }
    
    CONFIG_FILENAME = ".mrbuilder.json"
    
    def __init__(self, repo_path: str = "."):
        """
        Initialize Configuration Manager.
        
        Args:
            repo_path: Path to the repository
        """
        self.repo_path = os.path.abspath(repo_path)
        self.config_path = os.path.join(self.repo_path, self.CONFIG_FILENAME)
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or return defaults.
        
        Returns:
            Configuration dictionary
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                # Merge with defaults
                config = self.DEFAULT_CONFIG.copy()
                self._deep_merge(config, user_config)
                return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load config from {self.config_path}: {e}")
                print("Using default configuration")
        
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Save configuration to file.
        
        Args:
            config: Configuration to save (uses current config if None)
            
        Returns:
            True if successful, False otherwise
        """
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error: Failed to save config to {self.config_path}: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., "commit.max_subject_length")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> None:
        """
        Set a configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., "commit.max_subject_length")
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def _deep_merge(self, base: Dict, override: Dict) -> None:
        """
        Deep merge override dict into base dict.
        
        Args:
            base: Base dictionary to merge into
            override: Dictionary with values to override
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def init_config(self) -> bool:
        """
        Initialize a new configuration file with defaults.
        
        Returns:
            True if successful, False if file already exists
        """
        if os.path.exists(self.config_path):
            print(f"Configuration file already exists at {self.config_path}")
            return False
        
        success = self.save_config(self.DEFAULT_CONFIG)
        if success:
            print(f"Created configuration file at {self.config_path}")
        return success
    
    def show_config(self) -> str:
        """
        Get formatted configuration as JSON string.
        
        Returns:
            JSON formatted configuration
        """
        return json.dumps(self.config, indent=2)
