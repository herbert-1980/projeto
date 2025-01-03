from django.urls import path
from django.contrib.auth import views as auth_views
from apps.accounts import views
from apps.accounts.views import success, complete_user_profile_view


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('update_my_user/', views.update_my_user, name='update_my_user'),
    path('update_user/<slug:username>/', views.update_user, name='update_user'),
    path('register/', views.register_view, name='register'),
    path('complete-profile/', complete_user_profile_view, name='complete_user_profile'),
    path('success/', success, name='success'),
    path('logout/', views.logout_view, name='logout'),
    path('timeout/', views.timeout_view, name='timeout'),
    path('user_list/', views.list_users, name='user_list'),
    path('user_add/',  views.user_add, name='user_add'),
    path('complete_user_profile/<int:user_id>/', views.complete_user_profile, name='complete_user_profile'),
    path('accounts/password_reset/', views.password_reset_view, name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
