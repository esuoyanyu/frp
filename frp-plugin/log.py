#!/usr/bin/env python

#coding=< UTF-8>

import os
from datetime import datetime
from datetime import date
from datetime import timedelta

ERROR=0
INFO=1

class logger():
    def __init__(self, path, level, start, interval = 1):
        now = str(date.today()) + "-" + start
        self.interval = timedelta(days = interval)
        self.start_time = datetime.strptime(now, "%Y-%m-%d-%H-%M-%S")
        self.end_time = self.start_time + self.interval
        self.name = path + now + "." + level
        self.path = path
        self.level = level
        self.fd = None
   
    def write(self, date):
        if not os.path.exists(self.name):
            if self.fd != None:
                self.fd.close()
                self.fd = None
            self.fd = open(self.name, 'w')

        now = datetime.now()
        if self.fd == None or self.end_time < now:
            if self.end_time < now:
                self.start_time = self.end_time
                self.end_time += self.interval
                self.name = self.path + now.strftime("%Y-%m-%d-%H-%M-%s") + "." + self.level
                if self.fd != None:
                    self.fd.close()
                    self.fd = None
            self.fd = open(self.name, 'w')

        str_now = now.strftime("%Y-%m-%d-%H:%M:%S") + ":"
        ret = self.fd.write(str_now)
        ret = self.fd.write(date)
        self.fd.flush()

        return ret
    
    def __del__(self):
        if self.fd != None:
            self.fd.close()
            self.fd = None


class info(logger):
    def __init__(self, path, start = "08-00-00", interval = 1):
        super(info, self).__init__(path, 'info', start, interval)

class error(logger):
    def __init__(self, path, start = "08-00-00", interval = 7):
        super(error, self).__init__(path, 'error', start, interval)


class logger():
    def __init__(self, path, start, interval):
        self.error = error(path, start["error"], interval["error"])
        self.inof = info(path, start["info"], interval["info"])
    
    def write(self, level, date):
        if level == INFO:
            ret = self.inof.write(date)
        elif level == ERROR:
            ret = self.error.write(date)
        
        return ret

log = None
LOG_PATH = "/home/chy/bin/frp_0.43.0_linux_amd64/plugin/log"
interval = {"error" : 1, "info" : 7}
start = {"error" : "08-00-00", "info" : "08-00-00"}

def init_log():
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    global log
    log = logger(LOG_PATH + "/frps-position", start, interval)

    return log

def get_logger():
    if log != None:
        return log
