#!/usr/bin/env python

from matplotlib import pyplot, mpl
from lte_re import *


background_color_set= ( [x / 256 for x in (192., 227., 207.)]
                        ,[x / 256 for x in (51., 168., 159.)])
overlap_color = 'red'

#todo: It needs to support more than 3 task_time_map in one colorbar. 
front_color_set = ([x / 256 for x in(130., 219., 113.)],
                  [x / 256 for x in (9., 88., 101.)],
                  [x / 256 for x in (36., 46., 55.)]
                   )



task_color_map = {'dl':  front_color_set[0 % len(front_color_set)],
                 'rach':front_color_set[1 % len(front_color_set)],
                 'srs': front_color_set[2 % len(front_color_set)],
                 'pucch': front_color_set[3 % len(front_color_set)],
                 'pusch': front_color_set[4 % len(front_color_set)]
                 }



task_time_map = {'dl':  ((0.,.7), (4., 4.5), (5.0, 5.8), (9.0, 9.4)),
       'rach': ((3.1, 4.3),),
       'pusch': ((2.0, 2.8), (3.2, 4.5), (7.0, 7.8), (8.0, 8.7)),
       'srs': ((3.5, 3.9),),
       'pucch':((2.1, 2.5), (3.1, 3.5), (7.2, 7.6), (8.1, 8.5))}

def add_end_ticker(bounds, colors, start, duration, front_color):
    
    base = int(start)
    end = start + duration
    
    if base <0 or base > 10:
        print "Warning: time line data %f is out of range" %(start)
        return

    previous_ticker = bounds.index(start)+1
    
    if end >= bounds[previous_ticker]:
        new_ticker_value = bounds[previous_ticker]
        
        new_ticker_color= overlap_color
        if colors[previous_ticker-1] in background_color_set:
            new_ticker_color= front_color
        
        colors[previous_ticker-1]=new_ticker_color              
    else:
        new_ticker_value = end
        bounds.insert(previous_ticker, end)
        
        new_ticker_color= overlap_color
        if colors[previous_ticker-1] in background_color_set:
            new_ticker_color= front_color
                    
        colors.insert(previous_ticker-1, new_ticker_color)
           

    if new_ticker_value == base + 1:
        return new_ticker_value, duration - (new_ticker_value - start)
    else:
        return new_ticker_value, duration - (new_ticker_value - start)


def add_begin_ticker(bounds, colors, start, end, front_color):
    
    base = int(start)
    
    if base <0 or base > 10:
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



def add_time_line(bounds, colors, task_times, front_color):
    for each in task_times:
        is_begin_ticker_done = False
        start = each[0]
        end = each[1]
        duration = end -start
        
        if start <0 or start>10:
            continue
         
        while abs(duration)> 1e-5 :
            if abs(start)> 1e-5 and not is_begin_ticker_done:
                add_begin_ticker(bounds, colors, start, end, front_color)
            
            is_begin_ticker_done = True

            start, duration = add_end_ticker(bounds, colors, start, duration, front_color)


def create_colorbar(task_times, color_map=('blue', 'black', 'red'), frames=10):
    # (2.,2.7))  
    #  start position, end position 
    colors = []
    bounds = []
    # subframe lines
    for item in range(frames + 1):
        bounds.append(float(item))
    

    for item in range(frames):
        colors.append(background_color_set[item % 2])
       

    for i, task in enumerate(task_times):    
        add_time_line(bounds, colors, task, color_map[i])
      

    return bounds, colors

def add_colorbar(ax, tasks):
    task_times = [task_time_map[x] for x in tasks]
    color_map = [task_color_map[x] for x in tasks]
    
    bounds, colors = create_colorbar(task_times, color_map)
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
                                         drawedges=True
                                         )

    # todo: text box 
    ax = fig.add_axes([left - 0.01, bottom + 0.05, 0.001, 0.0001])
    ax.yaxis.set_ticklabels([text])
    ax.xaxis.set_visible(False)

def draw_gpp_task_view(tasks_set):
    fig = pyplot.figure("gpp L1 timeline", figsize=(16, 3))

    # task's time line 
    left, bottom, width, height = 0.05, 0.7, 0.9, 0.15     
    for tasks_per_core in tasks_set:
        ax = fig.add_axes([left, bottom, width, height])  # left, bottom, width, height
        cb = add_colorbar(ax, tasks_per_core)
        cb.ax.xaxis.set_visible(False)
        bottom -= height

    # legend 
    legend_left = 0.05
    legend_bottom = 0.25

    for tasks in tasks_set:
        for task in tasks:
            add_legend(fig, (legend_left, legend_bottom, 0.05, 0.08), task, task_color_map[task])
            legend_left += 0.15

        legend_left = 0.05
        legend_bottom -= 0.1

    pyplot.show() 
    
def get_gpp_run_data(sfn):
    global task_time_map
    tasknames={"dl", "rach", "pucch", "srs", "pusch" }
    for each in tasknames:
        task_time_map[each]= []
    
    set_filename('run.log')
    
    frame_base=get_frame_start_time()/1000
    
    for i in range(10):
        for each in tasknames:
            rtn=get_task_start_and_end_time(each, *get_packet_fn(each,sfn,i))
            if rtn is not None:
                task_time_map[each].append((rtn[0]/1000-frame_base,rtn[1]/1000-frame_base))
        
    print task_time_map  
                                
    
    
if __name__ == '__main__':
    get_gpp_run_data(1124)
    draw_gpp_task_view((('dl', 'rach',),
                    ('pucch', 'srs'),
                    ('pusch',)
                    ))
#     draw_gpp_task_view((('rach',),))
    