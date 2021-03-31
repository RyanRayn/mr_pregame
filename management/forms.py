from django import forms
from .models import BasketballTeamStats


class BasketballGame(forms.ModelForm):

    class Meta:
        model = BasketballTeamStats
        fields = '__all__'
