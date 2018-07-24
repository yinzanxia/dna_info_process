# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 14:39:11 2018

@author: mayn
"""

import matplotlib.pyplot as plt

import DNA_Geometry
import DNA_Object
import DNA_File
import DrawShape
import Util
from shapely.geometry import LineString

def show_room_layout(dna, vec_room2bed, vec_room2window, trans_vec, room_name):     
    vec_window2bed = {}    
    vec_window2bed['x'] = []
    vec_window2bed['y'] = []
    room = DNA_Object.get_room_by_usagename(dna, room_name)
    #print(dna['solutionId'], room['roomUsageName'])
    
    if 'doors' in dna:
        door_num, door_pos = DNA_Object.get_door_from_dna(dna)
    else:
        door_center, door_num, door_pos = DNA_Object.get_door_from_room(room)
    
    if 'walls' in dna:
        wall_num, wall_pos = DNA_Object.get_wall_from_dna(dna)
    else:        
        wall_num, wall_pos = DNA_Object.get_wall_from_room(room)    
    
    if 'windows' in dna:
        window_num, window_pos = DNA_Object.get_window_info_from_dna(dna)
    else:
        window_center,window_num,window_pos = DNA_Object.get_window_info_from_room(room) 
    
    '''
    if door_num > 0:
        room_polygon = DNA_Geometry.generate_room_polygon(room)
        door_polygon_list = DNA_Geometry.generate_door_geometry(door_num, door_pos)
        
        for w in range(len(door_polygon_list)):     
            #print('hi',room_polygon.boundary.coords, len(room_polygon.boundary.coords), list(room_polygon.boundary.coords))
            if DNA_Geometry.polygon_intersect_polygon_loosely(room_polygon, door_polygon_list[w]):
                #print('hi',room_polygon.boundary.coords, len(room_polygon.boundary.coords), list(room_polygon.boundary.coords))
                #print('[', w, ']', wall_pos['x'][w], wall_pos['y'][w])
                Util.trans_by_vec(door_pos, trans_vec)
                plt.plot(door_pos['x'][w], door_pos['y'][w], linewidth='1.5')
                '''
    
    bed_num, bed_center, bed_size, bed_point= DNA_Object.get_obj_info_from_room(room, 318)
    area_center, area = DNA_Object.get_room_area(room) 

    if bed_num > 0:
        if ((bed_size[0] > 1000 and bed_size[1] > 1100) or (bed_size[0] > 1100 and bed_size[1] > 1000)):            
            print('DNA',dna['solutionId'],'room', room_name, 'bed size maybe incorrect! bed_size is:',bed_size[0]*2,'x',bed_size[1]*2)
            return
        vec_room2bed['x'].append(bed_center[0]-area_center[0])
        vec_room2bed['y'].append(bed_center[1]-area_center[1])
        
        Util.trans_by_vec(bed_point, trans_vec)
        Util.trans_by_vec(area_center, trans_vec)
        Util.trans_by_vec(bed_center, trans_vec)
        plt.plot(bed_point['x'], bed_point['y'], linewidth='0.5')
        #print(bed_center)
        plt.plot(bed_center[0], bed_center[1], 'o')        
    
    
    
    wardrobe_num, wardobe_center, wardrobe_size, wardrobe_point = DNA_Object.get_obj_info_from_room(room, 120)
    if wardrobe_num > 0:
        Util.trans_by_vec(wardrobe_point, trans_vec)
        Util.trans_by_vec(wardobe_center, trans_vec)       
        plt.plot(wardrobe_point['x'], wardrobe_point['y'], linewidth='0.5')
        #print(bed_center)
        plt.plot(wardobe_center[0], wardobe_center[1], 'o')
        if (wardobe_center[0] > 600):
            print(dna['solutionId'])
      
    
    
    
#------------------------------------------------------------------------------
if __name__ == '__main__':    
    
    path = "E:/simulation_tools/simulation_py/dnafiles";
    dna_file_list = DNA_File.find_json_files(path)
    count = 0             
    #dna_list = ['suiyueruge.txt', 'lanseduonaohe.txt', 'xizhaomisuli.txt', 'qinqishuhua.txt', 'bimozhiyan.txt']   
    #dna_list = ['suiyueruge.txt', 'lanseduonaohe.txt', 'xizhaomisuli.txt']    
    vec_room2bed = {}
    vec_room2bed['x'] = []
    vec_room2bed['y'] = []
    
    vec_door2bed = {}
    vec_door2bed['x'] = []
    vec_door2bed['y'] = []
     
    flag = [False, False, False, True]
    for i in range(len(dna_file_list)): 
       
        dna = DNA_File.load_dna_by_file_name(dna_file_list[i])        
        
        if 'windows' in dna:
            if flag[0] == False and DrawShape.draw_house_area(dna):
                flag[0] = True
            
            if flag[1] == False and DrawShape.draw_house_door(dna):
                flag[1] = True
                
            if flag[2] == False and DrawShape.draw_house_window(dna):        
                flag[2] = True
            
            if flag[3] == False and DrawShape.draw_house_wall(dna):        
                flag[3] = True
    
        
        #处理户型平移（同一户型的位置坐标不一样，由于户型只画了一次，家具信息每次都画，因此家具相对于户型的位置不准确，需做平移处理）
        trans_vec1 = [0, 0]
        trans_vec2 = [0, 0]
        
        if (i == 0):
            base_room_center1, base_area1 = DNA_Object.get_room_area(DNA_Object.get_room_by_usagename(dna, '主卧'))
            base_room_center2, base_area2 = DNA_Object.get_room_area(DNA_Object.get_room_by_usagename(dna, '次卧'))
        else:
            cur_room_center1, cur_area1 = DNA_Object.get_room_area(DNA_Object.get_room_by_usagename(dna, '主卧'))
            cur_room_center2, cur_area2 = DNA_Object.get_room_area(DNA_Object.get_room_by_usagename(dna, '次卧'))
            trans_vec1 = Util.get_trans_vector(base_room_center1, cur_room_center1)
            trans_vec2 = Util.get_trans_vector(base_room_center2, cur_room_center2)
            
            
        
        #show_room_layout(dna, vec_room2bed, trans_vec1, '主卧')
        #show_room_layout(dna, vec_room2bed, trans_vec2, '次卧')
        count += 1
        #print("-------------------------------------------------------------\n")
    DrawShape.draw_relative_info(vec_room2bed)
    print(count, 'files processed.\n')
    print(vec_room2bed)

