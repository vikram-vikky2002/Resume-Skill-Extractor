"""
Configuration file for application credentials and settings
"""

# Default admin credentials
ADMIN_USERNAME = "hradmin"
ADMIN_PASSWORD = "hradmin123"  # In production, this should be stored securely, not hardcoded

# Session state keys
SESSION_AUTHENTICATED = "authenticated"
SESSION_USERNAME = "username"

# Authentication settings
AUTH_TIMEOUT_MINUTES = 30  # Session timeout in minutes
