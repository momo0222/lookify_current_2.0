from .models import Notifications

def notification_context_processor(request):
    if request.user.is_authenticated:
        notifs = Notifications.objects.filter(user_revoker=request.user, is_read=False).order_by('-created_at')
        notifs_count = notifs.count()

        return {
            'notifs': notifs,
            'notifs_count': notifs_count
        }
    else:
        return{
            "notifs": [],
            'notifs_count': 0
        }
