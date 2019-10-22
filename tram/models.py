from djongo import models

class Asset(models.Model):
    assetnummer = models.CharField(max_length=10, primary_key=True)
    beschrijving = models.CharField(null=True, max_length=70)
    bevat_logo = models.BooleanField()
    ip_adres = models.GenericIPAddressField(null=True)
    logo_online = models.BooleanField()
    telefoonnummer  = models.CharField(max_length=10, null=True)
    configuratie = models.ForeignKey("ConfiguratieLijst", on_delete=models.CASCADE)

    def __str__(self):
        return self.assetnummer
    

class Status(models.Model):
    inputnummer = models.SmallIntegerField()
    waarde = models.IntegerField()

    class Meta:
        abstract = True

class Configuratie(models.Model):
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




class LogoMelding(models.Model):
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
    


class ConfiguratieLijst(models.Model):
    _id = models.ObjectIdField()
    naam = models.CharField(max_length=50)
    config = models.ArrayModelField(model_container=Configuratie)

    def __str__(self):
        return self.naam
    

class Urgentieniveau(models.Model):
    niveau = models.SmallIntegerField(primary_key=True)
    beschrijving  = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.beschrijving
    
 
