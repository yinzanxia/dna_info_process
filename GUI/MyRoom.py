# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 08:54:32 2018

@author: mayn
"""

import MyUtils
import MyPoint
import MyWall

class RoomMeta:
    def __init__(self, shape_point_num, shape_pos, wall_point_num, wall_pos, door_num, door_pos, window_num, window_pos):
        self.shape_point_num = shape_point_num
        self.shape_pos = shape_pos
        self.wall_point_num = wall_point_num
        self.wall_pos = wall_pos
        self.door_num = door_num
        self.door_pos = door_pos
        self.window_num = window_num
        self.window_pos = window_pos
        
        self.shape_dx = 1
        self.shape_dy = 1
        self.shape_xmin = 0
        self.shape_xmax = 0
        self.shape_ymin = 0
        self.shape_ymax = 0
        self.initShapeInfo()
        
        self.wall_dx = 1
        self.wall_dy = 1
        self.wall_xmin = 0
        self.wall_xmax = 0
        self.wall_ymin = 0
        self.wall_ymax = 0
        self.initWallInfo()
        
        self.door_size_ratio = [0, 0, 0, 0]   #门的长度在四条边上所占的比例
        self.window_size_ratio = [0, 0, 0, 0] #窗的长度在四条边上所占的比例
        
        self.pattern = {}
        self.pattern[0] = [0, 0, 0]
        self.pattern[1] = [0, 0, 0]
        self.pattern[2] = [0, 0, 0]
        self.pattern[3] = [0, 0, 0]
        self.pattern[4] = [0, 0, 0]
        self.generateRoomParttern()
        
        
        self.objPosition = {}
        bed = 318
        wardrobe = 120
        self.objPosition[bed] = {}
        self.objPosition[bed]['x'] = []
        self.objPosition[bed]['y'] = []
        
        self.objPosition[wardrobe] = {}
        self.objPosition[wardrobe]['x'] = []
        self.objPosition[wardrobe]['y'] = []
    
    def initShapeInfo(self):
        x_min = 1000000
        x_max = -1000000
        y_min = 1000000
        y_max = -1000000
        
        for i in range(self.shape_point_num):
            x = self.shape_pos['x'][i]
            y = self.shape_pos['y'][i]
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            if y > y_max:
                y_max = y
            if y < y_min:
                y_min = y
        
        self.shape_dx = x_max - x_min
        self.shape_dy = y_max - y_min
        self.shape_xmin = x_min
        self.shape_xmax = x_max
        self.shape_ymin = y_min
        self.shape_ymax = y_max
        
        '''修正，防止出现除零错误'''
        
        if self.shape_dx <= 0:
            self.shape_dx = 1
        
        if self.shape_dy <= 0:
            self.shape_dy = 1
            
    def initWallInfo(self):
        x_min = 1000000
        x_max = -1000000
        y_min = 1000000
        y_max = -1000000
        
        for i in range(self.wall_point_num):
            x = self.wall_pos['x'][i]
            y = self.wall_pos['y'][i]
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            if y > y_max:
                y_max = y
            if y < y_min:
                y_min = y
        
        self.wall_dx = x_max - x_min
        self.wall_dy = y_max - y_min
        self.wall_xmin = x_min
        self.wall_xmax = x_max
        self.wall_ymin = y_min
        self.wall_ymax = y_max
        
        '''修正，防止出现除零错误'''
        
        if self.wall_dx <= 0:
            self.wall_dx = 1
        
        if self.wall_dy <= 0:
            self.wall_dy = 1
        
        
    def getShapeDx(self):
        return self.shape_dx
    
    def getShapeDy(self):
        return self.shape_dy


    def isWallFree(self, wall_idx):
        if wall_idx >= len(self.pattern):
            return False
    
        return sum(self.pattern[wall_idx]) == 0
    
    '''生成门窗模式'''
    def getDoorWindowPattern(self, obj_num, obj_pos, obj_type):
    
        for i in range(obj_num):       
            
            obj_x = obj_pos['x'][i]
            obj_y = obj_pos['y'][i]        
                    
            x_min, x_max, y_min, y_max = MyUtils.getListLimit(len(obj_x), obj_x, obj_y)
            
            center_x = (x_max + x_min) / 2.0
            center_y = (y_max + y_min) / 2.0
            
            delta_x = x_max - x_min
            delta_y = y_max - y_min
            if delta_x > delta_y:
                #平行于x轴, side = 2  or side= 4
                if delta_x > 1000 and obj_type == 1:
                    obj_type += 1
                side = MyUtils.getSideOrder(center_x, center_y, 0)
                
                if obj_type == 1:
                    self.door_size_ratio[side - 1] = delta_x * 1.0 / self.shape_dx
                elif obj_type == 2:
                    self.window_size_ratio[side - 1] = delta_x * 1.0 / self.shape_dx
                    
                if delta_x > self.shape_dx * 2 / 3:
                    self.pattern[side][0] = obj_type
                    self.pattern[side][1] = obj_type
                    self.pattern[side][2] = obj_type
                else:
                    if side == 2:
                        if center_x > 10:
                            self.pattern[side][0] = obj_type
                        elif center_x < -10:
                            self.pattern[side][2] = obj_type
                        else:
                            self.pattern[side][1] = obj_type
                    else: #side = 4
                        if center_x < -10:
                            self.pattern[side][0] = obj_type
                        elif center_x > 10:
                            self.pattern[side][2] = obj_type
                        else:
                            self.pattern[side][1] = obj_type
            else:
                #平行于y轴
                if delta_y > 1000 and obj_type == 1:
                    obj_type += 1
                side = MyUtils.getSideOrder(center_x, center_y, 1)
                
                if obj_type == 1:
                    self.door_size_ratio[side - 1] = delta_y * 1.0 / self.shape_dy
                elif obj_type == 2:
                    self.window_size_ratio[side - 1] = delta_y * 1.0 / self.shape_dy
                    
                if delta_y > self.shape_dy * 2 / 3:
                    self.pattern[side][0] = obj_type
                    self.pattern[side][1] = obj_type
                    self.pattern[side][2] = obj_type
                else:
                    if side == 1:
                        if center_y > 10:
                            self.pattern[side][0] = obj_type
                        elif center_y < -10:
                            self.pattern[side][2] = obj_type
                        else:
                            self.pattern[side][1] = obj_type
                    else:
                        if center_y < -10:
                            self.pattern[side][0] = obj_type
                        elif center_y > 10:
                            self.pattern[side][2] = obj_type
                        else:
                            self.pattern[side][1] = obj_type
    
    
    '''生成门和窗模式'''                   
    def generateRoomParttern(self):
        #obj_type: 1-door, 2-window
        #平行于x轴模式为*0, 平行与y轴模式为*1      
        
        self.getDoorWindowPattern(self.door_num, self.door_pos, 1)
        self.getDoorWindowPattern(self.window_num, self.window_pos,  2)
        
        
        
    def getFreeWall(self):
        free_wall = []
    
        '''根据pattern选择没有门和窗的墙， TODO：后续考虑窗尺寸小于一定阈值时的处理，拐角飘窗'''    
        for ikey, ivalue in self.pattern.items():
            if ikey != 0:
                value_sum = sum(ivalue)
                if value_sum == 0:
                    free_wall.append(ikey)
        return free_wall
        
     
        
    def filterFreeWallByExperience(self, free_wall):
        new_free_wall = []
        
        for i in range(len(free_wall)):
            new_free_wall.append(free_wall[i])
        
        '''根据经验对无门无窗的墙进行过滤，得到床头贴靠的墙'''   
        if len(new_free_wall) > 1:
            for ikey, ivalue in self.pattern.items():
                if ikey != 0:
                    value_sum = sum(ivalue)
                    if value_sum == 1:       #只有一个门
                        if ivalue[0] == 1:   #门靠近前驱
                            pre_wall = MyUtils.getPreWall(ikey)                        
                            if pre_wall in new_free_wall:
                                new_free_wall.remove(pre_wall)
                        elif ivalue[2] == 1:
                            post_wall = MyUtils.getPostWall(ikey)                        
                            if post_wall in new_free_wall:
                                new_free_wall.remove(post_wall)
                        
                        if len(new_free_wall) == 1:
                            break
                        
        return new_free_wall
    
    
    
    
    '''根据门窗位置预测床所贴靠的墙以及在墙上的相对位置'''
    def predictBedAreaByPattern(self):  
        
        free_wall = self.getFreeWall()    
        filtered_free_wall = self.filterFreeWallByExperience(free_wall)
        align = 0
        
        '''目前得到一种方案：床只有一面贴靠的墙； 根据经验选择床在该墙上贴靠的位置， -1表示靠近前驱，1表示靠近后驱，0表示床中心点在贴靠位于该墙的中央'''
        if len(filtered_free_wall) == 1:
            free_wall_index = filtered_free_wall[0]
            pre_wall = MyUtils.getPreWall(free_wall_index)
            post_wall = MyUtils.getPostWall(free_wall_index)
            
            #选择更贴靠窗的一侧，若两侧都贴靠窗，选择贴靠窗尺寸更大的
            if 2 in self.pattern[pre_wall] and 2 not in self.pattern[post_wall]:
                align = -1
            elif 2 not in self.pattern[pre_wall] and 2 in self.pattern[post_wall]:
                align = 1
            elif 2 in self.pattern[pre_wall] and 2 in self.pattern[post_wall]:
                if self.window_size_ratio[pre_wall - 1] > self.window_size_ratio[post_wall - 1]:
                    align = -1
                else:
                    align = 1
            else:
                #没有窗，可能是阳台门，比较大的门，当作窗处理
                if self.door_size_ratio[pre_wall - 1] > self.door_size_ratio[post_wall - 1]:
                    align = -1
                else:
                    align= 1
                        
                
        else:
            print('free_wall more than 1:', filtered_free_wall)
        return filtered_free_wall, align
    
    
    
    def generateBedPointByPrediction(self, free_wall, align):
        
        bed = 318
        w_x_min = self.shape_xmin
        w_x_max = self.shape_xmax
        w_y_min = self.shape_ymin
        w_y_max = self.shape_ymax
        
        x_list, y_list = self.getWallRangeByWallIdex(free_wall)
        
        if len(x_list) > 0:    
            w_x_max = max(x_list)
            w_x_min = min(x_list)
        
        if len(y_list) > 0:
            w_y_max = max(y_list)
            w_y_min = min(y_list)
            
        if free_wall == 1:
            self.objPosition[bed]['x'].append(w_x_max - 1000)
            self.objPosition[bed]['x'].append(w_x_max - 1000)
            mid_y = (w_y_max + w_y_min) / 2.0
            self.objPosition[bed]['y'].append((mid_y))
            if align == -1: 
                self.objPosition[bed]['y'].append(w_y_max*1.0 /3)
            elif align == 1: 
                self.objPosition[bed]['y'].append(w_y_min*1.0 /3)
            else:
                self.objPosition[bed]['y'].append(mid_y)
        
        if free_wall == 3:
            self.objPosition[bed]['x'].append(w_x_min + 1000)
            self.objPosition[bed]['x'].append(w_x_min + 1000)
            mid_y = (w_y_max + w_y_min) / 2.0
            self.objPosition[bed]['y'].append((mid_y))
            
            if align == -1:
                self.objPosition[bed]['y'].append(w_y_min*1.0/3)
            elif align == 1:
                self.objPosition[bed]['y'].append(w_y_max*1.0/3)
            else:
                self.objPosition[bed]['y'].append(mid_y)
                
        
        if free_wall == 2:
            self.objPosition[bed]['y'].append(w_y_min + 1000)
            self.objPosition[bed]['y'].append(w_y_min + 1000)
            mid_x = (w_x_max + w_x_min) / 2.0
            self.objPosition[318]['x'].append(mid_x)
            
            if align == -1:
                self.objPosition[bed]['x'].append(w_y_max*1.0/3)
            elif align == 1:
                self.objPosition[bed]['x'].append(w_x_min*1.0/3)
            else:
                self.objPosition[bed]['x'].append(mid_x)
                
        
        if free_wall == 4:
            self.objPosition[bed]['y'].append(w_y_max - 1000)
            self.objPosition[bed]['y'].append(w_y_max - 1000)
            mid_x = (w_x_max + w_x_min) / 2.0
            self.objPosition[bed]['x'].append(mid_x)
            
            if align == -1:
                self.objPosition[bed]['x'].append(w_x_min*1.0/3)
            elif align == 1:
                self.objPosition[bed]['x'].append(w_x_max*1.0/3)
            else:
                self.objPosition[bed]['x'].append(mid_x)
    
    '''根据床贴靠的墙和在墙上的相对位置依经验预测衣柜位置'''
    def predictWardrobeAreaByPattern(self, bed_wall, bed_align):
        pre_wall = MyUtils.getPreWall(bed_wall)
        post_wall = MyUtils.getPostWall(bed_wall)
        predict_wall = 0
        predict_align = 0
        
        if bed_align == -1:        
            predict_wall = post_wall
            predict_align = -1 
        elif bed_align == 1:        
            predict_wall = pre_wall
            predict_align = 1
           
        if self.pattern[predict_wall][predict_align + 1] == 1:
            predict_wall = bed_wall
            predict_align = -bed_align
            
        return predict_wall, predict_align
    
    
    def getWallRangeByWallIdex(self, free_wall_idx):
        
        x_min = self.wall_xmin
        x_max = self.wall_xmax
        y_min = self.wall_ymin
        y_max = self.wall_ymax
        
        x_list = []
        y_list = []
        if free_wall_idx == 1:
            #最右侧的wall
            for i in range(self.wall_point_num):
                x = self.wall_pos['x'][i]
                y = self.wall_pos['y'][i]
                if abs(x - x_max) < 100:
                    y_list.append(y)
                    
        if free_wall_idx == 2:
            #最下方的wall
            for i in range(self.wall_point_num):
                x = self.wall_pos['x'][i]
                y = self.wall_pos['y'][i]
                if abs(y - y_min) < 100:
                    x_list.append(x)
                    
        if free_wall_idx == 3:
            #最左侧的wall
            for i in range(self.wall_point_num):
                x = self.wall_pos['x'][i]
                y = self.wall_pos['y'][i]
                if abs(x - x_min) < 100:
                    y_list.append(y)
                    
        if free_wall_idx == 4:
            #最上方的wall
            for i in range(self.wall_point_num):
                x = self.wall_pos['x'][i]
                y = self.wall_pos['y'][i]
                if abs(y - y_max) < 100:
                    x_list.append(x)
                
    
        return x_list, y_list
    
    def isWallFreeWithAlign(self, wall_idx, align):
        if self.pattern[wall_idx][align+1] >= 1:
            return False
        else:
            return True
        
    #wall方向和长度

    def groupWalls(self):
        positive_x_walls = []
        negative_x_walls = []
        positive_y_walls = []
        negative_y_walls = []
        for i in range(self.wall_point_num-1):
            cur_x = self.wall_pos['x'][i]
            cur_y = self.wall_pos['y'][i]
            next_x = self.wall_pos['x'][i+1]
            next_y = self.wall_pos['y'][i+1]
            p1 = MyPoint.Point(cur_x, cur_y)
            p2 = MyPoint.Point(next_x, next_y)
            cur_wall = MyWall.LinearWall(p1, p2)
            
            if cur_wall.getDirection() == 0:             
                if cur_y > 0:
                    positive_x_walls.append(cur_wall)
                else:
                    negative_x_walls.append(cur_wall)
                
            if cur_wall.getDirection() == 1:            
                if cur_x > 0:
                    positive_y_walls.append(cur_wall)
                else:
                    negative_y_walls.append(cur_wall)
                
        return positive_x_walls, negative_x_walls, positive_y_walls, negative_y_walls
    
    
    def analyzeDoorInWall(self, wall):    
        door_range = {}
        door_range['x'] = []
        door_range['y'] = []
        
        if wall.getDirection() == 0:
            for i in range(self.door_num):
                door_x = self.door_pos['x'][i]
                door_y = self.door_pos['y'][i] 
                x_min, x_max, y_min, y_max = MyUtils.getListLimit(len(door_x), door_x, door_y)
                
                delta_x = x_max - x_min
                delta_y = y_max - y_min
                
                if delta_x < delta_y:
                    continue
                
                if abs(y_min - wall.getStartY()) < 100 or abs(y_max - wall.getStartY()) < 100:            
                    tmp = [x_min, x_max]
                    door_range['x'].append(tmp)
                
            
        if wall.getDirection() == 1:
            for i in range(self.door_num):
                door_x = self.door_pos['x'][i]
                door_y = self.door_pos['y'][i] 
                x_min, x_max, y_min, y_max = MyUtils.getListLimit(len(door_x), door_x, door_y)
                
                delta_x = x_max - x_min
                delta_y = y_max - y_min
                
                if delta_x > delta_y:
                    continue
                
                if abs(x_min - wall.getStartX()) < 100 or abs(x_max - wall.getStartX()) < 100:
                    tmp = [y_min, y_max]
                    door_range['y'].append(tmp)       
                
        return door_range
    
    

        
        
    '''沿衣柜背靠的墙搜索衣柜的长度，最长不超过1500, 同方向既有wall长度限制，又有door边框限制时，以更靠近的为准'''
    def searchVirtualCorner1(self, wall_index, start_align, start_x, start_y):
        x_min = self.wall_xmin
        x_max = self.wall_xmax
        y_min = self.wall_ymin
        y_max = self.wall_ymax
        
        pos_x_walls, neg_x_walls, pos_y_walls, neg_y_walls = self.groupWalls()
        virtual_len = 1500
        
        if wall_index == 1:
            dist = 100000
            for i in range(len(pos_y_walls)):
                cur_wall = pos_y_walls[i]  
                wall_len = cur_wall.getLength()
                       
                if wall_len > 500 and wall_len < y_max - y_min - 500:
                    if cur_wall.getStartX() < dist:
                        dist = cur_wall.getStartX()
                        virtual_len = wall_len 
                        print("cur_virtural_len=", virtual_len, cur_wall)   
                        
                door_info = self.analyzeDoorInWall(cur_wall)
                if len(door_info['y']) > 0:
                    if start_align == -1:
                        virtual_len = start_y - MyUtils.getYmaxOfDoorInWall(door_info)
                    else:
                        virtual_len = MyUtils.getYminOfDoorInWall(door_info) - start_y
                    print('cur_virtual_len(door)=', virtual_len, cur_wall)
                
        
        if wall_index == 3:
            dist = 100000
            for i in range(len(neg_y_walls)):
                cur_wall = neg_y_walls[i]
                wall_len = cur_wall.getLength()           
                           
                if  wall_len > 500 and wall_len < y_max - y_min - 500:
                    if 0 - cur_wall.getStartX() < dist:
                        dist = 0 - cur_wall.getStartX()
                        virtual_len = wall_len                            
                        print("cur_virtural_len=", virtual_len, cur_wall)
                
                if 0 - cur_wall.getStartX() < dist:
                    door_info = self.analyzeDoorInWall(cur_wall)
                    if len(door_info['y']) > 0:
                        if start_align == -1:
                            virtual_len = MyUtils.getYminOfDoorInWall(door_info) - start_y
                        else:
                            virtual_len = start_y - MyUtils.getYmaxOfDoorInWall(door_info)
                            
                        print('cur_virtual_len(door)=', virtual_len, cur_wall)
                        
        if wall_index == 2:
            dist = 100000
            for i in range(len(neg_x_walls)):
                cur_wall = neg_x_walls[i]
                wall_len = cur_wall.getLength()  
                
                if wall_len > 500 and wall_len < x_max - x_min - 500:
                    if 0 - cur_wall.getStartY() < dist:
                        dist = 0 - cur_wall.getStartY()
                        virtual_len = wall_len  
                        print("cur_virtural_len=", virtual_len, cur_wall)
                        
                door_info = self.analyzeDoorInWall(cur_wall)
                if len(door_info['x']) > 0:
                    if start_align == -1:
                        virtual_len = start_x - MyUtils.getXmaxOfDoorInWall(door_info)
                    else:
                        virtual_len = MyUtils.getXminOfDoorInWall(door_info) - start_x
                        
                    print('cur_virtual_len(door)=', virtual_len, cur_wall)
                        
        if wall_index == 4:
            dist = 100000
            for i in range(len(pos_x_walls)):
                cur_wall = pos_x_walls[i]
                wall_len = cur_wall.getLength()     
                
                if start_align == 1 and x_max - cur_wall.getStartX() > 200 and x_max - cur_wall.getEndX() > 200:
                    continue
                elif start_align == -1 and cur_wall.getStartX() - x_min > 200 and x_min - cur_wall.getEndX() >200:
                    continue
                
                if wall_len > 500 and wall_len < x_max - x_min - 500:
                    if cur_wall.getStartY() < dist:
                        dist = cur_wall.getStartY()
                        virtual_len = wall_len
                        print("cur_virtural_len=", virtual_len, cur_wall)
                        
                door_info = self.analyzeDoorInWall(cur_wall)
                if len(door_info['x']) > 0:
                    if start_align == -1:
                        virtual_len = MyUtils.getXminOfDoorInWall(door_info) - start_x
                    else:
                        virtual_len = start_x - MyUtils.getXmaxOfDoorInWall(door_info)
                        
                    print('cur_virtual_len(door)=', virtual_len, cur_wall)                      
                
                
        return virtual_len
    
    def generateWardrobePointByPrediction(self, bed_free_wall, bed_align):
        wardrobe = 120
        wardrobe_wall, wardrobe_align = self.predictWardrobeAreaByPattern(bed_free_wall, bed_align)
        
        if wardrobe_align == 0:
            return   #暂时不考虑这种场景        
        
        w_x_min = self.shape_xmin
        w_x_max = self.shape_xmax
        w_y_min = self.shape_ymin
        w_y_max = self.shape_ymax
        
        #x_list, y_list = getWallRangeByWallIdex(wardrobe_wall, wall_point_num, wall_pos)
        if wardrobe_align == -1:
            x_list1, y_list1 = self.getWallRangeByWallIdex(MyUtils.getPreWall(wardrobe_wall))
        else:
            x_list1, y_list1 = self.getWallRangeByWallIdex(MyUtils.getPostWall(wardrobe_wall))
        
       
        if len(x_list1) > 0:
            w_x_max = max(x_list1)
            w_x_min = min(x_list1)
            
        if len(y_list1) > 0:
            w_y_max = max(y_list1)
            w_y_min = min(y_list1)
            
        if wardrobe_align == -1 and self.isWallFreeWithAlign(MyUtils.getPreWall(wardrobe_wall), 1) == False:
            return
        
        if wardrobe_align == 1 and self.isWallFreeWithAlign(MyUtils.getPostWall(wardrobe_wall), -1) == False:
            return
            
        #virtual_size = searchVirtualCorner1(wardrobe_wall, wardrobe_align, wall_point_num, wall_pos)  
        virtual_size = 1500
        if wardrobe_wall == 1:
            if wardrobe_align == -1:            
                virtual_size = self.searchVirtualCorner1(wardrobe_wall, wardrobe_align, w_x_max, w_y_max) 
                self.objPosition[wardrobe]['x'].append(w_x_max)
                self.objPosition[wardrobe]['x'].append(w_x_max - 650)            
                self.objPosition[wardrobe]['x'].append(w_x_max - 650)
                self.objPosition[wardrobe]['x'].append(w_x_max)
                
                self.objPosition[wardrobe]['y'].append(w_y_max)
                self.objPosition[wardrobe]['y'].append(w_y_max)            
                self.objPosition[wardrobe]['y'].append(w_y_max - virtual_size)
                self.objPosition[wardrobe]['y'].append(w_y_max - virtual_size)
            elif wardrobe_align == 1:
                virtual_size = self.searchVirtualCorner1(wardrobe_wall, wardrobe_align, w_x_max, w_y_min) 
                self.objPosition[wardrobe]['x'].append(w_x_max)
                self.objPosition[wardrobe]['x'].append(w_x_max - 650)            
                self.objPosition[wardrobe]['x'].append(w_x_max - 650)
                self.objPosition[wardrobe]['x'].append(w_x_max)
                
                self.objPosition[wardrobe]['y'].append(w_y_min)
                self.objPosition[wardrobe]['y'].append(w_y_min)            
                self.objPosition[wardrobe]['y'].append(w_y_min + virtual_size)
                self.objPosition[wardrobe]['y'].append(w_y_min + virtual_size)
                
        
        if wardrobe_wall == 2:
            if wardrobe_align == -1:
                virtual_size = self.searchVirtualCorner1(wardrobe_wall, wardrobe_align, w_x_max, w_y_min) 
                self.objPosition[wardrobe]['x'].append(w_x_max)
                self.objPosition[wardrobe]['x'].append(w_x_max)
                self.objPosition[wardrobe]['x'].append(w_x_max - virtual_size)            
                self.objPosition[wardrobe]['x'].append(w_x_max - virtual_size)
                
                
                self.objPosition[wardrobe]['y'].append(w_y_min)
                self.objPosition[wardrobe]['y'].append(w_y_min + 650)            
                self.objPosition[wardrobe]['y'].append(w_y_min + 650)
                self.objPosition[wardrobe]['y'].append(w_y_min)
            elif wardrobe_align == 1:
                virtual_size = self.searchVirtualCorner1(wardrobe_wall, wardrobe_align, w_x_min, w_y_min) 
                self.objPosition[wardrobe]['x'].append(w_x_min)
                self.objPosition[wardrobe]['x'].append(w_x_min)
                self.objPosition[wardrobe]['x'].append(w_x_min + virtual_size)            
                self.objPosition[wardrobe]['x'].append(w_x_min + virtual_size)
                
                
                self.objPosition[wardrobe]['y'].append(w_y_min)
                self.objPosition[wardrobe]['y'].append(w_y_min + 650)            
                self.objPosition[wardrobe]['y'].append(w_y_min + 650)
                self.objPosition[wardrobe]['y'].append(w_y_min)
                
                
        if wardrobe_wall == 3:
            if wardrobe_align == -1:
                virtual_size = self.searchVirtualCorner1(wardrobe_wall, wardrobe_align, w_x_min, w_y_min) 
                self.objPosition[wardrobe]['x'].append(w_x_min)
                self.objPosition[wardrobe]['x'].append(w_x_min + 650)            
                self.objPosition[wardrobe]['x'].append(w_x_min + 650)
                self.objPosition[wardrobe]['x'].append(w_x_min)
                
                self.objPosition[wardrobe]['y'].append(w_y_min)
                self.objPosition[wardrobe]['y'].append(w_y_min)            
                self.objPosition[wardrobe]['y'].append(w_y_min + virtual_size)
                self.objPosition[wardrobe]['y'].append(w_y_min + virtual_size)
            elif wardrobe_align == 1:
                virtual_size = self.searchVirtualCorner1(wardrobe_wall, wardrobe_align, w_x_min, w_y_max) 
                self.objPosition[wardrobe]['x'].append(w_x_min)
                self.objPosition[wardrobe]['x'].append(w_x_min + 650)            
                self.objPosition[wardrobe]['x'].append(w_x_min + 650)
                self.objPosition[wardrobe]['x'].append(w_x_min)
                
                self.objPosition[wardrobe]['y'].append(w_y_max)
                self.objPosition[wardrobe]['y'].append(w_y_max)            
                self.objPosition[wardrobe]['y'].append(w_y_max - virtual_size)
                self.objPosition[wardrobe]['y'].append(w_y_max - virtual_size)
                
        
        if wardrobe_wall == 4:
            if wardrobe_align == -1:
                virtual_size = self.searchVirtualCorner1(wardrobe_wall, wardrobe_align, w_x_min, w_y_max) 
                self.objPosition[wardrobe]['x'].append(w_x_min)
                self.objPosition[wardrobe]['x'].append(w_x_min)
                self.objPosition[wardrobe]['x'].append(w_x_min + virtual_size)            
                self.objPosition[wardrobe]['x'].append(w_x_min + virtual_size)
                
                
                self.objPosition[wardrobe]['y'].append(w_y_max)
                self.objPosition[wardrobe]['y'].append(w_y_max - 650)            
                self.objPosition[wardrobe]['y'].append(w_y_max - 650)
                self.objPosition[wardrobe]['y'].append(w_y_max)
            elif wardrobe_align == 1:
                virtual_size = self.searchVirtualCorner1(wardrobe_wall, wardrobe_align, w_x_max, w_y_max) 
                self.objPosition[wardrobe]['x'].append(w_x_max)
                self.objPosition[wardrobe]['x'].append(w_x_max)
                self.objPosition[wardrobe]['x'].append(w_x_max - virtual_size)            
                self.objPosition[wardrobe]['x'].append(w_x_max - virtual_size)
                
                
                self.objPosition[wardrobe]['y'].append(w_y_max)
                self.objPosition[wardrobe]['y'].append(w_y_max - 650)            
                self.objPosition[wardrobe]['y'].append(w_y_max - 650)
                self.objPosition[wardrobe]['y'].append(w_y_max)
    
    '''根据贴靠的墙编号和在墙上的相对偏移预测床中心点的位置'''
    def generatePointByPrediction(self):
        free_wall_list, align = self.predictBedAreaByPattern()          
        if len(free_wall_list) > 0:
            self.generateBedPointByPrediction(free_wall_list[0], align)
            self.generateWardrobePointByPrediction(free_wall_list[0], align)
            
            
    def getObjPosition(self):
        return self.objPosition