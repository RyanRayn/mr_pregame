from django import forms
from .models import TeamStats


class BasketballGame(forms.ModelForm):

    class Meta:
        model = TeamStats
        fields = '__all__'
