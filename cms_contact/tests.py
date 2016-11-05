from django.core.urlresolvers import reverse
from django.test import TestCase


class AjaxPopulateAddressTest(TestCase):
    def setUp(self):
        pass

    def test_no_params(self):
        self.client.get(reverse('dataType'))
