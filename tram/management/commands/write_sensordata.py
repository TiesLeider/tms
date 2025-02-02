from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
import traceback
from tram.models import *
import os
import json
import platform
import datetime

class Command(BaseCommand):
    help = 'Schrijft sensordata weg naar bestanden'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        druk_configs =  ["Amstelveen", "ELL-Standaard"]
        
        def schrijf_data(assetnummer, veld):
            vandaag = datetime.date.today()
            
            qs = AbsoluteData.objects.filter(assetnummer=assetnummer).order_by("tijdstip")
            data = list(qs.values(veld, "tijdstip"))
            response = []
            for item in data:
                response.append( [round((item["tijdstip"].timestamp()) * 1000), item[veld]] )
            path = os.getcwd() + f'\\tram\\templates\\tram\\data\\{assetnummer}\\'  if platform.system().lower() == 'windows' else os.getcwd() + f'/tram/templates/tram/data/{assetnummer}/'

            if not os.path.exists(path):
                os.makedirs(path)

            # try:
            #     with open(path + f'{veld}.json', 'r+') as outfile:
            #         json_data = json.load(outfile)
            #         print(json_data)
            #         print(type(json_data))
            #         for item in response:
            #             json_data.append(item)
            #         json.dump(json_data, outfile)
            # except FileNotFoundError:
            #     with open(path + f'{veld}.json', 'w+') as outfile:
            #         json.dump(response, outfile)
            with open(path + f'{veld}.json', 'w+') as outfile:
                    json.dump(response, outfile)

        for asset in Asset.objects.filter(pollbaar=True):
            try:
                ad = AbsoluteData.objects.filter(assetnummer=asset).latest()
                if ad.omloop_a > 0:
                    schrijf_data(asset, "omloop_a")

                if ad.omloop_b > 0:
                    schrijf_data(asset, "omloop_b")

                if ad.druk_a1 > 0: # and asset.configuratie.naam in druk_configs:
                    schrijf_data(asset, "druk_a1")

                if ad.druk_a2 > 0: # and asset.configuratie.naam in druk_configs:
                    schrijf_data(asset, "druk_a2")

                if ad.druk_b1 > 0: # and asset.configuratie.naam in druk_configs:
                    schrijf_data(asset, "druk_b1")
                
                if ad.druk_b2 > 0: # and asset.configuratie.naam in druk_configs:
                    schrijf_data(asset, "druk_b2")
                
                if ad.kracht_a > 0:
                    schrijf_data(asset, "kracht_a")
                
                if ad.kracht_b > 0:
                    schrijf_data(asset, "kracht_b")

            except Exception as ex:
                # traceback.print_exc()
                # self.stdout.write(self.style.SUCCESS(f'{ex}'))
                continue

        self.stdout.write(self.style.SUCCESS("Done"))