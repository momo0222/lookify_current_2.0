from django.urls import path
from . import views
urlpatterns = [
    path("", views.dash, name="user-dash"),
    path("manage", views.opportunity_manager, name="opportunity-manager"),
    path("manage_exp", views.exp_manager, name="exp-manager"),
    path("manage_edu", views.edu_manager, name="edu-manager"),
    path("applications/<int:pk>", views.application_list, name="manage-application-list"),
    path("app/accept/<int:pk>", views.application_approve, name="accept-app"),
    path("app/deny/<int:pk>", views.application_reject, name="deny-app"),
    path("inbox", views.inbox, name="inbox"),
    path("delete_exp/<int:pk>/", views.delete_exp, name="delete-exp"),
    path("applied", views.application_manager, name="application-manager"),
path("delete_edu/<int:pk>/", views.delete_edu, name="delete-edu"),
]
