
import unittest


IMMDB_FM = {
            # key: (majorId, minorId, severity, source, additionalText pattern)
            "ConnectionToDBError": ("193", "1", "critical", "", ""),
            "ConnectionToSS7Error": ("193", "2", "major", "", ""),
            "ConnectionToDiameterStackError": ("193", "3", "critical", "%s", "")
            }

class Alarm(object):
    """
        Alarm with attribute name, additionalText and source
    """
    def __init__(self, name="", additionalText="", source=""):
        self.name = name
        self.additionalText = additionalText
        self.source = source

    def __str__(self):
        s = ("%s %s from %s " 
              % (self.name, self.additionalText, self.source))
        return s

class SANotice(object):
    """
        Notice of A NTF service
    """
    def __init__(self, alarm):
        self.name = alarm.name
        self.additionalText = alarm.additionalText
        self.source = alarm.source
        self.severity = "unknown"
        self.majorId = 0
        self.minorId = 0
        self.action = "raise"
        
    def setSeverity(self, severity):
        self.severity = severity

    def setMajorId(self, majorId):
        self.majorId = majorId
        
    def setMinorId(self, minorId):
        self.minorId = minorId
        
    def setAction(self, action):
        self.action = action
            
    def __str__(self):
        s = ("(%s.%s) %s %s %s %s from %s " 
              % (self.majorId, self.minorId, self.action, self.severity, 
                 self.name, self.additionalText, self.source))
        return s
    


class NtfService(object):
    """
        NtfService:
            1) send notice out
    """
    def __init__(self):
        pass
    
    def send(self, notice):
        print "send NTF notice:", notice
        


class AlarmService(NtfService):
    """
        send SANotice with following features:
            1) support re-send
            2)  
    """
    def __init__(self, alarmTypes):
        self.alarmTypes = alarmTypes
        
    def toNotice(self, alarm, action):
        notice = SANotice(alarm)
        notice.setSeverity(self.alarmTypes.getSeverity(alarm.name))
        notice.setMajorId(self.alarmTypes.getMajorId(alarm.name))
        notice.setMinorId(self.alarmTypes.getMinorId(alarm.name))
        notice.setAction(action)
        return notice
    
    def raiseAlarm(self, alarm):
        
        self.send(self.toNotice(alarm, "raise"))
    
    def clearAlarm(self, alarm):
        
        self.send(self.toNotice(alarm, "clear"))
        
        

class AlarmTypes(object):   
    def __init__(self, immdb_fm):
        "load all FM alarm types from DB"
        self.alarmTypes = immdb_fm
         
    def getMajorId(self, name):
        try:
            return self.alarmTypes[name][0]

        except KeyError:
            print "undefined alarm"
            return ""

    def getMinorId(self, name):
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
            
    def getAdditionalTextPattern(self, name):
        try:
            return self.alarmTypes[name][4]

        except KeyError:
            print "undefined alarm"
            return ""
            
        

class TestAlarm (unittest.TestCase):
    alarmTypes = AlarmTypes(IMMDB_FM)
    service = AlarmService(alarmTypes)

    def testCreateAlarmInstance(self):
        dbConnectionError = Alarm("ConnectionToDBError", "N/A", "PL-3")
        print str(dbConnectionError)

    def testRaiseAlarm(self):
        e = Alarm("ConnectionToSS7Error", "File", "PL-3")
        TestAlarm.service.raiseAlarm(e)
        
    def testClearAlarm(self):
        e = Alarm("ConnectionToDiameterStackError", "no1@hss.ericsson.se", "PL-3")
        TestAlarm.service.clearAlarm(e)
        
