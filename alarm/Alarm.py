
import unittest

import threading
from time import sleep
from Queue import Queue
from copy import copy
        
IMMDB_FM = {
            # key: (majorType, minorType, severity, source, additionalText pattern)
            "ConnectionToDBError": ("193", "1", "critical", "blade_level", ""),
            "ConnectionToSS7Error": ("193", "2", "major", "blade_level", ""),
            "ConnectionToDiameterStackError": ("193", "3", "critical", "cluster_level", "to peer %s")
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
        Alarm with attribute name, additionalText and source
    """
    def __init__(self):
        self.name = ""
        self.additionalText = ""
        self.source = ""
        
        self.severity = "unknown"
        self.majorType = 0
        self.minorType = 0
        self.action = "raise"

            
    def __str__(self):
        s = ("(%s.%s) %s %s %s %s from %s " 
              % (self.majorType, self.minorType, self.action, self.severity,
                 self.name, self.additionalText, self.source))
        return s
    

class NtfNotice():
    
    def __init__(self):
        self.name =""
        self.additionalText = ""
        self.majorId = 0
        self.minorId = 0
        self.source = ""
        self.severity = ""
        # and other field

    def __str__(self):
        s = ("(%s.%s) %s %s %s %s from %s " 
              % (self.majorId, self.minorId, self.action, self.severity,
                 self.name, self.additionalText, self.source))
        return s

class NoticeFactory(object):
    
    @staticmethod
    def create(alarm):
        notice = NtfNotice()
        notice.name = alarm.name
        notice.source = alarm.source
        notice.additionalText = alarm.additionalText
        notice.majorId = alarm.majorType
        notice.minorId = alarm.minorType
        notice.action = alarm.action
        notice.severity = alarm.severity
        
        return notice
    
    @staticmethod
    def toMajorId(majorType):
        return majorType
    
    @staticmethod
    def toMinorId(minorType):
        return minorType


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
        alarmTypes = AlarmTypes(IMMDB_FM)
        self.factory = AlarmFactory(alarmTypes)
        
        
    def create(self, name, additionalText=""):
        return self.factory.create(name, additionalText)
        
    def raiseAlarm(self, alarm):
        alarm.action = "raise"
        notice = NoticeFactory.create(alarm)

        self.send(notice)
    
    def clearAlarm(self, alarm):
        alarm.action = "clear"
        notice = NoticeFactory.create(alarm)
        
        self.send(notice)
        
        

class AlarmTypes(object):   
    def __init__(self, immdb_fm):
        "load all FM alarm types from DB"
        self.alarmTypes = immdb_fm
         
    def getMajorType(self, name):
        try:
            return self.alarmTypes[name][0]

        except KeyError:
            print "undefined alarm"
            return ""

    def getMinorType(self, name):
        try:
            return self.alarmTypes[name][1]

        except KeyError:
            print "undefined alarm"
            return ""
        
    def getSeverity(self, name):
        try:
            return self.alarmTypes[name][2]

        except KeyError:
            print "undefined alarm"
            return ""
   
   
    def getSource(self, name):
        try:
            return self.alarmTypes[name][3]

        except KeyError:
            print "undefined alarm"
            return ""
            
    def getAdditionalTextPattern(self, name):
        try:
            return self.alarmTypes[name][4]

        except KeyError:
            print "undefined alarm"
            return ""

 
class AlarmFactory(object):
    
    def __init__(self,alarmTypes):
        self.alarmTypes = alarmTypes
        
    
    def create(self, name, additionalText=""):
        " create alarm instance"
        alarm =  Alarm()
        
        alarm.name = name
        
        level = self.alarmTypes.getSource(alarm.name)
        alarm.source = self.source(level) 
        
        pattern = self.alarmTypes.getAdditionalTextPattern(alarm.name)
        alarm.additionalText = self.compose(pattern,additionalText)
        
        alarm.severity = (self.alarmTypes.getSeverity(alarm.name))
        alarm.majorType = (self.alarmTypes.getMajorType(alarm.name))
        alarm.minorType = (self.alarmTypes.getMinorType(alarm.name))
        alarm.action= ""
        
        return alarm
    
    def source(self, level):
        if level == "blade_level":
            s = HOST_NAME
        elif level == "cluster_level":
            s = "IPWorks Diameter AAA"
        else:
            s = "unknown source"
        
        return s
    
    def compose(self,pattern,text):
        if '%s' in pattern:
            s = pattern %(text)
        else:
            s = text
               
        return s
    

class TestAlarm (unittest.TestCase):

    def testClearAlarm(self):
        service = AlarmService()
        
        e = service.create("ConnectionToDiameterStackError", "no1@hss.ericsson.se")
        service.raiseAlarm(copy(e))
        service.clearAlarm(copy(e))
        
