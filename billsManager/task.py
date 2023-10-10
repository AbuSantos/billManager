# tasks.py
import logging
import datetime
from celery import shared_task
from .models import Bills, UserProfile

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone 
from background_task import background
from datetime import timedelta
from django.contrib import messages


logger = logging.getLogger(__name__)


@shared_task
def send_bill_reminders(bill_id, reminder_date):
    today = timezone.now().date()  # Get the current date in your project's timezone

    try:
        bill_instance = Bills.objects.get(id=bill_id)
    except Bills.DoesNotExist:
        return  # Handle the case where the Bill doesn't exist

    if bill_instance.bill_due_date == reminder_date:
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
   
    html_message = render_to_string('email_template.html', {'message': message})
    plain_message = strip_tags(html_message)  

    # Sending the email using Django's send_mail function
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,  
            [user.email],  
            html_message=html_message,  
            fail_silently=False,  
        )
        logger.info(f"Email sent successfully to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send email to {user.email}: {str(e)}")

@background(schedule = timedelta(minutes = 1))
def process_overdue_bills(bill_id):
    # Retrieve the bill by its ID
    bill = Bills.objects.get(pk = bill_id)

    # Check if the bill is overdue
    if bill.due_date <= timezone.now():
        # Check the user's wallet balance
        user_profile = UserProfile.objects.get(user=bill.user)

        if user_profile.wallet_balance >= bill.amount:
            # Sufficient funds in the wallet, deduct the bill amount
            user_profile.wallet_balance -= bill.amount
            user_profile.save()

            # Mark the bill as paid
            bill.status = 'Paid'
            bill.save()


        else:
            messages.success("Insufficient fund!")

        # # If this bill is recurring, schedule the next occurrence
        if bill.is_recurring:
            next_due_date = bill.due_date + timedelta(days=bill.frequency_days)
            process_overdue_bills(bill_id=bill.id).schedule(
                eta=next_due_date
            )
