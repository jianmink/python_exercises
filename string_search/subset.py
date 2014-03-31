
import unittest

class MyQueue(object):
    def __init__(self):
        self.p_index=[]
        
    def update(self,e,m):
        is_found=False
        for each in self.p_index:
            if each[0]==e:
                each[1]=m
                is_found=True
                break
            
        if not is_found:
            self.p_index.append([e,m])
    
    def size(self):
        return len(self.p_index)
    
    def segment(self):
        if self.size()==0:
            return None

        min_=self.p_index[0][1]
        max_=min_
        for each in self.p_index:
            k=each[1]
            if min_>k:
                min_=k
            if max_<k:
                max_=k
        return (min_,max_)
            
    
    def __str__(self):
        str_=''
        for each in self.p_index:
            str_+="(s[%d]:%s) "%(each[1],each[0])
        str_+='\n'
        return str_ 

def find_subset(text, p):
    '''
    text is a string sequence: e.g. 'hello it's a subset test'
    p is a characters set: e.g. (t, b, s)
    the minimum subset of text is 'bset', that contains all the elements of p.
    '''
    
    # save all subset's index
    q=MyQueue()
    subs=[]
    m=len(text)-1
    min_sub_len=len(text)
    while m>0:
        e=text[m]
        if e in p:
            q.update(e,m)
            if q.size()==len(p):
                i,j=q.segment()
                subs.append((i,j))
                sub_len=j-i+1
                print "subset(%d): %s" %(sub_len,text[i:j+1])
                
                if sub_len<min_sub_len:
                    min_sub_len=sub_len
        else:
            pass
        m-=1
    
    if len(subs)==0:
        return None
    
    #find out the minimum length subset
    min_subs=[]
    for each in subs:
        sub_len=each[1]-each[0]+1
        if sub_len==min_sub_len:
            min_subs.append(text[each[0]:each[1]+1])
    
    return min_subs
    
    
class TestSubset(unittest.TestCase):
    def test_find_subset(self):
        s='1232042'
        p=('2','0','4')
        r=find_subset(s,p)
        print r
        self.assertTrue('042' in r)
        self.assertTrue('204' in r)

def find_pair(s,a):
    r=[]
    i=0 
    j=len(s)-1
    while i < j:
        if s[i]+s[j]==a:
            r.append([i,j])
            j-=1
        elif s[i]+s[j]<a:
            i+=1
        else:
            j-=1
                
    return r


class TestPair(unittest.TestCase):
    def test_find_pair(self):
        s=[1,2,3,4,5,6,7,8]
        a=7
        r=find_pair(s,a)
        self.assertEqual(r,[[0,5],[1,4],[2,3]])
