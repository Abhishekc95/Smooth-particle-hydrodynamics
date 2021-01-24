import math as ma
import random
import pygame

blue = (0,0,255)

class rectangle:

    def __init__(self,cx,cy,w,h):
        self.cx = cx 
        self.cy = cy
        self.w = w
        self.h = h

    def contains (self,p):
        x = self.cx
        y = self.cy
        w = self.w
        h = self.h
        contain = False
        
        if ((p.pos[0] >= x-w/2 )and (p.pos[0] <= x+ w/2 ) and (p.pos[1] >= y-h/2) and (p.pos[1] <= y+h/2)):
            contain = True
        return contain
    
    """
    def intersects(self,c_range):
       
        x1 = self.cx - self.w/2
        y1 = self.cy - self.h/2
        x2 = self.cx + self.w/2
        y2 = self.cy + self.h/2

        xn = max(x1,min(c_range.cx,x2))
        yn = max(y1,min(c_range.cy,y2))

        dx = xn - c_range.cx
        dy = yn - c_range.cy

        return dx**2 + dy**2 < c_range.rsq 
    """

        

    
class circle: 

    def __init__(self,cx,cy,r):
        self.cx = cx 
        self.cy = cy
        self.r = r
        self.rsq = self.r*self.r

    def intersects(self,box):
       
        x1 = box.cx - box.w/2
        y1 = box.cy - box.h/2
        x2 = box.cx + box.w/2
        y2 = box.cy + box.h/2

        xn = max(x1,min(self.cx,x2))
        yn = max(y1,min(self.cy,y2))

        dx = xn - self.cx
        dy = yn - self.cy

        return ma.sqrt(dx**2 + dy**2) < self.r 

    def contains (self,p):
        dx = self.cx - p.pos[0]
        dy = self.cy - p.pos[1]
        contain = False
        
        if (ma.sqrt(dx**2 + dy**2) <= self.r):
            contain = True
        return contain

  





class quadTree:

    def __init__(self,box,capacity):
        self.box = box
        self.capacity = capacity
        self.divided = False
        self.points  = []

    def subdivide(self):
        cx = self.box.cx
        cy = self.box.cy
        w = self.box.w
        h = self.box.h

        self.ne = quadTree (rectangle(cx + w/4, cy - h/4, w/2 , h/2 ),self.capacity)
        self.nw = quadTree (rectangle(cx - w/4, cy - h/4, w/2 , h/2 ),self.capacity)
        self.se = quadTree (rectangle(cx + w/4, cy + h/4, w/2 , h/2 ),self.capacity)
        self.sw = quadTree (rectangle(cx - w/4, cy + h/4, w/2 , h/2 ),self.capacity)

        self.divided = True

    def insert (self,p):

        if (self.box.contains(p)) == False:
            return False

        if ( len(self.points) <= self.capacity):
            self.points.append(p)
            return True

        if self.divided == False:
            self.subdivide()
        
        return (self.ne.insert(p) or self.nw.insert(p) or self.se.insert(p) or self.sw.insert(p)) 

    def display(self,win):
        w = self.box.w
        h = self.box.h
        pygame.draw.rect(win,blue,(self.box.cx - w/2,self.box.cy - h/2 , w, h),1)
        
        if self.divided:
            self.ne.display(win)
            self.nw.display(win)
            self.se.display(win)
            self.sw.display(win)


    def nns(self,c_range,found):          # nearest radius search
        
        if not (c_range.intersects(self.box)):
            return False
        
        for p in self.points:
            if c_range.contains(p):
                found.append(p)

        if self.divided:
            self.ne.nns(c_range,found)
            self.nw.nns(c_range,found)
            self.se.nns(c_range,found)
            self.sw.nns(c_range,found)

        return found    

    def __del__(self):
        if self.divided:
            del self.ne
            del self.nw
            del self.se
            del self.sw
        