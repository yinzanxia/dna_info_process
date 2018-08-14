# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 21:57:10 2018

@author: mayn
"""

#from shapely.geometry import Polygon
#from shapely.geometry import LineString
import MyPoint
import MyWall


def isWallFree(pattern, wall_idx):
    if wall_idx >= len(pattern):
        return False
    
    return sum(pattern[wall_idx]) == 0


def growToXMin(center_x, center_y, x_min, wall_point_num, wall_pos):
    tmp_x = x_min
    wall_len = 0
    for i in range(wall_point_num-1):
        cur_x = wall_pos['x'][i]
        cur_y = wall_pos['y'][i]
        next_x = wall_pos['x'][i+1]
        next_y = wall_pos['y'][i+1]
        
        if abs(cur_x - next_x) < 50  and max(cur_x, next_x) > x_min and max(cur_x, next_x) < center_x and center_y > min(cur_y, next_y) and center_y < max(cur_y, next_y):  #平行与Y轴且在点与边界之间
            if tmp_x < max(cur_x, next_x):
                tmp_x = max(cur_x, next_x)
                wall_len = abs(cur_y - next_y)
                
    return tmp_x, wall_len
                    
def growToXMax(center_x, center_y, x_max, wall_point_num, wall_pos):
    tmp_x = x_max
    wall_len = 0
    for i in range(wall_point_num-1):
        cur_x = wall_pos['x'][i]
        cur_y = wall_pos['y'][i]
        next_x = wall_pos['x'][i+1]
        next_y = wall_pos['y'][i+1]
        
        if abs(cur_x - next_x) < 50  and min(cur_x, next_x) < x_max and min(cur_x, next_x) > center_x and center_y > min(cur_y, next_y) and center_y < max(cur_y, next_y):  #平行与Y轴且在点与边界之间
            if tmp_x > min(cur_x, next_x):
                tmp_x = min(cur_x, next_x)
                wall_len = abs(cur_y - next_y)
                
    return tmp_x, wall_len

def growToYMin(center_x, center_y, y_min, wall_point_num, wall_pos):
    tmp_y = y_min
    wall_len = 0
    for i in range(wall_point_num-1):
        cur_x = wall_pos['x'][i]
        cur_y = wall_pos['y'][i]
        next_x = wall_pos['x'][i+1]
        next_y = wall_pos['y'][i+1]
        if abs(cur_y - next_y) < 50  and max(cur_y, next_y) > y_min and max(cur_y, next_y) < center_y and center_x > min(cur_x, next_x) and center_x < max(cur_x, next_x):  #平行与X轴且在点与边界之间
            if tmp_y < max(cur_y, next_y):
                tmp_y = max(cur_y, next_y)
                wall_len = abs(cur_x, next_x)
    return tmp_y, wall_len

def growToYMax(center_x, center_y, y_max, wall_point_num, wall_pos):
    tmp_y = y_max
    wall = [0, 0, 0, 0]
    for i in range(wall_point_num-1):
        cur_x = wall_pos['x'][i]
        cur_y = wall_pos['y'][i]
        next_x = wall_pos['x'][i+1]
        next_y = wall_pos['y'][i+1]
        
        if abs(cur_y - next_y) < 50  and min(cur_y, next_y) < y_max and min(cur_y, next_y) > center_y and center_x > min(cur_x, next_x) and center_x < max(cur_x, next_x):  #平行与Y轴且在点与边界之间
            if tmp_y > min(cur_y, next_y):
                tmp_y = min(cur_y, next_y)
                wall[0] = cur_x
                wall[1] = cur_y
                wall[2] = next_x
                wall[3] = next_y
                
    return tmp_y, wall

def rectGrow(center_x, center_y, wall_point_num, wall_pos):
    x_min, x_max, y_min, y_max = getRectLimit(wall_point_num, wall_pos['x'], wall_pos['y'])
    left = center_x    
    right = center_x
    top = center_y
    bottom = center_y
    
    
    '''优先向某个方向生长应该检查距离最近的墙的距离而非边界墙的距离'''
    if center_x - x_min < x_max - center_x:
        #优先向x_min方向生长 
        left, wall_len = growToXMin(center_x, center_y, x_min, wall_point_num, wall_pos)        
    else:
        #优先向x_max方向生长        
        right, wall_len = growToXMax(center_x, center_y, x_max, wall_point_num, wall_pos)
    
    if center_y - y_min < y_max - center_y:
        #优先向y_min方向生长        
        bottom, wall_len1 = growToYMin(center_x, center_y, y_min, wall_point_num, wall_pos)
    else:
        #优先向y_max方向生长        
        top, wall = growToYMax(center_x, center_y, y_max, wall_point_num, wall_pos)
        
    '''以上完成两个方向上距离墙的搜索'''                
    
    return left, right, top, bottom

def rectGrowWithBackWall(back_wall, align, center_x, center_y, wall_point_num, wall_pos, door_num, door_pos):
    x_min, x_max, y_min, y_max = getRectLimit(wall_point_num, wall_pos['x'], wall_pos['y'])
    left = center_x    
    right = center_x
    top = center_y
    bottom = center_y
    
    if back_wall == 1:
        #优先向x_max方向生长 
        right, y_wall_len = growToXMax(center_x, center_y, x_max, wall_point_num, wall_pos)
        #然后向x_min方向生长，优先检查障碍wall，其次检查门边界和平行于Y且与back_wall相距一面墙的墙的X坐标，不超过660
        if align == -1:
            top, x_wall_len = growToYMax(center_x, center_y, y_max, wall_point_num, wall_pos)    
        else:  #align=1
            bottom, x_wall_len = growToYMin(center_x, center_y, y_min, wall_point_num, wall_pos)
        
    elif back_wall == 2:
        #优先向y_min方向生长   
        bottom = growToYMin(center_x, center_y, y_min, wall_point_num, wall_pos)
    elif back_wall == 3:
        #优先向x_min方向生长 
        left = growToXMin(center_x, center_y, x_min, wall_point_num, wall_pos)
    elif back_wall == 4:
        #优先向y_max方向生长        
        top, x_wall = growToYMax(center_x, center_y, y_max, wall_point_num, wall_pos)   
        
        if align == -1:
            left, y_wall = growToXMin(center_x, center_y, x_min, wall_point_num, wall_pos)
        else:  #align=1
            right, y_wall = growToXMax(center_x, center_y, x_max, wall_point_num, wall_pos)
            
                
 
               
    
    return left, right, top, bottom
        
def searchVirtualCorner(wall_index, start_align, wall_point_num, wall_pos):
    x_min, x_max, y_min, y_max = getRectLimit(wall_point_num, wall_pos['x'], wall_pos['y'])
    
    for i in range(wall_point_num -1):
        cur_x = wall_pos['x'][i]
        cur_y = wall_pos['y'][i]
        next_x = wall_pos['x'][i+1]
        next_y = wall_pos['y'][i+1]
        if wall_index == 1:
            if cur_x > 0 and abs(next_y - cur_y) > 500 and abs(next_y - cur_y) < y_max - y_min - 500:
                return abs(next_y - cur_y)
        
        if wall_index == 2:
            if cur_y < 0 and abs(next_x - cur_x) > 500 and abs(next_x - cur_x) < x_max - x_min - 500:
                return abs(next_x - cur_x)
            
        if wall_index == 3:
            if cur_x < 0 and abs(next_y - cur_y) > 500 and abs(next_y - cur_y) < y_max - y_min - 500:
                return abs(next_y - cur_y)
            
        if wall_index == 4:
            if cur_y > 0 and abs(next_x - cur_x) > 500 and abs(next_x - cur_x) < x_max - x_min - 500:
                return abs(next_x - cur_x)
            
    return 1500



def isBoundWall(cur_x, cur_y, next_x, next_y, x_min, x_max, y_min, y_max) :
    if abs(cur_y - next_y) < 30 and abs(cur_y - y_max) < 100:
        return True
    if abs(cur_y - next_y) < 30 and abs(cur_y - y_min) < 100:
        return True
    if abs(cur_x - next_x) < 30 and abs(cur_x - x_max) < 100:
        return True
    if abs(cur_x - next_x) < 30 and abs(cur_x - x_min) < 100:
        return True
    
    return False
    
def hasCrossWall(side, wall_point_num, wall_pos):
    x_min, x_max, y_min, y_max = getRectLimit(wall_point_num, wall_pos['x'], wall_pos['y'])
    for i in range(wall_point_num - 1):  
        cur_x = wall_pos['x'][i]
        cur_y = wall_pos['y'][i]
        next_x = wall_pos['x'][i+1]
        next_y = wall_pos['y'][i+1]
        if isBoundWall(cur_x, cur_y, next_x, next_y, x_min, x_max, y_min, y_max):
            continue
        if side == 1:
            if cur_x > 0 and next_x > 0 and abs(cur_x - next_x) > 200 and abs(cur_y - next_y) < 30:
                print("Side", side, " has cross wall!", cur_x, cur_y, next_x, next_y)
        if side == 3:
            if cur_x < 0 and next_x < 0 and abs(cur_x - next_x) > 200 and abs(cur_y - next_y) < 30:
                print("Side", side, " has cross wall!", cur_x, cur_y, next_x, next_y)
        
        if side == 2:
            if cur_y < 0 and next_y < 0 and abs(cur_x - next_x) < 30 and abs(cur_y - next_y) > 200:
                print("Side", side, " has cross wall!", cur_x, cur_y, next_x, next_y)
        
        if side == 4:
            if cur_y > 0 and next_y > 0 and abs(cur_x - next_x) < 30 and abs(cur_y - next_y) > 200:
                print("Side", side, " has cross wall!", cur_x, cur_y, next_x, next_y)
                        
            



def generate_polygon(x_list, y_list):
    num = len(x_list)
    point_list = []
    for i in range(num):           
        point_list.append((x_list[i],y_list[i]))
      
    polygon = Polygon(point_list)
    
    return polygon   
            

                
            
    

'''异形区域检测'''
def identifySpecialRect(shape_point_num, shape_pos, wall_point_num, wall_pos):
    x_min, x_max, y_min, y_max = getRectLimit(shape_point_num, shape_pos['x'], shape_pos['y'])
    print(shape_point_num, wall_point_num)
    
    wall_x = []
    wall_y = []
    for i in range(wall_point_num):
        wall_x.append(wall_pos['x'][i])
        wall_y.append(wall_pos['y'][i])
        
    wall_x.sort()
    wall_y.sort()
    
    thres1 = 60
    thres2 = 500
    left_min_dist = 10000000
    right_min_dist = 1000000
    top_min_dist = 10000000
    bottom_min_dist = 1000000
    
    for i in range(wall_point_num):
        if i == 0 or i == wall_point_num - 1:
            continue
        
        dist = wall_x[i] - wall_x[0]
        if dist > thres1 and dist < thres2 and dist < left_min_dist:
            left_min_dist = dist
            
        dist = wall_x[wall_point_num-1] - wall_x[i]
        if dist > thres1 and dist < thres2 and dist < right_min_dist:
            right_min_dist = dist
            
        dist = wall_y[i] - wall_y[0]
        if dist > thres1 and dist < thres2 and dist < bottom_min_dist:
            bottom_min_dist = dist
            
        dist = wall_y[wall_point_num - 1] - wall_y[i]
        if dist > thres1 and dist < thres2 and dist < top_min_dist:
            top_min_dist = dist
            
    print("Search:",left_min_dist, right_min_dist, top_min_dist, bottom_min_dist)
    hasCrossWall(1, wall_point_num, wall_pos)
    hasCrossWall(2, wall_point_num, wall_pos)
    hasCrossWall(3, wall_point_num, wall_pos)
    hasCrossWall(4, wall_point_num, wall_pos)
    '''
    wall_polygon = generate_polygon(wall_pos['x'], wall_pos['y'])
    left_rect_polygon = generate_polygon([wall_x[0], wall_x[0], wall_x[0] + 500, wall_x[0] + 500], 
                                         [wall_y[0], wall_y[wall_point_num-1], wall_y[wall_point_num-1], wall_y[0]])
    
    right_rect_polygon = generate_polygon([wall_x[wall_point_num-1], wall_x[wall_point_num-1], wall_x[wall_point_num-1]-500, wall_x[wall_point_num-1]-500],
                                          [wall_y[wall_point_num-1], wall_y[0],wall_y[0],wall_y[wall_point_num-1]])
    
    top_rect_polygon = generate_polygon([wall_x[0], wall_x[wall_point_num-1], wall_x[wall_point_num-1], wall_x[0]],
                                        [wall_y[wall_point_num-1], wall_y[wall_point_num-1], wall_y[wall_point_num-1]-500, wall_y[wall_point_num-1]-500])
    bottom_rect_polygon = generate_polygon([wall_x[0], wall_x[wall_point_num-1], wall_x[wall_point_num-1], wall_x[0]],
                                           [wall_y[0], wall_y[0], wall_y[0]+500, wall_y[0] + 500])



    left_p = left_rect_polygon.difference(wall_polygon)
    if left_p != None and left_p.area > 1000:
        print("LEFT!")
     
    right_p = right_rect_polygon.difference(wall_polygon)
    if right_p != None and right_p.area > 1000:
        print("RIGHT!")
       
    top_p = top_rect_polygon.difference(wall_polygon)
    if top_p != None and top_p.area > 1000:
        print("TOP!")
        
    bottom_p = bottom_rect_polygon.difference(wall_polygon)
    if bottom_p != None and bottom_p.area > 1000:
        print("BOTTOM!")
    '''
    
    
    
    '''
    垂直交线法
    在距离左边界300毫米处画一条平行与X轴或Y轴的线，检查区域内部是否有交点，定位出异形区域所处的方位
    
    
    '''
    
    
    










