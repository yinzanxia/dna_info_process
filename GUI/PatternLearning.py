# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 21:57:10 2018

@author: mayn
"""

'''门或窗的中心点坐标，方向 0: x轴平行， 方向1：y轴平行'''
def getSideOrder(x, y, direction):
    if direction == 0:
        if y > 0:
            return 4
        elif y < 0:
            return 2
        else:
            return 0  
    elif direction == 1:
        if x > 0:
            return 1
        elif x < 0:
            return 3
        else:
            return 0    


'''获取x列表和y列表的最大和最小值'''
def getRectLimit(num, x_list, y_list):
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

       
'''生成门窗模式'''
def getDoorWindowPattern(obj_num, obj_pos, pattern, obj_size_ratio, x_range, y_range, obj_type):
    
    for i in range(obj_num):       
        
        obj_x = obj_pos['x'][i]
        obj_y = obj_pos['y'][i]        
                
        x_min, x_max, y_min, y_max = getRectLimit(len(obj_x), obj_x, obj_y)
        
        center_x = (x_max + x_min) / 2.0
        center_y = (y_max + y_min) / 2.0
        
        delta_x = x_max - x_min
        delta_y = y_max - y_min
        if delta_x > delta_y:
            #平行于x轴, side = 2  or side= 4
            side = getSideOrder(center_x, center_y, 0)
            obj_size_ratio[side - 1] = delta_x * 1.0 / x_range
            if delta_x > x_range * 2 / 3:
                pattern[side][0] = obj_type
                pattern[side][1] = obj_type
                pattern[side][2] = obj_type
            else:
                if side == 2:
                    if center_x > 10:
                        pattern[side][0] = obj_type
                    elif center_x < -10:
                        pattern[side][2] = obj_type
                    else:
                        pattern[side][1] = obj_type
                else: #side = 4
                    if center_x < -10:
                        pattern[side][0] = obj_type
                    elif center_x > 10:
                        pattern[side][2] = obj_type
                    else:
                        pattern[side][1] = obj_type
        else:
            #平行于y轴
            side = getSideOrder(center_x, center_y, 1)
            obj_size_ratio[side - 1] = delta_y * 1.0 / y_range
            if delta_y > y_range * 2 / 3:
                pattern[side][0] = obj_type
                pattern[side][1] = obj_type
                pattern[side][2] = obj_type
            else:
                if side == 1:
                    if center_y > 10:
                        pattern[side][0] = obj_type
                    elif center_y < -10:
                        pattern[side][2] = obj_type
                    else:
                        pattern[side][1] = obj_type
                else:
                    if center_y < -10:
                        pattern[side][0] = obj_type
                    elif center_y > 10:
                        pattern[side][2] = obj_type
                    else:
                        pattern[side][1] = obj_type
                    

'''生成门和窗模式'''                   
def generateRoomParttern(door_num, door_pos, window_num, window_pos, x_range, y_range):
    #obj_type: 1-door, 2-window
    #平行于x轴模式为*0, 平行与y轴模式为*1
    pattern = {} 
    pattern[0] = [0, 0, 0]
    pattern[1] = [0, 0, 0]
    pattern[2] = [0, 0, 0]
    pattern[3] = [0, 0, 0]
    pattern[4] = [0, 0, 0]
    
    door_size_ratio = [0, 0, 0, 0]
    window_size_ratio = [0, 0, 0, 0]
    
    getDoorWindowPattern(door_num, door_pos, pattern, door_size_ratio,  x_range, y_range, 1)
    getDoorWindowPattern(window_num, window_pos, pattern, window_size_ratio, x_range, y_range, 2)
    
    return pattern, door_size_ratio, window_size_ratio
     

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

def isWallFree(pattern, wall_idx):
    if wall_idx >= len(pattern):
        return False
    
    return sum(pattern[wall_idx]) == 0

def getFreeWall(pattern):
    free_wall = []
    
    '''根据pattern选择没有门和窗的墙， TODO：后续考虑窗尺寸小于一定阈值时的处理，拐角飘窗'''    
    for ikey, ivalue in pattern.items():
        if ikey != 0:
            value_sum = sum(ivalue)
            if value_sum == 0:
                free_wall.append(ikey)
    return free_wall

def filterFreeWallByExperience(pattern, free_wall):
    '''根据经验对无门无窗的墙进行过滤，得到床头贴靠的墙'''   
    if len(free_wall) > 1:
        for ikey, ivalue in pattern.items():
            if ikey != 0:
                value_sum = sum(ivalue)
                if value_sum == 1:
                    if ivalue[0] == 1:
                        pre_wall = getPreWall(ikey)                        
                        if pre_wall in free_wall:
                            free_wall.remove(pre_wall)
                    elif ivalue[2] == 1:
                        post_wall = getPostWall(ikey)                        
                        if post_wall in free_wall:
                            free_wall.remove(post_wall)
                    
                    if len(free_wall) == 1:
                        break

'''根据门窗位置预测床所贴靠的墙以及在墙上的相对位置'''
def predictObjPostitionByPattern(pattern, door_size_ratio, window_size_ratio):  
    
    free_wall = getFreeWall(pattern)    
    filterFreeWallByExperience(pattern, free_wall)
    align = 0
    
    '''目前得到一种方案：床只有一面贴靠的墙； 根据经验选择床在该墙上贴靠的位置， -1表示靠近前驱，1表示靠近后驱，0表示床中心点在贴靠位于该墙的中央'''
    if len(free_wall) == 1:
        free_wall_index = free_wall[0]
        pre_wall = getPreWall(free_wall_index)
        post_wall = getPostWall(free_wall_index)
        
        #选择更贴靠窗的一侧，若两侧都贴靠窗，选择贴靠窗尺寸更大的
        if 2 in pattern[pre_wall] and 2 not in pattern[post_wall]:
            align = -1
        elif 2 not in pattern[pre_wall] and 2 in pattern[post_wall]:
            align = 1
        elif 2 in pattern[pre_wall] and 2 in pattern[post_wall]:
            if window_size_ratio[pre_wall - 1] > window_size_ratio[post_wall - 1]:
                align = -1
            else:
                align = 1
        else:
            #没有窗，可能是阳台门，比较大的门，当作窗处理
            if door_size_ratio[pre_wall - 1] > door_size_ratio[post_wall - 1]:
                align = -1
            else:
                align= 1
                    
            
    else:
        print('free_wall more than 1:', free_wall)
    return free_wall, align




'''根据贴靠的墙编号和在墙上的相对偏移预测床中心点的位置'''
def generatePointByPrediction(shape_point_num, shape_pos, wall_point_num, wall_pos, free_wall, align):
    objPosition = {}
    bed = 318
    wardrobe = 120
    objPosition[bed] = {}
    objPosition[bed]['x'] = []
    objPosition[bed]['y'] = []
    
    objPosition[wardrobe] = {}
    objPosition[wardrobe]['x'] = []
    objPosition[wardrobe]['y'] = []
    
    x_min, x_max, y_min, y_max = getRectLimit(shape_point_num, shape_pos['x'], shape_pos['y'])    
    
    x_list, y_list = getWallRangeByWallIdex(free_wall, wall_point_num, wall_pos)
    
    w_x_min = x_min
    w_x_max = x_max
    w_y_min = y_min
    w_y_max = y_max
    
    if len(x_list) > 0:    
        w_x_max = max(x_list)
        w_x_min = min(x_list)
    
    if len(y_list) > 0:
        w_y_max = max(y_list)
        w_y_min = min(y_list)
    
    if free_wall == 1:
        objPosition[bed]['x'].append(w_x_max - 1000)
        objPosition[bed]['x'].append(w_x_max - 1000)
        mid_y = (w_y_max + w_y_min) / 2.0
        objPosition[bed]['y'].append((mid_y))
        if align == -1: 
            objPosition[bed]['y'].append(w_y_max*1.0 /3)
        elif align == 1: 
            objPosition[bed]['y'].append(w_y_min*1.0 /3)
        else:
            objPosition[bed]['y'].append(mid_y)
    
    if free_wall == 3:
        objPosition[bed]['x'].append(w_x_min + 1000)
        objPosition[bed]['x'].append(w_x_min + 1000)
        mid_y = (w_y_max + w_y_min) / 2.0
        objPosition[bed]['y'].append((mid_y))
        
        if align == -1:
            objPosition[bed]['y'].append(w_y_min*1.0/3)
        elif align == 1:
            objPosition[bed]['y'].append(w_y_max*1.0/3)
        else:
            objPosition[bed]['y'].append(mid_y)
            
    
    if free_wall == 2:
        objPosition[bed]['y'].append(w_y_min + 1000)
        objPosition[bed]['y'].append(w_y_min + 1000)
        mid_x = (w_x_max + w_x_min) / 2.0
        objPosition[318]['x'].append(mid_x)
        
        if align == -1:
            objPosition[bed]['x'].append(w_y_max*1.0/3)
        elif align == 1:
            objPosition[bed]['x'].append(w_x_min*1.0/3)
        else:
            objPosition[bed]['x'].append(mid_x)
            
    
    if free_wall == 4:
        objPosition[bed]['y'].append(w_y_max - 1000)
        objPosition[bed]['y'].append(w_y_max - 1000)
        mid_x = (w_x_max + w_x_min) / 2.0
        objPosition[bed]['x'].append(mid_x)
        
        if align == -1:
            objPosition[bed]['x'].append(w_x_min*1.0/3)
        elif align == 1:
            objPosition[bed]['x'].append(w_x_max*1.0/3)
        else:
            objPosition[bed]['x'].append(mid_x)
            
    
    return objPosition


def getWallRangeByWallIdex(free_wall_idx, wall_point_num, wall_pos):
    x_min, x_max, y_min, y_max = getRectLimit(wall_point_num, wall_pos['x'], wall_pos['y'])
    x_list = []
    y_list = []
    if free_wall_idx == 1:
        #最右侧的wall
        for i in range(wall_point_num):
            x = wall_pos['x'][i]
            y = wall_pos['y'][i]
            if abs(x - x_max) < 100:
                y_list.append(y)
                
    if free_wall_idx == 2:
        #最下方的wall
        for i in range(wall_point_num):
            x = wall_pos['x'][i]
            y = wall_pos['y'][i]
            if abs(y - y_min) < 100:
                x_list.append(x)
                
    if free_wall_idx == 3:
        #最左侧的wall
        for i in range(wall_point_num):
            x = wall_pos['x'][i]
            y = wall_pos['y'][i]
            if abs(x - x_min) < 100:
                y_list.append(y)
                
    if free_wall_idx == 4:
        #最下方的wall
        for i in range(wall_point_num):
            x = wall_pos['x'][i]
            y = wall_pos['y'][i]
            if abs(y - y_max) < 100:
                x_list.append(x)
                
    
    return x_list, y_list
    
        
       
            













