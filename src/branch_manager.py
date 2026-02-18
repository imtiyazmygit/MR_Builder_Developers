"""
Branch Manager - Helps manage Git branches and workflows
"""

import os
import subprocess
from typing import List, Optional, Dict, Any


class BranchManager:
    """Manages Git branches and common workflows."""
    
    def __init__(self, repo_path: str = "."):
        """
        Initialize Branch Manager.
        
        Args:
            repo_path: Path to the git repository
        """
        self.repo_path = os.path.abspath(repo_path)
    
    def _run_git_command(self, args: List[str]) -> tuple[bool, str]:
        """
        Run a git command.
        
        Args:
            args: List of command arguments
            
        Returns:
            Tuple of (success, output)
        """
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, e.stderr.strip()
    
    def get_current_branch(self) -> Optional[str]:
        """
        Get the name of the current branch.
        
        Returns:
            Current branch name or None if not in a git repo
        """
        success, output = self._run_git_command(['branch', '--show-current'])
        return output if success else None
    
    def list_branches(self, remote: bool = False) -> List[str]:
        """
        List all branches.
        
        Args:
            remote: Whether to list remote branches
            
        Returns:
            List of branch names
        """
        args = ['branch']
        if remote:
            args.append('-r')
        
        success, output = self._run_git_command(args)
        if not success:
            return []
        
        branches = []
        for line in output.split('\n'):
            line = line.strip()
            if line:
                # Remove the asterisk for current branch
                line = line.lstrip('* ')
                branches.append(line)
        
        return branches
    
    def create_feature_branch(self, feature_name: str, base_branch: str = "main") -> tuple[bool, str]:
        """
        Create a new feature branch.
        
        Args:
            feature_name: Name of the feature
            base_branch: Base branch to branch from
            
        Returns:
            Tuple of (success, message)
        """
        branch_name = f"feature/{feature_name}"
        
        # Check if branch already exists
        if branch_name in self.list_branches():
            return False, f"Branch {branch_name} already exists"
        
        # Create and checkout the new branch
        success, output = self._run_git_command(['checkout', '-b', branch_name, base_branch])
        
        if success:
            return True, f"Created and switched to branch {branch_name}"
        else:
            return False, f"Failed to create branch: {output}"
    
    def suggest_branch_name(self, issue_number: Optional[int] = None, description: str = "") -> str:
        """
        Suggest a branch name based on convention.
        
        Args:
            issue_number: Optional issue/ticket number
            description: Brief description of the work
            
        Returns:
            Suggested branch name
        """
        # Normalize description
        description = description.lower()
        description = description.replace(' ', '-')
        # Remove special characters
        description = ''.join(c for c in description if c.isalnum() or c == '-')
        
        if issue_number:
            return f"feature/issue-{issue_number}-{description}"
        else:
            return f"feature/{description}"
    
    def get_branch_info(self) -> Dict[str, Any]:
        """
        Get information about the current branch.
        
        Returns:
            Dictionary with branch information
        """
        info = {
            'current_branch': self.get_current_branch(),
            'local_branches': self.list_branches(remote=False),
            'remote_branches': self.list_branches(remote=True),
        }
        
        # Get branch status
        success, output = self._run_git_command(['status', '--short'])
        if success:
            info['has_changes'] = bool(output)
            info['status'] = output
        
        return info
    
    def check_branch_exists(self, branch_name: str, remote: bool = False) -> bool:
        """
        Check if a branch exists.
        
        Args:
            branch_name: Name of the branch
            remote: Whether to check remote branches
            
        Returns:
            True if branch exists
        """
        branches = self.list_branches(remote=remote)
        if remote:
            # Remote branches include origin/ prefix
            return any(branch.endswith(branch_name) for branch in branches)
        return branch_name in branches
    
    def get_branch_naming_conventions(self) -> Dict[str, str]:
        """
        Get recommended branch naming conventions.
        
        Returns:
            Dictionary of branch type to naming convention
        """
        return {
            'feature': 'feature/description or feature/issue-123-description',
            'bugfix': 'bugfix/description or bugfix/issue-123-description',
            'hotfix': 'hotfix/description',
            'release': 'release/version',
            'experiment': 'experiment/description'
        }
