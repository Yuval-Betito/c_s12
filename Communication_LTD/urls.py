# Communication_LTD/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('axes/', include('axes.urls')),  # הוספת נתיב של django-axes
    path('', include('users.urls')),      # נתיבים של האפליקציה users
]
