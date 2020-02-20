from djongo import models

class Asset(models.Model):
    assetnummer = models.CharField(max_length=30)
    configuratie = models.ForeignKey("Configuratie", on_delete=models.CASCADE)

class ConfiguratieElement(models.Model):
    inputnummer = models.IntegerField()
    beschrijving = models.CharField(max_length=100)

class Configuratie(models.Model):
    naam = models.CharField(max_length=50)
    config = models.ArrayField(model_container=ConfiguratieElement)

    def __str__(self):
        return self.naam


class Data(models.Model):
    _id = models.ObjectIdField()
    asset = models.ForeignKey("Asset", on_delete=models.CASCADE)
    storing = models.IntegerField()
    niveau = models.IntegerField()
    tijdstip = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Data"

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
        print(self.asset.configuratie)
        beschrijvingen = []
        for obj in self.asset.configuratie.config:
            if obj.inputnummer in self.get_hoge_inputs():
                beschrijvingen.append(obj.beschrijving)
        return beschrijvingen

class Storing(models.Model):
    asset = models.ForeignKey("Asset", on_delete=models.CASCADE)
    beschrijving = models.CharField(max_length=100)
    tijdstip = models.DateTimeField(auto_now=True)
