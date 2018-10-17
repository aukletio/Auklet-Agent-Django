from os import environ


def set_config():
    environ.setdefault(
            'DJANGO_SETTINGS_MODULE',
            'config.settings'
        )