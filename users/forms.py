# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, Customer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re

# טופס רישום משתמש
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email address already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# טופס שינוי סיסמה מותאם
class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        try:
            validate_password(new_password1, self.user)
        except ValidationError as e:
            self.add_error('new_password1', e)
        return new_password1

# טופס איפוס סיסמה מותאם
class ResetPasswordForm(forms.Form):
    token = forms.CharField(max_length=100, required=True, label="Reset Token")
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password",
        help_text="Your password must be at least 10 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password"
    )
    
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        try:
            validate_password(password1, self.user)
        except ValidationError as e:
            raise ValidationError(e)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            self.add_error('new_password2', "Passwords do not match.")
        return cleaned_data

# טופס ליצירת לקוח חדש
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'customer_id', 'phone_number', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ערך ברירת מחדל לשדה phone_number
        self.fields['phone_number'].widget.attrs.update({'placeholder': '05xxxxxxxx'})
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^05\d{8}$', phone_number):
            raise ValidationError("Phone number must start with '05' and be followed by 8 digits.")
        return phone_number

    def save(self, commit=True):
        customer = super().save(commit=False)
        if commit:
            customer.save()
        return customer

