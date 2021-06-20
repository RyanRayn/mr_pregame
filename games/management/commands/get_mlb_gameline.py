from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Gets all MLB Gamelines for DB'

    def pitcher(self):
        print('Hello World!')

        return