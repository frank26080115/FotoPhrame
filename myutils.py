import sys, os, io, gc, random, time, datetime, subprocess, glob
import threading, queue

def get_all_files(dirpath, allexts):
    allfiles = []
    results  = []
    for ext in allexts:
        allfiles.extend(glob.glob(os.path.join(dirpath, ext        ), recursive = True))
        allfiles.extend(glob.glob(os.path.join(dirpath, ext.upper()), recursive = True))
    for i in allfiles:
        found = False
        for j in results:
            if i.lower() == j.lower():
                found = True
                break
        if not found:
            results.append(i)
    return results

def get_ip_address():
    import socket
    ip_address = '';
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("www.google.com", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except:
        s = subprocess.check_output(['hostname', '-I'])
        s = str(s)
        s = s.split(' ')
        return s[0]

class BgKeyboard(object):

    def __init__(self, parent, kb):
        self.parent = parent
        self.kb = kb
        self.queue = queue.Queue()
        self.t = threading.Thread(target = self.task)
        self.stop_event = threading.Event()
        self.t.start()

    def read_(self):
        return self.kb.read()

    def read(self):
        if self.queue.empty():
            return -1
        return self.queue.get()

    def halt(self):
        self.stop_event.set()

    def task(self):
        x = None
        last_key = 0
        while not self.stop_event.is_set():
            try:
                #x = ord(sys.stdin.read())
                x = self.kb.read()
            except KeyboardInterrupt as ex:
                x = 27
            if x is not None:
                if x > 0 and x != 0xFF:
                    if last_key != x:
                        print("key 0x%08X" % x, flush=True)
                        self.queue.put(x)
                    time.sleep(0.01)
                else:
                    time.sleep(0.0001)
                last_key = x

    def close(self):
        self.stop_event.set()
        pass

    def __del__(self):
        try:
            self.close()
        except:
            pass
