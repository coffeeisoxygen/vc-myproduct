"""
Utility modules for vc-myproduct application.

This package contains various utility modules:
- logger: Logging with colored console output and file rotation
- encrypt: Encryption/decryption using hardware-bound keys
"""

# Expose main functions for direct import
from app.utils.encrypt import decrypt, encrypt
from app.utils.logger import get_logger

__all__ = ["get_logger", "encrypt", "decrypt"]

# Package information
__version__ = "0.1.0"
