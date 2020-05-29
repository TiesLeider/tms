from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
import traceback
from tram.models import *
import os
import json
import platform

class Command(BaseCommand):
    help = 'Berekent de gemiddelde waarden'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        for asset in Asset.objects.filter(pollbaar=True):
            try:
                nu = datetime.datetime.now()
                gister = nu - datetime.timedelta(days=1)
                vorige_week = nu - datetime.timedelta(days=7)
                vorige_maand = nu - datetime.timedelta(days=30)
                ld_dag_qs = LogoData.objects.filter(assetnummer=asset, tijdstip__range=(gister, nu))
                ld_week_qs = LogoData.objects.filter(assetnummer=asset, tijdstip__range=(vorige_week, nu))
                ld_maand_qs = LogoData.objects.filter(assetnummer=asset, tijdstip__range=(vorige_maand, nu))
                

                ld_dag_agg = ld_dag_qs.aggregate(Avg("omloop_a"), Avg("omloop_b"))
                ld_week_agg = ld_week_qs.aggregate(Avg("omloop_a"), Avg("omloop_b"))
                ld_maand_agg = ld_maand_qs.aggregate(Avg("omloop_a"), Avg("omloop_b"))

                asset.gem_dag_omloop_a_freq = ld_dag_agg.get("omloop_a__avg") if ld_dag_qs.count() > 0 else 0
                asset.gem_week_omloop_a_freq = ld_week_agg.get("omloop_a__avg") if ld_week_qs.count() > 0 else 0
                asset.gem_maand_omloop_a_freq = ld_maand_agg.get("omloop_a__avg") if ld_maand_qs.count() > 0 else 0

                asset.gem_dag_omloop_b_freq = ld_dag_agg.get("omloop_b__avg") if ld_dag_qs.count() > 0 else 0
                asset.gem_week_omloop_b_freq = ld_week_agg.get("omloop_b__avg") if ld_week_qs.count() > 0 else 0
                asset.gem_maand_omloop_b_freq = ld_maand_agg.get("omloop_b__avg") if ld_maand_qs.count() > 0 else 0

                dag_qs = AbsoluteData.objects.filter(assetnummer=asset, tijdstip__range=(gister, nu))
                week_qs = AbsoluteData.objects.filter(assetnummer=asset, tijdstip__range=(vorige_week, nu))
                maand_qs = AbsoluteData.objects.filter(assetnummer=asset, tijdstip__range=(vorige_maand, nu))

                dag_gemiddelde_agg = dag_qs.aggregate(Avg("druk_a1"), Avg("druk_a2"), Avg("druk_b1"), Avg("druk_b2"))
                week_gemiddelde_agg = week_qs.aggregate(Avg("druk_a1"), Avg("druk_a2"), Avg("druk_b1"), Avg("druk_b2"))
                maand_gemiddelde_agg = maand_qs.aggregate(Avg("druk_a1"), Avg("druk_a2"), Avg("druk_b1"), Avg("druk_b2"))

                dag_qs_count = dag_qs.count()
                week_qs_count = week_qs.count()
                maand_qs_count = maand_qs.count()

                asset.gem_dag_druk_a1 = dag_gemiddelde_agg.get("druk_a1") if dag_qs_count > 0 else 0
                asset.gem_week_druk_a1 = week_gemiddelde_agg.get("druk_a1") if week_qs_count > 0 else 0
                asset.gem_maand_druk_a1 = maand_gemiddelde_agg.get("druk_a1") if maand_qs_count > 0 else 0

                asset.gem_dag_druk_a2 = dag_gemiddelde_agg.get("druk_a2") if dag_qs_count > 0 else 0
                asset.gem_week_druk_a2 = week_gemiddelde_agg.get("druk_a2") if week_qs_count > 0 else 0
                asset.gem_maand_druk_a2 = maand_gemiddelde_agg.get("druk_a1") if maand_qs_count > 0 else 0

                asset.gem_dag_druk_b1 = dag_gemiddelde_agg.get("druk_b1") if dag_qs_count > 0 else 0
                asset.gem_week_druk_b1 = week_gemiddelde_agg.get("druk_b1") if week_qs_count > 0 else 0
                asset.gem_maand_druk_b1 = maand_gemiddelde_agg.get("druk_b1") if maand_qs_count > 0 else 0

                asset.gem_dag_druk_b2 = dag_gemiddelde_agg.get("druk_b2") if dag_qs_count > 0 else 0
                asset.gem_week_druk_b2 = week_gemiddelde_agg.get("druk_b2") if week_qs_count > 0 else 0
                asset.gem_maand_druk_b2 = maand_gemiddelde_agg.get("druk_b2") if maand_qs_count > 0 else 0

                asset.save()

            except Exception as ex:
                print(ex)
                continue
                
        

        self.stdout.write(self.style.SUCCESS("Done"))