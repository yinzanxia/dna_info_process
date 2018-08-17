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
                        print(cur_obj)
                        if cur_obj["categoryId"] not in pos:
                            pos[cur_obj["categoryId"]] = []
                            
                        if '-ssc' in cur_obj["expression"]:
                            location = decodeExp(cur_obj["expression"])
                            rect = decodeExpWithSpecialArea(cur_obj["expression"])
                            tmp = {}
                            tmp['isArea'] = 1
                            tmp['x'] = location[0]
                            tmp['y'] = location[1]
                            tmp['z'] = location[2]
                            tmp['xmin'] = rect[0]
                            tmp['ymin'] = rect[1]
                            tmp['xmax'] = rect[2]
                            tmp['ymax'] = rect[3]
                            pos[cur_obj["categoryId"]].append(tmp)
                        else:
                            location = decodeExp(cur_obj["expression"])
                            dx = cur_obj['objDx']
                            dy = cur_obj['objDy']
                            if len(location) == 3:
                                tmp = {}
                                tmp['isArea'] = 0
                                tmp['x'] = location[0]
                                tmp['y'] = location[1]
                                tmp['z'] = location[2]
                                tmp['dx'] = dx
                                tmp['dy'] = dy
                                pos[cur_obj["categoryId"]].append(tmp)                        
    
    return pos;


'''解析表达式'''
#"-0.9698635655656643,-0.9523809523809524,0|0,0,0|0.0,0.0,-90.0|-s 1.0,1.0,1.0 -ssc -0.9698635655656643,-0.9619047619047619,0#-0.5969199439064733,-0.07142857142857126,0"
def decodeExpWithSpecialArea(exp_str): 
    index = exp_str.index('-ssc ')
    if index <= -1:
        return []
    
    rect_str = exp_str[index+len('-ssc '):]
    if rect_str.index('#') <= -1:
        return []
    point_str = rect_str.split('#')
    if len(point_str) != 2:
        return []

    min_point = point_str[0].split(',')
    max_point = point_str[1].split(',')
    if len(min_point) != 3:
        return []
    if len(max_point) != 3:
        return []
   
    #  xmin, ymin, xmax, ymax
    rect = [float(min_point[0]), float(min_point[1]), float(max_point[0]), float(max_point[1])]      
       
    return rect                                
                               
    
  


def recoverPositionPoint(pos, x_range, y_range):
    recover_position = {}
    
    for i_key, i_value in pos.items():
        recover_position[i_key] = []
        for i in range(len(i_value)):
            cur_pos = i_value[i]
            if 'isArea' in cur_pos:
                if cur_pos['isArea'] == 0:
                    tmp = {}
                    tmp['isArea'] = 0
                    tmp['x'] = cur_pos['x'] * x_range / 2.0
                    tmp['y'] = cur_pos['y'] * y_range / 2.0
                    tmp['z'] = cur_pos['z']
                    tmp['dx'] = cur_pos['dx']
                    tmp['dy'] = cur_pos['dy']
                    recover_position[i_key].append(tmp)
                elif cur_pos['isArea'] == 1:
                    tmp = {}
                    tmp['isArea'] = 1
                    tmp['x'] = cur_pos['x'] * x_range / 2.0
                    tmp['y'] = cur_pos['y'] * y_range / 2.0
                    tmp['z'] = cur_pos['z']
                    tmp['xmin'] = cur_pos['xmin'] * x_range / 2.0
                    tmp['ymin'] = cur_pos['ymin'] * y_range / 2.0
                    tmp['xmax'] = cur_pos['xmax'] * x_range / 2.0
                    tmp['ymax'] = cur_pos['ymax'] * y_range / 2.0
                    
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
            
def getRange(shape_point_num, shape_pos):
        x_min = 1000000
        x_max = -1000000
        y_min = 1000000
        y_max = -1000000
        
        for i in range(shape_point_num):
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
        
        shape_dx = x_max - x_min
        shape_dy = y_max - y_min       
       
        return shape_dx, shape_dy, min(x_min, y_min), max(x_max, y_max);
                

categoryMap = {}
categoryMap[318] = '床'
categoryMap[115] = '榻榻米'
categoryMap[120] = '移门衣柜'
categoryMap[111] = '平开门衣柜'
categoryMap[40] = '儿童床'
categoryMap[301] = '沙发'
categoryMap[323] = '梳妆台'
categoryMap[310] = '餐桌'
categoryMap[330] = '书桌/工作台'
categoryMap[355] = '坐便器'
categoryMap[342] = '浴室柜'
categoryMap[350] = '卫生间淋浴'
categoryMap[105] = '定制家具'
categoryMap[106] = '餐边柜'
categoryMap[107] = '厨柜'
categoryMap[109] = '吊柜'
categoryMap[113] = '书柜'
categoryMap[114] = '书桌'
categoryMap[116] = '卫浴柜'
categoryMap[117] = '洗衣柜'
categoryMap[118] = '玄关柜'
categoryMap[119] = '阳台收纳柜'                                  
categoryMap[152] = '灶台'
categoryMap[153] = '烟机'
categoryMap[154] = '集成灶'                                 
categoryMap[306] = '玄关柜'    
categoryMap[307] = '鞋柜'    
categoryMap[312] = '酒柜'       

def getCategoryNameById(categoryId):
    global categoryMap
    if categoryId in categoryMap:
        return categoryMap[categoryId]
    else:
        return '未知'
    