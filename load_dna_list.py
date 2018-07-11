# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 14:39:11 2018

@author: mayn
"""

import json
import matplotlib.pyplot as plt


def load_dna(file_name):
    f = open(file_name, encoding='utf-8')
    dna_list = json.load(f)
    return dna_list


def get_door_pos(room):
    door_pos = {}  #所有door的坐标
    door_pos['x'] = []
    door_pos['y'] = []
    door_num = len(room['doors'])
    center = []             
    #print('room的door数量为：',door_num)
    for j in range(door_num):
        cur_door = room['doors'][j]
        point_list = cur_door['points']
        #print(door_pos)
        for k in range(len(point_list)):
            door_pos['x'].append(point_list[k]['x'])
            door_pos['y'].append(point_list[k]['y'])
    #print('room的door的坐标信息：', door_pos)
    center.append(sum(door_pos['x']) * 1.0 / len(door_pos['x']))
    center.append(sum(door_pos['y']) * 1.0 / len(door_pos['y']))
    return center, door_num, door_pos

def get_wall_pos(room):
    wall_pos = {}
    wall_pos['x'] = []
    wall_pos['y'] = []
    wall_pos['z'] = []
    wall_num = len(room['walls'])
    for j in range(wall_num):
        cur_wall = room['walls'][j]
        point_list = cur_wall['points']
        for k in range(len(point_list)):
            wall_pos['x'].append(point_list[k]['x'])
            wall_pos['y'].append(point_list[k]['y'])
            wall_pos['z'].append(point_list[k]['z'])
    
    return wall_num, wall_pos
    
def get_room_area(room):
    area = {}
    area['x'] = []
    area['y'] = []
    center = []
    x = 0
    y = 0
    
    area_line_num = len(room['areas'])
    for j in range(area_line_num):
        cur_line = room['areas'][j]
        area['x'].append(cur_line['x'])
        area['y'].append(cur_line['y'])
        if j == 0:
            x = cur_line['x']
            y = cur_line['y']
    
    center.append(sum(area['x']) * 1.0 / area_line_num)
    center.append(sum(area['y']) * 1.0/ area_line_num)
    
    #为画封闭图形补充
    area['x'].append(x)
    area['y'].append(y)
    return center, area

def get_room_by_usagename(dna, usage_name):
    room_num = len(dna['roomList'])
    for i in range(room_num):        
        if dna['roomList'][i]['roomUsageName'] == usage_name:
            return dna['roomList'][i]
    return None
def get_bed_info_from_room(room):
    bed_pos = []   #x,y,z
    bed_size = []  #width,long,height
    point = {}
    point['x'] = []
    point['y'] = []
    model_num = len(room['modelLists'])
    for j in range(model_num):
        if room['modelLists'][j]['categoryId'] == 318:
            bed_pos.append(room['modelLists'][j]['points']['x'])
            bed_pos.append(room['modelLists'][j]['points']['y'])
            bed_pos.append(room['modelLists'][j]['points']['z'])
            bed_size.append(room['modelLists'][j]['boxextension']['long'])
            bed_size.append(room['modelLists'][j]['boxextension']['width'])
            bed_size.append(room['modelLists'][j]['boxextension']['height'])
            
            point['x'].append(bed_pos[0]-bed_size[0])
            point['x'].append(bed_pos[0]-bed_size[0])
            point['x'].append(bed_pos[0]+bed_size[0])
            point['x'].append(bed_pos[0]+bed_size[0])
            
            point['y'].append(bed_pos[1]-bed_size[1])
            point['y'].append(bed_pos[1]+bed_size[1])            
            point['y'].append(bed_pos[1]+bed_size[1])
            point['y'].append(bed_pos[1]-bed_size[1])
            
            #为画封闭图形补充
            point['x'].append(bed_pos[0]-bed_size[0])
            point['y'].append(bed_pos[1]-bed_size[1])
    return bed_pos, bed_size, point

def get_window_info_from_room(room):
    window = {}
    window['x'] = []
    window['y'] = []
    window_num = len(room['windows'])
    center=[]
    for j in range(window_num):
        cur_window = room['windows'][j]
        point_list = cur_window['points']
        for k in range(len(point_list)):
            window['x'].append(point_list[k]['x'])  
            window['y'].append(point_list[k]['y'])  
    center.append(sum(window['x']) * 1.0/2)
    center.append(sum(window['y']) * 1.0/2)
    return center, window

def show_room_list(dna):    
    

    room = get_room_by_usagename(dna, "主卧")
    print(room['roomUsageName'])
    #提取主卧的door信息
    door_center, door_num, door_pos = get_door_pos(room)
    print('主卧的door数量为：',door_num)
    print('主卧的door的坐标信息：', door_pos)   
    wall_num, walll_pos = get_wall_pos(room)    
    #print('主卧的wall数量为：',wall_num)
    #print('主卧的wall的坐标信息：', walll_pos) 
    bed_pos, bed_size, bed_point= get_bed_info_from_room(room)
    area_center, area = get_room_area(room)
    window_center,window_pos = get_window_info_from_room(room)
    plt.plot(door_pos['x'], door_pos['y'])
    #plt.plot(walll_pos['x'], walll_pos['y'])
    plt.plot(bed_point['x'], bed_point['y'])
    plt.plot(area['x'], area['y'])
    plt.plot(window_pos['x'], window_pos['y'])
    
    plt.plot(bed_pos[0], bed_pos[1], 'o')
    plt.plot(window_center[0], window_center[1], 'o')
    plt.plot(area_center[0], area_center[1], 'o')
    plt.plot(door_center[0], door_center[1], 'o')
    
        
dna_list = load_dna('suiyueruge.txt')
dna_list1 = load_dna('lanseduonaohe.txt')
show_room_list(dna_list)
show_room_list(dna_list1)

