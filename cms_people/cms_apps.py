from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class PeopleApphook(CMSApp):
    app_name = "people"
    name = _("People Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["cms_people.urls.people"]


apphook_pool.register(PeopleApphook)  # register the application
