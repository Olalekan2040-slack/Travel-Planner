from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from .models import UserProfile, EmailVerificationOTP, PasswordResetRequest
import random
import string

def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('trips:dashboard')
    
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        phone = request.POST.get('phone', '').strip()
        nationality = request.POST.get('nationality', '').strip()
        interests = request.POST.get('interests', '').strip()
        
        # Validation
        errors = []
        
        if not first_name:
            errors.append('First name is required')
        if not last_name:
            errors.append('Last name is required')
        if not email:
            errors.append('Email is required')
        if not password:
            errors.append('Password is required')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors.append('An account with this email already exists')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/register.html', {
                'form_data': request.POST
            })
        
        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(
                    username=email,  # Use email as username
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=False  # User will be activated after email verification
                )
                
                # Create user profile
                profile = UserProfile.objects.create(
                    user=user,
                    phone=phone,
                    nationality=nationality,
                    interests=interests
                )
                
                # Generate and send OTP
                otp = EmailVerificationOTP.objects.create(user=user)
                send_verification_email(user, otp.otp)
                
                # Store user email in session for verification page
                request.session['verification_email'] = email
                
                messages.success(request, 'Registration successful! Please check your email for verification code.')
                return redirect('accounts:verify_email')
                
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'accounts/register.html', {
                'form_data': request.POST
            })
    
    return render(request, 'accounts/register.html')

def verify_email(request):
    """Email verification view"""
    if request.user.is_authenticated:
        return redirect('trips:dashboard')
    
    email = request.session.get('verification_email')
    if not email:
        messages.error(request, 'No verification session found. Please register again.')
        return redirect('accounts:register')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp', '').strip()
        
        if not otp_code:
            messages.error(request, 'Please enter the verification code')
            return render(request, 'accounts/verify_email.html', {'email': email})
        
        try:
            user = User.objects.get(email=email)
            otp = EmailVerificationOTP.objects.filter(
                user=user, 
                otp=otp_code, 
                is_used=False
            ).first()
            
            if not otp:
                messages.error(request, 'Invalid verification code')
                return render(request, 'accounts/verify_email.html', {'email': email})
            
            if otp.is_expired():
                messages.error(request, 'Verification code has expired. Please request a new one.')
                return render(request, 'accounts/verify_email.html', {'email': email})
            
            # Activate user and mark OTP as used
            user.is_active = True
            user.save()
            
            profile = user.userprofile
            profile.is_email_verified = True
            profile.save()
            
            otp.is_used = True
            otp.save()
            
            # Clear session
            if 'verification_email' in request.session:
                del request.session['verification_email']
            
            # Log in the user
            login(request, user)
            
            messages.success(request, 'Email verified successfully! Welcome to GlobeTrek!')
            return redirect('trips:dashboard')
            
        except User.DoesNotExist:
            messages.error(request, 'User not found. Please register again.')
            return redirect('accounts:register')
        except Exception as e:
            messages.error(request, f'Verification failed: {str(e)}')
            return render(request, 'accounts/verify_email.html', {'email': email})
    
    return render(request, 'accounts/verify_email.html', {'email': email})

def resend_otp(request):
    """Resend OTP for email verification"""
    if request.method == 'POST':
        email = request.session.get('verification_email')
        if not email:
            messages.error(request, 'No verification session found.')
            return redirect('accounts:register')
        
        try:
            user = User.objects.get(email=email)
            
            # Mark old OTPs as used
            EmailVerificationOTP.objects.filter(user=user, is_used=False).update(is_used=True)
            
            # Create new OTP
            otp = EmailVerificationOTP.objects.create(user=user)
            send_verification_email(user, otp.otp)
            
            messages.success(request, 'Verification code resent successfully!')
            
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('accounts:register')
        except Exception as e:
            messages.error(request, f'Failed to resend code: {str(e)}')
    
    return redirect('accounts:verify_email')

def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('trips:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Please enter both email and password')
            return render(request, 'accounts/login.html', {'email': email})
        
        # Authenticate user (username is email)
        user = authenticate(request, username=email, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                
                # Redirect to next page or dashboard
                next_page = request.GET.get('next', 'trips:dashboard')
                return redirect(next_page)
            else:
                # User is not activated, redirect to verification
                request.session['verification_email'] = email
                messages.warning(request, 'Your account is not verified. Please verify your email.')
                return redirect('accounts:verify_email')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'accounts/login.html', {'email': email})
    
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    """User logout view"""
    user_name = request.user.get_full_name() or request.user.username
    logout(request)
    messages.success(request, f'Goodbye, {user_name}! You have been logged out successfully.')
    return redirect('core:home')

@login_required
def profile(request):
    """User profile view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        nationality = request.POST.get('nationality', '').strip()
        interests = request.POST.get('interests', '').strip()
        date_of_birth = request.POST.get('date_of_birth', '')
        
        try:
            # Update user
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            
            # Update profile
            profile.phone = phone
            profile.nationality = nationality
            profile.interests = interests
            
            if date_of_birth:
                from datetime import datetime
                profile.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            
            profile.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
            
        except Exception as e:
            messages.error(request, f'Failed to update profile: {str(e)}')
    
    return render(request, 'accounts/profile.html', {
        'profile': profile
    })

def password_reset_request(request):
    """Password reset request view"""
    if request.user.is_authenticated:
        return redirect('trips:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        
        if not email:
            messages.error(request, 'Please enter your email address')
            return render(request, 'accounts/password_reset_request.html')
        
        try:
            user = User.objects.get(email=email, is_active=True)
            
            # Mark old reset requests as used
            PasswordResetRequest.objects.filter(user=user, is_used=False).update(is_used=True)
            
            # Create new reset request
            reset_request = PasswordResetRequest.objects.create(user=user)
            send_password_reset_email(user, reset_request.token)
            
            messages.success(request, 'Password reset link sent to your email!')
            return redirect('accounts:login')
            
        except User.DoesNotExist:
            # Don't reveal that the user doesn't exist
            messages.success(request, 'If an account with this email exists, a password reset link has been sent.')
            return redirect('accounts:login')
        except Exception as e:
            messages.error(request, f'Failed to send reset email: {str(e)}')
    
    return render(request, 'accounts/password_reset_request.html')

def password_reset_confirm(request, token):
    """Password reset confirmation view"""
    if request.user.is_authenticated:
        return redirect('trips:dashboard')
    
    reset_request = get_object_or_404(
        PasswordResetRequest, 
        token=token, 
        is_used=False
    )
    
    if reset_request.is_expired():
        messages.error(request, 'This password reset link has expired. Please request a new one.')
        return redirect('accounts:password_reset_request')
    
    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if not password:
            messages.error(request, 'Please enter a new password')
            return render(request, 'accounts/password_reset_confirm.html', {'token': token})
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'accounts/password_reset_confirm.html', {'token': token})
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/password_reset_confirm.html', {'token': token})
        
        try:
            # Update password
            user = reset_request.user
            user.set_password(password)
            user.save()
            
            # Mark reset request as used
            reset_request.is_used = True
            reset_request.save()
            
            messages.success(request, 'Password reset successfully! You can now log in with your new password.')
            return redirect('accounts:login')
            
        except Exception as e:
            messages.error(request, f'Failed to reset password: {str(e)}')
    
    return render(request, 'accounts/password_reset_confirm.html', {'token': token})

def send_verification_email(user, otp_code):
    """Send email verification OTP"""
    if not settings.EMAIL_HOST_USER:
        print(f"Email verification OTP for {user.email}: {otp_code}")
        return
    
    subject = 'Verify Your GlobeTrek Account'
    message = f"""
    Hi {user.get_full_name() or user.username},
    
    Welcome to GlobeTrek! Please verify your email address by entering this code:
    
    Verification Code: {otp_code}
    
    This code will expire in 10 minutes.
    
    If you didn't create a GlobeTrek account, please ignore this email.
    
    Best regards,
    The GlobeTrek Team
    """
    
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    
    try:
        email.send()
    except Exception as e:
        print(f"Failed to send verification email: {e}")

def send_password_reset_email(user, token):
    """Send password reset email"""
    if not settings.EMAIL_HOST_USER:
        print(f"Password reset link for {user.email}: http://localhost:8000/accounts/password-reset/{token}/")
        return
    
    reset_url = f"http://localhost:8000/accounts/password-reset/{token}/"
    
    subject = 'Reset Your GlobeTrek Password'
    message = f"""
    Hi {user.get_full_name() or user.username},
    
    You requested to reset your password for your GlobeTrek account.
    
    Click the link below to reset your password:
    {reset_url}
    
    This link will expire in 1 hour.
    
    If you didn't request a password reset, please ignore this email.
    
    Best regards,
    The GlobeTrek Team
    """
    
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    
    try:
        email.send()
    except Exception as e:
        print(f"Failed to send password reset email: {e}")
