from django.contrib import admin

from cms_contact.models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
