If you wish set up Auklet using a wsgi middleware instead of the
default django middleware:

.. sourcecode:: python

    import os
    from django.core.wsgi import get_wsgi_application
    from django.conf import settings
    from auklet.middleware import WSGIAukletMiddleware

    application = get_wsgi_application()
    application = WSGIAukletMiddleware(application)
