import os
import sys
import uuid
import hashlib
import requests

from auklet.__about__ import __version__ as auklet_version
from auklet.errors import AukletConfigurationError

__all__ = ['open_auklet_url', 'create_file', 'clear_file', 'build_url',
           'get_commit_hash', 'get_mac', 'get_device_ip', 'get_agent_version',
           'post_auklet_url', 'setup_thread_excepthook', 'get_abs_path',
           'b', 'u']


def open_auklet_url(url, apikey):
    try:
        res = requests.get(url, headers={"Authorization": "JWT %s" % apikey})
    except requests.HTTPError as e:
        if e.status_code == 401:
            raise AukletConfigurationError(
                "Invalid configuration of Auklet Monitoring, "
                "ensure proper API key and app ID passed to "
                "Monitoring class"
            )
        raise e
    except Exception as e:
        return None
    return res


def post_auklet_url(url, apikey, data):
    try:
        res = requests.post(
            url,
            json=data,
            headers={"Authorization": "JWT %s" % apikey,
                     "Content-Type": "application/json"})
    except requests.HTTPError:
        return None
    return res.json()


def create_file(filename):
    open(filename, "a").close()


def clear_file(filename):
    open(filename, "w").close()


def build_url(base_url, extension):
    return '%s%s' % (base_url, extension)


def get_mac():
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    return hashlib.md5(b(mac)).hexdigest()


def get_commit_hash():
    try:
        with open(".auklet/version", "r") as auklet_file:
            return auklet_file.read().rstrip()
    except IOError:
        # TODO Error out app if no commit hash
        return ""

def get_abs_path(path):
    try:
        return os.path.abspath(path).split('/.auklet')[0]
    except IndexError:
        return ''


def get_device_ip():
    try:
        res = requests.get("https://api.ipify.org")
        return u(res.read())
    except (requests.RequestException, Exception):
        # TODO log to kafka if the ip service fails for any reason
        return None


def get_agent_version():
    return auklet_version


def setup_thread_excepthook():
    import threading
    """
    Workaround for `sys.excepthook` thread bug from:
    http://bugs.python.org/issue1230540

    Call once from the main thread before creating any threads.
    """
    init_original = threading.Thread.__init__

    def init(self, *args, **kwargs):

        init_original(self, *args, **kwargs)
        run_original = self.run

        def run_with_except_hook(*args2, **kwargs2):
            try:
                run_original(*args2, **kwargs2)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                sys.excepthook(*sys.exc_info())

        self.run = run_with_except_hook

    threading.Thread.__init__ = init


if sys.version_info < (3,):
    # Python 2 and 3 String Compatibility
    def b(x):
        return x

    def u(x):
        return x
else:
    # https://pythonhosted.org/six/#binary-and-text-data
    import codecs

    def b(x):
        # Produces a unicode string to encoded bytes
        return codecs.utf_8_encode(x)[0]

    def u(x):
        # Produces a byte string from a unicode object
        return codecs.utf_8_decode(x)[0]
