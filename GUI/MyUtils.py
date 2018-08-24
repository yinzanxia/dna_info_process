# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 09:19:05 2018

@author: mayn
"""



'''获取x列表和y列表的最大和最小值'''
def getListLimit(num, x_list, y_list):
    x_min = 1000000
    x_max = -1000000
    y_min = 1000000
    y_max = -1000000
    
    for i in range(num):
        if x_list[i] > x_max:
            x_max = x_list[i]
        
        if x_list[i] < x_min:
            x_min = x_list[i]
            
        if y_list[i] > y_max:
            y_max = y_list[i]
            
        if y_list[i] < y_min:
            y_min = y_list[i]
    
    return x_min, x_max, y_min, y_max  



'''门或窗的中心点坐标，方向 0: x轴平行， 方向1：y轴平行'''
def getSideOrder(x, y, direction):
    if direction == 0:
        if y > 500:
            return 4
        elif y < -500:
            return 2
        else:
            return 0  
    elif direction == 1:
        if x > 500:
            return 1
        elif x < -500:
            return 3
        else:
            return 0  
        
def getWindowSideOrder(x, y, wall_xmin, wall_xmax, wall_ymin, wall_ymax):
    if y > wall_ymax:
        return 4
    elif y < wall_ymin:
        return 2
    elif x < wall_xmin:
        return 3
    elif x > wall_xmax:
        return 1
    else:
        return 0
   
        
def getPreWall(cur_wall):
    pre_wall = cur_wall - 1
    if pre_wall == 0:
        pre_wall = 4
    
    return pre_wall

def getPostWall(cur_wall):
    post_wall = cur_wall + 1
    if post_wall == 5:
        post_wall = 1
    return post_wall



def getLimitOfDoorInWall(door_range):
    x_max = -1000000
    x_min = 10000000
    y_max = -1000000
    y_min = 10000000
    
    for i in range(len(door_range['x'])):
        tmp = door_range['x'][i]
        if x_max < tmp[0]:
            x_max = tmp[0]
        if x_max < tmp[1]:
            x_max = tmp[1]
            
        if x_min > tmp[0]:
            x_min = tmp[0]
        if x_min > tmp[1]:
            x_min = tmp[1]
            
    for i in range(len(door_range['y'])):
        tmp = door_range['y'][i]
        if y_max < tmp[0]:
            y_max = tmp[0]
        if y_max < tmp[1]:
            y_max = tmp[1]
            
        if y_min > tmp[0]:
            y_min = tmp[0]
        if y_min > tmp[1]:
            y_min = tmp[1]
            
    return x_min, x_max, y_min, y_max


def getYmaxOfDoorInWall(door_range):
    x_min, x_max, y_min, y_max = getLimitOfDoorInWall(door_range)    
    return y_max

def getYminOfDoorInWall(door_range):
    x_min, x_max, y_min, y_max = getLimitOfDoorInWall(door_range)    
    return y_min

def getXmaxOfDoorInWall(door_range):
    x_min, x_max, y_min, y_max = getLimitOfDoorInWall(door_range)    
    return x_max

def getXminOfDoorInWall(door_range):
    x_min, x_max, y_min, y_max = getLimitOfDoorInWall(door_range)    
    return x_min


def getGrowLimitWithDoorOrWindowInWall(x, y, door_range, direction, wall_min, wall_max): 
    min_left_dist = 10000000
    min_right_dist = 10000000
    
    if direction == 0:
        x_min = wall_min
        x_max = wall_max
        for i in range(len(door_range['x'])):
            tmp = door_range['x'][i]
            
            if tmp[0] < x and tmp[1] > x:
                return -1, -1
            
            if tmp[1] < x:
                if x - tmp[1] < min_left_dist:
                    min_left_dist = x - tmp[1]
                    x_min = tmp[1]
                    
            if tmp[0] > x:
                if tmp[0] - x < min_right_dist:
                    min_right_dist = tmp[0] - x
                    x_max = tmp[0] 
        return x_min, x_max
       
    min_top_dist = 1000000
    min_bottom_dist = 1000000
    if direction == 1:
        y_min = wall_min
        y_max = wall_max
        for i in range(len(door_range['y'])):
            tmp = door_range['y'][i]
            
            if tmp[0] < y and tmp[1] > y:
                return -1, -1
            
            if tmp[1] < y:
                if y - tmp[1] < min_bottom_dist:
                    min_bottom_dist = y - tmp[1]
                    y_min = tmp[1]
                    
            if tmp[0] > y:
                if tmp[0] - y < min_top_dist:
                    min_top_dist = tmp[0] - y
                    y_max = tmp[0]
        return y_min, y_max
          
            
    return -1, -1