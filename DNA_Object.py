# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 14:44:59 2018

@author: mayn
"""

import json

'''从dna中提取出roomlist'''
def get_room_list_from_dna(dna):
    cur_dict = {}  
    if 'roomList' in dna:        
        cur_dict = dna
        
    elif 'request' in dna and 'feedback' not in dna:
        cur_dict = json.loads(dna['request'])
       
    elif 'feedback' in dna:
        cur_dict = json.loads(dna['feedback'])
        
    if cur_dict:        
        room_num = len(cur_dict['roomList'])       
     
        return room_num, cur_dict['roomList']
    else:
        return 0, []


'''从dna中提取出roomlist'''
def get_room_list_from_dna_by_room_name(dna, room_name):
    cur_dict = {}  
    if 'roomList' in dna:        
        cur_dict = dna
        
    elif 'request' in dna and 'feedback' not in dna:
        cur_dict = json.loads(dna['request'])
       
    elif 'feedback' in dna:
        cur_dict = json.loads(dna['feedback'])
        
    if cur_dict:        
        room_num = len(cur_dict['roomList'])       
        cnt = 0
        room_list = []
        for i in range(room_num):
            if cur_dict['roomList'][i]['roomName'] == room_name:
                room_list.append(cur_dict['roomList'][i])
                cnt += 1
        return cnt, room_list
    else:
        return 0, []
'''从dna中提取某个room'''
def get_room_by_usagename(dna, usage_name):
    room_num = len(dna['roomList'])
    for i in range(room_num):        
        if dna['roomList'][i]['roomUsageName'] == usage_name:
            return dna['roomList'][i]
    return None

'''从某个房间中提取door信息，只包含该房间的doors'''
def get_door_from_room(room):
    door_pos = {}  #所有door的坐标
    door_pos['x'] = []
    door_pos['y'] = []
    door_num = len(room['doors'])
    center = {}
    center['x'] = []    
    center['y'] = []             
    #print('room的door数量为：',door_num)
    for j in range(door_num):
        cur_door = room['doors'][j]
        point_list = cur_door['points']
        x = []
        y = []
        #print(door_pos)
        for k in range(len(point_list)):
            x.append(point_list[k]['x'])
            y.append(point_list[k]['y'])
        door_pos['x'].append(x)
        door_pos['y'].append(y)
        #print('room的door的坐标信息：', door_pos)
        center['x'].append(sum(x) * 1.0 / len(x))
        center['y'].append(sum(y) * 1.0 / len(y))
    return center, door_num, door_pos

'''从dna中提取door信息，包含了整个户型中所有的doors'''
def get_door_from_dna(dna):
    
    if 'doors' in dna:
        door_num = len(dna['doors'])
        door_pos = {}
        door_pos['x'] = []
        door_pos['y'] = []
        for j in range(door_num):
            cur_door = dna['doors'][j]
            point_list = cur_door['points']
            temp_x = []
            temp_y = []
            for k in range(len(point_list)):
                temp_x.append(point_list[k]['x'])
                temp_y.append(point_list[k]['y'])
            door_pos['x'].append(temp_x)
            door_pos['y'].append(temp_y)                
        return door_num, door_pos
    else:
        return 0,{}
    
def get_door_list_from_dna(dna):    
    cur_dict = {}
  
    if 'roomList' in dna:        
        cur_dict = dna
        
    elif 'request' in dna and 'feedback' not in dna:
        cur_dict = json.loads(dna['request'])
       
    elif 'feedback' in dna:
        cur_dict = json.loads(dna['feedback'])
        
    if 'doors' in cur_dict:
        door_num, door_pos = get_door_from_dna(cur_dict)
        return door_num, door_pos
    else:
        return 0, {}    
 
def get_wall_list_from_dna(dna):
    cur_dict = {}
  
    if 'roomList' in dna:        
        cur_dict = dna
        
    elif 'request' in dna and 'feedback' not in dna:
        cur_dict = json.loads(dna['request'])
       
    elif 'feedback' in dna:
        cur_dict = json.loads(dna['feedback'])
        
    if 'walls' in cur_dict:
        wall_num, wall_pos = get_wall_from_dna(cur_dict)
        return wall_num, wall_pos
    else:
        return 0, {}
    
'''从某个房间中提取wall信息，只包含该房间的walls'''
def get_wall_from_room(room):
    wall_pos = {}
    wall_pos['x'] = []
    wall_pos['y'] = []
    wall_pos['z'] = []
    wall_num = len(room['walls'])
    for j in range(wall_num):
        cur_wall = room['walls'][j]
        point_list = cur_wall['points']
        x = []
        y = []
        z = []
        for k in range(len(point_list)):
            if point_list[k]['z'] > 0:
                continue
            x.append(point_list[k]['x'])
            y.append(point_list[k]['y'])
            z.append(point_list[k]['z'])
        wall_pos['x'].append(x)
        wall_pos['y'].append(y)
        wall_pos['z'].append(z)
    
    return wall_num, wall_pos

'''从dna中提取wall信息，包含了整个户型中所有的walls'''
def get_wall_from_dna(dna):
    if 'walls' in dna:
        wall_num = len(dna['walls'])
        wall_pos = {}
        wall_pos['x'] = []
        wall_pos['y'] = []
        wall_pos['z'] = []
        
        for j in range(wall_num):
            cur_wall = dna['walls'][j]
            point_list = cur_wall['wallPoints']
            x = []
            y = []
            z = []
            for k in range(len(point_list)):
                if point_list[k]['z'] > 0:
                    continue;
                x.append(point_list[k]['x'])
                y.append(point_list[k]['y'])
                z.append(point_list[k]['z'])
            wall_pos['x'].append(x)
            wall_pos['y'].append(y)
            wall_pos['z'].append(z)
        return wall_num, wall_pos
    else:
        return 0,{}
    
    
    
    
    
'''提取某个房间的形状信息'''          
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


'''从room中提取家具信息'''
def get_obj_info_from_room(room, cateId):
    bed_pos = []   #x,y,z
    bed_size = []  #width,long,height
    point = {}
    point['x'] = []
    point['y'] = []
    
    if 'modelLists' not in room:
        model_num = 0
        return model_num, bed_pos, bed_size, point
    
    model_num = len(room['modelLists'])
    bed_num = 0
    for j in range(model_num):
        if room['modelLists'][j]['categoryId'] == cateId:
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
            bed_num = bed_num + 1
    return bed_num, bed_pos, bed_size, point





'''从room中提取window信息'''
def get_window_info_from_room(room):
    window = {}
    window['x'] = []
    window['y'] = []
    window_num = len(room['windows'])
    center=[]
    for j in range(window_num):
        cur_window = room['windows'][j]
        point_list = cur_window['points']
        x = []
        y = []
        for k in range(len(point_list)):
            x.append(point_list[k]['x'])
            y.append(point_list[k]['y'])
        window['x'].append(x)  
        window['y'].append(y)  
        center.append(sum(x) * 1.0/2)
        center.append(sum(y) * 1.0/2)
    return center, window_num, window






'''从dna中提取window信息，包含了整个户型中所有的windows'''
def get_window_info_from_dna(dna):
    if 'windows' in dna:
        window_num = len(dna['windows'])
        window = {}
        window['x'] = []
        window['y'] = []
        window['z'] = []
        
        for j in range(window_num):
            cur_window = dna['windows'][j]
            point_list = cur_window['points']
            x = []
            y = []
            z = []
            for k in range(len(point_list)):                
                x.append(point_list[k]['x'])
                y.append(point_list[k]['y'])
                z.append(point_list[k]['z'])
            window['x'].append(x)
            window['y'].append(y)
            window['z'].append(z)
        return window_num, window
    else:
        return 0,{}
    
def get_window_list_from_dna(dna):
    cur_dict = {}
  
    if 'roomList' in dna:        
        cur_dict = dna
        
    elif 'request' in dna and 'feedback' not in dna:
        cur_dict = json.loads(dna['request'])
       
    elif 'feedback' in dna:
        cur_dict = json.loads(dna['feedback'])
        
    if 'windows' in cur_dict:
        window_num, window_pos = get_window_info_from_dna(cur_dict)
        return window_num, window_pos
    else:
        return 0, {}
 
'''从dna中提取room的center列表'''
def get_house_area_center(dna):
    room_num = len(dna['roomList'])
    x = 0
    y = 0
    for i in range(room_num):  
        room = dna['roomList'][i]
        area_center, area = get_room_area(room)
        x += area_center[0]
        y += area_center[1]
    center = []
    center.append(x * 1.0 / room_num)
    center.append(y * 1.0 / room_num)
    return center


''' room的外包矩形 '''
def get_room_size(dna, room_name):    
    room_num, room_list = get_room_list_from_dna(dna)    
    delta_x_list = []
    delta_y_list = []
    dst_room_num = 0
    for i in range(room_num):
        if room_list[i]['roomName'] == room_name:
            room_area = room_list[i]['areas']
            min_x = 10000000
            max_x = -10000000
            min_y = 10000000
            max_y = -10000000
            dst_room_num += 1
            for j in range(len(room_area)):
                cur_point = room_area[j]
                if cur_point['x'] < min_x:
                    min_x = cur_point['x']
                if cur_point['x'] > max_x:
                    max_x = cur_point['x']
                    
                if cur_point['y'] < min_y:
                    min_y = cur_point['y']
                if cur_point['y'] > max_y:
                    max_y = cur_point['y']
            delta_x = max_x - min_x
            delta_y = max_y - min_y
            if delta_x < delta_y:
                delta_x_list.append(delta_x)
                delta_y_list.append(delta_y)
            else:
                delta_x_list.append(delta_y)
                delta_y_list.append(delta_x)
    
   
    return dst_room_num, delta_x_list, delta_y_list



''' 去掉边边角角的主区域 '''
def get_room_major_size(dna, room_name):
    room_num, room_list = get_room_list_from_dna(dna)    
    delta_x_list = []
    delta_y_list = []
    dst_room_num = 0
    for i in range(room_num):
        if room_list[i]['roomName'] == room_name:
            point_list = room_list[i]['areas']
            x = []
            y = []
            dst_room_num += 1
            for j in range(len(point_list)):
                cur_point = point_list[j]
                x.append(cur_point['x'])
                y.append(cur_point['y'])
            x.sort()
            y.sort()
            
            if len(point_list) > 6:
                return 0, delta_x_list, delta_y_list
            
            x_max_dis = 0
            y_max_dis = 0
            for j in range(len(point_list) - 1):
                if x[j+1]-x[j] > x_max_dis:
                    x_max_dis = x[j+1] - x[j]
                
                if y[j+1] - y[j] > y_max_dis:
                    y_max_dis = y[j+1] - y[j]
            
            if x_max_dis < y_max_dis:
                delta_x_list.append(x_max_dis)
                delta_y_list.append(y_max_dis)
            else:
                delta_x_list.append(y_max_dis)
                delta_y_list.append(x_max_dis)
    
   
    return dst_room_num, delta_x_list, delta_y_list


def get_room_area_point_num(dna, room_name):
    room_num, room_list = get_room_list_from_dna(dna)    
    point_cnt = []
    sub_room_list = []
    for i in range(room_num):
        if room_list[i]['roomName'] == room_name:
            point_list = room_list[i]['areas'] 
            #if len(point_list) == 10:
            #   print('dna', dna['solutionId'], point_list)
            point_cnt.append(len(point_list))
            sub_room_list.append(room_list[i])
   
    return point_cnt, sub_room_list

    
