# users/validators.py
import hmac
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
import re

User = get_user_model()

class CustomPasswordValidator:
    """Validator for password strength."""
    def __init__(self, config):
        self.min_length = config.get("min_password_length", 10)
        self.require_uppercase = config["password_requirements"].get("uppercase", True)
        self.require_lowercase = config["password_requirements"].get("lowercase", True)
        self.require_digits = config["password_requirements"].get("digits", True)
        self.require_special = config["password_requirements"].get("special_characters", True)
        self.dictionary_check = config.get("dictionary_check", True)

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _(f"Password must be at least {self.min_length} characters long."),
                code='password_too_short',
            )
        
        if self.require_uppercase and not any(c.isupper() for c in password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter."),
                code='password_no_upper',
            )
        
        if self.require_lowercase and not any(c.islower() for c in password):
            raise ValidationError(
                _("Password must contain at least one lowercase letter."),
                code='password_no_lower',
            )
        
        if self.require_digits and not any(c.isdigit() for c in password):
            raise ValidationError(
                _("Password must contain at least one digit."),
                code='password_no_digit',
            )
        
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code='password_no_special',
            )
        
        if self.dictionary_check:
            common_passwords = ["123456", "password", "qwerty"]  # ניתן להרחיב רשימה זו
            if password.lower() in common_passwords:
                raise ValidationError(
                    _("Password cannot be a common password."),
                    code='password_in_dictionary',
                )

    def get_help_text(self):
        return _(
            f"Your password must be at least {self.min_length} characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
        )

class PasswordHistoryValidator:
    """Validator to prevent reuse of recent passwords."""
    def __init__(self, config):
        self.password_history = config.get("password_history", 3)
    
    def validate(self, password, user=None):
        if user:
            recent_passwords = user.password_history[-self.password_history:]
            for old_password in recent_passwords:
                try:
                    old_salt, old_hash = old_password.split('$')
                    entered_hash = hmac.new(old_salt.encode(), password.encode(), hashlib.sha256).hexdigest()
                    if hmac.compare_digest(old_hash, entered_hash):
                        raise ValidationError(
                            _(f"Password cannot match the last {self.password_history} passwords."),
                            code='password_used_before',
                        )
                except ValueError:
                    continue  # אם הפורמט אינו תקין, לדלג

    def get_help_text(self):
        return _(
            f"Your password cannot be the same as any of your last {self.password_history} passwords."
        )
