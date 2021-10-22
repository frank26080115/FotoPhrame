import sys, os, io, gc, random, time, datetime, subprocess, glob

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
