from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, CustomerForm, CustomPasswordChangeForm, ResetPasswordForm
from .models import User
import hashlib
import random
from django.core.mail import send_mail
from django.conf import settings

# פונקציה לשליחת המייל עם הטוקן
def send_reset_email(user, token):
    """Send reset email with the generated token."""
    subject = "Password Reset Request"
    message = f"Use the following token to reset your password: {token}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

# View להתחברות משתמש
def user_login(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'users/login.html')

# View להרשמת משתמש חדש
def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "There was an error in your registration. Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

# View לדף הבית (נדרש התחברות)
@login_required
def home(request):
    """Render the home page"""
    return render(request, 'users/home.html')

# View מותאם אישית לשינוי סיסמא
class CustomPasswordChangeView(PasswordChangeView):
    """Custom view for handling password change"""
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        """Update the session after password change"""
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Your password was changed successfully.")
        return response

# View להצגת הודעת הצלחה לאחר שינוי סיסמא
@login_required
def password_change_done(request):
    """Display password change success message"""
    return render(request, 'users/password_change_done.html')

# View ליצירת לקוח חדש (נדרש התחברות)
@login_required
def create_customer(request):
    """Handle creating a new customer"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f"Customer {customer.firstname} {customer.lastname} added successfully!")
            return redirect('home')
        else:
            messages.error(request, "Error in creating customer. Please check the form fields.")
    else:
        form = CustomerForm()

    return render(request, 'users/create_customer.html', {'form': form})

# View לפעולת שכחת סיסמא
def forgot_password(request):
    """Handle forgot password functionality"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate reset token
            random_value = f"{random.randint(1000, 9999)}{user.username}"
            reset_token = hashlib.sha1(random_value.encode()).hexdigest()
            user.reset_token = reset_token
            user.save()
            
            # Send reset token to email
            send_reset_email(user, reset_token)
            
            messages.success(request, "Reset token sent to your email.")
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
    return render(request, 'users/forgot_password.html')

# View לאיפוס סיסמא
def reset_password(request):
    """Handle reset password functionality"""
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data.get('token')
            new_password = form.cleaned_data.get('new_password1')
            try:
                user = User.objects.get(reset_token=token)
                user.set_password(new_password)
                user.reset_token = None  # Clear the reset token
                user.save()
                messages.success(request, "Password reset successfully.")
                return redirect('login')
            except User.DoesNotExist:
                form.add_error('token', "Invalid reset token.")
    else:
        form = ResetPasswordForm()
    return render(request, 'users/reset_password.html', {'form': form})

