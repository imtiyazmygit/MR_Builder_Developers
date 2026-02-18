"""
MR Builder - Core functionality for building merge/pull requests
"""

import os
from datetime import datetime
from typing import List, Dict, Optional


class MRBuilder:
    """Main class for building and managing merge/pull requests."""
    
    def __init__(self, repo_path: str = "."):
        """
        Initialize MR Builder.
        
        Args:
            repo_path: Path to the git repository
        """
        self.repo_path = os.path.abspath(repo_path)
        self.config = {}
        
    def generate_mr_description(self, 
                                title: str, 
                                changes: List[str], 
                                issue_refs: Optional[List[str]] = None) -> str:
        """
        Generate a comprehensive MR/PR description.
        
        Args:
            title: Title of the MR/PR
            changes: List of changes made
            issue_refs: Optional list of issue references
            
        Returns:
            Formatted MR/PR description
        """
        description = f"# {title}\n\n"
        
        description += "## Changes\n\n"
        for change in changes:
            description += f"- {change}\n"
        
        if issue_refs:
            description += "\n## Related Issues\n\n"
            for ref in issue_refs:
                description += f"- {ref}\n"
        
        description += f"\n## Generated\n\nCreated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return description
    
    def validate_mr_requirements(self) -> Dict[str, bool]:
        """
        Validate that MR requirements are met.
        
        Returns:
            Dictionary with validation results
        """
        validations = {
            'has_description': False,
            'has_tests': False,
            'has_documentation': False,
            'no_merge_conflicts': True
        }
        
        # Basic validation logic
        # In a real implementation, this would check actual files
        validations['has_description'] = True
        
        return validations
    
    def suggest_reviewers(self, files_changed: List[str]) -> List[str]:
        """
        Suggest reviewers based on changed files.
        
        Args:
            files_changed: List of files that were changed
            
        Returns:
            List of suggested reviewers
        """
        # Simple logic - in real implementation would check git history
        reviewers = []
        
        for file in files_changed:
            if file.endswith('.py'):
                reviewers.append('python-team')
            elif file.endswith(('.js', '.ts')):
                reviewers.append('frontend-team')
            elif file.endswith('.md'):
                reviewers.append('docs-team')
        
        return list(set(reviewers))
    
    def get_mr_checklist(self) -> List[str]:
        """
        Get a checklist for MR/PR review.
        
        Returns:
            List of checklist items
        """
        checklist = [
            "Code follows project style guidelines",
            "All tests pass",
            "Documentation is updated",
            "No debug code or console logs",
            "Changes are backward compatible",
            "Security considerations addressed",
            "Performance impact evaluated"
        ]
        
        return checklist
    
    def format_checklist(self, items: List[str], checked: Optional[List[bool]] = None) -> str:
        """
        Format checklist items into markdown.
        
        Args:
            items: List of checklist items
            checked: Optional list of boolean values indicating checked state
            
        Returns:
            Formatted markdown checklist
        """
        if checked is None:
            checked = [False] * len(items)
        
        checklist_md = "## Review Checklist\n\n"
        for item, is_checked in zip(items, checked):
            checkbox = "x" if is_checked else " "
            checklist_md += f"- [{checkbox}] {item}\n"
        
        return checklist_md
