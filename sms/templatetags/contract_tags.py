from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Canonical mapping for contract status derived from HouseRenter.active boolean.
# If later a multi-state field is added, extend this map.
STATUS_MAP = {
    True: {
        "label": "Đang hiệu lực",
        "short": "ACTIVE",
        "css": "success",
        "icon": "fa-check-circle"
    },
    False: {
        "label": "Không khả dụng",
        "short": "INACTIVE",
        "css": "secondary",
        "icon": "fa-ban"
    }
}

@register.simple_tag
def contract_status(contract):
    """Return dict with label, short, css, icon for a HouseRenter contract object.
    Usage: {% contract_status contract as st %} then st.label, st.css
    """
    if contract is None:
        return {"label": "Không xác định", "short": "UNKNOWN", "css": "dark", "icon": "fa-question-circle"}
    return STATUS_MAP.get(getattr(contract, 'active', False), STATUS_MAP[False])

@register.simple_tag
def contract_badge(contract):
    """Render a Bootstrap badge for contract status."""
    st = contract_status(contract)
    html = f'<span class="badge bg-{st["css"]}"><i class="fas {st["icon"]} me-1"></i>{st["label"]}</span>'
    return mark_safe(html)
