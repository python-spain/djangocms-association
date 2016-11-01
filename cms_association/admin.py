from django.contrib import admin

from cms_association.models import Association

@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    pass
