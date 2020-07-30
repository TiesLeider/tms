from django.test import SimpleTestCase
from django.urls import reverse, resolve
from tram.views import *
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):

#Storing
    def test_index_url_resolves(self):
        url = reverse("index")
        self.assertEquals(resolve(url).func, index)
    
    def test_storing_gezien_url_resolves(self):
        url = reverse("storing_gezien", args=["1"])
        self.assertEquals(resolve(url).func, storing_gezien)

    def test_storing_deactiveren_url_resolves(self):
        url = reverse("storing_deactiveren",  args=["1"])
        self.assertEquals(resolve(url).func, deactiveer_storing)

    def test_sms_lijst_url_resolves(self):
        url = reverse("sms_lijst")
        self.assertEquals(resolve(url).func, sms_lijst)

#API
    def api_docs_url_resolves(self):
        url = reverse("url_docs")
        self.assertEquals(resolve(url).func, api_docs)

    def test_asset_reset_alle_url_resolves(self):
        url = reverse("asset_reset_alle",  args=["W001"])
        self.assertEquals(resolve(url).func, reset_teller_alle)

    def test_alle_actieve_storingen_url_resolves(self):
        url = reverse("alle_actieve_storingen")
        self.assertEquals(resolve(url).func, get_actieve_storingen)

    def test_index_form_url_resolves(self):
        url = reverse("index_form")
        self.assertEquals(resolve(url).func, index_form)

    def test_check_online_assets_url_resolves(self):
        url = reverse("check_online_assets")
        self.assertEquals(resolve(url).func, check_online_assets)

    def test_get_sms_data_url_resolves(self):
        url = reverse("get_sms_data")
        self.assertEquals(resolve(url).func, get_sms_data)

    def test_get_sensor_waarden_url_resolves(self):
        url = reverse("get_sensor_waarden", args=["W001", "omloop_a"])
        self.assertEquals(resolve(url).func, get_sensor_waarden)
    
    def test_get_ip_nummers_url_resolves(self):
        url = reverse("get_ipnummers")
        self.assertEquals(resolve(url).func, get_ipnummers)
    
    def test_dashboard_omlopen_url_resolves(self):
        url = reverse("dashboard_omlopen")
        self.assertEquals(resolve(url).func, dashboard_omlopen)
    
    def test_dashboard_omlopen_timerange_url_resolves(self):
        url = reverse("dashboard_omlopen_timerange", args=["01-05-2020", "20-05-2020"])
        self.assertEquals(resolve(url).func, dashboard_omlopen_timerange)
    
    def test_dashboard_storingen_url_resolves(self):
        url = reverse("dashboard_storingen", args=["omloop_a"])
        self.assertEquals(resolve(url).func, dashboard_storingen)
    
    def test_dashboard_storingen_timerange_url_resolves(self):
        url = reverse("dashboard_storingen_timerange",  args=["omloop_a", "01-05-2020", "20-05-2020"])
        self.assertEquals(resolve(url).func, dashboard_storingen_timerange)

#Asset
    def test_insert_logo_data_resolves(self):
        url = reverse("insert_logo_data")
        self.assertEquals(resolve(url).func, insert_logo_data)

    def test_insert_sms_data_resolves(self):
        url = reverse("insert_sms_data")
        self.assertEquals(resolve(url).func, insert_sms_data)

    def test_asset_index_url_resolves(self):
        url = reverse("asset_index", args=["W001"])
        self.assertEquals(resolve(url).func, asset_index)

    def test_asset_reset_teller_url_resolves(self):
        url = reverse("asset_reset_teller", args=["W001"])
        self.assertEquals(resolve(url).func, reset_teller_standen)
    
    def test_asset_reset_alle_url_resolves(self):
        url = reverse("asset_reset_alle")
        self.assertEquals(resolve(url).func, reset_teller_alle)

    def test_asset_corrigeer_omlopen_url_resolves(self):
        url = reverse("asset_corrigeer_omlopen", args=["W001"])
        self.assertEquals(resolve(url).func, corrigeer_omlopen)
    
    def test_asset_lijst_url_resolves(self):
        url = reverse("asset_lijst")
        self.assertEquals(resolve(url).func, asset_lijst)
    
    def test_dashboard_url_resolves(self):
        url = reverse("dashboard")
        self.assertEquals(resolve(url).func, dashboard)

#User Account Control
    def test_change_password_url_resolves(self):
        url = reverse("change_password")
        self.assertEquals(resolve(url).func, change_password)

#Systeem
    def test_livesign_url_resolves(self):
        url = reverse("livesign")
        self.assertEquals(resolve(url).func, livesign)

    def test_error_url_resolves(self):
        url = reverse("error")
        self.assertEquals(resolve(url).func, error)
    
    def test_logfile_url_resolves(self):
        url = reverse("logfile")
        self.assertEquals(resolve(url).func, show_api_log)