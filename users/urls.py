from django.urls import path
from .views import register, user_login, home, create_customer, forgot_password, reset_password  # ייבוא הפונקציות מ-views

# URLs עבור האפליקציה users
urlpatterns = [
    path('register/', register, name='register'),  # נתיב לרישום משתמשים חדשים
    path('login/', user_login, name='login'),      # נתיב לכניסה למערכת
    path('', home, name='home'),                   # דף הבית (נתיב ריק)
    path('customer/add/', create_customer, name='add_customer'),  # הוספת לקוח חדש
    path('forgot_password/', forgot_password, name='forgot_password'),  # שכחתי סיסמה
    path('reset_password/', reset_password, name='reset_password'),  # איפוס סיסמה
]
