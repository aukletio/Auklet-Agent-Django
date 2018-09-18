import json
import msgpack

from uuid import uuid4
from datetime import datetime
from auklet.stats import Event, SystemMetrics
from auklet.utils import create_file, get_commit_hash, \
    get_abs_path, get_device_ip, open_auklet_url, build_url, \
    get_agent_version, u

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request, HTTPError, URLError


MB_TO_B = 1e6
S_TO_MS = 1000


class Client(object):
    producer_types = None
    brokers = None
    commit_hash = None
    mac_hash = None
    offline_filename = ".auklet/local.txt"
    limits_filename = ".auklet/limits"
    usage_filename = ".auklet/usage"
    com_config_filename = ".auklet/communication"
    abs_path = None

    reset_data = False
    data_day = 1
    data_limit = None
    data_current = 0
    offline_limit = None
    offline_current = 0

    system_metrics = None

    def __init__(self, apikey=None, app_id=None,
                 base_url="https://api.auklet.io/", mac_hash=None):
        self.apikey = apikey
        self.app_id = app_id
        self.base_url = base_url
        self.send_enabled = True
        self.producer = None
        self.mac_hash = mac_hash
        self._load_limits()
        create_file(self.offline_filename)
        create_file(self.limits_filename)
        create_file(self.usage_filename)
        create_file(self.com_config_filename)
        self.commit_hash = get_commit_hash()
        self.abs_path = get_abs_path(".auklet/version")
        self.system_metrics = SystemMetrics()

    def _get_config(self):
        res = open_auklet_url(
            build_url(
                self.base_url,
                "private/devices/{}/app_config/".format(self.app_id)),
            self.apikey)
        if res is not None:
            return json.loads(u(res.read()))['config']

    def _load_limits(self):
        try:
            with open(self.limits_filename, "r") as limits:
                limits_str = limits.read()
                if limits_str:
                    data = json.loads(limits_str)
                    self.data_day = data['data']['normalized_cell_plan_date']
                    temp_limit = data['data']['cellular_data_limit']
                    if temp_limit is not None:
                        self.data_limit = data['data'][
                                              'cellular_data_limit'] * MB_TO_B
                    else:
                        self.data_limit = temp_limit
                    temp_offline = data['storage']['storage_limit']
                    if temp_offline is not None:
                        self.offline_limit = data['storage'][
                                                 'storage_limit'] * MB_TO_B
                    else:
                        self.offline_limit = data['storage']['storage_limit']
        except IOError:
            return

    def _build_usage_json(self):
        return {"data": self.data_current, "offline": self.offline_current}

    def _update_usage_file(self):
        try:
            with open(self.usage_filename, 'w') as usage:
                usage.write(json.dumps(self._build_usage_json()))
        except IOError:
            return False

    def check_data_limit(self, data, current_use, offline=False):
        if self.offline_limit is None and offline:
            return True
        if self.data_limit is None and not offline:
            return True
        data_size = len(data)
        temp_current = current_use + data_size
        if temp_current >= self.data_limit:
            return False
        if offline:
            self.offline_current = temp_current
        else:
            self.data_current = temp_current
        self._update_usage_file()
        return True

    def update_network_metrics(self, interval):
        self.system_metrics.update_network(interval)

    def check_date(self):
        if datetime.today().day == self.data_day:
            if self.reset_data:
                self.data_current = 0
                self.reset_data = False
        else:
            self.reset_data = True

    def update_limits(self):
        config = self._get_config()
        if config is None:
            return 60000
        with open(self.limits_filename, 'w+') as limits:
            limits.truncate()
            limits.write(json.dumps(config))
        new_day = config['data']['normalized_cell_plan_date']
        temp_limit = config['data']['cellular_data_limit']
        if temp_limit is not None:
            new_data = config['data']['cellular_data_limit'] * MB_TO_B
        else:
            new_data = temp_limit
        temp_offline = config['storage']['storage_limit']
        if temp_offline is not None:
            new_offline = config['storage']['storage_limit'] * MB_TO_B
        else:
            new_offline = config['storage']['storage_limit']
        if self.data_day != new_day:
            self.data_day = new_day
            self.data_current = 0
        if self.data_limit != new_data:
            self.data_limit = new_data
        if self.offline_limit != new_offline:
            self.offline_limit = new_offline
        # return emission period in ms
        return config['emission_period'] * S_TO_MS

    def build_event_data(self, type, traceback, tree):
        event = Event(type, traceback, tree, self.abs_path)
        event_dict = dict(event)
        event_dict['application'] = self.app_id
        event_dict['publicIP'] = get_device_ip()
        event_dict['id'] = str(uuid4())
        event_dict['timestamp'] = str(datetime.utcnow())
        event_dict['systemMetrics'] = dict(self.system_metrics)
        event_dict['macAddressHash'] = self.mac_hash
        event_dict['commitHash'] = self.commit_hash
        event_dict['agentVersion'] = get_agent_version()
        return event_dict

    def build_log_data(self, msg, data_type, level):
        log_dict = {
            "message": msg,
            "type": data_type,
            "level": level,
            "application": self.app_id,
            "publicIP": get_device_ip(),
            "id": str(uuid4()),
            "timestamp": str(datetime.utcnow()),
            "systemMetrics": dict(SystemMetrics()),
            "macAddressHash": self.mac_hash,
            "commitHash": self.commit_hash,
            "agentVersion": get_agent_version()
        }
        return log_dict

    def build_msgpack_event_data(self, type, traceback, tree):
        event_data = self.build_event_data(type, traceback, tree)
        return msgpack.packb(event_data, use_bin_type=False)

    def build_msgpack_log_data(self, msg, data_type, level):
        log_data = self.build_log_data(msg, data_type, level)
        return msgpack.packb(log_data, use_bin_type=False)
