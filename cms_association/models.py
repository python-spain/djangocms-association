from cities.models import District, City, Subregion, Region, Country
from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models


class AbstractAddress(models.Model):
    street = models.CharField(max_length=120)
    poiny = PointField(blank=True, null=True)
    district = models.ForeignKey(District, blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
    custom_city = models.CharField(max_length=40, blank=True)
    custom_postal_code = models.CharField(max_length=15, blank=True)
    subregion = models.ForeignKey(Subregion, blank=True, null=True, on_delete=models.SET_NULL)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    def clean(self):
        if not self.city and not self.custom_city:
            raise ValidationError(_('You must provide a city or a custom city'))
        elif self.city and self.custom_city:
            raise ValidationError(_('You can not provide custom city if you provided a city'))
        elif not self.custom_postal_code and self.custom_city:
            raise ValidationError(_('You must provide a postal code if you use a custom city'))

    class Meta:
        abstract = True


class Address(AbstractAddress):
    pass
