from django.test import SimpleTestCase
from django.urls import reverse, resolve
from website.views import index, ContactPage


# Create your tests here
class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_contact_page_url_is_resolved(self):
        url = reverse('contact_us')
        self.assertEquals(resolve(url).func.view_class, ContactPage)
