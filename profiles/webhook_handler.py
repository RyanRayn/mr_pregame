from django.http import HttpResponse


class StripeWH_Handler:
    """ Handle Stripe Webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle generic/unknown/unexpected webhook event """

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_invoice_payment_succeeded(self, event):
        """ Handle invoice.payment_succeeded webhook from Stripe """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_invoice_payment_failed(self, event):
        """ Handle invoice.payment_failed webhook from Stripe """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
