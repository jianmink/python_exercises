
import unittest


def partition(s):
    x = s[0]
    subl = [a for a in s[1:] if a <= x]
    subr = [a for a in s[1:] if a>x]
    
    print subl, x, subr
    return subl,x,subr

def qsort(s):
    if len(s) < 2: return s
    
    l,t,r=partition(s)
    return qsort(l)+[t,]+qsort(r) 



'''
A[p,r]

p     i            j             r
-----------------------------------
       |         |             | x |
-----------------------------------
<=x        >x       unrestricted

'''
class Demo():
    @staticmethod
    def partition(a,p,r):
        pivot=a[r]
    
        i = p-1
        for j in range(p,r):
            if a[j] <=pivot:
                i=i+1
                a[i],a[j]=a[j],a[i]
                
        
        a[i+1],a[r]=a[r],a[i+1]
        
        print a[p:i+1],a[i+1],a[i+2:r+1]
        return i+1
    
    @staticmethod
    def qsort(A):
        print         
        Demo.qsortImp(A, 0, len(A)-1)
        print A

    @staticmethod
    def qsortImp(A,p,r):
        if p<r:    
            q=Demo.partition(A,p,r)
            Demo.qsortImp(A,p,q-1)
            Demo.qsortImp(A,q+1,r)
            
 
A=[5,3,2,1,4]
Demo().qsort(A)


class TestQsort(unittest.TestCase):
    
#     def test_empty_list(self):
#         self.assertEqual([],qsort([]))
#     
#     def test_list_1_2_3(self):
#         self.assertEqual([1,2,3],qsort([1,2,3]))
    
    def test_list_4_3_1_2(self):
        self.assertEqual([1,2,3,4,5],qsort([5,3,1,2,4]))
