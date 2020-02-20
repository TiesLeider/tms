from django.test import SimpleTestCase
from django.urls import reverse, resolve
from tram.views import *

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
    def test_asset_reset_alle_url_resolves(self):
        url = reverse("asset_reset_alle",  args=["W001"])
        self.assertEquals(resolve(url).func, reset_teller_alle)

    def test_get_omlopen_totaal_url_resolves(self):
        url = reverse("get_omlopen_totaal",  args=["W001", "12-12-2019", "13-12-2019"])
        self.assertEquals(resolve(url).func, get_omlopen_totaal)

    def test_get_omlopen_freq_url_resolves(self):
        url = reverse("get_omlopen_freq", args=["W001", "12-12-2019", "13-12-2019"])
        self.assertEquals(resolve(url).func, get_omlopen_freq)

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

#Asset
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
    
    def test_asset_chart_url_resolves(self):
        url = reverse("asset_chart", args=["W001"])
        self.assertEquals(resolve(url).func, asset_chart)
