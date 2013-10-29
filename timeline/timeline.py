#!/usr/bin/env python

from matplotlib import pyplot, mpl
from lte_re import *

import logging 
import logging.config

# create logger
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleExample')

background_colors= ( [x / 256 for x in (192., 227., 207.)]
                        ,[x / 256 for x in (51., 168., 159.)])

front_colors = ()
tasks_color_map = {}
tasks_time_map =  {}

START_INDEX=-1
END_INDEX=10

def add_end_ticker(bounds, colors, start, duration, front_color, overlap_color='r'):
    
    base = int(start)
    end = start + duration
    
    if base <START_INDEX or base > END_INDEX:
        print "Warning: time line data %f is out of range" %(start)
        return

    previous_ticker = bounds.index(start)+1
    
    if end >= bounds[previous_ticker]:
        new_ticker_value = bounds[previous_ticker]
        
        new_ticker_color= overlap_color
        if colors[previous_ticker-1] in background_colors:
            new_ticker_color= front_color
        
        colors[previous_ticker-1]=new_ticker_color              
    else:
        new_ticker_value = end
        bounds.insert(previous_ticker, end)
        
        new_ticker_color= overlap_color
        if colors[previous_ticker-1] in background_colors:
            new_ticker_color= front_color
                    
        colors.insert(previous_ticker-1, new_ticker_color)
           

    if new_ticker_value == base + 1:
        return new_ticker_value, duration - (new_ticker_value - start)
    else:
        return new_ticker_value, duration - (new_ticker_value - start)


def add_begin_ticker(bounds, colors, start, end, front_color):
    base = int(start)
    
    if base <START_INDEX or base > END_INDEX:
        print "Warning: time line data %f is out of range" %(start)
        return
    
    if start in bounds:
        return
    
    index = bounds.index(base)
    
    while 1:
        if bounds[index + 1] > start:
            break
        index += 1

    bounds.insert(index + 1, start)
    colors.insert(index, colors[index]) 

def add_task(bounds, colors, task_times, front_color, overlap_color='r'):
    for each in task_times:
        is_begin_ticker_done = False
        start = each[0]
        end = each[1]
        duration = end -start
        
        if start <START_INDEX  or start>END_INDEX:
            continue
         
        while abs(duration)> 1e-5 :
            if abs(start)> 1e-5 and not is_begin_ticker_done:
                add_begin_ticker(bounds, colors, start, end, front_color)
            
            is_begin_ticker_done = True

            start, duration = add_end_ticker(bounds, colors, start, duration, front_color, overlap_color)


import matplotlib.colors as mcolors

def get_mixed_color(color_map):
    c = mcolors.ColorConverter().to_rgb    
    new_color=[0., 0., 0.]   

    mix_func=lambda x, y: x+y
    for each in color_map:
        new_color=map(mix_func, new_color, c(each))

    return [each/len(color_map) for each in new_color]


def create_data_set(task_times, color_map=('blue', 'black', 'red'), frames=END_INDEX):
    # (2.,2.7))  
    #  start position, end position 
    colors = []
    bounds = []
    # subframe lines
    for item in range(frames + 1):
        bounds.append(float(item))
    

    for item in range(frames):
        colors.append(background_colors[item % 2])
                   
    logger.debug("len(color_map) %d" %(len(color_map)))
    
    for i, each_task in enumerate(task_times):    
        add_task(bounds, colors, each_task, color_map[i],get_mixed_color(color_map))
      
    return bounds, colors

def add_colorbar(ax, tasks):
    task_times= [tasks_time_map[x]  for x in tasks]
    color_map = [tasks_color_map[x] for x in tasks]
    
    bounds, colors = create_data_set(task_times, color_map)
    cmap = mpl.colors.ListedColormap(colors)


    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                         norm=norm,
                                         ticks=bounds,
                                         spacing='proportional',
                                         orientation='horizontal',
                                         drawedges=True
                                         )
    return cb

def add_legend(fig, (left, bottom, width, height), text, color='r'):
    # add colorbar for each legend item
    ax = fig.add_axes([left, bottom, width, height])
    ax.xaxis.set_visible(False)

    cmap = mpl.colors.ListedColormap([color, ])
    bounds = [0, 1]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                         norm=norm,
                                         ticks=bounds,
                                         spacing='proportional',
                                         orientation='horizontal',
                                         extend='min',
                                         drawedges=True)

    ax = fig.add_axes([left - 0.01, bottom + 0.05, 0.001, 0.0001])
    ax.yaxis.set_ticklabels([text])
    ax.xaxis.set_visible(False)



def draw_tasks_timeline_view(tasks_set,sfn=0):
    fig = pyplot.figure("gpp L1 timeline", figsize=(16, 5))
    pyplot.cla()
    pyplot.clf()

    # task's time line 
    left, bottom, width, height = 0.05, 0.8, 0.9, 0.12     
    for tasks_per_core in tasks_set:
        ax = fig.add_axes([left, bottom, width, height])  # left, bottom, width, height
        cb = add_colorbar(ax, tasks_per_core)
        cb.ax.xaxis.set_visible(False)
        bottom -= height

    # legend for tasks
    legend_left = 0.1
    legend_bottom = 0.35

    for tasks in tasks_set:
        for task in tasks:
            add_legend(fig, (legend_left, legend_bottom, 0.05, 0.08), task, tasks_color_map[task])
            legend_left += 0.15

        # legend for conflict
#        add_legend(fig, (legend_left, legend_bottom, 0.05, 0.08), "conflict", 'r')
        legend_left = 0.1
        legend_bottom -= 0.1
        
    fig_text=pyplot.figtext(0.5, 0.95, 'sfn = %d' %(sfn))
           
    pyplot.draw()
#    pyplot.show()

is_1st_block_met=0
def get_tasks_run_data(filename='run.log',sfn=None, start_sfn=None):
    global tasks_time_map
    global is_1st_block_met
    tasknames={"dl", "rach", "pucch", "srs", "pusch" }
    for each in tasknames:
        tasks_time_map[each]= []
    
    while 1:
        block_sfn,block=next_block(filename)
        if block_sfn ==0xffff or block == []:
            return False, block_sfn
        
        
        if is_1st_block_met ==0:                    
            if start_sfn is None:
                is_1st_block_met=1
            else:
                if block_sfn != start_sfn:
                    continue
                else:
                    is_1st_block_met=1
        
        if sfn is None:
            sfn = block_sfn
            break
        elif block_sfn == sfn:
            break 
        

    frame_base=get_frame_start_time_plus(block)/1000
    
    for i in range(END_INDEX):
        for each in tasknames:
            rtn=get_task_start_and_end_time_plus(block,each, *get_packet_fn(each,sfn,i))
            if rtn is not None:
                tasks_time_map[each].append((rtn[0]/1000-frame_base,rtn[1]/1000-frame_base))
    
#    print tasks_time_map
    return True, block_sfn  
                                
def init():
    global front_colors, tasks_color_map, tasks_time_map
    front_colors = ([x / 256 for x in(130., 219., 113.)],
                  [x / 256 for x in (9., 88., 101.)],
                  [x / 256 for x in (36., 46., 55.)])

    tasks_color_map = {'dl':  front_colors[0 % len(front_colors)],
                 'rach':front_colors[1 % len(front_colors)],
                 'srs': front_colors[2 % len(front_colors)],
                 'pucch': front_colors[3 % len(front_colors)],
                 'pusch': front_colors[4 % len(front_colors)] }
       
    
if __name__ == '__main__':
    init()
    
    import time
    
    pyplot.ion()
    
    num_of_pic=2
    for i in range(num_of_pic):
        rtn, block_sfn=get_tasks_run_data('task_run_4_test.log')
        if rtn:
            draw_tasks_timeline_view((('dl', 'rach',), 
                        ('pucch', 'srs'),('pusch',)), 
                               sfn=block_sfn)
        time.sleep(5)
    print "done!"
    