"""
Input validation utilities
"""
import re
from typing import Dict, List, Optional, Tuple
import html

class InputValidator:
    """Handles input validation and sanitization"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email address format
        Returns (is_valid, error_message)
        """
        if not email:
            return False, "Email is required"
        
        email = email.strip()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return False, "Please enter a valid email address"
        
        if len(email) > 254:
            return False, "Email address is too long"
        
        return True, ""
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """
        Validate name input
        Returns (is_valid, error_message)
        """
        if not name:
            return False, "Name is required"
        
        name = name.strip()
        
        if len(name) < 2:
            return False, "Name must be at least 2 characters long"
        
        if len(name) > 100:
            return False, "Name must be less than 100 characters"
        
        # Allow letters, spaces, hyphens, and apostrophes
        name_pattern = r"^[a-zA-Z\s\-']+$"
        if not re.match(name_pattern, name):
            return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
        
        return True, ""
    
    @staticmethod
    def validate_subject(subject: str) -> Tuple[bool, str]:
        """
        Validate subject line
        Returns (is_valid, error_message)
        """
        if not subject:
            return False, "Subject is required"
        
        subject = subject.strip()
        
        if len(subject) < 3:
            return False, "Subject must be at least 3 characters long"
        
        if len(subject) > 200:
            return False, "Subject must be less than 200 characters"
        
        return True, ""
    
    @staticmethod
    def validate_message(message: str) -> Tuple[bool, str]:
        """
        Validate message content
        Returns (is_valid, error_message)
        """
        if not message:
            return False, "Message is required"
        
        message = message.strip()
        
        if len(message) < 10:
            return False, "Message must be at least 10 characters long"
        
        if len(message) > 2000:
            return False, "Message must be less than 2000 characters"
        
        return True, ""
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        Sanitize text input to prevent XSS attacks
        """
        if not text:
            return ""
        
        # Strip whitespace
        text = text.strip()
        
        # Escape HTML entities
        text = html.escape(text)
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        return text
    
    @staticmethod
    def validate_contact_form(name: str, email: str, subject: str, message: str) -> Dict[str, str]:
        """
        Validate entire contact form
        Returns dictionary of field errors
        """
        errors = {}
        
        # Validate name
        is_valid, error = InputValidator.validate_name(name)
        if not is_valid:
            errors['name'] = error
        
        # Validate email
        is_valid, error = InputValidator.validate_email(email)
        if not is_valid:
            errors['email'] = error
        
        # Validate subject
        is_valid, error = InputValidator.validate_subject(subject)
        if not is_valid:
            errors['subject'] = error
        
        # Validate message
        is_valid, error = InputValidator.validate_message(message)
        if not is_valid:
            errors['message'] = error
        
        return errors
    
    @staticmethod
    def sanitize_contact_form(name: str, email: str, subject: str, message: str) -> Dict[str, str]:
        """
        Sanitize all contact form inputs
        """
        return {
            'name': InputValidator.sanitize_input(name),
            'email': InputValidator.sanitize_input(email),
            'subject': InputValidator.sanitize_input(subject),
            'message': InputValidator.sanitize_input(message)
        }
    
    @staticmethod
    def is_safe_url(url: str) -> bool:
        """
        Check if URL is safe (basic validation)
        """
        if not url:
            return False
        
        # Allow only http/https protocols
        allowed_protocols = ['http://', 'https://']
        if not any(url.startswith(protocol) for protocol in allowed_protocols):
            return False
        
        # Basic domain validation
        try:
            from urllib.parse import urlparse
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def validate_github_username(username: str) -> Tuple[bool, str]:
        """
        Validate GitHub username format
        Returns (is_valid, error_message)
        """
        if not username:
            return False, "Username is required"
        
        username = username.strip()
        
        # GitHub username rules
        if len(username) > 39:
            return False, "Username must be 39 characters or less"
        
        if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', username):
            return False, "Username may only contain alphanumeric characters or hyphens"
        
        if username.startswith('-') or username.endswith('-'):
            return False, "Username cannot begin or end with a hyphen"
        
        if '--' in username:
            return False, "Username cannot contain consecutive hyphens"
        
        return True, ""

class SecurityValidator:
    """Advanced security validation utilities"""
    
    @staticmethod
    def check_sql_injection(text: str) -> bool:
        """
        Basic SQL injection pattern detection
        Returns True if potentially dangerous patterns are found
        """
        if not text:
            return False
        
        text_lower = text.lower()
        
        # Common SQL injection patterns
        dangerous_patterns = [
            'union select', 'drop table', 'delete from', 'insert into',
            'update set', 'exec ', 'execute ', '--', '/*', '*/',
            'script>', '<script', 'javascript:', 'vbscript:',
            'onload=', 'onerror=', 'onclick='
        ]
        
        return any(pattern in text_lower for pattern in dangerous_patterns)
    
    @staticmethod
    def check_xss_patterns(text: str) -> bool:
        """
        Basic XSS pattern detection
        Returns True if potentially dangerous patterns are found
        """
        if not text:
            return False
        
        text_lower = text.lower()
        
        # Common XSS patterns
        xss_patterns = [
            '<script', '</script>', 'javascript:', 'vbscript:',
            'onload=', 'onerror=', 'onclick=', 'onmouseover=',
            'onfocus=', 'onblur=', 'onchange=', 'onsubmit=',
            'data:', 'blob:', 'eval(', 'expression('
        ]
        
        return any(pattern in text_lower for pattern in xss_patterns)
    
    @staticmethod
    def is_safe_content(text: str) -> Tuple[bool, str]:
        """
        Comprehensive content safety check
        Returns (is_safe, reason)
        """
        if not text:
            return True, ""
        
        # Check for SQL injection patterns
        if SecurityValidator.check_sql_injection(text):
            return False, "Content contains potentially dangerous SQL patterns"
        
        # Check for XSS patterns
        if SecurityValidator.check_xss_patterns(text):
            return False, "Content contains potentially dangerous script patterns"
        
        # Check content length (prevent DoS)
        if len(text) > 10000:
            return False, "Content is too long"
        
        return True, ""