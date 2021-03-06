# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 10:36:16 2018

@author: mayn
"""

import json
from copy import deepcopy

def getRoomListFromResponse(resp_text):
    if type(resp_text) == dict:    
        if "data" in resp_text:
            return resp_text["data"]
        else:
            return []
    else:
         return []

def isResponseOK(resp_text):   
    if type(resp_text) == dict:    
        if "code" in resp_text and resp_text["code"] <= 200:
            return True
        else:
            return False
    else:
        return False
    

def getRoomDetailShowInfo(resp_text):
    if type(resp_text) == dict:
        if "data" in resp_text and type(resp_text["data"]) is dict:
            cur_data = resp_text["data"]
            if "room" in cur_data:
                cur_data = cur_data["room"]
            room_text = "|id:%d|roomId:%d|solutionId:%d|roomName:%s|markFeature:%s|rid:%s|" % (cur_data["id"], cur_data["roomId"],cur_data["solutionId"], cur_data["roomName"], cur_data["markFeature"], cur_data["rid"])
            return room_text
    else:
        return ""
   
    
'''获取指定room的rid'''
def getRidFromResp(resp_text):
    if type(resp_text) == dict:
        if "data" in resp_text and type(resp_text["data"]) is dict:
            cur_data = resp_text["data"]
            if "room" in cur_data:
                cur_data = cur_data["room"]
            return cur_data["rid"]
    else:
        return ""



'''解析表达式'''
def decodeExp(exp_str):
    
    exp_list = exp_str.split("|")
    if len(exp_list) > 0:
        location_str = exp_list[0][2:]
        location_str = location_str.split(',')
        location = [float(item) for item in location_str]
        return location
    else:
        return []
        


'''从响应信息中解析该room下的主家具位置列表'''
def getExpList(detail_room_response_text):
    pos = {}
    if type(detail_room_response_text) == dict:
        if "data" in detail_room_response_text and type(detail_room_response_text["data"]) is dict:
            cur_data = detail_room_response_text["data"]
            if "relationship" in cur_data:
                cur_data = cur_data["relationship"]
                if type(cur_data) is list:
                    for i in range(len(cur_data)):
                        cur_obj = cur_data[i]
                        if cur_obj["categoryId"] not in pos:
                            pos[cur_obj["categoryId"]] = []
                            
                        location = decodeExp(cur_obj["expression"])
                        if len(location) > 0:
                            tmp = {}
                            tmp['x'] = location[0]
                            tmp['y'] = location[1]
                            tmp['z'] = location[2]
                            pos[cur_obj["categoryId"]].append(tmp)
                        
    
    return pos;

def recoverPositionPoint(pos, x_range, y_range):
    recover_position = {}
    
    for i_key, i_value in pos.items():
        recover_position[i_key] = []
        for i in range(len(i_value)):
            cur_pos = i_value[i]
            tmp = {}
            tmp['x'] = cur_pos['x'] * x_range / 2.0
            tmp['y'] = cur_pos['y'] * y_range / 2.0
            tmp['z'] = cur_pos['z']
            recover_position[i_key].append(tmp)
            
    return recover_position
        
    
def isBedroom(resp_text):
    if type(resp_text) == dict:
        if "data" in resp_text and type(resp_text["data"]) is dict:
            cur_data = resp_text["data"]
            if "room" in cur_data:
                cur_data = cur_data["room"]
            room_name = cur_data["roomName"]
            if room_name == "主卧" or room_name == "次卧" or room_name == "第三房" or room_name == "第四房":
                return True      
    return False
    
def getIdFromShowText(show_txt):
    res = show_txt.split("|")
    #print(res)
    return res[1]
    
def getDoorInfoFromRoom(resp_text):
    door_pos = {}
    door_pos['x'] = []
    door_pos['y'] = []
    door_num = 0
    if type(resp_text) == dict:
        if "data" in resp_text and type(resp_text["data"]) is dict:
            cur_data = resp_text["data"]      
            if "room" in cur_data:
                cur_data = cur_data["room"]
            if "doors" in cur_data:                
                door_list = json.loads(cur_data["doors"]) 
                for d in range(len(door_list)):                    
                    door = door_list[d]
                    tmpx = []
                    tmpy = []
                    door_num += 1
                    if "points" in door:
                        point_list = door["points"]                        
                        for i in range(len(point_list)):
                            cur_point = point_list[i]
                            if (cur_point['z'] < 10):
                                tmpx.append(cur_point['x'])
                                tmpy.append(cur_point['y'])
                    if len(tmpx) > 0:  #plot成矩形
                        tmpx.append(tmpx[0])
                        tmpy.append(tmpy[0])
                    door_pos['x'].append(tmpx)
                    door_pos['y'].append(tmpy) 
    return door_num, door_pos

def getWindowInfoFromRoom(resp_text):
    door_pos = {}
    door_pos['x'] = []
    door_pos['y'] = []
    door_num = 0
    window_str = "windows"
    if type(resp_text) == dict:
        if "data" in resp_text and type(resp_text["data"]) is dict:
            cur_data = resp_text["data"]
            if "room" in cur_data:
                cur_data = cur_data["room"]            
            if window_str in cur_data:                
                window_list = json.loads(cur_data[window_str])                 
                for d in range(len(window_list)):                    
                    window = window_list[d]
                    tmpx = []
                    tmpy = []
                    door_num += 1
                    if "points" in window:
                        point_list = window["points"]                        
                        for i in range(len(point_list)):
                            cur_point = point_list[i]
                            if (cur_point['z'] < 3000):
                                tmpx.append(cur_point['x'])
                                tmpy.append(cur_point['y'])                                
                    if len(tmpx) > 0:  #plot成矩形
                        tmpx.append(tmpx[0])
                        tmpy.append(tmpy[0])
                    door_pos['x'].append(tmpx)
                    door_pos['y'].append(tmpy) 
    
    return door_num, door_pos

def removeDuplicateItem(src_list):
    if type(src_list) is list:
        dst_list = []    
        for item in src_list:
            if item not in dst_list:
                dst_list.append(item)
        return dst_list
    else:
        return src_list

def splitWall(wall_list):
    split_idx = []
    seg_num = 1
    split_idx.append(0)
    for i in range(len(wall_list) - 1):
        start_x, start_y = wall_list[i]['x'], wall_list[i]['y']
        end_x, end_y = wall_list[i+1]['x'], wall_list[i+1]['y']
        if abs(start_x - end_x) > 100 and abs(start_y - end_y) > 100:
            split_idx.append(i)
            seg_num += 1
    
    split_idx.append(len(wall_list) - 1)
    new_wall_list = []
    
    for i in range(len(split_idx) - 1):
        new_wall_list.append(wall_list[split_idx[i]:split_idx[i+1]+1])
    
    print(new_wall_list)
    return new_wall_list
        
def getWallShapeInfoFromRoom(resp_text, obj_type):
    shape_pos = {}
    shape_pos['x'] = []
    shape_pos['y'] = []
    point_num = 0
    
    if type(resp_text) is dict:
        if "data" in resp_text and type(resp_text["data"]) is dict:
            cur_data = resp_text["data"]
            if "room" in cur_data:
                cur_data = cur_data["room"]
            if obj_type in cur_data:
                shape_list = json.loads(cur_data[obj_type])                
                for i in range(len(shape_list)):
                    cur_point = shape_list[i]
                    shape_pos['x'].append(cur_point['x'])
                    shape_pos['y'].append(cur_point['y'])
                    point_num += 1
    
    return point_num, shape_pos

def getShapeRange(point_num, shape_pos):
    x_min = 1000000
    x_max = -1000000
    y_min = 1000000
    y_max = -1000000
    
    for i in range(point_num):
        x = shape_pos['x'][i]
        y = shape_pos['y'][i]
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y > y_max:
            y_max = y
        if y < y_min:
            y_min = y
    
    x_range = x_max - x_min
    y_range = y_max - y_min
    
    return x_range, y_range

def getWallInfoFromRoom(resp_text):
    wall_pos = {}
    wall_pos['x'] = []
    wall_pos['y'] = []
    wall_num = 0
    
    if type(resp_text) is dict:
        if "data" in resp_text and type(resp_text["data"]) is dict:
            cur_data = resp_text["data"]
            if "room" in cur_data:
                cur_data = cur_data["room"]
            if "walls" in cur_data:
                shape_list = json.loads(cur_data["walls"])     
                new_list = removeDuplicateItem(shape_list)   
                new_list = splitWall(new_list)
                wall_num = len(new_list)
                for i in range(wall_num):
                    cur_point_list = new_list[i]
                    x = []
                    y = []
                    for j in range(len(cur_point_list)):
                        x.append(cur_point_list[j]['x'])
                        y.append(cur_point_list[j]['y'])
                    if len(x) > 0:
                        x.append(x[0])
                        y.append(y[0])
                    wall_pos['x'].append(x)
                    wall_pos['y'].append(y) 

    return wall_num, wall_pos


        

def deepCopyResponseText(resp_text):
    if type(resp_text) is dict:
        copy_resp = deepcopy(resp_text)
        return copy_resp
    else:
        return None
    

def encodeFeedBack(parent, child):
    
    if 'feedback' not in parent:
        parent['feedback'] = child
    else:
        for ikey, ivalue in child.items():            
            parent['feedback'][ikey] = ivalue
                