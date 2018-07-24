# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 14:52:03 2018

@author: mayn
"""

import matplotlib.pyplot as plt
import DNA_Object
import json


def draw_area(dna, room):
    area_center, area = DNA_Object.get_room_area(room)
    plt.plot(area['x'], area['y'], linewidth='0.5', color='k',)
    plt.xlim((-15000, 20000))
    plt.ylim((-15000, 20000))
    #plt.plot(area_center[0], area_center[1], '*', linewidth='0.5')
    title = 'Id'+str(dna['solutionId'])
    plt.title(title)

def draw_bounds(minx, miny, maxx, maxy):
    x = [minx, maxx, maxx, minx, minx]
    y = [miny, miny, maxy, maxy, miny]
    plt.plot(x, y, linewidth = '0.8', color='r')

def draw_house_area(dna):
    #plt.figure()
    cur_dict = {}
  
    if 'roomList' in dna:        
        cur_dict = dna
        
    elif 'request' in dna and 'feedback' not in dna:
        cur_dict = json.loads(dna['request'])
       
    elif 'feedback' in dna:
        cur_dict = json.loads(dna['feedback'])

    if cur_dict:        
        room_num = len(cur_dict['roomList'])
       
        for i in range(room_num):
            room = cur_dict['roomList'][i]
            draw_area(dna, room)
            #bed = 318
            #draw_room_obj(room, bed)
            '''if room['roomUsageName'] == '主卧':
                print('主卧area:',area)'''
        #plt.show()
        return True
    else:
        return False
    
def draw_room_area(dna, room_name):
    plt.figure()
    cur_dict = {}
  
    if 'roomList' in dna:        
        cur_dict = dna
        
    elif 'request' in dna and 'feedback' not in dna:
        cur_dict = json.loads(dna['request'])
       
    elif 'feedback' in dna:
        cur_dict = json.loads(dna['feedback'])

    if cur_dict:        
        room_num = len(cur_dict['roomList'])
       
        for i in range(room_num):
            room = cur_dict['roomList'][i]
            if room['roomName'] == room_name:
                draw_area(dna, room)
                #bed = 318
                #draw_room_obj(room, bed)               
        return True
    else:
        return False
def draw_house_wall(dna):
    cur_dict = {}
  
    if 'roomList' in dna:        
        cur_dict = dna
        
    elif 'request' in dna and 'feedback' not in dna:
        cur_dict = json.loads(dna['request'])
       
    elif 'feedback' in dna:
        cur_dict = json.loads(dna['feedback'])
        
    if 'walls' in cur_dict:
        wall_num, wall_pos = DNA_Object.get_wall_from_dna(cur_dict)
        for i in range(wall_num):  
            plt.plot(wall_pos['x'][i], wall_pos['y'][i], alpha=0.7, color='b', linewidth=1, solid_capstyle='round', zorder=2)
        return True
    else:
        return False
    
    
def draw_house_window(dna):
    cur_dict = {}
  
    if 'roomList' in dna:        
        cur_dict = dna
        
    elif 'request' in dna and 'feedback' not in dna:
        cur_dict = json.loads(dna['request'])
       
    elif 'feedback' in dna:
        cur_dict = json.loads(dna['feedback'])
        
    if 'windows' in cur_dict:
        window_num, window_pos = DNA_Object.get_window_info_from_dna(cur_dict)
        for i in range(window_num):
            plt.plot(window_pos['x'][i], window_pos['y'][i], alpha=0.7, color='c', linewidth='0.5', solid_capstyle='round', zorder=2)
        return True
    else:
        return False



def draw_house_door(dna):    
    cur_dict = {}
  
    if 'roomList' in dna:        
        cur_dict = dna
        
    elif 'request' in dna and 'feedback' not in dna:
        cur_dict = json.loads(dna['request'])
       
    elif 'feedback' in dna:
        cur_dict = json.loads(dna['feedback'])
        
    if 'doors' in cur_dict:
        door_num, door_pos = DNA_Object.get_door_from_dna(cur_dict)
        for i in range(door_num):
            #print('【door',i,'pos】', door_pos['x'][i], door_pos['y'][i])
            plt.plot(door_pos['x'][i], door_pos['y'][i], alpha=0.7, color='r', linewidth='0.5', solid_capstyle='round', zorder=2)
        return True
    else:
        return False
    
def draw_room_obj(room, obj_category):
    obj_num, obj_center, obj_size, obj_point= DNA_Object.get_obj_info_from_room(room, obj_category)
    if obj_num > 0:  
        plt.plot(obj_point['x'], obj_point['y'], linewidth='0.5')
        #print(bed_center)
        plt.plot(obj_center[0], obj_center[1], 'o')    
        return True
    else:
        return False

def draw_house_obj(dna, obj_category, close_flag):
    room_num, room = DNA_Object.get_room_list_from_dna(dna)
    count = 0
    for i in range(room_num):
        flag = draw_room_obj(room[i], obj_category)
        if flag == True:
            count += 1
    if count == 0 and close_flag == True:
        plt.close()
        
        
def draw_relative_info(room2bed):
    plt.figure()
    plt.plot(room2bed['x'], room2bed['y'], '*')



def draw_scatter_distribution(data, title_name, xlabel, ylabel):
    plt.figure()
    #解决中文显示问题
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    plt.plot(data['x'], data['y'], '*')
    plt.title(title_name)
    #plt.grid(True, linestyle="-.", color='k', linewidth='0.5')
    plt.plot([0, 10000], [0, 10000], '-')
    plt.plot([0, 10000], [3000, 3000], '-')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)