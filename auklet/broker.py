from __future__ import absolute_import

import ssl
import logging
import paho.mqtt.client as mqtt

from auklet.utils import build_url, create_file

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request, HTTPError, URLError

__all__ = ["MQTTClient"]


class MQTTClient(object):
    producer = None
    brokers = "mq.feeds.auklet.io"
    client = None
    username = None
    password = None
    port = 8883
    producer_types = {
        "monitoring": "django/profiler/{}/{}",
        "event": "django/events/{}/{}",
    }

    def __init__(self, broker_url, port, app_id, org_id, apikey, base_url,
                 auklet_dir):
        self.brokers = broker_url
        self.port = int(port)
        self.org_id = org_id
        self.app_id = app_id
        self.apikey = apikey
        self.base_url = base_url
        self.auklet_dir = auklet_dir
        self.create_producer()
        topic_suffix = "{}/{}".format(
            self.org_id, self.app_id)
        self.producer_types = {
            "monitoring": "python/profiler/{}".format(topic_suffix),
            "event": "python/events/{}".format(topic_suffix),
        }

    def _get_certs(self):
        url = Request(
            build_url(self.base_url, "private/devices/certificates/"),
            headers={"Authorization": "JWT {}".format(self.apikey)})
        try:
            try:
                res = urlopen(url)
            except HTTPError as e:
                # Allow for accessing redirect w/o including the
                # Authorization token.
                res = urlopen(e.geturl())
        except (URLError, Exception) as e:
            print(e)
            return False
        try:
            filename = "{}/ca.pem".format(self.auklet_dir)
            create_file(filename)
            f = open(filename, "wb")
            f.write(res.read())
            print(f)
            print(f.seek(0))
            print(f.read())
        except Exception as e:
            import traceback
            import subprocess
            traceback.print_exc()
            p = subprocess.Popen("whoami", stdout=subprocess.PIPE, shell=True)
            output, err = p.communicate()
            print("WHOAMI OUTPUT: ", output)
            print("TRYING TO CREATE FILE:", e)
        return True

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logging.debug("Unexpected disconnection from MQTT")

    def create_producer(self):
        if self._get_certs():
            self.producer = mqtt.Client(client_id=self.app_id,
                                        protocol=mqtt.MQTTv311,
                                        transport="ssl")
            self.producer.username_pw_set(
                username=self.app_id,
                password=self.apikey)
            self.producer.enable_logger()
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(capath="{}/".format(self.auklet_dir))
            context.options &= ~ssl.OP_NO_SSLv3
            self.producer.tls_set_context()
            self.producer.on_disconnect = self.on_disconnect
            self.producer.connect_async(self.brokers, self.port)
            self.producer.loop_start()

    def produce(self, data, data_type="monitoring"):
        self.producer.publish(self.producer_types[data_type], payload=data)
