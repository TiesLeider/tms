from django.contrib import admin
from .models import *

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display=("assetnummer", "beschrijving", "bevat_logo", "ip_adres", "logo_online", "telefoonnummer")

@admin.register(LogoData)
class LogoDataAdmin(admin.ModelAdmin):
    list_display=("assetnummer_id", "tijdstip", "storing")
    


# Register your models here.
# admin.site.register(LogoMelding)
admin.site.register(Configuratie)
admin.site.register(Urgentieniveau)