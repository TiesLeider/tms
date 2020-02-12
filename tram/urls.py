from django.urls import path
from . import views
 

urlpatterns = [
    path("", views.index, name="index"),
    path("insertlogodata",views.insert_logo_data, name="insert_logo_data"),
    path("insertsmsdata", views.insert_sms_data, name="insert_sms_data"),
    path("insertlogoonline",views.insert_logo_online, name="insert_logo_online"),
    path("storing/<int:storing_id>/gezien",views.storing_gezien, name="storing_gezien"),
    path("storing/<int:storing_id>/deactiveer",views.deactiveer_storing, name="storing_deactiveren"),
    path("asset/<str:assetnummer>", views.asset_index, name="asset_index"),
    path("asset/<str:assetnummer>/resetteller", views.asset.reset_teller_standen, name="asset_reset_teller"),
    path("asset/<str:assetnummer>/corrigeer_omlopen", views.asset.corrigeer_omlopen, name="asset_corrigeer_omlopen"),
    path("api/resettelleralle", views.asset.reset_teller_alle, name="asset_reset_alle"),
    path("api/omlopen_totaal/<str:assetnummer>/<str:van_datum>/<str:tot_datum>", views.api.get_omlopen_totaal, name="get_omlopen_totaal"),
    path("api/omlopen_freq/<str:assetnummer>/<str:van_datum>/<str:tot_datum>", views.api.get_omlopen_freq, name="get_omlopen_freq"),
    path("api/alle_actieve_storingen/", views.get_actieve_storingen, name="alle_actieve_storingen"),
    path("index_form", views.index_form, name="index_form"),
    path("asset_chart/<str:assetnummer>", views.asset_chart, name="asset_chart"),
    path("api/check_online_assets", views.check_assets_online, name="check_online_assets"),
    path("api/get_sms_storingen", views.get_sms_data, name="get_sms_data"),
    path("sms", views.sms_lijst, name="sms_lijst")
]  