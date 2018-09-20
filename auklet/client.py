import json
import msgpack

from time import time
from uuid import uuid4

from django.conf import settings

from auklet.errors import AukletConfigurationError
from auklet.broker import MQTTClient
from auklet.stats import Event, SystemMetrics, FilenameCaches
from auklet.utils import create_file, get_agent_version, get_device_ip, \
                         get_mac, get_abs_path, open_auklet_url, build_url, u

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
    identification_filename = ".auklet/identification"

    def __init__(self):
        auklet_config = settings.AUKLET_CONFIG
        self.apikey = auklet_config.get("api_key", None)
        self.app_id = auklet_config.get("app_id", None)
        self.release = auklet_config.get("release", None)
        self.version = auklet_config.get("version", None)
        self.base_url = auklet_config.get("base_url", "https://api.auklet.io/")

        if self.apikey is None:
            raise AukletConfigurationError(
                "Please set api_key in AUKLET_CONFIG settings")
        if self.app_id is None:
            raise AukletConfigurationError(
                "Please set app_id in AUKLET_CONFIG settings")
        if self.release is None:
            raise AukletConfigurationError(
                "Please set release in AUKLET_CONFIG settings")
        create_file(self.identification_filename)
        self.org_id = self.get_org_id()
        self.abs_path = get_abs_path(self.identification_filename)
        self.mac_hash = get_mac()
        self.device_ip = get_device_ip()
        self.agent_version = get_agent_version()
        self.broker = MQTTClient(self)
        self.file_cache = FilenameCaches()

    def get_org_id(self):
        try:
            with open(self.identification_filename, "r") as id_file:
                res = id_file.read()
        except IOError:
            res = False
        if not res:
            res = open_auklet_url(
                build_url(self.base_url,
                          "private/devices/{}/app_config/".format(
                              self.app_id)),
                self.apikey
            )
            res = json.loads(u(res.content))['config']['org_id']
        if res is not None:
            self.write_org_id(res)
            return res

    def write_org_id(self, org_id):
        with open(self.identification_filename, "w") as id_file:
            id_file.write(org_id)

    def build_event_data(self, type, traceback):
        event = Event(type, traceback, self.file_cache, self.abs_path)
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
        event_dict['absPath'] = self.abs_path
        return event_dict

    def build_msgpack_event_data(self, type, traceback):
        event_data = self.build_event_data(type, traceback)
        return msgpack.packb(event_data, use_bin_type=False)

    def produce_event(self, type, traceback):
        self.broker.produce(self.build_msgpack_event_data(type, traceback))


def init_client():
    global client
    client = DjangoClient()
