from django.conf import settings
from django.shortcuts import render, get_object_or_404
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

    stripe_total = membership.price
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    print(intent)
    form = SignupForm

    template = "profiles/get_membership.html"
    context = {
        'profile': profile,
        'form': form,
        'membership': membership,
        'stripe_public_key': stripe_public_key,
        'stripe_secret_key': 'stripe_secret_key',
    }

    return render(request, template, context)
