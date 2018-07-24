# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 13:33:35 2018

@author: mayn
"""

from shapely.geometry import Polygon
from shapely.geometry import LineString


def generate_room_polygon(room):
    point_list = []
       
    area_point_num = len(room['areas'])
    for j in range(area_point_num):
        cur_point = room['areas'][j]      
        point_list.append((cur_point['x'],cur_point['y']))
      
    polygon = Polygon(point_list)
    
    return polygon

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
                x.append(point_list[k]['x'])
                y.append(point_list[k]['y'])
                z.append(point_list[k]['z'])
            wall_pos['x'].append(x)
            wall_pos['y'].append(y)
            wall_pos['z'].append(z)
        return wall_num, wall_pos
    else:
        return 0,{}
    
    
def generate_wall_polygon(wall_num, wall_pos):
    polygon = []
    
    for i in range(wall_num):
        point_num = len(wall_pos['x'][i])
        cur_point_list = []
        for j in range(point_num):
            cur_point_list.append((wall_pos['x'][i][j], wall_pos['y'][i][j]))   
        cur_point_list = list(set(cur_point_list))
        if len(cur_point_list) > 2:
            p = Polygon(cur_point_list)
            polygon.append(p)
    return polygon

def generate_door_geometry(door_num, door_pos):
    geometry_obj = []
    for i in range(door_num):
        point_num = len(door_pos['x'][i])
        cur_point_list = []
        for j in range(point_num):
            cur_point_list.append((door_pos['x'][i][j], door_pos['y'][i][j]))
        cur_point_list = list(set(cur_point_list))
        
        if len(cur_point_list) > 2:
            p = Polygon(cur_point_list)            
        else:
            p = LineString(cur_point_list)
        geometry_obj.append(p)
    return geometry_obj
            
def polygon_touches_polygon(polygon1, polygon2):
    list1, len1 = list(polygon1.boundary.coords), len(polygon1.boundary.coords)
    list2, len2 = list(polygon2.boundary.coords), len(polygon2.boundary.coords)
    
    for i in range(len1 - 1):
        line1 = LineString([list1[i], list1[i+1]])
        for j in range(len2 - 1):
            line2 = LineString([list2[j], list2[j+1]])
            if line1.touches(line2):
                print(line1, line2)
                return True
        
    return False
  
def polygon_move_left(polygon, factor):
    p_list, p_len = list(polygon.boundary.coords), len(polygon.boundary.coords)
    new_list = []
    
    for i in range(p_len):
        new_list.append((p_list[i][0] - factor, p_list[i][1]))
    
    return Polygon(new_list)

def polygon_move_right(polygon, factor):
    p_list, p_len = list(polygon.boundary.coords), len(polygon.boundary.coords)
    new_list = []
    
    for i in range(p_len):
        new_list.append((p_list[i][0] + factor, p_list[i][1]))
    
    return Polygon(new_list)

def polygon_move_up(polygon, factor):
    p_list, p_len = list(polygon.boundary.coords), len(polygon.boundary.coords)
    new_list = []
    
    for i in range(p_len):
        new_list.append((p_list[i][0] , p_list[i][1] + factor))
    
    return Polygon(new_list)

def polygon_move_down(polygon, factor):
    p_list, p_len = list(polygon.boundary.coords), len(polygon.boundary.coords)
    new_list = []
    
    for i in range(p_len):
        new_list.append((p_list[i][0], p_list[i][1] - factor))
    
    return Polygon(new_list)

def get_line_from_polygon(polygon1, polygon2, factor):
    return

def polygon_intersect_polygon_loosely(polygon1, polygon2, factor=50):
    
    left_polygon1 = polygon_move_left(polygon1, factor)
    if left_polygon1.intersects(polygon2):
        return True
    
    right_polygon1 = polygon_move_right(polygon1, factor)
    if right_polygon1.intersects(polygon2):
        return True
    
    up_polygon1 = polygon_move_up(polygon1, factor)
    if up_polygon1.intersects(polygon2):
        return True
    
    down_polygon1 = polygon_move_down(polygon1, factor)
    if down_polygon1.intersects(polygon2):
        return True
    
    return False


def polygon_touches_polygon(polygon1, polygon2):
    list1, len1 = list(polygon1.boundary.coords), len(polygon1.boundary.coords)
    list2, len2 = list(polygon2.boundary.coords), len(polygon2.boundary.coords)
    
    for i in range(len1 - 1):
        line1 = LineString([list1[i], list1[i+1]])
        for j in range(len2 - 1):
            line2 = LineString([list2[j], list2[j+1]])
            if line1.touches(line2):
                print(line1, line2)
                return True
        
    return False

def get_shortest_line(polygon, process_flag):
    point_list, point_num = list(polygon.boundary.coords), len(polygon.boundary.coords)
    min_len = 10000000
    index = 0
    p1 = (0, 0)
    p2 = (0, 0)
    for i in range(point_num - 1):
        if process_flag[i] == True:
            continue
        start = i
        end = (i + 1)
        line = LineString([point_list[start], point_list[end]])
        if line.length < min_len:
            min_len = line.length
            p1 = point_list[start]
            p2 = point_list[end]
            index = i

    return LineString([p1, p2]), index

def is_fuzzy_equal(data1, data2):
    if abs(data1-data2) < 50:       
        return True
    else:
        return False
'''
0: 平行于x轴
1： 平行于y轴
-1：其他
'''
def get_line_direction(line):
    x1, y1 = line.boundary[0].x, line.boundary[0].y
    x2, y2 = line.boundary[1].x, line.boundary[1].y

    if is_fuzzy_equal(x1, x2) == True and is_fuzzy_equal(y1, y2) == False:
        return 1
    elif is_fuzzy_equal(y1, y2) == True and is_fuzzy_equal(x1, x2) == False:
        return 0
    else:
        return -1

def get_parallel_line_distance(line1, line2, direction):
    x1, y1 = line1.boundary[0].x, line1.boundary[0].y
    x2, y2 = line2.boundary[0].x, line2.boundary[0].y
    if direction == 0:
        if y1 > y2:
            return y1 - y2, -1, direction
        else:
            return y2 - y1, 1, direction
    elif direction == 1:
        if x1 > x2:
            return x1 - x2, -1, direction
        else:
            return x2 - x1, 1, direction
    else:
        return -1, -1, -1


def get_dest_line(polygon, shortest_line):
    line_direction = get_line_direction(shortest_line)
    point_list, point_num = list(polygon.boundary.coords), len(polygon.boundary.coords)
    min_dist = 10000000
    dest_line = shortest_line
    min_sign = 0
    min_direction = -1
    for i in range(point_num - 1):
        line = LineString([point_list[i], point_list[i+1]])
        direction = get_line_direction(line)
        if direction != line_direction:
            continue
        if line.equals(shortest_line):
            continue

        dist, sign, direction = get_parallel_line_distance(shortest_line, line, direction)
        if dist < min_dist:
            min_dist = dist
            dest_line = line
            min_sign = sign
            min_direction = direction

    return dest_line, min_dist, min_sign, min_direction

def is_line_in_bounds(line, polygon):
    x1, y1 = line.boundary[0].x, line.boundary[0].y
    x2, y2 = line.boundary[1].x, line.boundary[1].y
    minx, miny, maxx, maxy = polygon.bounds

    if (is_fuzzy_equal(x1, x2) and is_fuzzy_equal(x1, minx)) or (is_fuzzy_equal(x1, x2) and is_fuzzy_equal(x1, maxx)):
        return True
    elif (is_fuzzy_equal(y1, y2) and is_fuzzy_equal(y1, miny)) or (is_fuzzy_equal(y1, y2) and is_fuzzy_equal(y1, maxy)):
        return True
    else:
        return False
    
def generate_box_polygon(minx, miny, maxx, maxy):
    return Polygon([(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)])

def fuzzy_shortest_line(polygon, flag, minx, miny, maxx, maxy):
    #minx, miny, maxx, maxy = polygon.bounds
    shortest_line, index = get_shortest_line(polygon, flag)
    flag[index] = True
    print("short line:",shortest_line.boundary)
    if is_line_in_bounds(shortest_line, polygon) == False:
        return minx, miny, maxx, maxy
    else:
        dest_line, distance, sign, direction = get_dest_line(polygon, shortest_line)
        x1, y1 = shortest_line.boundary[0].x, shortest_line.boundary[0].y

        if direction == 0:
            # 平行与x轴
            if is_fuzzy_equal(y1, miny) and miny + distance * sign < maxy - 500:
                miny = miny + distance * sign
            elif is_fuzzy_equal(y1, maxy) and maxy + distance * sign > miny + 500:
                maxy = maxy + distance * sign
        elif direction == 1:
            # 平行与y轴
            if is_fuzzy_equal(x1, minx) and minx + distance * sign < maxx - 500:
                minx = minx + distance * sign
            elif is_fuzzy_equal(x1, maxx) and maxx + distance * sign > minx + 500:
                maxx = maxx + distance * sign
        return minx, miny, maxx, maxy

def get_fuzzy_bounds(polygon):
    point_num = len(polygon.boundary.coords) - 1
    minx, miny, maxx, maxy = polygon.bounds
    print(minx, miny, maxx, maxy)
    loop = 0
    if point_num <= 6 and point_num > 4:
        loop = 1
    else:
        loop = 10

    flag = []
    for i in range(point_num):
        flag.append(False)

    for i in range(loop):
        minx, miny, maxx, maxy = fuzzy_shortest_line(polygon, flag, minx, miny, maxx, maxy)
        print("cur_box:", minx, miny, maxx, maxy)
        box_polygon = generate_box_polygon(minx, miny, maxx, maxy)
        if box_polygon.area < 1:
            break;
        if (box_polygon.difference(polygon).area / box_polygon.area < 0.2):
            break
    return minx, miny, maxx, maxy

