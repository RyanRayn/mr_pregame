from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import UserProfile

class StripeWH_Handler:
    """ Handle Stripe Webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle generic/unknown/unexpected webhook event """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_invoice_payment_succeeded(self, event):
        """ Handle invoice.payment_succeeded webhook from Stripe """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_invoice_payment_failed(self, event):
        """ Handle invoice.payment_failed webhook from Stripe """

        intent = event.data.object
        profile = UserProfile.objects.filter(stripe_customer_id=intent.customer)
        cust_email = intent.customer_email

        subject = render_to_string(
            'profiles/emails/missed_payment_subject.txt',
            {'profile': profile})
        body = render_to_string(
            'profiles/emails/missed_payment.txt',
            {'profile': profile, 'contact_email': settings.DEFAULT_FROM_EMAIL})
            
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
