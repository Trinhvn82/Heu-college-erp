from .models import Notification

def notifications_context(request):
    if not request.user.is_authenticated:
        return {
            'unread_notifications_count': 0,
            'recent_notifications': []
        }
    qs = Notification.objects.filter(user=request.user, is_read=False)
    return {
        'unread_notifications_count': qs.count(),
        'recent_notifications': Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    }
