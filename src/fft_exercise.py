#!/usr/bin/env python
import unittest
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.mlab as mlab

# correlation 
#    fft --> point to point multiplex --> fft

def my_corr(a,b):
    count_I=0.0
    count_Q=0.0
    for i in range(0,a.size):
        count_I+=a[i].real*b[i].real
        count_I+=a[i].imag*b[i].imag
        count_Q-=a[i].real*b[i].imag
        count_Q+=a[i].imag*b[i].real
#     print "my_corr: ",count_I, count_Q
    return complex(count_I, count_Q) 

def my_shift(a, n):
    return np.concatenate((a[n:],a[:n]),axis=1)

def my_auto_correlation(a):
    result=[]
    for i in range(a.size):
        result.append(my_corr(a,my_shift(a,i)))
    return result
    

def fft_test():
    np.fft.fft(np.exp(2j * np.pi * np.arange(8) / 8))
    # array([ -3.44505240e-16 +1.14383329e-17j,
    # 8.00000000e+00 -5.71092652e-15j,
    # 2.33482938e-16 +1.22460635e-16j,
    # 1.64863782e-15 +1.77635684e-15j,
    # 9.95839695e-17 +2.33482938e-16j,
    # 0.00000000e+00 +1.66837030e-15j,
    # 1.14383329e-17 +1.22460635e-16j,
    # -1.64863782e-15 +1.77635684e-15j])
    
    
    t = np.arange(256)
    sp = np.fft.fft(np.sin(t))
    freq = np.fft.fftfreq(t.shape[-1])
    plt.plot(freq, sp.real, freq, sp.imag)
    # [<matplotlib.lines.Line2D object at 0x...>, <matplotlib.lines.Line2D object at 0x...>]
    plt.show()
    
    # In this example, real input has an FFT which is Hermitian, i.e., symmetric
    # in the real part and anti-symmetric in the imaginary part, as described in
    # the `numpy.fft` documentation.
    
def auto_correlation(Nzc, u):
    n_=np.array([x *(x+1) for x in range(Nzc)])
    zcs_td=np.exp(-1j * u * math.pi * n_ /Nzc)
       
    result = my_auto_correlation(zcs_td)
    x = np.arange(Nzc)

#     plt.plot(x, result)
    plt.bar(x, [y.real for y in result], width=0.25, facecolor='green')
    plt.bar(x, [y.imag for y in result], width=0.25, facecolor='blue', bottom=[y.real for y in result])
    plt.axis([-10, Nzc-1, -Nzc-1, Nzc+1])
    plt.grid(True)
    plt.show()


    
    
def fft_zadoff_chu_839():
    u=84
    Nzc=839
    n_=np.array([x *(x+1) for x in range(Nzc)])
    
#     print n_
    zcs_time_domain=np.exp(-1j * u * math.pi * n_ /Nzc)
    
    zcs_freq_domain=np.fft.fft(zcs_time_domain)
    
    x = range(Nzc)
#     plt.plot(x, sp.real)
    plt.plot(x, zcs_freq_domain.real)
    plt.axis([0, 839, -100, 100])
    plt.grid(True)
    plt.show()
 
def histogram():
    mu, sigma = 100, 15
    x = mu + sigma*np.random.randn(10000)
    
    # the histogram of the data
    n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
    
    # add a 'best fit' line
    y = mlab.normpdf( bins, mu, sigma)
    l = plt.plot(bins, y, 'r--', linewidth=1)  
    
    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    plt.axis([40, 160, 0, 0.03])
    plt.grid(True)
    
    plt.show()

class Test_fft(unittest.TestCase):
    def test_auto_correlation_zcs_839_5(self):
        auto_correlation(39, 5)
        #dummy assert
        self.assertTrue(1)
    
if __name__ == "__main__":
    unittest.main()
