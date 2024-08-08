from django.contrib import admin
from .models import CustomUser, OrganizationProfile, Profile, Experience, Education, ContactRequest, School

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(OrganizationProfile)
admin.site.register(School)

