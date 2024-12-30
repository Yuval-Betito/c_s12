# users/validators.py
import hmac
import hashlib
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class CustomPasswordValidator:
    """Validator for password strength."""
    def __init__(self, min_length, require_uppercase, require_lowercase, require_digits, require_special_characters, dictionary_check):
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digits = require_digits
        self.require_special_characters = require_special_characters
        self.dictionary_check = dictionary_check

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
        
        if self.require_special_characters and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code='password_no_special',
            )
        
        if self.dictionary_check:
            common_passwords = ["123456", "password", "qwerty"]  # ניתן להוסיף עוד
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
    def __init__(self, password_history):
        self.password_history = password_history
    
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
