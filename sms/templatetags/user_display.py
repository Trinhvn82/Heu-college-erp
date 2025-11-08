from django import template

register = template.Library()

@register.simple_tag
def display_name(user):
    """Return the best human-friendly name for a user.
    Priority: full name (first_name + last_name) -> username.
    """
    if not user:
        return ""
    try:
        full = user.get_full_name()
    except Exception:
        full = ""
    if full:
        return full
    # Fallback to username
    return getattr(user, 'username', '') or ''
