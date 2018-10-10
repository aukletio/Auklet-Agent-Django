from __future__ import absolute_import

import sys
import signal
from six import iteritems
from six.moves import _thread

from auklet.monitoring.logging import AukletLogging
from auklet.stats import Stack


class Monitoring(object):
    samples_taken = 0
    timer = signal.ITIMER_PROF
    sig = signal.SIGPROF
    stopping = False
    stopped = False

    interval = 1e-3  # 1ms

    total_samples = 0

    emission_rate = 60000  # 60 seconds
    network_rate = 10000  # 10 seconds
    hour = 3600000  # 1 hour

    def __init__(self):
        signal.signal(self.sig, self.sample)
        signal.siginterrupt(self.sig, False)
        self.stack = Stack()
        super(Monitoring, self).__init__()

    def start(self):
        # Set a timer which fires a SIGALRM every `interval` seconds
        signal.setitimer(self.timer, self.interval, self.interval)

    def stop(self):
        self.stopping = True

    def wait_for_stop(self):
        while not self.stopped:
            pass

    def sample(self, sig, current_frame):
        """Samples the given frame."""
        if self.stopping:
            signal.setitimer(self.timer, 0, 0)
            self.stopped = True
            return
        current_thread = _thread.get_ident()
        for thread_id, frame in iteritems(sys._current_frames()):
            if thread_id == current_thread:
                frame = current_frame
            frames = []
            while frame is not None:
                frames.append(frame)
                frame = frame.f_back
            self.stack.update_hash(frames)
        self.total_samples += 1
        self.samples_taken += 1

    def get_stack(self):
        return self.stack.get()
