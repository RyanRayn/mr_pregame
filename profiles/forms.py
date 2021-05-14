from django import forms
from .models import UserProfile, Membership


class SignupForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = '__all__'
