from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from ..models import *

def index(request):
    return render(request, "tram/index.html", {"storingen": Storing.objects.select_related("data").filter(actief=True, gezien=False).order_by('-data__tijdstip')[:30]})
    # return render(request, "tram/index.html", {"storingen": AbsoluteData.objects.exclude(storing_beschrijving=[]).order_by("-tijdstip")})

def alle_storingen(request):
    return render(request, "tram/index_alle.html", {"storingen": Storing.objects.select_related("data").filter(actief=True, gezien=False).order_by('-data__tijdstip')})
    # return render(request, "tram/index.html", {"storingen": AbsoluteData.objects.exclude(storing_beschrijving=[]).order_by("-tijdstip")})

def storing_gezien(request, storing_id):
    storing = get_object_or_404(Storing, pk = storing_id)
    storing.gezien = True
    storing.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def deactiveer_storing(request, storing_id):
    storing = get_object_or_404(Storing, pk = storing_id)
    storing.gezien = True
    storing.actief = False
    storing.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    
@receiver(post_save, sender=LogoData) 
def opslaan_logo_data(sender, instance, **kwargs):
    def maak_nieuwe_storing(absulute_data, bericht):
        new_storing = Storing(
            assetnummer = absulute_data.assetnummer,
            gezien = False,
            actief = True,
            bericht = bericht,
            som = 1,
            score = 0,
            data = absulute_data
        )
        new_storing.score = new_storing.get_score()
        new_storing.save()
    
    asset = Asset.objects.get(assetnummer=instance.assetnummer.assetnummer)
    asset.logo_online = True
    asset.disconnections = 0
    asset.laatste_data = instance
    asset.save()
    asset = None

    ad = AbsoluteData(
        assetnummer = asset,
        storing_beschrijving = instance.get_storing_beschrijvingen() if (instance.storing != 0) else [],
        druk_a1 = instance.druk_a1,
        druk_a2 = instance.druk_a2,
        druk_b1 = instance.druk_b1,
        druk_b2 = instance.druk_b2,
        kracht_a = instance.kracht_a,
        kracht_b = instance.kracht_b,
        omloop_a = instance.omloop_a,
        omloop_b = instance.omloop_b,
    )


    vorige_ad = AbsoluteData.objects.filter(assetnummer=ad.assetnummer).order_by('-tijdstip').first()
    ad.save()
    if vorige_ad == None:
        #Er is geen vorige data van dit wisselnummer
        if len(ad.storing_beschrijving) > 0:
            for b in ad.storing_beschrijving:
                maak_nieuwe_storing(ad, b)
        else:
            pass
    else:
        #Er is een vorige polling geweest van deze asset
        if len(ad.storing_beschrijving) > 0:
            #Bij deze polling is een storing vastgelegd
            for sb in ad.storing_beschrijving:
                vorige_storing = Storing.objects.filter(assetnummer=ad.assetnummer, bericht=sb).first()
                if vorige_storing:
                    if (vorige_storing.actief == True) and (vorige_storing.gezien == False):
                        #De storing is niet gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.data = ad
                    elif (vorige_storing.actief == True) and (vorige_storing.gezien == True):
                        #De storing is actief en gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.gezien = False
                        vorige_storing.data = ad
                    elif (vorige_storing.actief == False):
                        #De storing is niet langer actief
                        maak_nieuwe_storing(ad, sb)
                    vorige_storing.save()
                else:
                    #Er zijn geen storings-records gevonden van de vorige data
                    maak_nieuwe_storing(ad, sb)
        else:
            #Er was geen storing bij deze polling
            pass




@receiver(pre_save, sender=AbsoluteData)
def opslaan_abs_data(sender, instance, **kwargs):
    print(f"AD {instance.assetnummer} opgeslagen")

