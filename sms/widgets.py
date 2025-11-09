"""
Custom widgets for forms with Vietnamese date format (dd/mm/yyyy)
"""
from django import forms


class VietnameseDateInput(forms.DateInput):
    """
    Custom DateInput widget with dd/mm/yyyy format.
    Uses HTML5 date input type but with Vietnamese format support.
    """
    input_type = 'date'
    format_key = 'DATE_INPUT_FORMATS'
    
    def __init__(self, attrs=None, format=None):
        default_attrs = {'class': 'form-control', 'type': 'date'}
        if attrs:
            default_attrs.update(attrs)
        # Use dd/mm/yyyy format by default
        super().__init__(attrs=default_attrs, format=format or '%d/%m/%Y')


class VietnameseDateTimeInput(forms.DateTimeInput):
    """
    Custom DateTimeInput widget with Vietnamese datetime format.
    """
    input_type = 'datetime-local'
    format_key = 'DATETIME_INPUT_FORMATS'
    
    def __init__(self, attrs=None, format=None):
        default_attrs = {'class': 'form-control', 'type': 'datetime-local'}
        if attrs:
            default_attrs.update(attrs)
        # HTML5 datetime-local uses ISO format internally: YYYY-MM-DDTHH:MM
        super().__init__(attrs=default_attrs, format=format or '%Y-%m-%dT%H:%M')
