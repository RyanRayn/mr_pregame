from django import forms
from .models import BasketballTeamStats, BaseballTeamStats, StartingPitcher


class BasketballGame(forms.ModelForm):

    class Meta:
        model = BasketballTeamStats
        fields = '__all__'


class BaseballGame(forms.ModelForm):

    class Meta:
        model = BaseballTeamStats
        fields = '__all__'


class Pitcher(forms.ModelForm):

    class Meta:
        model = StartingPitcher
        fields = '__all__'
