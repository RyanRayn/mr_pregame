from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import UserProfile, Membership
from .forms import SignupForm
import stripe


def profile(request):
    """ Display the user's profile """
    profile = get_object_or_404(UserProfile, user=request.user)

    template = "profiles/profile.html"
    context = {
        'profile': profile,
    }

    return render(request, template, context)


def get_membership(request):
    stripe_public_key = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    profile = get_object_or_404(UserProfile, user=request.user)
    membership = Membership.objects.get(membership_type='Paid')

    if request.method == "POST":
        try:
            token = request.POST['stripeToken']

            stripe.Customer.modify(
                profile.stripe_customer_id, source=token)

            subscription = stripe.Subscription.create(
                customer=profile.stripe_customer_id,
                items=[
                    {
                        'price': membership.stripe_plan_id,
                    }
                ],
            )

            return redirect(reverse('update_membership',
                            kwargs={
                                    'subscription_id': subscription.id,
                                    }))
        except stripe.error.CardError:
            messages.info(request, "Your card has been declined.")

    form = SignupForm

    template = "profiles/get_membership.html"
    context = {
        'profile': profile,
        'form': form,
        'membership': membership,
        'stripe_public_key': stripe_public_key,
        'stripe_secret_key': stripe_secret_key,
    }

    return render(request, template, context)


def update_membership(request, subscription_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    cust_id = profile.stripe_customer_id
    paid_membership = Membership.objects.get(membership_type='Paid')

    UserProfile.objects.update_or_create(
                stripe_customer_id=cust_id, defaults={
                    'membership_type': paid_membership,
                    'stripe_subscription_id': subscription_id,
                    'active': True
                }
            )
    messages.info(request, "Welcome to the team! Time to get paid.")
    return redirect('/profile')
