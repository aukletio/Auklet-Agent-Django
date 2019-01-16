from os import environ


def set_config():
    environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'settings'
    )


if __name__ == "__main__":
    set_config()
