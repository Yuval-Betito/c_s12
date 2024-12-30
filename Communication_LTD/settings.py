from pathlib import Path
import os
import json

# בסיס הפרויקט
BASE_DIR = Path(__file__).resolve().parent.parent

# סודי - ודאי לשמור על סודיות המפתח הזה ולא לחשוף אותו בקוד פומבי
SECRET_KEY = "django-insecure-gl=b&u71jf7ix(s^b^+y8^!eiubw&i43$r+l%)yhw#!fju)(p@"

# מצב פיתוח - יש לשנות ל-False בייצור
DEBUG = True

ALLOWED_HOSTS = []  # יש לעדכן את זה עם הדומיינים שלך בייצור

# אפליקציות מותקנות
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",  # האפליקציה users
    "axes",   # התקנת django-axes להגבלת ניסיונות הכניסה
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",  # הוספת AxesMiddleware
]

# כתובות URL הראשיות
ROOT_URLCONF = "Communication_LTD.urls"

# תבניות
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],  # תיקיית templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = "Communication_LTD.wsgi.application"

# מסד נתונים
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# מודל משתמש מותאם
AUTH_USER_MODEL = 'users.User'

# הגדרת אימייל - יש לעדכן עם הפרטים שלך
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'  # למשל: 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@communication_ltd.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
DEFAULT_FROM_EMAIL = 'no-reply@communication_ltd.com'

# טעינת קובץ קונפיגורציה לסיסמאות
PASSWORD_CONFIG_PATH = BASE_DIR / 'password_config.json'
if os.path.exists(PASSWORD_CONFIG_PATH):
    with open(PASSWORD_CONFIG_PATH, 'r', encoding='utf-8') as f:
        PASSWORD_CONFIG = json.load(f)
else:
    PASSWORD_CONFIG = {
        "min_password_length": 10,
        "password_requirements": {
            "uppercase": True,
            "lowercase": True,
            "digits": True,
            "special_characters": True
        },
        "password_history": 3,
        "dictionary_check": True,
        "login_attempts": 3
    }

# אבטחת סיסמאות לפי קובץ הקונפיגורציה
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": PASSWORD_CONFIG.get("min_password_length", 10)},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "users.validators.CustomPasswordValidator",
        "OPTIONS": {
            "min_length": PASSWORD_CONFIG.get("min_password_length", 10),
            "require_uppercase": PASSWORD_CONFIG["password_requirements"].get("uppercase", True),
            "require_lowercase": PASSWORD_CONFIG["password_requirements"].get("lowercase", True),
            "require_digits": PASSWORD_CONFIG["password_requirements"].get("digits", True),
            "require_special_characters": PASSWORD_CONFIG["password_requirements"].get("special_characters", True),
            "dictionary_check": PASSWORD_CONFIG.get("dictionary_check", True),
        },
    },
    {
        "NAME": "users.validators.PasswordHistoryValidator",
        "OPTIONS": {
            "password_history": PASSWORD_CONFIG.get("password_history", 3),
        },
    },
]

# שפה וזמן
LANGUAGE_CODE = "he"

TIME_ZONE = "Asia/Jerusalem"

USE_I18N = True

USE_TZ = True

# סטאטיים
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# הגדרות התחברות והתנתקות
LOGIN_REDIRECT_URL = '/'  # דף הבית לאחר התחברות
LOGOUT_REDIRECT_URL = 'login'  # מפנה לדף הלוגין לאחר התנתקות

# אוטומטית שדה ראשי
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# הגדרות django-axes
AXES_FAILURE_LIMIT = PASSWORD_CONFIG.get("login_attempts", 3)  # מספר הניסיונות המקסימלי
AXES_COOLOFF_TIME = 1  # זמן ההמתנה בשעות
AXES_LOCKOUT_CALLABLE = 'axes.handlers.database.AxesDatabaseHandler'  # ניתן להתאים לפי הצורך

