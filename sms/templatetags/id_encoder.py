"""
Django template tags for encoding/decoding IDs in templates

Usage in templates:
    {% load id_encoder %}
    
    {# Encode an ID #}
    <a href="{% url 'bill_detail' bill_id=bill.id|encode_id %}">View Bill</a>
    
    {# Or in URL reverse #}
    {{ bill.id|encode_id }}
"""

from django import template
from sms.utils.id_encoder import encode_id, decode_id

register = template.Library()


@register.filter(name='encode_id')
def encode_id_filter(value):
    """
    Template filter to encode an integer ID
    
    Usage:
        {{ bill.id|encode_id }}
    """
    return encode_id(value)


@register.filter(name='decode_id')  
def decode_id_filter(value):
    """
    Template filter to decode a hash string
    
    Usage:
        {{ hash_string|decode_id }}
    """
    return decode_id(value)


@register.simple_tag
def encode_url_id(id_value):
    """
    Template tag to encode an ID for use in URLs
    
    Usage:
        {% encode_url_id bill.id %}
    """
    return encode_id(id_value) or ''


@register.simple_tag
def decode_url_id(hash_value):
    """
    Template tag to decode a hash from URL
    
    Usage:
        {% decode_url_id request.GET.id %}
    """
    return decode_id(hash_value) or ''
