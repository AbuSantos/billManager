# tasks.py
import logging
import datetime
from celery import shared_task
from .models import Bills

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone 

logger = logging.getLogger(__name__)


@shared_task
def send_bill_reminders(bill_id, reminder_date):
    today = timezone.now().date()  # Get the current date in your project's timezone

    try:
        bill_instance = Bills.objects.get(id=bill_id)
    except Bills.DoesNotExist:
        return  # Handle the case where the Bill doesn't exist

    if bill_instance.bill_due_date == reminder_date:
        # Implement your reminder logic here (e.g., sending emails, notifications)
        # Example: Send an email reminder
        send_email_to_user(
            bill_instance.user,
            f'Reminder: Your bill "{bill_instance.bill_name}" is due on {bill_instance.bill_due_date}'
        )

def send_email_to_user(user, subject, message):
    """
    Send an email reminder to a user.
    
    :param user: The user to whom the email should be sent.
    :param subject: The subject of the email.
    :param message: The email message content.
    """
    # Compose the email content
    html_message = render_to_string('email_template.html', {'message': message})
    plain_message = strip_tags(html_message)  # Strip HTML tags for plain text version

    # Send the email using Django's send_mail function
    try:
        # Send the email using Django's send_mail function
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,  # Use your email address or a configured sender
            [user.email],  # Recipient's email address
            html_message=html_message,  # Email content with HTML
            fail_silently=False,  # Set to True to suppress errors (not recommended in production)
        )
        logger.info(f"Email sent successfully to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send email to {user.email}: {str(e)}")

    
