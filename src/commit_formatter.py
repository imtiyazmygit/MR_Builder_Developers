"""
Commit Formatter - Helps format commit messages following best practices
"""

from typing import List, Optional
from enum import Enum


class CommitType(Enum):
    """Standard commit types following conventional commits."""
    FEAT = "feat"
    FIX = "fix"
    DOCS = "docs"
    STYLE = "style"
    REFACTOR = "refactor"
    TEST = "test"
    CHORE = "chore"
    PERF = "perf"
    CI = "ci"
    BUILD = "build"


class CommitFormatter:
    """Formats commit messages following conventional commit standards."""
    
    def __init__(self):
        self.max_subject_length = 72
        self.max_body_line_length = 100
    
    def format_commit_message(self, 
                             commit_type: CommitType,
                             scope: Optional[str],
                             subject: str,
                             body: Optional[str] = None,
                             footer: Optional[str] = None,
                             breaking: bool = False) -> str:
        """
        Format a commit message following conventional commits specification.
        
        Args:
            commit_type: Type of commit (feat, fix, etc.)
            scope: Optional scope of the commit
            subject: Short description of the commit
            body: Optional detailed description
            footer: Optional footer (e.g., issue references)
            breaking: Whether this is a breaking change
            
        Returns:
            Formatted commit message
        """
        # Build the header
        header = commit_type.value
        
        if scope:
            header += f"({scope})"
        
        if breaking:
            header += "!"
        
        header += f": {subject}"
        
        # Validate header length
        if len(header) > self.max_subject_length:
            print(f"Warning: Header exceeds {self.max_subject_length} characters")
        
        # Build full message
        message = header
        
        if body:
            message += f"\n\n{self._wrap_text(body, self.max_body_line_length)}"
        
        if breaking:
            if footer:
                footer = f"BREAKING CHANGE: {footer}"
            else:
                footer = "BREAKING CHANGE: This commit contains breaking changes"
        
        if footer:
            message += f"\n\n{footer}"
        
        return message
    
    def _wrap_text(self, text: str, max_length: int) -> str:
        """
        Wrap text to a maximum line length.
        
        Args:
            text: Text to wrap
            max_length: Maximum length per line
            
        Returns:
            Wrapped text
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def parse_commit_message(self, message: str) -> dict:
        """
        Parse a commit message to extract its components.
        
        Args:
            message: Commit message to parse
            
        Returns:
            Dictionary with parsed components
        """
        lines = message.split('\n')
        header = lines[0]
        
        # Parse header
        parts = header.split(':', 1)
        if len(parts) != 2:
            return {'valid': False, 'message': message}
        
        type_scope = parts[0].strip()
        subject = parts[1].strip()
        
        # Extract type and scope
        breaking = type_scope.endswith('!')
        if breaking:
            type_scope = type_scope[:-1]
        
        if '(' in type_scope:
            commit_type = type_scope.split('(')[0]
            scope = type_scope.split('(')[1].rstrip(')')
        else:
            commit_type = type_scope
            scope = None
        
        # Extract body and footer
        body = None
        footer = None
        
        if len(lines) > 2:
            body_lines = []
            footer_lines = []
            in_footer = False
            
            for line in lines[2:]:
                if line.startswith('BREAKING CHANGE:') or line.startswith('Closes:') or line.startswith('Fixes:'):
                    in_footer = True
                
                if in_footer:
                    footer_lines.append(line)
                else:
                    body_lines.append(line)
            
            if body_lines:
                body = '\n'.join(body_lines).strip()
            if footer_lines:
                footer = '\n'.join(footer_lines).strip()
        
        return {
            'valid': True,
            'type': commit_type,
            'scope': scope,
            'subject': subject,
            'body': body,
            'footer': footer,
            'breaking': breaking
        }
    
    def validate_commit_message(self, message: str) -> tuple[bool, List[str]]:
        """
        Validate a commit message against conventional commits rules.
        
        Args:
            message: Commit message to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        parsed = self.parse_commit_message(message)
        
        if not parsed['valid']:
            errors.append("Commit message does not follow conventional commits format")
            return False, errors
        
        # Validate type
        valid_types = [t.value for t in CommitType]
        if parsed['type'] not in valid_types:
            errors.append(f"Invalid commit type: {parsed['type']}. Must be one of {', '.join(valid_types)}")
        
        # Validate subject
        if len(parsed['subject']) > self.max_subject_length:
            errors.append(f"Subject exceeds {self.max_subject_length} characters")
        
        if parsed['subject'] and parsed['subject'][0].isupper():
            errors.append("Subject should start with lowercase")
        
        if parsed['subject'].endswith('.'):
            errors.append("Subject should not end with a period")
        
        return len(errors) == 0, errors
