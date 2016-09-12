
import copy

ATTRIBUTE_HAS_MULTI_VALUE = ("host", "applicationId") #, "dest",  )


class OtpdiaObject(object):
    def __init__(self):
        self.key_value_pairs={}
        pass
    
    def parse(self, text):
        for each in text:
            t = each.split()
            if len(t) < 3: continue
                
            k = t[0].rstrip()
            if k in ATTRIBUTE_HAS_MULTI_VALUE:
                value_list = [each.rstrip() for each in t[2:] if '(' not in each ]                
                self.key_value_pairs[k] = value_list
            else:
                v = t[2].rstrip()    
                self.key_value_pairs[k] = v
                
    def get(self, k):
        return self.key_value_pairs[k]