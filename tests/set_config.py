from os import environ


def set_config():
    environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'settings'
    )


file_name = "settings.py"
data = 'SECRET_KEY = 123\n\n' \
       'AUKLET_CONFIG = {\n' \
       '    "api_key": "123",\n' \
       '    "application": "123",\n' \
       '    "organization": "123ß"\n' \
       '}'
open(file_name, "a").close()
with open(file_name, "w") as file:
    file.write(data)
