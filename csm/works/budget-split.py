#! /usr/bin/python
#coding: UTF-8
import copy
'''
Created on 2017年3月31日

@author: zhichaozhou
'''

class Rect(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def rotate(self):
        t = self.w
        self.w = self.h
        self.h = t
    def area(self):
        return self.w * self.h
    def insect(self, r):
        x,x1,y,y1=self.x,self.x+self.w,self.y,self.y+self.h
        rx,rx1,ry,ry1=r.x,r.x+r.w,r.y,r.y+r.h
        return not (rx1 <= x or x1 <= rx or ry1 <= y or y1 <= ry)  
    def inrect(self, r):
        return 0<=r.x and r.x+r.w<=self.w and 0<=r.y and r.y+r.h<=self.h
    def __repr__(self):
        return "%d_%d-%dx%d"%(self.x,self.y,self.w,self.h)
    
class Board(Rect):
    def __init__(self, w, h):
        self.x = self.y = 0
        self.w = w
        self.h = h
    def put(self, b):
        r = Rect(0, 0, b.w, b.h)
        if (b.w <= self.w and b.h <= self.h):
            if self.search(r):
                self.setrect(r)
                return True
        if (b.w <= self.h and b.h <= self.w):
            r.x=r.y= 0
            r.rotate()
            if self.search(r):
                self.setrect(r)
                return True
        return False
    def search(self,r): 
        self.mapp=[]
        for i in xrange(self.w): 
            self.mapp.append([0 for _ in xrange(self.h)])    
        if self.putted:
            oldpos=[(r.x,r.y)]
            while len(oldpos):                
                r.x,r.y=oldpos[0]
                oldpos=oldpos[1:]                
                if self.mapp[r.x][r.y]:continue
                self.visit(r)
                cr = filter(lambda x:x.insect(r), self.putted)
                
                if cr:
                    rr = cr[0]
                    x,y = r.x,r.y
                    r.x,r.y=rr.x+rr.w,y
                    if self.inrect(r):oldpos.append((r.x,r.y))
                    r.x,r.y = x,rr.y+rr.h
                    if self.inrect(r):oldpos.append((r.x,r.y))
                else:
                    return self.inrect(r)
            return False
        else:
            return True
    def visit(self, r):
        for x in xrange(r.x, r.x+r.w):
            for y in xrange(r.y, r.y+r.h):
                if x < self.w and y < self.h:
                    self.mapp[x][y] = 1
    def setrect(self, r):
        self.putted.append(r)
    def split(self, arr):
        add, self.putted = True, []
        while add:
            add = False
            for n in arr:
                while n[1]>0 and self.put(n[0]):
                    add = True
                    n[1] -= 1
        del self.mapp


srcArr = [[Board(55,45),160],[Board(45,30),150],[Board(50,30),300]]
sumarea = reduce(lambda x,y:x+(y[0]).area()*y[1],[0]+srcArr)      
best, num = None, 1    
while num:
    result=[]
    arr=copy.deepcopy(srcArr)
    cnt=reduce(lambda x,y:x+y[1],[0]+arr)
    while cnt:
        b=Board(110,240)
        b.split(arr)
        cnt=reduce(lambda x,y:x+y[1],[0]+arr)
        result.append(b.putted)
    if best == None or len(best) > len(result):
        best = result
        area = len(best)*b.area()#est[0].area()
        print float(sumarea) / area
    num -= 1
    
for b in best:
    print b
print len(best)