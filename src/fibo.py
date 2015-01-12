
import unittest

''' 
        F0, ...                                                                              F20
        0, 1, 1, 2, 3, 5, 8, 13, 21, 34 , 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765
'''
FIB=(0, 1, 1, 2, 3, 5, 8, 13, 21, 34 , 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765)


def fibo_r(n):
    return fibo_recursive_imp(n)

def fibo_recursive_imp(n):
    if n<2: return n
    else:
        return fibo_recursive_imp(n -1) + fibo_recursive_imp(n -2)


def fibo_dp(n):
    F=[0,1]

    if n>1:
        for i in range(2,n+1): F.append(F[i-2] + F[i-1])
    
    return F[n]

def fibo(n):
    F=[0,1]

    if n<2: return F[n]
        
    for _ in range(2,n+1): F[0],F[1] = F[1], F[0]+F[1]
    
    return  F[1]

class FiboTest(unittest.TestCase):
    def test_F1_is_1(self):
        self.assertEqual(1, fibo_dp(1))
 
    def test_F9_is_34(self):
        self.assertEqual(FIB[9], fibo_r(9))

    def test_F10_is_55(self):
        self.assertEqual(FIB[10], fibo(10))
  
    def test_F20_is_6756(self):
        self.assertEqual(FIB[20], fibo_dp(20))

    def testPerformance(self):
        n=30
        
        a=fibo_r(n)
        b=fibo_dp(n)
        c=fibo(n)
        self.assertEqual(a,b)
        self.assertEqual(a,c)


# if __name__ == '__main__':
#     unittest.main()
