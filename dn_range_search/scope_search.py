


'''
dn_range:
    len:    number of dn digits
    min_dn:  min int value that dn string represents
    max_dn:  max int value that dn string represents  
    e.g. 
    len   : 5
    min_dn: 12300 
    max_dn: 45600

limitation: no overlap between two dn_range 
            that means for each dn, there is at most one matched dn_range for it.
            
'''


class ScopeMap():
    def __init__(self):
        self.maxDn = 0
        self.searchMap={}


class SearchImp():
    def __init__(self):
        self.scopeMaps=[]
        for _ in range(18):
            self.scopeMaps.append(ScopeMap()) 


    def find(self, dn):
        