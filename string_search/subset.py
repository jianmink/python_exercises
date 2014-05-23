
import unittest

'''
This algorithm is used to find out the minimum length substring from a text string, 
where the substring contains all elements from the pattern set.
For example,  text='1231' and pattern = {2,1}, the minimum substring is '12'


solution description:
    init min_len as the size of text.
    *) one by one visit element of the text from the tail  
            if it is a pattern element
                update pattern element's index list
                if all pattern element had been found, update the min_len, save the substring
            
'''

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
    
    #m: the index in text 
    m=len(text)-1
    
    min_len=len(text)
    while m>0:
        e=text[m]
        if e in p:
            q.update(e,m)
            if q.size()==len(p):
                i,j=q.segment()
                subs.append((i,j))
                len_=j-i+1
                print "subset(%d): %s" %(len_,text[i:j+1])
                
                if len_<min_len:
                    min_len=len_
        else:
            pass
        m-=1
    
    if len(subs)==0:
        return None
    
    #find out the minimum length subset
    m_subs=[]
    for each in subs:
        len_=each[1]-each[0]+1
        if len_==min_len:
            m_subs.append(text[each[0]:each[1]+1])
    
    return m_subs
    
    
class TestSubset(unittest.TestCase):
    def test_find_subset(self):
        s='1232042'
        p=('2','0','4')
        r=find_subset(s,p)
        print r
        self.assertTrue('042' in r)
        self.assertTrue('204' in r)
