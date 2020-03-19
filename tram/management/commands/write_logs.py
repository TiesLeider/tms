from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
import traceback
from tram.models import *
from tram.admin import AbsoluteDataResource
import os
import json
import platform
import datetime

class Command(BaseCommand):
    help = 'Schrijft logdata weg naar bestanden'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):

        #Maak variabelen
        gister = datetime.date.today() - datetime.timedelta(days=1)
        eergister = datetime.date.today() - datetime.timedelta(days=2)
        qs = AbsoluteData.objects.filter(tijdstip__lte=eergister)
        path = os.getcwd() + f'\\tram\\data\\'  if platform.system().lower() == 'windows' else os.getcwd() + f'/tram/data/'
        if not os.path.exists(path):
            os.makedirs(path)

        #Export de data
        dataset = AbsoluteDataResource().export(queryset=qs)

        with open(path + f"{eergister.strftime('%d-%m-%Y')}.csv", "w") as data_file:
            data_file.write(dataset.csv)
            data_file.close()

        #Verwijder de records
        # qs.delete()

