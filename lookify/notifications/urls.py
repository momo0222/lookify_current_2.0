from django.urls import path
from . import views

urlpatterns = [
    path('mark_as_read/', views.mark_as_read, name='mark_as_read'),
]
