from django.contrib import admin
from .models import *

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display=("assetnummer", "beschrijving", "ip_adres", "logo_online", "disconnections")

@admin.register(LogoData)
class LogoDataAdmin(admin.ModelAdmin):
    list_display=("assetnummer_id", "tijdstip", "storing")




@admin.register(Configuratie)
class ConfiguratieAdmin(admin.ModelAdmin):
    list_display=("naam",)


# Register your models here.
# admin.site.register(LogoMelding)
# admin.site.register(Configuratie)
admin.site.register(Urgentieniveau)