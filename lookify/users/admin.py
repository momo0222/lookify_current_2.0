from django.contrib import admin
from .models import CustomUser, OrganizationProfile, Profile, Experience, Education, ContactRequest

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(ContactRequest)

