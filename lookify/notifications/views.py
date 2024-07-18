from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notifications
from django.http import JsonResponse
@login_required
def notification_view(request):
    return render(request, 'notifications/notification_list.html')
def mark_as_read(request):
    if request.method == 'POST':
        notification_ids = request.POST.getlist('notification_ids[]')
        notifications = Notifications.objects.filter(id__in=notification_ids, user_revoker=request.user, is_read=False)
        notifications.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

def send_notification(request, sender, receiver, type):
    notification = Notifications.objects.create(
        user_sender=sender,
        user_revoker=receiver,
        status="unread",
        type_of_notification=type
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{receiver.id}',
        {
            'type': 'send_notification',
            'notification': {
                'id': notification.id,
                'sender': sender.username,
                'receiver': receiver.username,
                'created_at': str(notification.created_at),
                'status': notification.status,
                'type_of_notification': notification.type_of_notification,
            }
        }
    )

