from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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

    

