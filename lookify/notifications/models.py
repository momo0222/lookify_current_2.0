from django.db import models


from django.conf import settings


# Create your models here.
class Notifications(models.Model):
    user_sender=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,related_name='user_sender',on_delete=models.CASCADE)
    user_revoker=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,related_name='user_revoker',on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    type_of_notification=models.CharField(max_length=264,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    