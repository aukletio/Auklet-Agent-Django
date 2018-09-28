# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.apps import AppConfig


class AukletConfig(AppConfig):
    name = "auklet.client"
    label = "auklet_client"
    verbose_name = "Auklet"

    def ready(self):
        from .client import init_client
        init_client()
