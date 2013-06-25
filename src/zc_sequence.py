
import math


class ZCS():
    '''
    zadoff chu sequence 
    a(k) = exp i(M*pi*(k)*(k+1)/Nzc)
    '''
    def __init__(self,n=5,m=1):
        self.nzc=n
        self.M=m
        self.create()
    
    def create(self):
        self.sequence=[]
        for k in range (0, self.nzc):
            I = math.cos(self.M*math.pi*(k)*(k+1)/self.nzc)
            Q = math.sin(self.M*math.pi*(k)*(k+1)/self.nzc)           
            self.sequence.append((I,Q))
#         print self.sequence


    def get_sequence(self):
        return self.sequence

    def shift(self,offset):
#         print "sub1", self.sequence[offset:]
#         print "sub2", self.sequence[:offset]
#         print "conc", self.sequence[offset:]+self.sequence[:offset]
        return self.sequence[offset:]+self.sequence[:offset]


class ZCS_LTE():
    '''
    zadoff chu sequence variation in LTE standard ts 36.211 v9
        a(n) = exp -j(u*pi*(n)*(n+1)/Nzc)
    compare to standard ZCS formular a(k) = exp i(M*pi*(k)*(k+1)/Nzc), 
    it is the conjugate.
    
    and, From the correlation calculation
                                 __________
            R(x) = sigma (a(k) * a(k+shift))
          
            ____         ----
            R(X) = sigma (a(k) * a(k+shift))
            k in range (0, nzc)
            The correlation results are conjugate too.
    '''
    def __init__(self,nzc=5,u=1):
        self.nzc=nzc
        self.u=u
        self.create()
    
    def create(self):
        self.sequence=[]
        for k in range (0, self.nzc):
            I = math.cos(self.u*math.pi*(k)*(k+1)/self.nzc)
            Q = -math.sin(self.u*math.pi*(k)*(k+1)/self.nzc)           
            self.sequence.append((I,Q))


    def get_sequence(self):
        return self.sequence

    def shift(self,offset):
        return self.sequence[offset:]+self.sequence[:offset]


        
def acorr(a,b):
    count_I=0
    count_Q=0
    for i in range(0, len(a)):
        print " %e, %e" %((a[i][0]*b[i][0]+a[i][1]*b[i][1]),
                          (a[i][0]*b[i][1]-a[i][1]*b[i][0]))
        count_I+=a[i][0]*b[i][0]+a[i][1]*b[i][1]
        count_Q-=a[i][0]*b[i][1]-a[i][1]*b[i][0]
        print "%e,%e -- %e, %e " %(a[i][0], a[i][1], b[i][0], b[i][1])
        print "step %d: I=%e, Q=%e" %(i, count_I, count_Q)
    print "acorr: ",count_I, count_Q
    return count_I, count_Q 
                
    
        