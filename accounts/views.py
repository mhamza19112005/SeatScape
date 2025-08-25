from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
# import requests
import json

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')

def AuthPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    context = {'active_tab': 'login'}
    
    if request.method == 'POST':
        action = request.POST.get('action')
        # Preserve ?next redirects if provided
        next_url = request.POST.get('next') or request.GET.get('next')
        
        if action == 'login':
            username = (request.POST.get('username') or '').strip()
            # support either "password" or legacy "pass" field name
            password = request.POST.get('password') or request.POST.get('pass') or ''
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url or 'home')
            else:
                messages.error(request, 'Invalid username or password.')
                context['active_tab'] = 'login'
                
        elif action == 'signup':
            uname = (request.POST.get('username') or '').strip()
            email = (request.POST.get('email') or '').strip()
            pass1 = request.POST.get('password1') or ''
            pass2 = request.POST.get('password2') or ''
            
            if not uname or not pass1:
                messages.error(request, 'Username and password are required.')
                context['active_tab'] = 'signup'
            elif pass1 != pass2:
                messages.error(request, 'Passwords do not match.')
                context['active_tab'] = 'signup'
            elif User.objects.filter(username=uname).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                context['active_tab'] = 'signup'
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please use a different email or try logging in.')
                context['active_tab'] = 'signup'
            else:
                try:
                    user = User.objects.create_user(uname, email, pass1)
                    login(request, user)
                    messages.success(request, f'Account created successfully! Welcome, {uname}!')
                    return redirect(next_url or 'home')
                except Exception as e:
                    messages.error(request, 'Error creating account. Please try again.')
                    context['active_tab'] = 'signup'
        else:
            messages.error(request, 'Invalid action.')
            context['active_tab'] = 'login'
    
    return render(request, 'auth.html', context)

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                # Generate password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Create reset link
                reset_url = request.build_absolute_uri(
                    f'/reset-password/{uid}/{token}/'
                )
                
                # Send email
                subject = 'Password Reset Request - SeatScape'
                message = f'''
Hello {user.username},

You requested a password reset for your SeatScape account.

Click the link below to reset your password:
{reset_url}

⚠️  IMPORTANT: This link will expire in 2 minute for security reasons.

If you didn't request this password reset, please ignore this email.

Best regards,
SeatScape Team
                '''
                
                try:
                    from django.core.mail import send_mail
                    send_mail(
                        subject,
                        message,
                        'mhamza19112005@gmail.com',  # From email
                        [email],  # To email
                        fail_silently=False,
                    )
                    messages.success(request, f'Password reset link has been sent to {email}. Please check your email.')
                except Exception as e:
                    # Fallback for development - show link in console
                    print(f"Password reset link for {email}: {reset_url}")
                    messages.info(request, f'Password reset link sent! Check your console/terminal for the link.')
                
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email address.')
        else:
            messages.error(request, 'Please enter your email address.')
    
    return render(request, 'forget_password.html')

def reset_password(request, uidb64, token):
    try:
        from django.utils.http import urlsafe_base64_decode
        from django.utils import timezone
        from datetime import timedelta
        
        uid = urlsafe_base64_decode(uidb64)
        if isinstance(uid, bytes):
            uid = uid.decode()
        user = User.objects.get(pk=uid)
        
        # Check if token is valid and not expired
        if default_token_generator.check_token(user, token):
            # Check if token is expired (2 minute)
            from django.conf import settings
            timeout_seconds = getattr(settings, 'PASSWORD_RESET_TIMEOUT', 120)
            
            # Get the time when the token was created (we'll use a simple approach)
            # In production, you might want to store token creation time in database
            token_age = timezone.now() - timedelta(seconds=timeout_seconds)
            
            # For now, we'll use Django's built-in token validation
            # The token_generator.check_token already handles expiration based on PASSWORD_RESET_TIMEOUT
            if request.method == 'POST':
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                
                if password1 and password2 and password1 == password2:
                    user.set_password(password1)
                    user.save()
                    messages.success(request, 'Password reset successfully! You can now login with your new password.')
                    return redirect('login')
                else:
                    messages.error(request, 'Passwords do not match.')
            
            return render(request, 'reset_password.html')
        else:
            messages.error(request, 'Invalid reset link.')
            return redirect('login')
            
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid reset link.')
        return redirect('login')

# Keep old endpoints working by redirecting to the unified page
def LoginPage(request):
    return redirect('auth')

def SignupPage(request):
    return redirect('auth')

def LogoutPage(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
