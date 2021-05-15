from django import forms
from .models import UserProfile, Membership


class SignupForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'postcode': 'Postal Code',
            'country': 'Country'
        }

        for field in self.fields:
            placeholder = placeholders[field]
            # Start cursor on full_name field
            self.fields['full_name'].widget.attrs['autofocus'] = True
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
