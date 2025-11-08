"""
Custom Django path converter for Hashids
Allows using encoded IDs directly in URL patterns

Usage in urls.py:
    from sms.utils.hashid_converter import HashidConverter
    from django.urls import register_converter
    
    register_converter(HashidConverter, 'hashid')
    
    urlpatterns = [
        path('bill/<hashid:bill_id>/detail/', views.bill_detail, name='bill_detail'),
    ]
"""

from .id_encoder import decode_id, encode_id
from django.conf import settings


class HashidConverter:
    """
    Django URL converter for Hashids
    Automatically converts between hash strings and integer IDs
    """
    # Match hash strings using configured minimum length; restrict to alphanumerics
    _min_len = getattr(settings, 'HASHIDS_MIN_LENGTH', 8)
    regex = f"[A-Za-z0-9]{{{_min_len},}}"
    
    def to_python(self, value):
        """
        Convert URL hash string to Python integer
        
        Args:
            value: Hash string from URL
            
        Returns:
            Integer ID
            
        Raises:
            ValueError: If hash is invalid
        """
        decoded = decode_id(value)
        if decoded is None:
            raise ValueError(f"Invalid hashid: {value}")
        return decoded
    
    def to_url(self, value):
        """
        Convert Python integer to URL hash string
        
        Args:
            value: Integer ID
            
        Returns:
            Hash string for URL
        """
        encoded = encode_id(value)
        if encoded is None:
            raise ValueError(f"Cannot encode ID: {value}")
        return encoded
