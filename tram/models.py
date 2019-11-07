from djongo import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

class Asset(models.Model):
    assetnummer = models.CharField(max_length=10, primary_key=True)
    beschrijving = models.CharField(null=True, max_length=70)
    bevat_logo = models.BooleanField(default=True)
    ip_adres = models.GenericIPAddressField(null=True)
    logo_online = models.BooleanField(default=False)
    telefoonnummer  = models.CharField(max_length=10, null=True)
    configuratie = models.ForeignKey("Configuratie", on_delete=models.CASCADE)
    laatste_data = models.ForeignKey("LogoData", on_delete=models.CASCADE, default=None)
    aantal_omlopen = models.IntegerField(default=0)
    weging = models.IntegerField(default=1)
    disconnections = models.IntegerField(default=0)
    laatste_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.assetnummer

    def heeft_laatste_storing(self):
        heeft_ls = False
        try:
            heeft_ls = (self.laatste_data is not None)
        except LogoData.DoesNotExist:
            pass
        return heeft_ls

class ConfiguratieElement(models.Model):
    ANALOOG = 'analoog'
    PULSE = 'pulse'
    DIGITAAL = 'digitaal'
    SIGNAALTYPE_KEUZES = [
        (ANALOOG, 'Analoog'),
        (PULSE, 'Dig. pulse'),
        (DIGITAAL, 'Digitaal')
    ]

    inputnummer = models.SmallIntegerField()
    signaaltype = models.CharField(choices=SIGNAALTYPE_KEUZES, default=DIGITAAL, max_length=15)
    beschrijving = models.CharField(max_length=50, null=True)
    urgentieniveau = models.ForeignKey("Urgentieniveau", on_delete=models.CASCADE)




class LogoData(models.Model):
    _id = models.ObjectIdField()
    assetnummer = models.ForeignKey("Asset", on_delete=models.CASCADE)
    storing = models.IntegerField()
    druk_a1 = models.IntegerField()
    druk_a2 = models.IntegerField()
    druk_b1 = models.IntegerField()
    druk_b2 = models.IntegerField()
    kracht_a = models.IntegerField()
    kracht_b = models.IntegerField()
    omloop_a = models.IntegerField()
    omloop_b = models.IntegerField()
    tijdstip = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assetnummer} @ {self.tijdstip.strftime('%m/%d/%Y - %H:%M:%S')}"


    def get_bin_waarden(self):
    #Het omzetten van de hex/int waarde naar binaire waarden
        inputs = []
        for pin in bin(self.storing)[2:]:
            inputs.append(int(pin))
        inputs.reverse()
        return inputs

    def get_hoge_inputs(self):
    #Gebruikt de binaire waarden om te bepalen welke waarden hoog zijn.
        hoge_inputs = []
        for idx, val in enumerate(self.get_bin_waarden()):
            if val != 0:
                hoge_inputs.append(idx+1)
        return hoge_inputs

    def get_storing_beschrijvingen(self):
        beschrijvingen = []
        for obj in self.assetnummer.configuratie.config:
            if obj.inputnummer in self.get_hoge_inputs():
                beschrijvingen.append(obj.beschrijving)
        return beschrijvingen

    def get_storings_score(self):
        score = 0
        for obj in self.assetnummer.configuratie.config:
            if obj.inputnummer in self.get_hoge_inputs():
                score += obj.urgentieniveau.niveau
        return score
        

class AbsoluteData(models.Model):
    _id = models.ObjectIdField()
    assetnummer = models.ForeignKey("Asset", on_delete=models.CASCADE)
    storing = models.ForeignKey("Storing", on_delete=models.CASCADE, default=None, null=True)
    storing_beschrijving = models.ListField(default=[])
    druk_a1 = models.IntegerField()
    druk_a2 = models.IntegerField()
    druk_b1 = models.IntegerField()
    druk_b2 = models.IntegerField()
    kracht_a = models.IntegerField()
    kracht_b = models.IntegerField()
    omloop_a = models.IntegerField()
    omloop_b = models.IntegerField()
    tijdstip = models.DateTimeField(auto_now=True)

    def heeft_storing(self):
        heeft_s = False
        try:
            heeft_s = (self.storing is not None)
        except AbsoluteData.DoesNotExist:
            pass
        return heeft_s

    def __str__(self):
        return f"{self.assetnummer} @ {self.tijdstip.strftime('%m/%d/%Y - %H:%M:%S')}"

class Storing(models.Model):
    _id = models.ObjectIdField()
    assetnummer = models.ForeignKey("Asset", on_delete=models.CASCADE)
    gezien = models.BooleanField()
    actief = models.BooleanField()
    score = models.IntegerField()


class Configuratie(models.Model):
    _id = models.ObjectIdField()
    naam = models.CharField(max_length=50)
    config = models.ArrayModelField(model_container=ConfiguratieElement)

    def __str__(self):
        return self.naam
    

class Urgentieniveau(models.Model):
    niveau = models.SmallIntegerField(primary_key=True)
    beschrijving  = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.beschrijving
    
@receiver(post_save, sender=LogoData) 
def opslaan_logo_data(sender, instance, **kwargs):

    def maak_nieuwe_storing(ins):
        new_storing = Storing(
            assetnummer = asset,
            gezien = False,
            actief = True,
            score = ins.get_storings_score()
        )
        new_storing.save()
        ad.storing = new_storing
        ad.save()
    
    asset = Asset.objects.get(assetnummer=instance.assetnummer)
    asset.logo_online = True
    asset.disconnections = 0
    asset.laatste_data = instance
    asset.save()

    ad = AbsoluteData(
        assetnummer = asset,
        storing_beschrijving = instance.get_storing_beschrijvingen() if (instance.storing != 0) else [],
        storing = None,
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
    if vorige_ad == None:
        if len(ad.storing_beschrijving) > 0:
            maak_nieuwe_storing(instance)
        else:
            ad.save()
    
    else:
        if len(ad.storing_beschrijving) > 0 and vorige_ad.heeft_storing() == False:
            maak_nieuwe_storing(instance)
        elif len(ad.storing_beschrijving) > 0 and vorige_ad.heeft_storing() == True:
            bestaande_storing = vorige_ad.storing
            bestaande_storing.score += instance.get_storings_score()
            bestaande_storing.save()
            ad.storing = bestaande_storing
            ad.save()

        elif len(ad.storing_beschrijving) == 0 and vorige_ad.heeft_storing() == True:
            bestaande_storing = vorige_ad.storing
            bestaande_storing.actief = False
            bestaande_storing.save()
            ad.save()
        else:
            ad.save()

# @receiver(pre_save, sender=AbsoluteData)
# def opslaan_abs_data(sender, instance, **kwargs):
#     if instance.storing_beschrijving.lenght == 0:
#         instance.save()