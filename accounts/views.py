from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.forms import (  # Add these imports
    AuthenticationForm,
    PasswordResetForm,
     UserCreationForm,
    SetPasswordForm
)

from registration.forms import UserRegistrationForm, LoginForm
from registration.models import User
from website.models import Category




def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your school information.')
            return redirect('school_info')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    category = Category.objects.all()
    context={
            'cat':category,
            'form': form,
        }
    return render(request, 'accounts/login.html', context)
# 

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')



from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
# from .forms import PasswordResetForm

User = get_user_model()



def password_reset_request(request):
    # Redirect authenticated users (optional)
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect(settings.LOGIN_REDIRECT_URL)
    
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email__iexact=email)
            
            if associated_users.exists():
                for user in associated_users:
                    # Prepare email context
                    context = {
                        "email": user.email,
                        "domain": getattr(settings, "SITE_DOMAIN", request.get_host()),
                        "site_name": getattr(settings, "SITE_NAME", "Your Site"),
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "https" if request.is_secure() else "http",
                    }

                    # Render email content
                    subject = render_to_string(
                        "registration/password_reset_subject.txt",
                        context
                    ).strip()
                    
                    email_content = render_to_string(
                        "registration/password_reset_email.html",
                        context
                    )

                    # Send email
                    try:
                        send_mail(
                            subject,
                            email_content,
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            fail_silently=False,
                            html_message=email_content
                        )
                    except Exception as e:
                        messages.error(
                            request,
                            f"An error occurred while sending the password reset email. Please try again later."
                        )
                        # Log the error for debugging
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.error(f"Password reset email error: {str(e)}")
                        return redirect(reverse('password_reset'))

                messages.success(
                    request,
                    "We've emailed you instructions for setting your password. "
                    "If you don't receive an email, please check your spam folder."
                )
                return redirect(reverse('password_reset_done'))
            
            # Always show success message even if email doesn't exist (security best practice)
            messages.success(
                request,
                "If that email address exists in our system, we've sent password reset instructions."
            )
            return redirect(reverse('password_reset_done'))
    else:
        form = PasswordResetForm()

    return render(
        request,
        "registration/password_reset_form.html",
        {"form": form}
    )

# def password_reset_request(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)  # Now properly defined
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             associated_users = User.objects.filter(email=email)
#             if associated_users.exists():
#                 for user in associated_users:
#                     subject = "Password Reset Requested"
#                     email_template_name = "accounts/password_reset_email.html"
#                     c = {
#                         "email": user.email,
#                         'domain': settings.SITE_DOMAIN,
#                         'site_name': 'School Contest',
#                         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                         "user": user,
#                         'token': default_token_generator.make_token(user),
#                         'protocol': 'https' if request.is_secure() else 'http',
#                     }
#                     email = render_to_string(email_template_name, c)
#                     try:
#                         send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
#                     except Exception as e:
#                         messages.error(request, f'Error sending email: {e}')
#                         return redirect('password_reset')
#                     messages.success(request, 'Password reset email has been sent.')
#                     return redirect('password_reset_done')
#     else:
#         form = PasswordResetForm()
#     return render(request, "accounts/password_reset.html", {"form": form})