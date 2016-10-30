import re

import unicodedata
from django.core.validators import URLValidator, EmailValidator
from django.utils.http import urlquote
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.validators import validate_international_phonenumber


class RegexValidator(object):
    def __init__(self, pattern):
        self.regex = re.compile(pattern)

    def __call__(self, value):
        return self.regex.match(value)


class Href(object):
    def __init__(self, url_pattern, value_pattern='{}'):
        self.url_pattern = url_pattern
        self.value_pattern = value_pattern

    def __call__(self, value):
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(
            self.url_pattern.format(urlquote(value, '/@+')),
            self.value_pattern.format(escape(value))
        ))


def multi_lang_common_validator(value):
    """Validate usernames with support for all languages but with strange symbols
    """
    if len(value) > 50:
        return False
    for c in value:
        cat = unicodedata.category(c)
        if not (cat.startswith('L') or cat == 'Nd' or c in '-_ '):
            return False
    return True


CONTACT_FIELD_TYPES = [
    (
        _('VCS'),
        (
            ('GITHUB', _('Github'), {'validator': RegexValidator('^([a-z0-9](?:-?[a-z0-9]){0,38})$'),
                                     'to_html': Href('https://github.com/{}/')}),
            ('BITBUCKET', _('Bitbucket'), {'validator': multi_lang_common_validator,
                                           'to_html': Href('https://bitbucket.org/{}/')}),
            ('GITLAB', _('Gitlab'), {'validator': multi_lang_common_validator,
                                     'to_html': Href('https://gitlab.com/{}')}),
        ),
    ),
    (
        _('Social'),
        (
            ('TWITTER', _('Twitter'), {'validator': RegexValidator('^\w{1,15}$'),
                                       'to_html': Href('https://twitter.com/{}', '@{}')}),
            ('FACEBOOK', _('Facebook'), {'validator': multi_lang_common_validator,
                                         'to_html': Href('https://www.facebook.com/{}/')}),
            ('GOOGLE-PLUS', _('Google+'), {'validator': multi_lang_common_validator,
                                           'to_html': Href('https://plus.google.com/+{}', '+{}')}),
            ('LINKEDIN', _('LinkedIn'), {'validator': multi_lang_common_validator,
                                         'to_html': Href('https://www.linkedin.com/in/{}/')}),
            ('PINTEREST', _('Pinterest'), {'validator': multi_lang_common_validator,
                                           'to_html': Href('https://www.pinterest.com/{}/')}),
            ('TUMBLR', _('Tumblr'), {'validator': multi_lang_common_validator,
                                     'to_html': Href('http://{}.tumblr.com')}),
            ('WEBSITE', _('Website'), {
                'validator': URLValidator,
                'to_html': lambda x: mark_safe('<a href="{0}" rel="nofollow" target="_blank">{0}</a>'.format(escape(x)))
            }),
        ),
    ),
    (
        _('Communication'),
        (
            ('TELEPHONE', _('Telephone'), {'validator': validate_international_phonenumber}),
            ('MOBILE', _('Mobile'), {'validator': validate_international_phonenumber}),
            ('WHATSAPP', _('WhatsApp'), {'validator': validate_international_phonenumber}),
            ('TELEGRAM', _('Telegram'), {'validator': multi_lang_common_validator,
                                         'to_html': Href('https://telegram.me/{}', '@{}')}),
            ('SKYPE', _('Skype'), {'validator': multi_lang_common_validator, 'to_html': Href('skype:{}?call')}),
            ('FMESSENGER', _('Facebook Messenger'), {'validator': multi_lang_common_validator}),
            ('LINE', _('Line'), {'validator': multi_lang_common_validator}),
            ('IRC', _('IRC'), {'validator': EmailValidator, 'to_html': Href('irc:///{}')}),
            ('JABBER', 'Jabber/XMPP', {'validator': EmailValidator, 'to_html': Href('xmpp://{}')}),
        ),
    ),
]


def remove_social_options(sections):
    """Remove additional options in SOCIAL_TYPES
    """
    for section in sections:
        yield section[0], [choice[:2] for choice in section[1]]


def social_by_keys(sections):
    """Convert the social list in a dictionary by key.
    """
    data = {}
    for section in CONTACT_FIELD_TYPES:
        section_name = section[0]
        for choice in section[1]:
            data[choice[0]] = dict(name=choice[1], section_name=section_name, **choice[2] if len(choice) > 2 else {})
    return data


SOCIAL = social_by_keys(CONTACT_FIELD_TYPES)
