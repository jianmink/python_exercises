
import unittest

import threading
from time import sleep
from Queue import Queue
from copy import copy
        
IMMDB_FM = {
            # key: (majorType, minorType, severity, source, additionalText pattern)
            "ConnectionToDBError": ("193", "1", "critical", ""),
            "ConnectionToSS7Error": ("193", "2", "major", ""),
            "ConnectionToDiameterStackError": ("193", "3", "critical", "to peer %s")
            }

HOST_NAME = "PL-3"

'''
dependency
    user 
        Alarm
        AlarmService
            create()
            raiseAlarm()
            clearAlarm()
    
    AlarmService
        Alarm
        AlarmFactory
        NtfNoticeFactory
        NtfService

    NtfService
        NtfNotice
        Queue
        
'''


class Alarm(object):
    """
        Alarm with attribute name, text and source
    """
    def __init__(self):
        self.name = ""
        self.text = []
        self.source = ""
            
    def __str__(self):
        return ("%s %s from %s " 
              %(self.name, self.text, self.source))
              
class NtfNotice():
    
    def __init__(self):
        self.name =""
        self.additionalText = ""
        self.majorId = 0
        self.minorId = 0
        self.notificationObj = ""
        self.severity = ""
        # and other field

    def __str__(self):
        s = ("(%s.%s) %s %s %s from %s " 
              % (self.majorId, self.minorId, self.severity,
                 self.name, self.additionalText, self.notificationObj))
        return s

class NoticeFactory(object):
    
    @staticmethod
    def create(alarm,alarmType,the_type="RAISE"):
        notice = NtfNotice()
        notice.name = alarm.name
        
        notice.notificationObj = NoticeFactory.source(alarm.source)
        
        notice.additionalText = NoticeFactory.compose(alarmType.textFormat, alarm.text)
        
        notice.majorId = alarmType.majorType
        notice.minorId = alarmType.minorType
    
        if the_type == "CLEAR":
            notice.severity = "CLEAR_ALARM"
        else:
            notice.severity = alarmType.defaultSeverity
        
        return notice

    @staticmethod
    def compose(the_format,text):
        if '%s' in the_format:
            s = the_format %(text)
        else:
            s = text
               
        return s
    
    @staticmethod
    def source(level):
        if level == "blade_level":
            s = HOST_NAME
        elif level == "cluster_level":
            s = "IPWorks Diameter AAA"
        else:
            s = "unknown source"
        
        return s


class NtfService(object):
    """
        NtfService:
            1) send notice out
    """
    def __init__(self):
        self.queue = Queue(600)
        self.thread = threading.Thread(
                                       target=NtfService.loop,
                                       args=(self.queue,))
        self.thread.start()
    
    def __del__(self):
        self.thread.join()
    
    def send(self, notice):
        self.queue.put(notice)
    
    @staticmethod
    def loop(queue):
        sleep(1)
        while not queue.empty():
            print queue.get()
        
        

class AlarmService(NtfService):
    """
        send SANotice with following features:
            1) support re-send
            2)  
    """
    def __init__(self):
        NtfService.__init__(self)
        self.alarmTypes = AlarmTypes(IMMDB_FM)
        self.factory = AlarmFactory()
        
        
    def create(self, name, text=""):
        return self.factory.create(name, text)
        
    def raiseAlarm(self, alarm):
        alarmType=self.alarmTypes.get(alarm.name)
        notice = NoticeFactory.create(alarm,alarmType,"RAISE")

        self.send(notice)
    
    def clearAlarm(self, alarm):
        alarmType=self.alarmTypes.get(alarm.name)
        notice = NoticeFactory.create(alarm, alarmType, "CLEAR")
        
        self.send(notice)
        
        

class AlarmTypes(object):   
    def __init__(self, immdb_fm):
        "load all FM alarm types from DB"
        self.alarmTypes = immdb_fm

    def get(self,name):
        t = (name,) + self.alarmTypes[name]
        return AlarmType(t)

class AlarmType(object):
    def __init__(self, attrs):
        self.name = attrs[0]
        self.majorType = attrs[1]
        self.minorType = attrs[2]
        self.defaultSeverity = attrs[3]
        self.textFormat=attrs[4]
        
 
class AlarmFactory(object):
    
    def __init__(self):
        pass
    
    def create(self, name, text="", scope="BLADE_LEVEL"):
        " create alarm instance"
        alarm =  Alarm()
        
        alarm.name = name
        alarm.text = text
        alarm.scope = scope
        
        return alarm
    

class TestAlarm (unittest.TestCase):

    def testClearAlarm(self):
        service = AlarmService()
        
        e = service.create(name="ConnectionToDiameterStackError", text="no1@hss.ericsson.se")
        service.raiseAlarm(copy(e))
        service.clearAlarm(copy(e))
        
