from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class EventApphook(CMSApp):
    app_name = "association"
    name = _("Event Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["cms_event.urls"]


apphook_pool.register(EventApphook)  # register the application
