#!/usr/bin/env python
import time
import os

def game_of_Life_rules(state, num_live_neighbours):
    if state and (num_live_neighbours == 2 or num_live_neighbours == 3):
        state=True
    elif not state and num_live_neighbours == 3:
        state=True
    else:
        state=False
    
    return state


class Person():
    def __init__(self):
        """constructor"""
        self.state = True
        self.liveNB=0
        self.position=(0,0)
    
    def set_num_live_neighbours(self, liveNB):
        self.liveNB=liveNB
        return self
    
    def get_num_live_neighbours(self):
        return self.liveNB
    
    def live(self):
        self.state=True
        return self
        
    def die(self):
        self.state=False
        return self
    
    def next_round(self):
        self.state=game_of_Life_rules(self.state, self.liveNB)
        return self.state
    
    #coordinate
    def set_x_y(self, x,y):
        self.position=(x,y)
        return self

    def get_x_y(self):
        return self.position


neighbourhood=((-1,-1),(-1,0),(-1,1), (0,-1),(0,1), (1,-1),(1,0),(1,1))
class Group():
    """ a group of live person"""
    
    def __init__(self): 
        """constructor"""
        self.live_members={}
        pass
        
    
    def get_num_live_member(self):
        return 0 if self.live_members=={} else len(self.live_members)
     
    def add_live_member(self, member):
        self.live_members[member.position]=member
        self.set_live_neighbours_4_all_live_members()
        pass
    
    def get_person(self,x,y):
        if self.live_members.has_key((x,y)):
            return self.live_members[(x,y)]
        else:
            zombie=Person().die().set_x_y(x,y)
            self.set_his_live_neighbours(zombie)
            return zombie
    
    def clean(self):
        self.live_members={}
        
    def set_live_neighbours_4_all_live_members(self):
        for key in self.live_members:
            person=self.live_members[key]
            person.set_num_live_neighbours(self.count_live_neighbours(key))
            
    def set_his_live_neighbours(self,him):
        liveNB=self.count_live_neighbours(him.get_x_y())
        him.set_num_live_neighbours(liveNB)
        pass
    
    def count_live_neighbours(self,(x,y)):
        count=0
        for (i,j) in neighbourhood:
            if (x+i,y+j) in self.live_members:
                count+=1
        return count
     
    def next_round(self):
        # update the live member's next_round generation state
        revives={}
        for (x,y) in self.live_members:
            self.live_members[(x,y)].next_round()
            # revive, rule 4
            for (i,j) in neighbourhood:
                if (x+i,y+j) not in self.live_members:
                    zombie=self.get_person(x+i,y+j)
                    if zombie.next_round():
                        revives[zombie.get_x_y()]=zombie
                                    
        # remove the member to be die from the live member map
        copy_= self.live_members.copy()
        for key in copy_:
            if not copy_[key].state:
                self.live_members.pop(key)
        
        # add_live_member revives into live_members
        self.live_members.update(revives)
        
        # update every live members's neighourship in the new generation
        self.set_live_neighbours_4_all_live_members()
        
   
        
class Game():
    """ game """
    def __init__(self,x=3,y=3):
        self.group=Group()
        self.board=(x,y)
    
    def init(self,matrix):
        for x, item in enumerate(matrix):
            for y, sub_item in enumerate(item):
                if sub_item == 1:
                    self.group.add_live_member(Person().set_x_y(x,y))
    
    def run(self,times,display=True):
        if display:
            self.printf(self.to_matrix())
        matrix=[]
        for _ in range(0,times):
            self.group.next_round()
            matrix=self.to_matrix()
            if display:
                self.printf(matrix)
                time.sleep(0.5)
        
        return matrix
        
    def to_matrix(self):
        board=[]
        for i in range(0,self.board[0]):
            line=[]
            for j in range(0,self.board[1]):
                if self.group.live_members.has_key((i,j)):
                    line.append(1)
                else:
                    line.append(0)
            board.append(line)
                    
        return board
    
    def to_string(self,matrix):
        str_=''
        for item in matrix:
            str_+= "   "
            for subitem in item:
                if subitem == 1:
                    str_+= '* '
                else:
                    str_+= '  '
            str_+='\n'
        return str_
        
    
    def printf(self, matrix):
        os.system("clear")
        print 
        print '*'*self.board[1]+' game of life '+'*'*self.board[1]
        print 
        print self.to_string(matrix),
        print
        print '*'*self.board[1]+' game of life '+'*'*self.board[1]
        
        
        
    
