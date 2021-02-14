from django import forms
from .models import League, Team, Season, Game


class BasketballGame(forms.ModelForm):

    class Meta:
        model = Game
        fields = '__all__'
