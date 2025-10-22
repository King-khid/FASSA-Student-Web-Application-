from django.core.mail import send_mail
from django.conf import settings
import string
import random

def generate_temporary_password(length=10):
    """Generate a random temporary password."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def send_account_email(user_email, full_name, role, temp_password):
    """Send plain text email notifying user of account creation."""
    role_text = "Faculty Admin" if role == 'ADMIN' else "Student"
    subject = "Your FASSA Account Has Been Created"
    message = f"""
Hello {full_name},

An account has been created for you as a FASSA {role_text}.
Here are your login details:

Email: {user_email}
Temporary Password: {temp_password}

Login here: http://127.0.0.1:8000/api/accounts/login/

Please change your password after logging in.

Regards,
FASSA
"""
    from_email = f"FASSA <{settings.EMAIL_HOST_USER}>"
    send_mail(subject, message, from_email, [user_email], fail_silently=False)


def send_student_verification_email(user_email, full_name, verification_token):
    """Send email verification link to student after registration."""
    subject = "Verify Your FASSA Account"
    verification_link = f"http://127.0.0.1:8000/api/accounts/verify/{verification_token}/"
    message = f"""
Hello {full_name},

Thank you for registering at FASSA. Please verify your account by clicking the link below:

{verification_link}

Once verified, you can log in using your email and password.

Regards,
FASSA
"""
    from_email = f"FASSA <{settings.EMAIL_HOST_USER}>"
    send_mail(subject, message, from_email, [user_email], fail_silently=False)


def send_password_reset_email(email, token):
    reset_link = f"http://127.0.0.1:8000/api/accounts/password-reset/confirm/?token={token}"
    subject = "Reset Your FASSA Password"
    message = f"""
Hello,

Click the link below to reset your password:

{reset_link}

If you did not request this, ignore this email.

Regards,
FASSA
"""
    from_email = f"FASSA <{settings.EMAIL_HOST_USER}>"
    send_mail(subject, message, from_email, [email], fail_silently=False)
