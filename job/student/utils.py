
import random
import string

def generate_otp(length=6):
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))


from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    subject = 'OTP verification for CareerBuddy registration'
    message = f'Your OTP code is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)