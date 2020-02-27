from django.urls import path
from . import views
 

urlpatterns = [
    #Storing
    path("", views.index, name="index"),
    path("storing/<int:storing_id>/gezien",views.storing_gezien, name="storing_gezien"),
    path("storing/<int:storing_id>/deactiveer",views.deactiveer_storing, name="storing_deactiveren"),
    path("sms", views.sms_lijst, name="sms_lijst"),

    #API
    path("api/resettelleralle", views.asset.reset_teller_alle, name="asset_reset_alle"),
    path("api/omlopen_totaal/<str:assetnummer>/<str:van_datum>/<str:tot_datum>", views.api.get_omlopen_totaal, name="get_omlopen_totaal"),
    path("api/omlopen_freq/<str:assetnummer>/<str:van_datum>/<str:tot_datum>", views.api.get_omlopen_freq, name="get_omlopen_freq"),
    path("api/alle_actieve_storingen/", views.get_actieve_storingen, name="alle_actieve_storingen"),
    path("index_form", views.index_form, name="index_form"),
    path("api/check_online_assets", views.check_online_assets, name="check_online_assets"),
    path("api/get_sms_storingen", views.get_sms_data, name="get_sms_data"),
    path("api/get_sensor_waarden/<str:assetnummer>/<str:veld>", views.api.get_sensor_waarden, name="get_sensor_waarden"),

    #Asset
    path("insertlogodata",views.insert_logo_data, name="insert_logo_data"),
    path("insertsmsdata", views.insert_sms_data, name="insert_sms_data"),
    path("insertlogoonline",views.insert_logo_online, name="insert_logo_online"),
    path("asset/<str:assetnummer>", views.asset_index, name="asset_index"),
    path("asset/<str:assetnummer>/resetteller", views.asset.reset_teller_standen, name="asset_reset_teller"),
    path("asset/<str:assetnummer>/corrigeer_omlopen", views.asset.corrigeer_omlopen, name="asset_corrigeer_omlopen"),
    path("asset_chart/<str:assetnummer>", views.asset_chart, name="asset_chart"),
    path("analyse/<str:assetnummer>/<str:veld>", views.asset_analyse, name="asset_analyse"),
]  