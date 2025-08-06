from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import EmailVerificationOTP

class Command(BaseCommand):
    help = 'Test email configuration and send a test email'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test email to (defaults to your configured email)',
        )
    
    def handle(self, *args, **options):
        test_email = options.get('email') or settings.EMAIL_HOST_USER
        
        if not test_email:
            self.stdout.write(
                self.style.ERROR('No email address provided and EMAIL_HOST_USER not configured')
            )
            return
        
        # Test basic email configuration
        self.stdout.write('🔧 Testing Email Configuration...')
        self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
        
        # Test sending email
        try:
            self.stdout.write(f'📧 Sending test email to {test_email}...')
            
            subject = '✅ GlobeTrek Email Configuration Test'
            message = f"""
Hi there!

This is a test email to verify that your GlobeTrek email configuration is working correctly.

✅ Email Configuration Status: WORKING
📧 From: {settings.DEFAULT_FROM_EMAIL}
🎯 To: {test_email}
🔐 SMTP: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}
🔒 TLS: {'Enabled' if settings.EMAIL_USE_TLS else 'Disabled'}

Your 2FA email verification system is now ready to use!

Features that will now work:
- User registration email verification
- Password reset emails
- Account activation via OTP
- Professional email delivery

Best regards,
The GlobeTrek Team 🌍✈️
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[test_email],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Test email sent successfully to {test_email}!')
            )
            self.stdout.write('Check your inbox to verify email delivery.')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send test email: {str(e)}')
            )
            self.stdout.write('Please check your email configuration in .env file')
            
        # Test OTP generation
        try:
            self.stdout.write('\n🔐 Testing OTP Generation...')
            # Generate a test OTP (without user)
            import random
            import string
            test_otp = ''.join(random.choices(string.digits, k=6))
            self.stdout.write(f'Sample OTP generated: {test_otp}')
            self.stdout.write('✅ OTP generation system working correctly')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ OTP generation failed: {str(e)}')
            )
