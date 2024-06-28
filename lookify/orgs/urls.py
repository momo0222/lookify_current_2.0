from django.urls import path
from . import views

urlpatterns = [
    path('', views.org_home, name="org-home")
]
