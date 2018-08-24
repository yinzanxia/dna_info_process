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
            
        print('RoomShape init: x_min,x_max, y_min,y_max ', x_min, x_max, y_min, y_max)
            
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
            
        print('RoomWall init: x_min,x_max, y_min,y_max ', x_min, x_max, y_min, y_max)
        
        
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
        window_flag = (obj_type == 2)
    
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
                if window_flag:
                    side = MyUtils.getWindowSideOrder(center_x, center_y, self.wall_xmin, self.wall_xmax, self.wall_ymin, self.wall_ymax)
                else:
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
                if window_flag:
                    side = MyUtils.getWindowSideOrder(center_x, center_y, self.wall_xmin, self.wall_xmax, self.wall_ymin, self.wall_ymax)
                else:
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
        
        print('RoomPattern init:', self.pattern)
        
        
        
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
                        
        if len(new_free_wall) > 1:
            for ikey, ivalue in self.pattern.items():
                if ikey != 0:
                    if 2 in ivalue:  
                        pre_wall = MyUtils.getPreWall(ikey)   
                        post_wall = MyUtils.getPostWall(ikey) 
                        tmp = []
                        if pre_wall in new_free_wall:
                            tmp.append(pre_wall)
                            return tmp
                        elif post_wall in new_free_wall:
                            tmp.append(post_wall)
                            return tmp                       
                        
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

    def groupWalls(self, point):
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
                if cur_y > point.getY():
                    positive_x_walls.append(cur_wall)
                else:
                    negative_x_walls.append(cur_wall)
                
            if cur_wall.getDirection() == 1:            
                if cur_x > point.getX():
                    positive_y_walls.append(cur_wall)
                else:
                    negative_y_walls.append(cur_wall)
        
        self.connectWalls(positive_x_walls, 0)
        self.connectWalls(negative_x_walls, 0)
        self.connectWalls(positive_y_walls, 1)
        self.connectWalls(negative_y_walls, 1)
        return positive_x_walls, negative_x_walls, positive_y_walls, negative_y_walls
    
    def checkConnectXWalls(self, walls):
        num = len(walls)
        tmp = []
        for i in range(num-1):
                wall1 = walls[i]
                for j in range(i+1, num):
                    wall2 = walls[j]
                    if wall1.canConnect(wall2):
                        y = wall1.getStartY()
                        xmin = min(wall1.getMinX(), wall2.getMinX())
                        xmax = max(wall1.getMaxX(), wall2.getMaxX())
                        newWall = MyWall.LinearWall(MyPoint.Point(xmin,y), MyPoint.Point(xmax,y))
                        tmp.append(wall1)
                        tmp.append(wall2)
                        tmp.append(newWall)
                        return tmp
        return tmp
    
    def checkConnectYWalls(self, walls):
        num = len(walls)
        tmp = []
        for i in range(num-1):
                wall1 = walls[i]
                for j in range(i+1, num):
                    wall2 = walls[j]
                    if wall1.canConnect(wall2):
                        x = wall1.getStartX()
                        ymin = min(wall1.getMinY(), wall2.getMinY())
                        ymax = max(wall1.getMaxY(), wall2.getMaxY())
                        newWall = MyWall.LinearWall(MyPoint.Point(x,ymin), MyPoint.Point(x,ymax))
                        tmp.append(wall1)
                        tmp.append(wall2)
                        tmp.append(newWall)
                        print('-------------------------\n')
                        wall1.showDetail()
                        wall2.showDetail()
                        newWall.showDetail()
                        print('-------------------------\n')
                        return tmp
        return tmp
        
    def connectWalls(self, walls, direction): 
        for i in range(len(walls)):
            walls[i].showDetail()
        if direction == 0:
            result = self.checkConnectXWalls(walls)
            while len(result) != 0:
                walls.remove(result[0])
                walls.remove(result[1])
                walls.append(result[2])
                result = self.checkConnectXWalls(walls)
        elif direction == 1:
            result = self.checkConnectYWalls(walls)
            while len(result) != 0:
                walls.remove(result[0])
                walls.remove(result[1])
                walls.append(result[2])
                result = self.checkConnectYWalls(walls)
                        
                
    
    
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
    
    def analyzeWindowInWall(self, wall):    
        door_range = {}
        door_range['x'] = []
        door_range['y'] = []
        
        if wall.getDirection() == 0:
            for i in range(self.window_num):
                door_x = self.window_pos['x'][i]
                door_y = self.window_pos['y'][i] 
                x_min, x_max, y_min, y_max = MyUtils.getListLimit(len(door_x), door_x, door_y)                
                               
                if abs(y_min - wall.getStartY()) < 100 or abs(y_max - wall.getStartY()) < 100:            
                    tmp = [x_min, x_max]
                    door_range['x'].append(tmp)
                
            
        if wall.getDirection() == 1:
            for i in range(self.window_num):
                door_x = self.window_pos['x'][i]
                door_y = self.window_pos['y'][i] 
                x_min, x_max, y_min, y_max = MyUtils.getListLimit(len(door_x), door_x, door_y)  
                
                if abs(x_min - wall.getStartX()) < 100 or abs(x_max - wall.getStartX()) < 100:
                    tmp = [y_min, y_max]
                    door_range['y'].append(tmp)       
                
        return door_range
    
    '''判断墙是否是边界上的墙，方向和长度, 不考虑到边界的距离，因为边墙有时是分隔墙'''
    def isBoundWall(self, wall) :        
        if wall.getDirection() == 0 and self.wall_dx -  wall.getLength() < 500:
            return True
        elif wall.getDirection() == 1 and self.wall_dy -  wall.getLength() < 500:
            return True  
        
        return False
        
    def isYWallFarFromBottom(self, cur_wall):
        if cur_wall.getStartY() - self.wall_ymin > 200 and  cur_wall.getEndY() -self.wall_ymin  >200:
            return True
        else:
            return False
            
            
    def isYWallFarFromTop(self, cur_wall):
        if self.wall_ymax - cur_wall.getStartY() > 200 and self.wall_ymax - cur_wall.getEndY() > 200:
            return True
        else:
            return False
    
    def searchInPositiveYWalls(self, pos_y_walls, start_align, start_y):
        dist = 100000   
        wall_flag = False
        door_flag = False
        virtual_len = 1500
        len1 = virtual_len
        len2 = virtual_len
        for i in range(len(pos_y_walls)):
            cur_wall = pos_y_walls[i]  
            cur_wall.showDetail()
            wall_len = cur_wall.getLength()
            
            if start_align == -1 and self.isYWallFarFromTop(cur_wall):
                continue
            elif start_align == 1 and self.isYWallFarFromBottom(cur_wall):
                continue            
            
            '''找距离中心最近的非边界墙的长度'''
            if wall_len > 500 and self.isBoundWall(cur_wall) == False:
                if cur_wall.getStartX() < dist:
                    dist = cur_wall.getStartX()                        
                    wall_flag = True
                    len1 = wall_len
                    print("cur_virtural_len=", len1, cur_wall.getStartX(), cur_wall.getStartY(), cur_wall.getEndX(), cur_wall.getEndY())   
                    
            door_info = self.analyzeDoorInWall(cur_wall)
            if len(door_info['y']) > 0:
                door_flag = True
                if start_align == -1:
                    len2 = start_y - MyUtils.getYmaxOfDoorInWall(door_info)
                else:
                    len2 = MyUtils.getYminOfDoorInWall(door_info) - start_y                    
                print('cur_virtual_len(door)=', len2, cur_wall.getStartX(), cur_wall.getStartY(), cur_wall.getEndX(), cur_wall.getEndY())
                
            
        if wall_flag and door_flag:
            virtual_len = min(len1, len2)                
        elif wall_flag and door_flag == False:
            virtual_len = len1
        elif wall_flag == False and door_flag:
            virtual_len = len2
            
        return virtual_len
                
   
    def searchInNegativeYWalls(self, neg_y_walls, start_align, start_y):
        dist = 100000
        wall_flag = False
        door_flag = False
        virtual_len = 1500
        len1 = len2 = virtual_len
        for i in range(len(neg_y_walls)):
            cur_wall = neg_y_walls[i]
            cur_wall.showDetail()
            wall_len = cur_wall.getLength()  
            
            if start_align == -1 and self.isYWallFarFromBottom(cur_wall):
                continue
            if start_align == 1 and self.isYWallFarFromTop(cur_wall):
                continue
                       
            if  wall_len > 500 and self.isBoundWall(cur_wall) == False:
                if 0 - cur_wall.getStartX() < dist:
                    dist = 0 - cur_wall.getStartX()
                    wall_flag = True
                    len1 = wall_len                            
                    print("cur_virtural_len=", len1, cur_wall.getStartX(), cur_wall.getStartY(), cur_wall.getEndX(), cur_wall.getEndY())
            
            
            door_info = self.analyzeDoorInWall(cur_wall)
            if len(door_info['y']) > 0:
                door_flag = True
                if start_align == -1:
                    len2 = MyUtils.getYminOfDoorInWall(door_info) - start_y
                else:
                    len2 = start_y - MyUtils.getYmaxOfDoorInWall(door_info)
                    
                print('cur_virtual_len(door)=', len2 , cur_wall.getStartX(), cur_wall.getStartY(), cur_wall.getEndX(), cur_wall.getEndY())
                
        if wall_flag and door_flag:
            virtual_len = min(len1, len2)                
        elif wall_flag and door_flag == False:
            virtual_len = len1
        elif wall_flag == False and door_flag:
            virtual_len = len2
            
        return virtual_len
    
    
    def isXWallFarFromLeft(self, cur_wall):
        if cur_wall.getStartX() - self.wall_xmin > 200 and cur_wall.getEndX()- self.wall_xmin >200:
            return True
        else:
            return False
            
            
    def isXWallFarFromRight(self, cur_wall):
        if self.wall_xmax - cur_wall.getStartX() > 200 and self.wall_xmax - cur_wall.getEndX() > 200:
            return True
        else:
            return False
    
    def searchInPositiveXWalls(self, pos_x_walls, start_align, start_x):
        dist = 100000
        wall_flag = False
        door_flag = False
        virtual_len = 1500
        len1 = len2 = virtual_len
        for i in range(len(pos_x_walls)):
            cur_wall = pos_x_walls[i]
            wall_len = cur_wall.getLength()     
            
            if start_align == 1 and self.isXWallFarFromRight(cur_wall):
                continue
            elif start_align == -1 and self.isXWallFarFromLeft(cur_wall):
                continue
            
            if wall_len > 500 and self.isBoundWall(cur_wall) == False:
                if cur_wall.getStartY() < dist:
                    dist = cur_wall.getStartY()
                    len1 = wall_len
                    wall_flag = True
                    print("cur_virtural_len=", len1, cur_wall.getStartX(), cur_wall.getStartY(), cur_wall.getEndX(), cur_wall.getEndY())
                    
            door_info = self.analyzeDoorInWall(cur_wall)
            if len(door_info['x']) > 0:
                door_flag = True
                if start_align == -1:
                    len2 = MyUtils.getXminOfDoorInWall(door_info) - start_x
                else:
                    len2 = start_x - MyUtils.getXmaxOfDoorInWall(door_info)
                    
                print('cur_virtual_len(door)=', len2 , cur_wall.getStartX(), cur_wall.getStartY(), cur_wall.getEndX(), cur_wall.getEndY())  
                
        if wall_flag and door_flag:
            virtual_len = min(len1, len2)                
        elif wall_flag and door_flag == False:
            virtual_len = len1
        elif wall_flag == False and door_flag:
            virtual_len = len2
        
        return virtual_len
        
    def searchInNegativeXWalls(self, neg_x_walls, start_align, start_x):
        dist = 100000
        wall_flag = False
        door_flag = False
        virtual_len = 1500
        len1 = len2 = virtual_len
        for i in range(len(neg_x_walls)):
            cur_wall = neg_x_walls[i]
            wall_len = cur_wall.getLength()  
            
            if start_align == 1 and self.isXWallFarFromLeft(cur_wall):
                continue
            elif start_align == -1 and self.isXWallFarFromRight(cur_wall):
                continue
            
            if wall_len > 500 and self.isBoundWall(cur_wall) == False:
                if 0 - cur_wall.getStartY() < dist:
                    dist = 0 - cur_wall.getStartY()
                    len1 = wall_len 
                    wall_flag = True
                    print("cur_virtural_len=", len1, cur_wall.getStartX(), cur_wall.getStartY(), cur_wall.getEndX(), cur_wall.getEndY())
                    
            door_info = self.analyzeDoorInWall(cur_wall)
            if len(door_info['x']) > 0:
                door_flag = True
                if start_align == -1:
                    len2 = start_x - MyUtils.getXmaxOfDoorInWall(door_info)
                else:
                    len2 = MyUtils.getXminOfDoorInWall(door_info) - start_x
                    
                print('cur_virtual_len(door)=', len2 , cur_wall.getStartX(), cur_wall.getStartY(), cur_wall.getEndX(), cur_wall.getEndY())
                
        if wall_flag and door_flag:
            virtual_len = min(len1, len2)                
        elif wall_flag and door_flag == False:
            virtual_len = len1
        elif wall_flag == False and door_flag:
            virtual_len = len2
            
        return virtual_len
                     
    '''沿衣柜背靠的墙搜索衣柜的长度，最长不超过1500, 同方向既有wall长度限制，又有door边框限制时，以更靠近的为准'''
    def searchVirtualCorner1(self, wall_index, start_align, start_x, start_y):        
        zero_point = MyPoint.Point(0, 0)
        pos_x_walls, neg_x_walls, pos_y_walls, neg_y_walls = self.groupWalls(zero_point)
        virtual_len = 1500
        
        if wall_index == 1:
            virtual_len = self.searchInPositiveYWalls(pos_y_walls, start_align, start_y)  
        elif wall_index == 3:
            virtual_len = self.searchInNegativeYWalls(neg_y_walls, start_align, start_y)                        
        elif wall_index == 2:
            virtual_len = self.searchInNegativeXWalls(neg_x_walls, start_align, start_x)                        
        elif wall_index == 4:
            virtual_len = self.searchInPositiveXWalls(pos_x_walls, start_align, start_x)  
                
        return virtual_len
    
    def searchAreaFromPoint(self, startPoint):
        pos_x_walls, neg_x_walls, pos_y_walls, neg_y_walls = self.groupWalls(startPoint)
        return
    
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
    

    
    def growToXMin(self, center_point):
        tmp_x = self.wall_xmin
        wall_len = 0
        for i in range(self.wall_point_num-1):
            cur_x = self.wall_pos['x'][i]
            cur_y = self.wall_pos['y'][i]
            next_x = self.wall_pos['x'][i+1]
            next_y = self.wall_pos['y'][i+1]   
            
            wall = MyWall.LinearWall(MyPoint.Point(cur_x, cur_y), MyPoint.Point(next_x, next_y))
            
            if wall.isYWall() == False:
                continue   
           
            if wall.isHorizontalLeftOfPoint(center_point):  #平行与Y轴且在点与边界之间
                if tmp_x < wall.getMaxX():
                    tmp_x = wall.getMaxX()
                    wall_len = wall.getLength()
                    
        return tmp_x, wall_len
    
    def growToXMin1(self, center_point, neg_y_walls):
        tmp_x = self.wall_xmin
        #wall_len = 0
        wall_index = -1
        for i in range(len(neg_y_walls)):             
            cur_wall = neg_y_walls[i]             
            if cur_wall.isYWall() == False:
                continue   
           
            if cur_wall.isHorizontalLeftOfPoint(center_point):  #平行与Y轴且在点与边界之间
                if tmp_x < cur_wall.getMaxX():
                    tmp_x = cur_wall.getMaxX()
                    #wall_len = cur_wall.getLength()
                    wall_index = i
        if wall_index != -1:            
            return tmp_x, neg_y_walls[wall_index]
        else:
            return -1, neg_y_walls[0]
    

    def growToXMax(self, center_point):
        tmp_x = self.wall_xmax
        wall_len = 0
        for i in range(self.wall_point_num-1):
            cur_x = self.wall_pos['x'][i]
            cur_y = self.wall_pos['y'][i]
            next_x = self.wall_pos['x'][i+1]
            next_y = self.wall_pos['y'][i+1]   
            
            wall = MyWall.LinearWall(MyPoint.Point(cur_x, cur_y), MyPoint.Point(next_x, next_y))
            
            if wall.isYWall() == False:
                continue
                       
            if wall.isHorizontalRightOfPoint(center_point):  #平行与Y轴且在点与边界之间
                if tmp_x > wall.getMinX():
                    tmp_x = wall.getMinX()
                    wall_len = wall.getLength()
                    
        return tmp_x, wall_len
    
    def growToXMax1(self, center_point, pos_y_walls):
        tmp_x = self.wall_xmax
        #wall_len = 0
        wall_index = -1
        for i in range(len(pos_y_walls)):
            cur_wall = pos_y_walls[i]             
            if cur_wall.isYWall() == False:
                continue
                       
            if cur_wall.isHorizontalRightOfPoint(center_point):  #平行与Y轴且在点与边界之间
                if tmp_x > cur_wall.getMinX():
                    tmp_x = cur_wall.getMinX()
                    #wall_len = cur_wall.getLength()
                    wall_index = i
                    
        if wall_index != -1:            
            return tmp_x, pos_y_walls[wall_index]
        else:
            return -1, pos_y_walls[0]
    

    def growToYMin(self, center_point):
        tmp_y = self.wall_ymin
        wall_len = 0
        for i in range(self.wall_point_num-1):
            cur_x = self.wall_pos['x'][i]
            cur_y = self.wall_pos['y'][i]
            next_x = self.wall_pos['x'][i+1]
            next_y = self.wall_pos['y'][i+1]
            
            wall = MyWall.LinearWall(MyPoint.Point(cur_x, cur_y), MyPoint.Point(next_x, next_y))
            
            if wall.isXWall() == False:
                continue
                       
            if wall.isVerticalLowerOfPoint(center_point):  #平行与X轴且在点与边界之间
                if tmp_y < wall.getMaxY():
                    tmp_y = wall.getMaxY()
                    wall_len = wall.getLength()
        return tmp_y, wall_len
    
    def growToYMin1(self, center_point, neg_x_walls):
        tmp_y = self.wall_ymin
        #wall_len = 0
        wall_index = -1
        for i in range(len(neg_x_walls)):   
            wall = neg_x_walls[i]            
            if wall.isXWall() == False:
                continue
                       
            if wall.isVerticalLowerOfPoint(center_point):  #平行与X轴且在点与边界之间
                if tmp_y < wall.getMaxY():
                    tmp_y = wall.getMaxY()
                    #wall_len = wall.getLength()
                    wall_index = i;
        if wall_index != -1:
            return tmp_y, neg_x_walls[wall_index]
        else:
            return -1, neg_x_walls[0]

    def growToYMax(self, center_point):
        tmp_y = self.wall_ymax
        wall_len = 0
        for i in range(self.wall_point_num-1):
            cur_x = self.wall_pos['x'][i]
            cur_y = self.wall_pos['y'][i]
            next_x = self.wall_pos['x'][i+1]
            next_y = self.wall_pos['y'][i+1]
            
            wall = MyWall.LinearWall(MyPoint.Point(cur_x, cur_y), MyPoint.Point(next_x, next_y))
            
            if wall.isXWall() == False:
                continue
            
            if wall.isVerticalHigherOfPoint(center_point):  #平行与Y轴且在点与边界之间
                if tmp_y > wall.getMinY():
                    tmp_y =  wall.getMinY()
                    wall_len = wall.getLength()
                    
        return tmp_y, wall_len
    
    def growToYMax1(self, center_point, pos_x_walls):
        tmp_y = self.wall_ymax
        #wall_len = 0
        wall_index = -1
        for i in range(len(pos_x_walls)): 
            wall = pos_x_walls[i]            
            if wall.isXWall() == False:
                continue
            
            if wall.isVerticalHigherOfPoint(center_point):  #平行与Y轴且在点与边界之间
                if tmp_y > wall.getMinY():
                    tmp_y =  wall.getMinY()
                    #wall_len = wall.getLength()
                    wall_index = i
                    
        if wall_index != -1:
            return tmp_y, pos_x_walls[wall_index]
        else:
            return -1, pos_x_walls[0]
        
    def checkYWallDoorWindow(self, center_x, center_y, right_wall):
        door_range_info = self.analyzeDoorInWall(right_wall)
        window_range_info = self.analyzeWindowInWall(right_wall)
        right_y_min = right_wall.getMinY()
        right_y_max = right_wall.getMaxY()
        if len(door_range_info['y']) > 0:
            y_min1, y_max1 = MyUtils.getGrowLimitWithDoorOrWindowInWall(center_x, center_y, door_range_info, 1, right_wall.getMinY(), right_wall.getMaxY())
            if y_min1 == -1 and y_max1 == -1:
                return -1, -1
            right_y_min = max(y_min1, right_y_min)
            right_y_max = min(y_max1, right_y_max)
        if len(window_range_info['y']) > 0:
            y_min2, y_max2 = MyUtils.getGrowLimitWithDoorOrWindowInWall(center_x, center_y, window_range_info, 1, right_wall.getMinY(), right_wall.getMaxY())
            if y_min2 == -1 and y_max2 == -1:
                return -1, -1
            right_y_min = max(y_min2, right_y_min)
            right_y_max = min(y_max2, right_y_max)
            
        
        return right_y_min, right_y_max
    
    def checkXWallDoorWindow(self, center_x, center_y, top_wall):
        door_range_info = self.analyzeDoorInWall(top_wall)
        window_range_info = self.analyzeWindowInWall(top_wall)
        top_x_min = top_wall.getMinX()
        top_x_max = top_wall.getMaxX()
        if len(door_range_info['x']) > 0:
            x_min1, x_max1 = MyUtils.getGrowLimitWithDoorOrWindowInWall(center_x, center_y, door_range_info, 0, top_wall.getMinX(), top_wall.getMaxX())
            if x_min1 == -1 and x_max1 == -1:
                return -1, -1
            top_x_min = max(x_min1, top_x_min)
            top_x_max = min(x_max1, top_x_max)
        if len(window_range_info['x']) > 0:
            x_min2, x_max2 = MyUtils.getGrowLimitWithDoorOrWindowInWall(center_x, center_y, window_range_info, 0, top_wall.getMinX(), top_wall.getMaxX())
            if x_min2 == -1 and x_max2 == -1:
                return -1, -1
            top_x_min = max(x_min2, top_x_min)
            top_x_max = min(x_max2, top_x_max)
            
        return top_x_min, top_x_max
    
    def rectGrow(self, center_x, center_y, wall_index):
        left = right = center_x
        top = bottom = center_y
        
        startPoint = MyPoint.Point(center_x, center_y)
        
        '''优先向某个方向生长应该检查距离最近的墙的距离而非边界墙的距离'''
        '''
        if center_x - self.wall_xmin < self.wall_xmax - center_x:
            #优先向x_min方向生长 
            left, wall_len = self.growToXMin(startPoint)        
        else:
            #优先向x_max方向生长        
            right, wall_len = self.growToXMax(startPoint)
        
        if center_y - self.wall_ymin < self.wall_ymax - center_y:
            #优先向y_min方向生长        
            bottom, wall_len1 = self.growToYMin(startPoint)
        else:
            #优先向y_max方向生长        
            top, wall_len = self.growToYMax(startPoint)
        '''    
        '''以上完成两个方向上距离墙的搜索''' 
        '''
        left, left_wall_len = self.growToXMin(startPoint) 
        right, right_wall_len = self.growToXMax(startPoint)
        bottom, bottom_wall_len = self.growToYMin(startPoint)
        top, top_wall_len = self.growToYMax(startPoint)    
        '''
        
        pos_x_walls, neg_x_walls, pos_y_walls, neg_y_walls = self.groupWalls(MyPoint.Point(center_x, center_y))
        print("Pos_x_walls:")
        for i in range(len(pos_x_walls)):
            pos_x_walls[i].showDetail()
         
        print("Neg_x_walls:")
        for i in range(len(neg_x_walls)):
            neg_x_walls[i].showDetail()
            
        print("Pos_y_walls:")
        for i in range(len(pos_y_walls)):
            pos_y_walls[i].showDetail()
            
        print("Neg_y_walls:")
        for i in range(len(neg_y_walls)):
            neg_y_walls[i].showDetail()
            
        left_wall_lst = []
        right_wall_lst = []
        top_wall_lst = []
        bottom_wall_lst = []
        
        bottom = self.wall_ymin
        top = self.wall_ymax
        left = self.wall_xmin
        right = self.wall_xmax
        
        if len(neg_y_walls) > 0:
            left, left_wall = self.growToXMin1(startPoint, neg_y_walls) 
            left_wall_lst.append(left_wall)
        else:
            left = self.wall_xmin
        
        if len(pos_y_walls) > 0:
            right, right_wall = self.growToXMax1(startPoint, pos_y_walls)
            right_wall_lst.append(right_wall)
        else:
            right = self.wall_xmax
        
        if len(neg_x_walls) > 0:
            bottom, bottom_wall = self.growToYMin1(startPoint, neg_x_walls)
            bottom_wall_lst.append(bottom_wall)
        else:
            bottom = self.wall_ymin
        if len(pos_x_walls) > 0:
            top, top_wall = self.growToYMax1(startPoint, pos_x_walls) 
            top_wall_lst.append(top_wall)
        else:
            top = self.wall_ymax

        if wall_index == 1:
            if len(right_wall_lst) > 0:
                bottom, top = self.checkYWallDoorWindow(center_x, center_y, right_wall_lst[0])
            elif len(left_wall_lst) > 0:
                bottom, top = self.checkYWallDoorWindow(center_x, center_y, left_wall_lst[0])           
                
            
            if abs(top - top_wall.getMinY()) < 100 and len(top_wall_lst)>0:
                top_x_min, top_x_max = self.checkXWallDoorWindow(center_x, center_y, top_wall_lst[0])
                left = max(top_x_min, left)
                right = min(top_x_max, right)
                
            if abs(bottom - bottom_wall.getMaxY()) < 100 and len(bottom_wall_lst)>0:
                bottom_x_min, bottom_x_max = self.checkXWallDoorWindow(center_x, center_y, bottom_wall_lst[0])
                left = max(bottom_x_min, left)
                right = min(bottom_x_max, right)
            
        elif wall_index == 2:
            if len(bottom_wall_lst)>0:
                left, right = self.checkXWallDoorWindow(center_x, center_y, bottom_wall_lst[0])   
            elif len(top_wall_lst)>0:
                left, right = self.checkXWallDoorWindow(center_x, center_y, top_wall_lst[0])   
            
            if abs(left -left_wall.getMaxX()) < 100 and len(left_wall_lst)>0:
                left_y_min, left_y_max = self.checkYWallDoorWindow(center_x, center_y, left_wall_lst[0])
                top = min(left_y_max, top)
                bottom = max(left_y_min, bottom)
            if abs(right - right_wall.getMinX()) < 100 and len(right_wall_lst)>0:
                right_y_min, right_y_max = self.checkYWallDoorWindow(center_x, center_y, right_wall_lst[0])
                top = min(top, right_y_max)
                bottom = max(bottom, right_y_min)
            
        elif wall_index == 3:
            if len(left_wall_lst)>0:
                bottom, top = self.checkYWallDoorWindow(center_x, center_y, left_wall_lst[0])
            elif len(right_wall_lst)>0:
                bottom, top = self.checkYWallDoorWindow(center_x, center_y, right_wall_lst[0])
            
            
            if abs(top - top_wall.getMinY()) < 100 and len(top_wall_lst)>0:
                top_x_min, top_x_max = self.checkXWallDoorWindow(center_x, center_y, top_wall_lst[0])
                left = max(top_x_min, left)
                right = min(top_x_max, right)
                
            if abs(bottom - bottom_wall.getMaxY()) < 100 and len(bottom_wall_lst)>0:
                bottom_x_min, bottom_x_max = self.checkXWallDoorWindow(center_x, center_y, bottom_wall_lst[0])
                left = max(bottom_x_min, left)
                right = min(bottom_x_max, right) 
                
        elif wall_index == 4:
            if len(top_wall_lst) > 0:
                left, right = self.checkXWallDoorWindow(center_x, center_y, top_wall_lst[0])
            elif len(bottom_wall_lst) > 0:
                left, right = self.checkXWallDoorWindow(center_x, center_y, bottom_wall_lst[0])
            
            if abs(left -left_wall.getMaxX()) < 100 and len(left_wall_lst) > 0:
                left_y_min, left_y_max = self.checkYWallDoorWindow(center_x, center_y, left_wall_lst[0])
                top = min(left_y_max, top)
                bottom = max(left_y_min, bottom)
            if abs(right - right_wall.getMinX()) < 100 and len(right_wall_lst) > 0:
                right_y_min, right_y_max = self.checkYWallDoorWindow(center_x, center_y, right_wall_lst[0])
                top = min(top, right_y_max)
                bottom = max(bottom, right_y_min)
                
        return left, right, top, bottom
        
        
