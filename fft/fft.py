from matplotlib.pylab import *
import numpy as np
import cmath
import unittest

def draw(points):
    figure("Amplitude", figsize=(5,5))
    plot(arange(len(points)),points)
    show()

def dft(x):
    count=0
    X=[]
    N=len(x)
    w=cmath.exp(complex(0,-2*cmath.pi/N))
    for k in range(N):
        s=complex(0,0)
        for n in range(N):
            s+=x[n]*(w**(n*k)) 
            count+=1
        X.append(s)
    print "perf: %d"%(count)
    return X

def idft(X):
    x=[]
    N=len(X)
    w=cmath.exp(complex(0,2*cmath.pi/N))
    for n in range(N):
        s=complex(0,0)
        for k in range(N):
            s+=X[k]*(w**(n*k))
        s/=N
        x.append(s)
    return x
    
recursive_fft_count=0
def recursive_fft(A):
    global recursive_fft_count
    N=len(A)
    if N==1:
        return A

    w_n= cmath.exp(complex(0,-2*cmath.pi/N))
    w=1
    print 'n= ',N, " w_n= ",w_n 
    
    A_0= [A[i] for i in range(N) if i%2==0 ]
    A_1= [A[i] for i in range(N) if i%2==1 ]
    
    y_0=recursive_fft(A_0)
    y_1=recursive_fft(A_1)
    
    print_(y_0)
    print_(y_1)
    
    # Y[k] -> sigma( aj* (w**kj))
    Y= [0 for _ in range(N)]
    for k in range(N/2):
        Y[k] = y_0[k] + y_1[k]*w
        Y[k+N/2] = y_0[k] - y_1[k]*w
        w=w*w_n
        recursive_fft_count+=2
    
    print "Y:",
    print_(Y)
    return Y

def print_(z):
    sign={True:'+',False:'-'}
    for each in z:
        print "(%.2f%s%.2fj) "%(each.real,sign[each.imag>0], abs(each.imag)),
    print 

class TestFFT(unittest.TestCase):
    unittest.skip('')
    def test_dft_brute_force(self):
        x=[]
        for n in range(8):
            x.append(cmath.cos(2*cmath.pi*n/8))
        print_(x)
        X=dft(x)
        print_(X)
#         print_(idft(X))
#         draw(X)
    
    def fft_recursive_test(self,N):
        print "---"
        global recursive_fft_count
        recursive_fft_count=0
        x=[]
        for n in range(N):
            x.append(cmath.cos(2*cmath.pi*n/N))
        print_(x)
        X=recursive_fft(x)
        E=dft(x)
        print "X: ",
        print_(X)
        print "E: ",
        print_(E)
        print "perf(recursive): ", recursive_fft_count
        return X
    
        
#     @unittest.skip('')
    def test_fft_4(self):
        self.fft_recursive_test(4)
        
    def test_fft_8(self):
        self.fft_recursive_test(8)
        
    def test_fft_64(self):
        X=self.fft_recursive_test(64)
#         draw(X)
        
