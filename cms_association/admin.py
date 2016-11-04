from django import forms
from django.contrib import admin

from cms_association.models import Association
from cms_contact.admin import IncludeAddressForm, IncludeAddressAdmin


class AssociationForm(IncludeAddressForm):
    class Meta:
        model = Association
        exclude = ()


@admin.register(Association)
class AssociationAdmin(IncludeAddressAdmin):
    prepopulated_fields = {"slug": ("name",)}

    class Media:
        js = ('cms_contact/src/js/jquery-admin-init.js',)
        css = {'all': ('//cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/css/select2.min.css',
                       'pywebes/src/libs/select2-bootstrap-theme/dist/select2-bootstrap.css',)}
