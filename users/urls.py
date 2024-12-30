# users/urls.py
from django.urls import path
from .views import register, user_login, home, create_customer, forgot_password, reset_password  # Importing the views

# URLs for the users app
urlpatterns = [
    path('register/', register, name='register'),  # User registration path
    path('login/', user_login, name='login'),      # Login path
    path('', home, name='home'),                   # Home path
    path('customer/add/', create_customer, name='add_customer'),  # Add new customer
    path('forgot_password/', forgot_password, name='forgot_password'),  # Forgot password
    path('reset_password/', reset_password, name='reset_password'),  # Reset password
]
