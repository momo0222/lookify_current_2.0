from django.urls import path
from . import views
urlpatterns = [
    path("create/", views.opportunity, name="create-opp"),
    path("", views.opportunity_home, name="opportunity-home"),
    path("<int:pk>/", views.post_detail, name="post-detail"),
    path("delete/<int:pk>/", views.delete_opportunity, name="delete-opportunity"),
    path("data", views.data, name="data"),
    path("like/<int:pk>/", views.like_opportunity, name="likes"),
    path("apply/<int:pk>/", views.apply_opportunity, name="apply"),
    
]
