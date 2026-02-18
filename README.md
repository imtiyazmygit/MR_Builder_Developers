# MR Builder for Developers

A comprehensive toolkit to help developers build and manage merge requests (MR) and pull requests (PR) efficiently. This tool provides utilities for formatting commit messages, managing branches, generating PR descriptions, and maintaining code review checklists.

## Features

- 📝 **MR/PR Description Generator** - Create comprehensive, well-formatted PR descriptions
- ✅ **MR/PR Checklist** - Generate review checklists to ensure quality standards
- 🎯 **Commit Message Formatter** - Format commits following conventional commits specification
- ✔️ **Commit Validator** - Validate commit messages against best practices
- 🌿 **Branch Manager** - Manage Git branches with naming conventions
- 👥 **Reviewer Suggestions** - Suggest reviewers based on changed files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/imtiyazmygit/MR_Builder_Developers.git
cd MR_Builder_Developers
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the CLI executable (optional):
```bash
chmod +x mr_builder_cli.py
```

## Usage

### Command Line Interface

#### Generate MR/PR Description

```bash
python mr_builder_cli.py generate-mr "Add user authentication" \
  --changes "Implement JWT authentication,Add login endpoint,Update user model" \
  --issues "#123,#124"
```

#### Format Commit Messages

```bash
# Basic commit
python mr_builder_cli.py format-commit feat "add user login"

# With scope
python mr_builder_cli.py format-commit feat "add user login" --scope auth

# With body and footer
python mr_builder_cli.py format-commit fix "resolve login bug" \
  --scope auth \
  --body "Fixed an issue where users couldn't login after password reset" \
  --footer "Fixes #456"

# Breaking change
python mr_builder_cli.py format-commit feat "change API response format" \
  --breaking \
  --body "API now returns data in a new format"
```

#### Validate Commit Messages

```bash
# Validate a message directly
python mr_builder_cli.py validate-commit \
  --message "feat: add new feature"

# Validate from a file
python mr_builder_cli.py validate-commit --file commit_msg.txt
```

#### Branch Management

```bash
# Show branch information
python mr_builder_cli.py branch-info

# Suggest a branch name
python mr_builder_cli.py suggest-branch "add user profile page" --issue 789
```

#### Generate Review Checklist

```bash
python mr_builder_cli.py checklist
```

### Python API

You can also use MR Builder directly in your Python scripts:

```python
from src.mr_builder import MRBuilder
from src.commit_formatter import CommitFormatter, CommitType
from src.branch_manager import BranchManager

# Generate MR description
builder = MRBuilder()
description = builder.generate_mr_description(
    title="Add User Authentication",
    changes=["Implement JWT", "Add login endpoint"],
    issue_refs=["#123", "#124"]
)
print(description)

# Format commit message
formatter = CommitFormatter()
message = formatter.format_commit_message(
    commit_type=CommitType.FEAT,
    scope="auth",
    subject="add user login",
    body="Implement user authentication with JWT tokens"
)
print(message)

# Manage branches
manager = BranchManager()
current_branch = manager.get_current_branch()
print(f"Current branch: {current_branch}")

# Suggest branch name
branch_name = manager.suggest_branch_name(
    issue_number=123,
    description="add user profile"
)
print(f"Suggested: {branch_name}")
```

## Configuration

MR Builder supports a configuration file (`.mrbuilder.json`) to customize its behavior:

### Initialize Configuration

```bash
# Create a new configuration file with defaults
python mr_builder_cli.py config init

# View current configuration
python mr_builder_cli.py config show

# Get a specific configuration value
python mr_builder_cli.py config get commit.max_subject_length

# Set a configuration value
python mr_builder_cli.py config set commit.max_subject_length 80
```

### Configuration Options

See `.mrbuilder.json.example` for a complete example. Key configuration options:

- **commit.max_subject_length**: Maximum length for commit subject (default: 72)
- **commit.max_body_line_length**: Maximum line length for commit body (default: 100)
- **commit.allowed_types**: List of allowed commit types
- **branch.naming_pattern**: Pattern for branch names (default: "feature/{description}")
- **branch.include_issue_number**: Whether to include issue numbers in branch names
- **mr.default_reviewers**: Default reviewers for MRs/PRs
- **mr.checklist_items**: Customizable checklist items for code review

## Conventional Commits

This tool follows the [Conventional Commits](https://www.conventionalcommits.org/) specification:

**Format:** `<type>(<scope>): <subject>`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes
- `build`: Build system changes

**Examples:**
- `feat(auth): add login endpoint`
- `fix(api): resolve null pointer exception`
- `docs: update README with installation steps`

## Branch Naming Conventions

Recommended branch naming patterns:

- **Features:** `feature/description` or `feature/issue-123-description`
- **Bug fixes:** `bugfix/description` or `bugfix/issue-123-description`
- **Hotfixes:** `hotfix/description`
- **Releases:** `release/version`
- **Experiments:** `experiment/description`

## Examples

See the [examples](./examples) directory for more usage examples:

- `example_usage.py` - Complete Python API examples
- `example_workflow.md` - Example workflow for using MR Builder

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch using the naming conventions above
3. Make your changes following conventional commits
4. Submit a pull request with a comprehensive description

## License

MIT License - feel free to use this tool in your projects!

## Author

MR Builder Developers Team
