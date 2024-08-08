from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='users-home'),
    path('register/',views.RegisterView.as_view(), name='users-register'),
    path('profile/<str:username>', views.profile_view, name='profile-view'),
    path('find_users/', views.user_search, name="find-users"),
    path('ajax/school-search/', views.SchoolAjaxView.as_view(), name='school_ajax_search'),
    path("school/add",views.addSchool,name="add-school"),
    path('login/modal', views.ModalSignInView.as_view(), name="signin-modal"),
    path('update/indv', views.ProfileUpdate.as_view(), name='update_profile'),
    path('update/org', views.OrgProfileUpdate.as_view(), name='update-org-profile'),
    path('submit_message/<str:receiver>', views.submitContact, name="submit_message"),
    path("create_exp/", views.expo, name="create-exp"),
    path("create_edu/", views.edu, name="create-edu"),
    path("check_username/", views.check_username, name="check-username"),
    path("check_email/", views.check_email, name="check-email"),
    path("tutorial/", views.tutorial, name="tutorial"),
    path("sendtest", views.send_lookify_email, name="send-lookify-email"),
    path("password_reset", views.password_reset,name="password-reset" ),
    path('password_reset/done/', TemplateView.as_view(template_name="users/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', TemplateView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

