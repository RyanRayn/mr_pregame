from django import forms
from .models import BasketballTeamStats, BaseballGame
from .models import StartingPitcher, TeamName, Season


class BasketballGame(forms.ModelForm):

    class Meta:
        model = BasketballTeamStats
        fields = '__all__'


class AwayBaseballGames(forms.ModelForm):

    class Meta:
        model = BaseballGame
        fields = '__all__'

    runs_first_five = forms.IntegerField(label='Runs 5', required=False,
                                         initial=0)
    runs_allowed_first_five = forms.IntegerField(label='Runs allowed 5',
                                                 required=False, initial=0)
    home_runs = forms.IntegerField(label='HR', required=False, initial=0)
    home_runs_against = forms.IntegerField(label='HR allowed', required=False,
                                           initial=0)
    bullpen_inning_thirds = forms.IntegerField(label='BP outs',
                                               required=False, initial=0)
    bullpen_runs = forms.IntegerField(label='BP runs', required=False,
                                      initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        seasons = Season.objects.filter(name='MLB2021')
        names = [(season.id, season.name) for season in seasons]
        self.fields['season'].choices = names

        team_names = TeamName.objects.filter(league__name='MLB').order_by(
                                             'name')
        teams = [(team.id, team.name)for team in team_names]
        self.fields['name'].choices = teams


class HomeBaseballGames(forms.ModelForm):

    class Meta:
        model = BaseballGame
        fields = '__all__'

    runs_first_five = forms.IntegerField(label='Runs 5', required=False,
                                         initial=0)
    runs_allowed_first_five = forms.IntegerField(label='Runs allowed 5',
                                                 required=False, initial=0)
    home_runs = forms.IntegerField(label='HR', required=False, initial=0)
    home_runs_against = forms.IntegerField(label='HR allowed', required=False,
                                           initial=0)
    bullpen_inning_thirds = forms.IntegerField(label='BP outs',
                                               required=False, initial=0)
    bullpen_runs = forms.IntegerField(label='BP runs', required=False,
                                      initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        seasons = Season.objects.filter(name='MLB2021')
        names = [(season.id, season.name) for season in seasons]
        self.fields['season'].choices = names

        team_names = TeamName.objects.filter(league__name='MLB').order_by(
                                             'name')
        teams = [(team.id, team.name)for team in team_names]
        self.fields['name'].choices = teams


class Pitcher(forms.ModelForm):

    class Meta:
        model = StartingPitcher
        fields = '__all__'

    inning_thirds = forms.IntegerField(label='Outs', required=False, initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        team_names = TeamName.objects.filter(league__name='MLB').order_by(
                                             'name')
        teams = [(team.id, team.name)for team in team_names]
        self.fields['team'].choices = teams

        seasons = Season.objects.filter(name='MLB2021')
        names = [(season.id, season.name) for season in seasons]
        self.fields['season'].choices = names
