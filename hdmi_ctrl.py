import subprocess

def force_off():
    subprocess.Popen("xset dpms force standby".split())

def force_on():
    subprocess.Popen("xset dpms force on".split())

def is_monitor_on():
    s = subprocess.check_output(['xset', 'q'])
    s = str(s)
    if len(s) <= 0:
        print("unable to parse monitor status")
        return True
    s = s.lower()
    if "monitor is off" in s or "monitor is susp" in s:
        return False
    return True

def hide_mouse():
    subprocess.Popen(['unclutter', '-idle', '3'])
