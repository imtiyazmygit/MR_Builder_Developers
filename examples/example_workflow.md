# Example Workflow: Using MR Builder in Your Development Process

This document demonstrates a typical workflow for using MR Builder tools throughout your development process.

## Scenario: Adding a New Feature

You've been assigned to work on issue #789: "Add user profile page"

### Step 1: Create a Feature Branch

First, let's create a properly named feature branch:

```bash
# Get a suggested branch name
python mr_builder_cli.py suggest-branch "add user profile page" --issue 789

# Output: Suggested branch name: feature/issue-789-add-user-profile-page

# Create the branch
git checkout -b feature/issue-789-add-user-profile-page
```

### Step 2: Make Your Changes

Develop your feature by making necessary code changes to implement the user profile page.

### Step 3: Commit Your Changes

Use the commit formatter to create well-formatted commit messages:

```bash
# First commit - add the profile component
python mr_builder_cli.py format-commit feat "add user profile component" \
  --scope frontend \
  --body "Created a new UserProfile component that displays user information including avatar, name, and bio"

# Output:
# feat(frontend): add user profile component
#
# Created a new UserProfile component that displays user information
# including avatar, name, and bio

# Copy the output and commit
git add src/components/UserProfile.js
git commit -m "feat(frontend): add user profile component

Created a new UserProfile component that displays user information
including avatar, name, and bio"

# Second commit - add API endpoint
python mr_builder_cli.py format-commit feat "add profile API endpoint" \
  --scope api \
  --body "Implemented GET /api/users/:id/profile endpoint that returns user profile data"

git add src/api/profile.js
git commit -m "feat(api): add profile API endpoint

Implemented GET /api/users/:id/profile endpoint that returns user profile data"
```

### Step 4: Validate Your Commits (Optional)

Before pushing, you can validate your commit messages:

```bash
# Check the last commit
git log -1 --pretty=%B > /tmp/commit_msg.txt
python mr_builder_cli.py validate-commit --file /tmp/commit_msg.txt

# Output: ✓ Commit message is valid
```

### Step 5: Generate PR Description

When ready to create a pull request, generate a comprehensive description:

```bash
python mr_builder_cli.py generate-mr "Add user profile page" \
  --changes "Add UserProfile React component,Implement profile API endpoint,Add profile route,Update navigation menu" \
  --issues "#789"

# Output:
# # Add user profile page
#
# ## Changes
#
# - Add UserProfile React component
# - Implement profile API endpoint
# - Add profile route
# - Update navigation menu
#
# ## Related Issues
#
# - #789
#
# ## Generated
#
# Created on 2026-02-18 12:34:56
```

Copy this output to use as your PR description on GitHub.

### Step 6: Generate Review Checklist

Include a review checklist in your PR:

```bash
python mr_builder_cli.py checklist

# Output:
# ## Review Checklist
#
# - [ ] Code follows project style guidelines
# - [ ] All tests pass
# - [ ] Documentation is updated
# - [ ] No debug code or console logs
# - [ ] Changes are backward compatible
# - [ ] Security considerations addressed
# - [ ] Performance impact evaluated
```

Add this checklist to your PR description or as a comment.

### Step 7: Check Branch Status

Before pushing, verify your branch status:

```bash
python mr_builder_cli.py branch-info

# Output:
# Current branch: feature/issue-789-add-user-profile-page
#
# Local branches (3):
#   - main
#   - feature/issue-789-add-user-profile-page
#   - bugfix/login-error
```

### Step 8: Push and Create PR

```bash
git push origin feature/issue-789-add-user-profile-page

# Then create a PR on GitHub using:
# - Title: "Add user profile page"
# - Description: (use the generated description from Step 5)
# - Checklist: (use the checklist from Step 6)
```

## Advanced: Handling Breaking Changes

If your change introduces breaking changes:

```bash
python mr_builder_cli.py format-commit feat "change user API response format" \
  --scope api \
  --breaking \
  --body "Modified user API to return data in a new standardized format" \
  --footer "All clients must update to handle new response structure"

# Output:
# feat(api)!: change user API response format
#
# Modified user API to return data in a new standardized format
#
# BREAKING CHANGE: All clients must update to handle new response structure
```

## Tips for Teams

1. **Establish conventions**: Share branch naming and commit conventions with your team
2. **Automate validation**: Add commit message validation to your git hooks
3. **Template PRs**: Use the generated descriptions as templates for consistency
4. **Review checklists**: Include checklists in all PRs to ensure quality standards

## Summary

By using MR Builder throughout your development process, you ensure:
- ✅ Consistent branch naming
- ✅ Well-formatted commit messages
- ✅ Comprehensive PR descriptions
- ✅ Thorough code review checklists
- ✅ Better team collaboration
