# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('password-change-done/', views.password_change_done, name='password_change_done'),
    path('create-customer/', views.create_customer, name='create_customer'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
