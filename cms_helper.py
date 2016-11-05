from cms_contact import settings_test

HELPER_SETTINGS = {x: getattr(settings_test, x) for x in dir(settings_test) if x.isupper()}

def run():
    from djangocms_helper import runner
    runner.cms('cms_contact')


def setup():
    import sys
    from djangocms_helper import runner
    runner.setup('cms_contact', sys.modules[__name__], use_cms=True)


if __name__ == '__main__':
    run()
