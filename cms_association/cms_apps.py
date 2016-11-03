from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class AssociationApphook(CMSApp):
    app_name = "association"
    name = _("Association Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["cms_association.urls"]


apphook_pool.register(AssociationApphook)  # register the application
