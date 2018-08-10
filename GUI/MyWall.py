# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 20:30:33 2018

@author: mayn
"""

import MyPoint

class LinearWall:
    def __init__(self, p1, p2):
        self.startPoint = MyPoint.Point(p1.x, p1.y)
        self.endPoint = MyPoint.Point(p2.x, p2.y)
        if self.isXWall():
            self.direction = 0
        elif self.isYWall():
            self.direction = 1
        else:
            self.direction = -1
        
        
    def isXWall(self):
        if abs(self.startPoint.getY() - self.endPoint.getY()) < 50 and abs(self.startPoint.getX() - self.endPoint.getX()) > 200:
            return True
        else:
            return False
        
    def isYWall(self):
        if abs(self.startPoint.getY() - self.endPoint.getY()) > 200 and abs(self.startPoint.getX() - self.endPoint.getX()) <50:
            return True
        else:
            return False
        
    def getDirection(self):
        return self.direction
    
    def getLength(self):
        dx = abs(self.startPoint.getX() - self.endPoint.getX())
        dy = abs(self.startPoint.getY() - self.endPoint.getY())
        if dx > dy:
            return dx
        else:
            return dy
        
    
    def getStartX(self):
        return self.startPoint.getX()
    
    def getStartY(self):
        return self.startPoint.getY()
    
    def getEndX(self):
        return self.endPoint.getX()
    
    def getEndY(self):
        return self.endPoint.getY()
    
    def getMaxX(self):
        return max(self.startPoint.getX(), self.endPoint.getX())
    
    def getMinX(self):
        return min(self.startPoint.getX(), self.endPoint.getX())
    
    def getMaxY(self):
        return max(self.startPoint.getY(), self.endPoint.getY())
    
    def getMinY(self):
        return min(self.startPoint.getY(), self.endPoint.getY())
    
    