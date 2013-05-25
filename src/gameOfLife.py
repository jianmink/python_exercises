#!/usr/bin/env python
import time

def gameOfLifeRule(current_state, numOfLiveNeighbours):
    if current_state and (numOfLiveNeighbours == 2 or numOfLiveNeighbours == 3):
        next_state=True
    elif not current_state and numOfLiveNeighbours == 3:
        next_state=True
    else:
        next_state=False
    
    return next_state


class Person():
    "a person"
    
    def __init__(self):
        """constructor"""
        self.state = True
        self.liveNB=0
        self.position=(0,0)
    
    def setLiveNB(self, liveNB):
        self.liveNB=liveNB
        return self
    
    def getLiveNB(self):
        return self.liveNB
    
    def live(self):
        self.state=True
        return self
        
    def die(self):
        self.state=False
        return self
    
    def next(self):
        self.state=gameOfLifeRule(self.state, self.liveNB)
        return self.state
    
    def setPosition(self, x,y):
        self.position=(x,y)
        return self

    def getPosition(self):
        return self.position


class Group():
    """ a group of live person"""
    
    def __init__(self): 
        """constructor"""
        self.liveMembers={}
        pass
        
    
    def getLiveMember(self):
        if None==len(self.liveMembers):
            return 0
        else:
            return len(self.liveMembers)
    
    def add(self, member):
        self.liveMembers[member.position]=member
        self.calculateLiveNBOfAllLiveMembers()
        pass
    
    def get(self,x,y):
        if self.liveMembers.has_key((x,y)):
            return self.liveMembers[(x,y)]
        else:
            zombie=Person().die().setPosition(x,y)
            self.calculateLiveNB(zombie)
            return zombie
    
    def clean(self):
        self.liveMembers={}
        
    def calculateLiveNBOfAllLiveMembers(self):
        for key in self.liveMembers:
            person=self.liveMembers[key]
            person.setLiveNB(self.countNB(key))
            
    def calculateLiveNB(self,him):
        liveNB=self.countNB(him.getPosition())
        him.setLiveNB(liveNB)
        pass
    
    def countNB(self,position):
        x = position[0]
        y = position[1]
        liveNB=0
        for i in range(-1,2):
            for j in range(-1,2):
                if self.liveMembers.has_key((x+i,y+j)):
                    liveNB=liveNB+1
        if self.liveMembers.has_key((x,y)):
            liveNB=liveNB-1
        return liveNB
     
    def next(self):
        # update the live member's next generation state
        revives={}
        for key in self.liveMembers:
            person=self.liveMembers[key]
            person.next()
            x=key[0]
            y=key[1]
            # revive the person follow rule 4
            for i in range(-1,2):
                for j in range(-1,2):
                    if not self.liveMembers.has_key((x+i,y+j)):
                        zombie=self.get(x+i,y+j)
                        if zombie.next():
                            revives[zombie.getPosition()]=zombie
                                    
        # remove the member to be die from the live member map
        oldLiveMembers=self.liveMembers
        self.liveMembers={}
        for key in oldLiveMembers:
            if oldLiveMembers[key].state==True:
                self.liveMembers[key]=oldLiveMembers[key]
        
        # add revives into liveMembers
        self.liveMembers.update(revives)
        
        # update every live members's neighourship in the new generation
        self.calculateLiveNBOfAllLiveMembers()
        
   
import os     
        
class Game():
    """ game """
    def __init__(self,x=3,y=3):
        self.group=Group()
        self.board=(x,y)
    
    def init(self,matrix):
        x=0
        for item in matrix:
            y=0
            for sub_item in item:
#                 print '(%d,%d)' %(x,y),sub_item,
                if sub_item == 1:
                    self.group.add(Person().setPosition(x,y))
                y=y+1
            x=x+1
    
    def run(self,times):
        self.printf(self.toMatrix())
        matrix=[]
        for _ in range(0,times):
            self.group.next()
            matrix=self.toMatrix()
            self.printf(matrix)
            time.sleep(1)
        
        return matrix
        
    def toMatrix(self):
        board=[]
        for i in range(0,self.board[0]):
            line=[]
            for j in range(0,self.board[1]):
                if self.group.liveMembers.has_key((i,j)):
                    line.append(1)
                else:
                    line.append(0)
            board.append(line)
                    
        return board
    
    def printf(self, matrix):
        os.system("clear")
        print 
        print '*'*self.board[1]+' game of life '+'*'*self.board[1]
        print 
        for item in matrix:
            print "   ",
            for subitem in item:
                if subitem == 1:
                    print '*',
                else:
                    print ' ',
            print
        print
        print '*'*self.board[1]+' game of life '+'*'*self.board[1]
        
        
        
    
