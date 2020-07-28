from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from tms_webapp.settings import BASE_DIR
import traceback
from tram.models import *
import os
import json
import platform
import datetime

class Command(BaseCommand):
    help = 'Verwijderd lege drukwaarden'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for root, dirs, files in os.walk(os.path.join(BASE_DIR, 'tram/templates/tram/data')):
            for file in files:
                path = os.path.join(root, file).split("/")
                assetnummer = path[-2] if not path[-2].statswith("w") else "W"+path[-2]
                if Asset.objects.get(assetnummer=assetnummer).laatste_data.druk_b1 == 0:
                    print(assetnummer)