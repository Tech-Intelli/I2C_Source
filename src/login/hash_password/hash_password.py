"""
Module for password hashing

Returns:
    _Hash: Hashed password
"""

import hashlib


def hash_password(password):
    """Hashes the password

    Returns:
        _Hash: Returns the password hash
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
