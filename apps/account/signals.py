from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from graphql_jwt.signals import token_issued


@receiver(token_issued)
def handle_token_issued(sender, request, user, **kwargs):
    print(f"Token issued for user {user.phone_number}")

    if not settings.DEBUG and settings.EMAIL_HOST_USER:
        subject = "Token Issued"
        message = "Your token has been issued."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)


token_issued.connect(handle_token_issued)
