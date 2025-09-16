
from django.urls import path
from . import views
# Password reset modules
from django.contrib.auth import views as auth_views


# Create your urls here

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('signup/', views.Signup, name='signup'),
    path('verify/email', views.verify_view, name='verify_email'),
    path('profile/', views.ProfileView, name='profile'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/search/user', views.search_user, name='search_user'),
    path('profile/<str:username>/', views.retrive_user_profile, name='other_users'),
    path('profile/delete/', views.delete_profile, name="delete_profile"),
    path('account/delete', views.delete_account, name='delete_account'),
    path('user/activate/account/<uidb64>/<token>/', views.ActivateView, name='activate'),
    
    # password reset
    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='reset_password'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name='password_reset_complete'),
]