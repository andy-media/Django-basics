from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_confirmation_email(school, payment):
    """
    Send payment confirmation email to school
    """
    subject = f'Payment Confirmation - {school.name}'
    context = {
        'school': school,
        'payment': payment,
        'site_name': settings.SITE_NAME,
        'contact_email': settings.DEFAULT_FROM_EMAIL,
    }
    
    # Render both HTML and text versions
    html_message = render_to_string('payments/email/confirmation.html', context)
    text_message = render_to_string('payments/email/confirmation.txt', context)
    
    email = EmailMessage(
        subject,
        text_message,
        settings.DEFAULT_FROM_EMAIL,
        [school.user.email],
        reply_to=[settings.REPLY_TO_EMAIL],
    )
    email.content_subtype = "html"  # Main content is HTML
    email.send()