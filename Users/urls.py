from django.contrib.auth import views as auth_views
from django.urls import path, include

from .views import *

app_name = "Users"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("profile/", profile, name="profile"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    path('register/', register, name='register'),
    path('add_poems/', add_poems, name='add_poems'),
     #path('edit_poems/<int:pk>', edit_poems, name='edit_poems'),
    path('read_poems/', read_poems, name='read_poems'),
    path('my_account/', profile_view, name='my_account'),
]
