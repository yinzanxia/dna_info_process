# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 20:18:24 2018

@author: mayn
解析不同的户型，生成不同的户型图
"""
import json
import DrawShape
import DNA_Object
import DNA_Geometry
import matplotlib.pyplot as plt

def on_button_press(event):
    pos = plt.ginput(1)
    print(pos)
    x, y = pos[0]
    plt.plot(x, y, '*')
    plt.show()

def stat_room_size(dna, room_name, room_cnt, width, long, result):
    for i in range(room_cnt):              
        result['x'].append(width[i])
        result['y'].append(long[i])
        
        if (long[i] > 1600000) or (long[i] < 3000):
            print('dna', dna['solutionId'])
            #DrawShape.draw_house_area(dna)
            DrawShape.draw_room_area(dna, room_name)

path = "E:/simulation_tools/simulation_py/dnafiles/dna_data_201807197_171051.dat";
f = open(path, 'r',encoding='UTF-8')
count = 0
skip_id_list = [20, 42, 89, 111, 112, 113, 132, 136, 139, 142, 143]
skip_solution_list = [6580]  #客厅信息不正确

room_size_dict = {}  #统计不同类型的房间的尺寸
room_area_point_cnt_dict={}  #统计不同类型的房间的area包含的点的数量
for line in f.readlines():
    dna = json.loads(line)    
    if dna['id'] in skip_id_list or dna['solutionId'] in skip_solution_list:
        continue
    count += 1
    
    '''
    DrawShape.draw_house_area(dna)
    DrawShape.draw_house_door(dna)
    DrawShape.draw_house_window(dna)
    DrawShape.draw_house_wall(dna)
    
    break
    
    '''
    
    #fig, ax = plt.subplots()
    #fig.canvas.mpl_connect('button_press_event', on_button_press)
    #DrawShape.draw_house_obj(dna, 318, True)
    #print(count)     
    room_name_list = ['次卧']    
    
    for n in range(len(room_name_list)):
        room_name = room_name_list[n]
        if room_name not in room_size_dict:
            room_size_dict[room_name] = {}
            room_size_dict[room_name]['x'] = []
            room_size_dict[room_name]['y'] = []
        
        if room_name not in room_area_point_cnt_dict:
            room_area_point_cnt_dict[room_name] = {}

        room_cnt, width, long = DNA_Object.get_room_major_size(dna, room_name)
        stat_room_size(dna, room_name, room_cnt, width, long, room_size_dict[room_name])
        point_cnt, room_list = DNA_Object.get_room_area_point_num(dna, room_name)
        
        for i in range(len(point_cnt)):
            cnt = point_cnt[i]
            
            if True:#cnt == 10: # and dna['solutionId'] == 11414:
                DrawShape.draw_room_area(dna, room_name)
                DrawShape.draw_house_door(dna)
                DrawShape.draw_house_window(dna)                
                polygon = DNA_Geometry.generate_room_polygon(room_list[i])
                minx, miny, maxx, maxy = DNA_Geometry.get_fuzzy_bounds(polygon)
                DrawShape.draw_bounds(minx, miny, maxx, maxy)
            if cnt in room_area_point_cnt_dict[room_name]:
                room_area_point_cnt_dict[room_name][cnt] += 1
            else:
                room_area_point_cnt_dict[room_name][cnt] = 1   
f.close()

print(count)
title = []
title_tail = '主空间尺寸'
for i in range(len(room_name_list)):
    cur_title = room_name_list[i] + title_tail
    if room_name_list[i] in room_size_dict:
        DrawShape.draw_scatter_distribution(room_size_dict[room_name_list[i]], cur_title, '短边(毫米)', '长边(毫米)')


#print(room_area_point_cnt)