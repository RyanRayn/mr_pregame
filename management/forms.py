from django import forms
from .models import BasketballTeamStats, MLBGame, MLBGameLine
from .models import StartingPitcher, TeamName, Season


class BasketballGame(forms.ModelForm):

    class Meta:
        model = BasketballTeamStats
        fields = '__all__'


class AwayBaseballGames(forms.ModelForm):

    class Meta:
        model = MLBGame
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
    opponent_at_bats = forms.IntegerField(label='Op. At bats', required=False,
                                          initial=0)
    opponent_errors = forms.IntegerField(label='Op. Errors', required=False,
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
        model = MLBGame
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
    opponent_at_bats = forms.IntegerField(label='Op. At bats', required=False,
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


class EditGameLine(forms.ModelForm):

    class Meta:
        model = MLBGameLine
        fields = ['summary', 'away_team', 'away_starter',
                  'away_starter_record', 'away_starter_era',
                  'away_starter_k', 'home_team', 'home_starter',
                  'home_starter_record', 'home_starter_era',
                  'home_starter_k', 'pick_type', 'pick']

    away_starter = forms.CharField(label='Away Starter', required=False)
    away_starter_era = forms.DecimalField(label='Away ERA', required=False)
    away_starter_k = forms.IntegerField(label='Away K', required=False)
    away_starter_record = forms.CharField(label='Away Record', required=False)
    home_starter = forms.CharField(label='Home Starter', required=False)
    home_starter_era = forms.DecimalField(label='Home ERA', required=False)
    home_starter_k = forms.IntegerField(label='Home K', required=False)
    home_starter_record = forms.CharField(label='Home Record', required=False)
