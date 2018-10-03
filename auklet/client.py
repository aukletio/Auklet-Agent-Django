import msgpack

from time import time
from uuid import uuid4

from django.conf import settings

from auklet.errors import AukletConfigurationError
from auklet.broker import MQTTClient
from auklet.stats import Event, SystemMetrics, FilenameCaches
from auklet.utils import get_agent_version, get_device_ip, get_mac, \
                         create_dir

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request, HTTPError, URLError


_client = None


def get_client():
    """
    Get an Auklet Client
    """
    global _client
    if _client is None:
        _client = DjangoClient()
    return _client


class DjangoClient(object):
    def __init__(self):
        auklet_config = settings.AUKLET_CONFIG
        self.apikey = auklet_config.get("api_key", None)
        self.app_id = auklet_config.get("application", None)
        self.release = auklet_config.get("release", None)
        self.version = auklet_config.get("version", None)
        self.org_id = auklet_config.get("organization", None)
        self.broker_url = auklet_config.get("broker", "mq.feeds.auklet.io")
        self.port = auklet_config.get("port", 8883)
        self.base_url = auklet_config.get("base_url", "https://api.auklet.io/")

        if self.apikey is None:
            raise AukletConfigurationError(
                "Please set api_key in AUKLET_CONFIG settings")
        if self.app_id is None:
            raise AukletConfigurationError(
                "Please set application in AUKLET_CONFIG settings")
        if self.org_id is None:
            raise AukletConfigurationError(
                "Please set organization in AUKLET_CONFIG settings")
        self.auklet_dir = create_dir()
        self.mac_hash = get_mac()
        self.device_ip = get_device_ip()
        self.agent_version = get_agent_version()
        self.broker = MQTTClient(self.broker_url, self.port, self.app_id,
                                 self.org_id, self.apikey, self.base_url,
                                 self.auklet_dir)
        self.file_cache = FilenameCaches()

    def build_event_data(self, type, traceback):
        event = Event(type, traceback, self.file_cache)
        event_dict = dict(event)
        event_dict['application'] = self.app_id
        event_dict['publicIP'] = get_device_ip()
        event_dict['id'] = str(uuid4())
        event_dict['timestamp'] = int(round(time() * 1000))
        event_dict['systemMetrics'] = dict(SystemMetrics())
        event_dict['macAddressHash'] = self.mac_hash
        event_dict['release'] = self.release
        event_dict['version'] = self.version
        event_dict['agentVersion'] = get_agent_version()
        event_dict['device'] = None
        return event_dict

    def build_msgpack_event_data(self, type, traceback):
        event_data = self.build_event_data(type, traceback)
        return msgpack.packb(event_data, use_bin_type=False)

    def produce_event(self, type, traceback):
        self.broker.produce(self.build_msgpack_event_data(type, traceback))


def init_client():
    global client
    client = DjangoClient()
