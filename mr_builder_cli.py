#!/usr/bin/env python3
"""
MR Builder CLI - Command-line interface for MR Builder tools
"""

import sys
import argparse
from src.mr_builder import MRBuilder
from src.commit_formatter import CommitFormatter, CommitType
from src.branch_manager import BranchManager
from src.config_manager import ConfigManager


def generate_mr_description(args):
    """Generate MR/PR description."""
    builder = MRBuilder(args.repo)
    
    changes = args.changes.split(',') if args.changes else []
    issues = args.issues.split(',') if args.issues else None
    
    description = builder.generate_mr_description(
        title=args.title,
        changes=changes,
        issue_refs=issues
    )
    
    print(description)


def format_commit(args):
    """Format a commit message."""
    formatter = CommitFormatter()
    
    try:
        commit_type = CommitType[args.type.upper()]
    except KeyError:
        print(f"Error: Invalid commit type '{args.type}'")
        print(f"Valid types: {', '.join([t.name.lower() for t in CommitType])}")
        sys.exit(1)
    
    message = formatter.format_commit_message(
        commit_type=commit_type,
        scope=args.scope,
        subject=args.subject,
        body=args.body,
        footer=args.footer,
        breaking=args.breaking
    )
    
    print(message)


def validate_commit(args):
    """Validate a commit message."""
    formatter = CommitFormatter()
    
    message = args.message
    if args.file:
        with open(args.file, 'r') as f:
            message = f.read()
    
    is_valid, errors = formatter.validate_commit_message(message)
    
    if is_valid:
        print("✓ Commit message is valid")
        sys.exit(0)
    else:
        print("✗ Commit message is invalid:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


def branch_info(args):
    """Show branch information."""
    manager = BranchManager(args.repo)
    
    info = manager.get_branch_info()
    
    print(f"Current branch: {info['current_branch']}")
    print(f"\nLocal branches ({len(info['local_branches'])}):")
    for branch in info['local_branches'][:10]:
        print(f"  - {branch}")
    if len(info['local_branches']) > 10:
        print(f"  ... and {len(info['local_branches']) - 10} more")
    
    if info.get('has_changes'):
        print(f"\n⚠ You have uncommitted changes")


def suggest_branch(args):
    """Suggest a branch name."""
    manager = BranchManager(args.repo)
    
    issue_num = int(args.issue) if args.issue else None
    branch_name = manager.suggest_branch_name(
        issue_number=issue_num,
        description=args.description
    )
    
    print(f"Suggested branch name: {branch_name}")


def mr_checklist(args):
    """Generate MR/PR checklist."""
    builder = MRBuilder(args.repo)
    
    items = builder.get_mr_checklist()
    checklist = builder.format_checklist(items)
    
    print(checklist)


def config_init(args):
    """Initialize configuration file."""
    config = ConfigManager(args.repo)
    config.init_config()


def config_show(args):
    """Show current configuration."""
    config = ConfigManager(args.repo)
    print(config.show_config())


def config_set(args):
    """Set a configuration value."""
    config = ConfigManager(args.repo)
    config.set(args.key, args.value)
    if config.save_config():
        print(f"Set {args.key} = {args.value}")
    else:
        print("Failed to save configuration")
        sys.exit(1)


def config_get(args):
    """Get a configuration value."""
    config = ConfigManager(args.repo)
    value = config.get(args.key)
    if value is not None:
        print(f"{args.key} = {value}")
    else:
        print(f"Key '{args.key}' not found in configuration")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='MR Builder - Tools for managing merge/pull requests',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Generate MR description
    mr_parser = subparsers.add_parser('generate-mr', help='Generate MR/PR description')
    mr_parser.add_argument('title', help='Title of the MR/PR')
    mr_parser.add_argument('--changes', help='Comma-separated list of changes')
    mr_parser.add_argument('--issues', help='Comma-separated list of issue references')
    mr_parser.add_argument('--repo', default='.', help='Path to repository')
    mr_parser.set_defaults(func=generate_mr_description)
    
    # Format commit message
    commit_parser = subparsers.add_parser('format-commit', help='Format a commit message')
    commit_parser.add_argument('type', help='Commit type (feat, fix, docs, etc.)')
    commit_parser.add_argument('subject', help='Short description')
    commit_parser.add_argument('--scope', help='Scope of the commit')
    commit_parser.add_argument('--body', help='Detailed description')
    commit_parser.add_argument('--footer', help='Footer (e.g., issue references)')
    commit_parser.add_argument('--breaking', action='store_true', help='Mark as breaking change')
    commit_parser.set_defaults(func=format_commit)
    
    # Validate commit message
    validate_parser = subparsers.add_parser('validate-commit', help='Validate a commit message')
    validate_parser.add_argument('--message', help='Commit message to validate')
    validate_parser.add_argument('--file', help='File containing commit message')
    validate_parser.set_defaults(func=validate_commit)
    
    # Branch info
    branch_parser = subparsers.add_parser('branch-info', help='Show branch information')
    branch_parser.add_argument('--repo', default='.', help='Path to repository')
    branch_parser.set_defaults(func=branch_info)
    
    # Suggest branch name
    suggest_parser = subparsers.add_parser('suggest-branch', help='Suggest a branch name')
    suggest_parser.add_argument('description', help='Brief description of the work')
    suggest_parser.add_argument('--issue', help='Issue/ticket number')
    suggest_parser.add_argument('--repo', default='.', help='Path to repository')
    suggest_parser.set_defaults(func=suggest_branch)
    
    # MR checklist
    checklist_parser = subparsers.add_parser('checklist', help='Generate MR/PR checklist')
    checklist_parser.add_argument('--repo', default='.', help='Path to repository')
    checklist_parser.set_defaults(func=mr_checklist)
    
    # Configuration commands
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_subparsers = config_parser.add_subparsers(dest='config_command', help='Configuration command')
    
    # Config init
    config_init_parser = config_subparsers.add_parser('init', help='Initialize configuration file')
    config_init_parser.add_argument('--repo', default='.', help='Path to repository')
    config_init_parser.set_defaults(func=config_init)
    
    # Config show
    config_show_parser = config_subparsers.add_parser('show', help='Show current configuration')
    config_show_parser.add_argument('--repo', default='.', help='Path to repository')
    config_show_parser.set_defaults(func=config_show)
    
    # Config set
    config_set_parser = config_subparsers.add_parser('set', help='Set a configuration value')
    config_set_parser.add_argument('key', help='Configuration key (dot notation)')
    config_set_parser.add_argument('value', help='Value to set')
    config_set_parser.add_argument('--repo', default='.', help='Path to repository')
    config_set_parser.set_defaults(func=config_set)
    
    # Config get
    config_get_parser = config_subparsers.add_parser('get', help='Get a configuration value')
    config_get_parser.add_argument('key', help='Configuration key (dot notation)')
    config_get_parser.add_argument('--repo', default='.', help='Path to repository')
    config_get_parser.set_defaults(func=config_get)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
