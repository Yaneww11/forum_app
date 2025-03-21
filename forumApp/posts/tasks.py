from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_approval_mail(auth_username, auth_email, post_title):
        send_mail(
            subject='Your post has been approved',
            message=f'Hi {auth_username}, \nYour post {post_title} has been approved',
            from_email="yaneyanev2807@gmail.com",
            recipient_list=[auth_email]
        )