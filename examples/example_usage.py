"""
Example usage of MR Builder Python API
"""

import sys
import os
# Add parent directory to path to import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mr_builder import MRBuilder
from src.commit_formatter import CommitFormatter, CommitType
from src.branch_manager import BranchManager


def example_mr_builder():
    """Example of using MRBuilder class."""
    print("=== MR Builder Example ===\n")
    
    builder = MRBuilder()
    
    # Generate MR description
    description = builder.generate_mr_description(
        title="Add User Authentication System",
        changes=[
            "Implement JWT-based authentication",
            "Add login and logout endpoints",
            "Update user model with password hashing",
            "Add authentication middleware"
        ],
        issue_refs=["#123", "#124"]
    )
    
    print("Generated MR Description:")
    print(description)
    print("\n" + "="*50 + "\n")
    
    # Get MR checklist
    checklist_items = builder.get_mr_checklist()
    checklist = builder.format_checklist(checklist_items)
    print("MR Checklist:")
    print(checklist)
    print("\n" + "="*50 + "\n")
    
    # Suggest reviewers
    files = ["src/auth.py", "src/models/user.py", "docs/api.md"]
    reviewers = builder.suggest_reviewers(files)
    print(f"Suggested reviewers for {files}:")
    for reviewer in reviewers:
        print(f"  - {reviewer}")
    print("\n" + "="*50 + "\n")


def example_commit_formatter():
    """Example of using CommitFormatter class."""
    print("=== Commit Formatter Example ===\n")
    
    formatter = CommitFormatter()
    
    # Format a feature commit
    message = formatter.format_commit_message(
        commit_type=CommitType.FEAT,
        scope="auth",
        subject="add JWT authentication",
        body="Implement JWT-based authentication system with token refresh. "
             "Users can now login and receive access tokens for API requests.",
        footer="Closes #123"
    )
    
    print("Formatted Commit Message:")
    print(message)
    print("\n" + "="*50 + "\n")
    
    # Format a breaking change
    breaking_message = formatter.format_commit_message(
        commit_type=CommitType.FEAT,
        scope="api",
        subject="change response format",
        body="API responses now return data in a standardized envelope format.",
        breaking=True,
        footer="All API clients need to be updated"
    )
    
    print("Breaking Change Commit:")
    print(breaking_message)
    print("\n" + "="*50 + "\n")
    
    # Validate commit messages
    test_messages = [
        "feat(auth): add login endpoint",
        "fix: resolve bug",
        "Bad commit message",
        "feat(api): Add new feature.",  # Should fail - ends with period
    ]
    
    print("Validating commit messages:")
    for msg in test_messages:
        is_valid, errors = formatter.validate_commit_message(msg)
        status = "✓" if is_valid else "✗"
        print(f"{status} '{msg}'")
        if errors:
            for error in errors:
                print(f"    - {error}")
    print("\n" + "="*50 + "\n")


def example_branch_manager():
    """Example of using BranchManager class."""
    print("=== Branch Manager Example ===\n")
    
    manager = BranchManager()
    
    # Get current branch
    current = manager.get_current_branch()
    print(f"Current branch: {current}")
    print()
    
    # Suggest branch names
    suggestions = [
        (None, "add user profile page"),
        (123, "fix login bug"),
        (456, "update documentation"),
    ]
    
    print("Branch name suggestions:")
    for issue, desc in suggestions:
        branch = manager.suggest_branch_name(issue_number=issue, description=desc)
        issue_str = f"Issue #{issue}" if issue else "No issue"
        print(f"  {issue_str}, '{desc}' -> {branch}")
    print()
    
    # Show naming conventions
    conventions = manager.get_branch_naming_conventions()
    print("Branch naming conventions:")
    for branch_type, convention in conventions.items():
        print(f"  {branch_type:12} -> {convention}")
    print("\n" + "="*50 + "\n")


def main():
    """Run all examples."""
    print("\n" + "="*50)
    print("MR Builder for Developers - Python API Examples")
    print("="*50 + "\n")
    
    example_mr_builder()
    example_commit_formatter()
    example_branch_manager()
    
    print("\nAll examples completed!")


if __name__ == "__main__":
    main()
