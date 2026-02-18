"""
MR Builder for Developers
A tool to help developers build and manage merge/pull requests efficiently.
"""

__version__ = "1.0.0"
__author__ = "MR Builder Developers"

from .mr_builder import MRBuilder
from .commit_formatter import CommitFormatter
from .branch_manager import BranchManager
from .config_manager import ConfigManager

__all__ = ['MRBuilder', 'CommitFormatter', 'BranchManager', 'ConfigManager']
