"""
Utility module for encoding and decoding IDs in URLs
Uses Hashids to obfuscate integer IDs and prevent enumeration attacks

Usage:
    from sms.utils.id_encoder import encode_id, decode_id
    
    # In views
    encoded = encode_id(123)  # Returns: 'Xdr9k'
    decoded = decode_id('Xdr9k')  # Returns: 123
    
    # In templates
    {% load id_encoder %}
    {{ object.id|encode_id }}
"""

from hashids import Hashids
from django.conf import settings

# Get salt from settings or use default
HASHIDS_SALT = getattr(settings, 'HASHIDS_SALT', 'your-secret-salt-change-in-production')
HASHIDS_MIN_LENGTH = getattr(settings, 'HASHIDS_MIN_LENGTH', 8)
HASHIDS_ALPHABET = getattr(settings, 'HASHIDS_ALPHABET', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')

# Initialize Hashids
hashids = Hashids(
    salt=HASHIDS_SALT,
    min_length=HASHIDS_MIN_LENGTH,
    alphabet=HASHIDS_ALPHABET
)


def encode_id(id_value):
    """
    Encode an integer ID to a hash string
    
    Args:
        id_value: Integer ID to encode
        
    Returns:
        String hash (e.g., 'jR7qKm3p')
        
    Example:
        >>> encode_id(123)
        'jR7qKm3p'
    """
    if id_value is None:
        return None
    
    try:
        return hashids.encode(int(id_value))
    except (ValueError, TypeError):
        return None


def decode_id(hash_value):
    """
    Decode a hash string back to integer ID
    
    Args:
        hash_value: String hash to decode
        
    Returns:
        Integer ID or None if invalid
        
    Example:
        >>> decode_id('jR7qKm3p')
        123
    """
    if not hash_value:
        return None
    
    try:
        decoded = hashids.decode(str(hash_value))
        return decoded[0] if decoded else None
    except (IndexError, AttributeError):
        return None


def encode_multiple(*ids):
    """
    Encode multiple IDs into a single hash
    
    Args:
        *ids: Variable number of integer IDs
        
    Returns:
        String hash representing all IDs
        
    Example:
        >>> encode_multiple(123, 456, 789)
        'AgR7qKm3pXy8'
    """
    try:
        return hashids.encode(*[int(i) for i in ids])
    except (ValueError, TypeError):
        return None


def decode_multiple(hash_value):
    """
    Decode a hash string back to multiple IDs
    
    Args:
        hash_value: String hash to decode
        
    Returns:
        Tuple of integers or empty tuple if invalid
        
    Example:
        >>> decode_multiple('AgR7qKm3pXy8')
        (123, 456, 789)
    """
    if not hash_value:
        return ()
    
    try:
        return hashids.decode(str(hash_value))
    except AttributeError:
        return ()
