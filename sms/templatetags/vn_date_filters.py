"""
Custom template filters for Vietnamese date and currency formatting
"""
from django import template
from django.template.defaultfilters import date as django_date_filter
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter(name='vn_date')
def vn_date(value, arg='d/m/Y'):
    """
    Format a date using Vietnamese format (dd/mm/yyyy by default).
    
    Usage in templates:
        {{ some_date|vn_date }}  # Returns dd/mm/yyyy
        {{ some_date|vn_date:'d/m/Y H:i' }}  # Returns dd/mm/yyyy HH:MM
    """
    if not value:
        return ''
    return django_date_filter(value, arg)


@register.filter(name='vn_datetime')
def vn_datetime(value):
    """
    Format a datetime using Vietnamese format (dd/mm/yyyy HH:MM).
    
    Usage in templates:
        {{ some_datetime|vn_datetime }}
    """
    if not value:
        return ''
    return django_date_filter(value, 'd/m/Y H:i')


@register.filter(name='vn_short_date')
def vn_short_date(value):
    """
    Format a date using short Vietnamese format (dd/mm/yy).
    
    Usage in templates:
        {{ some_date|vn_short_date }}
    """
    if not value:
        return ''
    return django_date_filter(value, 'd/m/y')


@register.filter(name='vn_currency')
def vn_currency(value):
    """
    Format a number as Vietnamese currency with comma separators.
    Simple implementation without locale dependency.
    
    Usage in templates:
        {{ amount|vn_currency }}  # Returns 1,000,000
        {{ amount|vn_currency }} VNĐ  # Returns 1,000,000 VNĐ
    """
    if value is None or value == '':
        return '0'
    try:
        # Convert to int first to remove decimals
        num = int(float(value))
        # Format with comma separator using Python's format
        return "{:,}".format(num)
    except (ValueError, TypeError):
        return str(value)


@register.filter(name='vnd')
def vnd(value):
    """
    Format a number as Vietnamese currency with VNĐ suffix.
    Simple implementation without locale dependency.
    
    Usage in templates:
        {{ amount|vnd }}  # Returns 1,000,000 VNĐ
    """
    if value is None or value == '':
        return '0 VNĐ'
    try:
        num = int(float(value))
        formatted = "{:,}".format(num)
        return f"{formatted} VNĐ"
    except (ValueError, TypeError):
        return f"{value} VNĐ"
