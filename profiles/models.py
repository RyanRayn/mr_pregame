from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

MEMBERSHIP_CHOICES = (
    ('Free', 'Free'),
    ('Paid', 'Paid'),
)


class Membership(models.Model):
    """ Offered memberships """

    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES, default='Free', max_length=30)
    price = models.IntegerField(default=30)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    billing info and payment history
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    active = models.BooleanField(default=True)
    stripe_customer_id = models.CharField(max_length=40)
    membership_type = models.ForeignKey(
        Membership, on_delete=models.SET_NULL, null=True)
    stripe_subscription_id = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20, blank=True)
    country = CountryField(blank_label='Country *', null=True, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=True)
    street_address1 = models.CharField(max_length=80, blank=True)
    street_address2 = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create or update user profile """

    if created:
        UserProfile.objects.get_or_create(user=instance)

    user_membership, created = UserProfile.objects.get_or_create(user=instance)

    if (user_membership.stripe_customer_id is None or
            user_membership.stripe_customer_id == ''):
        new_customer_id = stripe.Customer.create(email=instance.email)
        user_membership.stripe_customer_id = new_customer_id['id']
        user_membership.save()


post_save.connect(create_or_update_user_profile, sender=User)
