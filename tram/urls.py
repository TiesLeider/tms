from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
 

urlpatterns = [
    #Storing
    path("", views.index, name="index"),
    path("storing/<int:storing_id>/gezien",views.storing_gezien, name="storing_gezien"),
    path("storing/<int:storing_id>/deactiveer",views.deactiveer_storing, name="storing_deactiveren"),
    path("sms", views.sms_lijst, name="sms_lijst"),

    #API
    path("api/", views.api_docs, name="api_docs"),
    path("api/resettelleralle", views.asset.reset_teller_alle, name="asset_reset_alle"),
    path("api/alle_actieve_storingen/", views.get_actieve_storingen, name="alle_actieve_storingen"),
    path("index_form", views.index_form, name="index_form"),
    path("api/check_online_assets", views.check_online_assets, name="check_online_assets"),
    path("api/get_sms_storingen", views.get_sms_data, name="get_sms_data"),
    path("api/get_sensor_waarden/<str:assetnummer>/<str:veld>", views.api.get_sensor_waarden, name="get_sensor_waarden"),
    path("api/get_sensor_waarden_oud/<str:assetnummer>/<str:veld>", views.api.get_sensor_waarden_oud, name="get_sensor_waarden"),
    path("api/get_maand_gemiddelde/<str:assetnummer>/<str:veld>", views.api.get_maand_gemiddelde, name="get_maand_gemiddelde"),
    path("api/get_ipnummers", views.get_ipnummers, name="get_ipnummers"),
    path("api/dashboard_omlopen", views.dashboard_omlopen, name="dashboard_omlopen"),
    path("api/dashboard_omlopen/<str:van_datum>/<str:tot_datum>", views.dashboard_omlopen_timerange, name="dashboard_storingen_timerange"),
    path("api/dashboard/storing/<str:storing>", views.dashboard_storingen, name="dashboard_storingen"),
    path("api/dashboard/storing/<str:storing>/<str:van_datum>/<str:tot_datum>", views.dashboard_storingen_timerange, name="dashboard_storingen_timerange"),

    #Asset
    path("insertlogodata",views.insert_logo_data, name="insert_logo_data"),
    path("insertsmsdata", views.insert_sms_data, name="insert_sms_data"),
    path("asset/<str:assetnummer>", views.asset_index, name="asset_index"),
    path("asset/<str:assetnummer>/resetteller", views.asset.reset_teller_standen, name="asset_reset_teller"),
    path("asset/<str:assetnummer>/corrigeer_omlopen", views.asset.corrigeer_omlopen, name="asset_corrigeer_omlopen"),
    path("asset_chart/<str:assetnummer>", views.asset_chart, name="asset_chart"),
    path("analyse/<str:assetnummer>/<str:veld>", views.asset_analyse, name="asset_analyse"),
    path("asset_lijst", views.asset_lijst, name="asset_lijst"),
    path("asset_dashboard/", views.dashboard, name="dashboard"),

    #User Account Control
    path("login", auth_views.LoginView.as_view(template_name="tram/login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(template_name="tram/logout.html"), name="logout"),
    path("change_password", views.change_password, name="change_password"),

    #Systeem
    path("livesign", views.livesign, name="livesign"),
    path("error", views.error, name="error"),
    path("logfile", views.show_api_log, name="logfile")
]  
