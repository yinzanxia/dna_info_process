# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 14:58:13 2018

@author: mayn
"""



'''获取平移向量'''
def get_trans_vector(src_vec, dst_vec):
    vec = list(map(lambda x: x[0]-x[1], zip(dst_vec, src_vec)))
    return vec

def trans_by_vec(cur_pos, trans_vec):
    if isinstance(cur_pos, dict):
        
        for i in range(len(cur_pos['x'])):
            if isinstance(cur_pos['x'][i], list):
                for j in range(len(cur_pos['x'][i])):
                    cur_pos['x'][i][j] -= trans_vec[0]
            else:
                cur_pos['x'][i] -= trans_vec[0]
            
        for i in range(len(cur_pos['y'])):
            if isinstance(cur_pos['y'][i], list):
                for j in range(len(cur_pos['y'][i])):
                    cur_pos['x'][i][j] -= trans_vec[1]
            else:
                cur_pos['y'][i] -= trans_vec[1]
    elif isinstance(cur_pos, list):
        for i in range(len(trans_vec)):
            cur_pos[i] -= trans_vec[i]
            

def get_relative_vec(area_center, bed_num, bed_size, bed_center, window_num, window_center):
    vec_room2bed = {}
    vec_room2bed['x'] = []
    vec_room2bed['y'] = []
    if bed_num > 0:
        if ((bed_size[0] > 1000 and bed_size[1] > 1100) or (bed_size[0] > 1100 and bed_size[1] > 1000)):            
            #print('DNA',dna['solutionId'],'room', room_name, 'bed size maybe incorrect! bed_size is:',bed_size[0]*2,'x',bed_size[1]*2)
            return
        vec_room2bed['x'].append(bed_center[0]-area_center[0])
        vec_room2bed['y'].append(bed_center[1]-area_center[1])
    

        