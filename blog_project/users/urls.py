from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<int:id>/', views.profile_view, name='profile'),
    path('profile/<int:id>/follow/', views.follow_user, name='follow_user'),
    path('profile/<int:id>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]