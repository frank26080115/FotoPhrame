import subprocess, datetime
from enum import Enum

TIME_TO_SLEEP = 600

class MonitorState(Enum):
    On         = 0
    OnPending  = 1
    Off        = 2
    OffPending = 3

class HdmiCtrl(object):

    def __init__(self, parent, time_to_sleep = TIME_TO_SLEEP):
        self.parent = parent
        self.time_to_sleep = time_to_sleep
        self.mon_state = MonitorState.On
        self.last_activity_time = datetime.datetime.now()

    def force_off(self):
        self.last_activity_time = datetime.datetime.now()
        subprocess.Popen("xset dpms force standby".split())
        self.mon_state = MonitorState.OffPending

    def force_on(self):
        self.last_activity_time = datetime.datetime.now()
        subprocess.Popen("xset dpms force on".split())
        self.mon_state = MonitorState.OnPending

    def set_timer(self, time_to_sleep = None):
        if time_to_sleep is not None:
            self.time_to_sleep = time_to_sleep
        #self.last_activity_time = datetime.datetime.now()
        subprocess.Popen(("xset s %u %u" % (self.time_to_sleep, self.time_to_sleep)).split())

    def get_seconds_since(self):
        now = datetime.datetime.now()
        span = now - self.last_activity_time
        return span.total_seconds()

    def poke(self, force = False):
        if force or self.get_seconds_since() > (self.time_to_sleep / 2):
            self.force_on()
            self.set_timer()
            self.hide_mouse()

    def is_monitor_reported_on(self):
        s = subprocess.check_output(['xset', 'q'])
        s = str(s)
        if len(s) <= 0:
            print("unable to parse monitor status")
            return True
        s = s.lower()
        if "monitor is off" in s or "monitor is susp" in s:
            return False
        return True

    def is_monitor_on(self):
        x = self.is_monitor_reported_on()
        if self.mon_state == MonitorState.On and x:
            return True
        elif self.mon_state == MonitorState.On and not x:
            self.mon_state = MonitorState.Off
            return False
        elif self.mon_state == MonitorState.OnPending and x:
            self.mon_state = MonitorState.On
            return True
        elif self.mon_state == MonitorState.OnPending and not x:
            return True
        elif self.mon_state == MonitorState.Off and x:
            self.mon_state = MonitorState.On
            return True
        elif self.mon_state == MonitorState.Off and not x:
            self.mon_state = MonitorState.Off
            return False
        elif self.mon_state == MonitorState.OffPending and x:
            return False
        elif self.mon_state == MonitorState.OffPending and not x:
            self.mon_state = MonitorState.Off
            return False
        return True

    def hide_mouse(self):
        subprocess.Popen(['unclutter', '-idle', '3', '-grab'])
