#!/usr/bin/env python
import sys
import json
import time
import unittest
import tableprint
import csv


def find_plan(plan_file):
    plan = []
    # find the plan from json file: now >= start and now <= end
    with open(plan_file) as f:
        plans = json.load(f)['plan']
        if len(plans) == 0:
            print "No valid plan, exit"
            sys.exit (1)
        
        for each in plans:
            start = time.mktime(time.strptime(each['start'], "%Y-%m-%d"))
            end = time.mktime(time.strptime(each['end'], "%Y-%m-%d"))
            
            now = time.time()
            if now >= start and now <= end:
                print "Plan found"
                plan = each
                break
    
    return plan

def dispatch(plan_file, case_file):
    start_time= time.time()
    g_assignment={} 
    
    plan = find_plan(plan_file)
    
    if not plan: return a_assignment
    
    with open(case_file) as f_case_list:
        for each in f_case_list:
            case = each.strip().split()[0]
            if not case : continue
            
            is_assigned = False
            for p in plan['teams']:
                pattern = p["assignment"]
                team = p['team']
                
                for p in pattern:
                    if p not in case: continue 
                        
    #                 print "dispatch ", case, " to ", team
                    is_assigned = True
                    if not g_assignment.has_key(team) :
                        g_assignment[team]=[case]
                    else:
                        if case not in g_assignment[team]:
                            g_assignment[team].append(case)
                    
            if not is_assigned: 
                if not g_assignment.has_key('unassigned'): g_assignment['unassigned']=[case]
                else: g_assignment['unassigned'].append(case)
    
#     for k,v in g_assignment.items():
#         print k,v 
                   
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print "elapsed %f seconds" %( elapsed_time) 
    return g_assignment           

def print_assignment(assignment):
    
    header=['Case', 'Team']
    data =[]
    for team in sorted(assignment.keys()):
        for each in assignment[team]:
            data.append([each,team])
        
    tableprint.table(data, header, style='fancy_grid', width=20)

def out_csv(assignment):
    with open('assignment.csv','w') as csvfile:
         fieldnames = ['Case', 'Team']
         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
         writer.writeheader()
         for team in sorted(assignment.keys()):
             for each in assignment[team]:
                 writer.writerow({'Case': each, 'Team': team})
                
        
class TestDispatcher(unittest.TestCase):
    def test_dispatch_fail_case_from_fail_case_file(self):
        assignment = dispatch('plan.json', 'fail_case_list')
        print_assignment(assignment)
        out_csv(assignment)
    
    
if __name__=="__main__":
    if len(sys.argv) != 3:
        print "Invalid option number ",len(sys.argv) 
        print "Usage: dipatcher.py <plan.json> <case_list>"
        print 
        sys.exit(1)
        
    assignment=dispatch(sys.argv[1],sys.argv[2])
    
    print_assignment(assignment)
    out_csv(assignment)
    