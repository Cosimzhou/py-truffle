#! /usr/bin/python
# -*- coding: UTF-8 -*-
from pygame.locals import *
from sys import exit
from time import time

import pygame as PYG 

from csm.tools.furniture.geo import Vector, Contour, Adaptor, Point
 

class Application(Adaptor):
    def __init__(self, w, h):
        Adaptor.__init__(self, w, h)
        self.content = []
        self.buff = []
        self.dragStaff = None
        self.rulerPoint = None
        self.buffIdx = 0
        self.contentIdx = -1
        self.contentIdxLocked = False
        
        # xxxxxxx
        PYG.init()
        self.font = PYG.font.Font(None, 20)
        self.screen = PYG.display.set_mode(self.size(), 0, 32) 
        self.screen.fill(0xffffff00)
        
    def draw(self):
        self.screen.fill(0xffffff00)
        PYG.draw.lines(self.screen, 0, True, self.points(), 1)
        n = 0
        for c in self.content: 
            if type(c) is list: 
                PYG.draw.lines(self.screen, 0xff00 if n==self.contentIdx else 0, True, self.points(c), 1)
            n += 1
            
        if self.dragStaff:
            pos = PYG.mouse.get_pos()
            PYG.draw.lines(self.screen, 0xff000000, True, self.points(self.dragStaff.points, *pos), 1)
        if self.rulerPoint:
            pos = PYG.mouse.get_pos()
            PYG.draw.lines(self.screen, 0x0000ff00, True, (self.rulerPoint, pos), 1)
            dis = self.distanceBetween(self.rulerPoint, pos)
            self.screen.blit(self.font.render("%f"%dis, True, (255,0,0)), (pos[0]+20,pos[1]))

    def readfile(self, fpath):
        furno, fixed, comment = 0, True, ''
        with open(fpath) as f:
            for l in f.readlines():
                l = l.strip('\t \r\n')
                if not l:
                    pass
                elif l.startswith('#'):
                    if fixed:
                        self.content.append(l[1:].strip())
                    else:
                        comment += l+'\n'
                elif l.startswith('$'):
                    fixed = False
                else:
                    if furno:
                        if fixed:
                            self.content.append(Contour(l).getPoints())
                        else:
                            self.buff.append((Contour(l), comment))
                            comment = ''
                    else:
                        self.contour = Contour(l)
                        self.autofit()
                    furno += 1
    def writefile(self, fpath):
        with open(fpath,'w+') as f:
            f.write(self.contour.getInstruct())
            f.write('\n')
            for c in self.content:
                if type(c) is str:
                    f.write("# "+c)
                else:
                    cnt = Contour()
                    cnt.points = c
                    cnt.origin = c[0]
                    f.write(cnt.getInstruct())
                f.write('\n')
            f.write('$ fixed components end and drag ones begin\n')
            for b in self.buff:
                f.write(b[1])
                f.write(b[0].getInstruct(False))
                f.write('\n')
            
    def setDragStaff(self, *pos):
        if self.contentIdxLocked:
            self.dragFixedStaff(*pos)
            return
        self.dragStaff.origin = self.rossecorp(Point(*pos))
        self.content.append(self.dragStaff.getPoints())
        self.dragStaff = None
    def changeDragStaff(self):
        if self.buff:
            self.dragStaff = self.buff[self.buffIdx][0]
            self.buffIdx += 1
            if len(self.buff) <= self.buffIdx: self.buffIdx = 0
    def changeFixedStaff(self, drt):
        if self.content and not self.contentIdxLocked:
            loop = 0
            if drt > 0:
                while True:
                    self.contentIdx += 1
                    if self.contentIdx >= len(self.content):
                        self.contentIdx = 0
                        if loop==2:
                            self.contentIdx = -1
                            break
                        loop += 1
                    if type(self.content[self.contentIdx]) is list:
                        break
            else:
                while True:
                    self.contentIdx -= 1
                    if self.contentIdx < 0:
                        self.contentIdx = len(self.content)-1
                        if loop==2:
                            self.contentIdx = -1
                            break
                        loop += 1
                    if type(self.content[self.contentIdx]) is list:
                        break
    def deleteFixedStaff(self):
        if self.contentIdxLocked: return
        if self.content and 0<=self.contentIdx<len(self.content) and type(self.content[self.contentIdx]) is list:
            del self.content[self.contentIdx]
            self.contentIdx -= 1
    def dragFixedStaff(self, *pos):
        if self.contentIdxLocked:
            self.dragStaff.origin = self.rossecorp(Point(*pos))
            self.content[self.contentIdx] = self.dragStaff.getPoints()
            self.dragStaff = None
            self.contentIdx = -1
            self.contentIdxLocked = False
        elif self.content and 0<=self.contentIdx<len(self.content) and type(self.content[self.contentIdx]) is list:
            cnt = Contour()
            cnt.points = self.content[self.contentIdx]
            cnt.setInstruct(cnt.getInstruct())
            self.dragStaff = cnt
            self.content[self.contentIdx] = None
            self.contentIdxLocked = True
    def transZoom(self, func):
        if self.rulerPoint:
            p = self.rossecorp(Point(*self.rulerPoint))
        func()
        if self.rulerPoint:
            p = self.processor(p)
            self.rulerPoint = (p.x, p.y)
            
            
ADT = Application(1024, 720)

# ADT.readfile("/Users/zhouzhichao/tmp/furniture.fur")
ADT.readfile("/Users/zhouzhichao/tmp/save.fur")
ADT.draw()

def zoomInFunc():
    ADT.sx *= 1.1
    ADT.sy *= 1.1
def zoomOutFunc():    
    ADT.sx /= 1.1
    ADT.sy /= 1.1
def moveZoomFunc(keymap, unit):
    if K_LEFT in keymap: ADT.ccx += unit
    if K_RIGHT in keymap: ADT.ccx -= unit 
    if K_UP in keymap: ADT.ccy += unit
    if K_DOWN in keymap: ADT.ccy -= unit
    
keymap, keytime = set(), 0
while True:
    PYG.display.update()
    for event in PYG.event.get():
        if event.type == QUIT:
            ADT.writefile("/Users/zhouzhichao/tmp/save.fur")
            exit()
        if event.type == MOUSEMOTION:
            ADT.draw()
        if event.type == KEYDOWN:
            keymap.add(event.key)
        if event.type == KEYUP:
            if event.key in keymap:
                keymap.remove(event.key)            
            
    if keymap and time() - keytime > 0.2:
        keytime = time()
        pos = PYG.mouse.get_pos()
        shift = (K_LSHIFT in keymap) or (K_RSHIFT in keymap)
        if K_SPACE in keymap:
            ADT.setDragStaff(*pos)
        elif K_EQUALS in keymap:
            ADT.transZoom(zoomInFunc)
        elif K_MINUS in keymap:     
            ADT.transZoom(zoomOutFunc)   
        elif K_r in keymap:
            if ADT.dragStaff: ADT.dragStaff.rotate(5 if shift else -5)
        elif K_n in keymap:
            ADT.changeDragStaff()
        elif K_m in keymap:
            ADT.dragStaff = None
            ADT.changeFixedStaff(1 if shift else 0)
        elif K_h in keymap:
            ADT.dragFixedStaff(*pos)
        elif K_BACKSPACE in keymap:
            ADT.deleteFixedStaff()
        elif K_l in keymap:
            ADT.rulerPoint = None if ADT.rulerPoint else pos
        else:
            unit = 10 if shift else 30
            ADT.transZoom(lambda:moveZoomFunc(keymap, unit))
        ADT.draw()
        
#             elif event.key == K_w:
#                 box.rotate(-5)
#                 ADT.draw()
#                 PYG.draw.lines(ADT.screen, (0,0,255), True, ADT.points(box.points, *pos), 1)

#             points = []
#             screen.fill((255,255,255))
            
#         if event.type == MOUSEBUTTONDOWN:
#             screen.fill((255,255,255))
#             # 画随机矩形
#             rc = (randint(0,255), randint(0,255), randint(0,255))
#             rp = (randint(0,639), randint(0,479))
#             rs = (639-randint(rp[0], 639), 479-randint(rp[1], 479))
#             PYG.draw.rect(screen, rc, Rect(rp, rs))
#             # 画随机圆形
#             rc = (randint(0,255), randint(0,255), randint(0,255))
#             rp = (randint(0,639), randint(0,479))
#             rr = randint(1, 200)
#             PYG.draw.circle(screen, rc, rp, rr) 
#             # 获得当前鼠标点击位置
#             x, y = PYG.mouse.get_pos()
#             points.append((x, y)) 
#             # 根据点击位置画弧线
#             angle = (x/639.)*pi*2.
#             PYG.draw.arc(screen, (0,0,0), (0,0,639,479), 0, angle, 3)
#             # 根据点击位置画椭圆
#             # 从左上和右下画两根线连接到点击位置
#             PYG.draw.line(screen, (0, 0, 255), (0, 0), (x, y))
#             PYG.draw.line(screen, (255, 0, 0), (640, 480), (x, y))
#             # 画点击轨迹图
#             if len(points) > 1:
#                 PYG.draw.lines(screen, (155, 155, 0), False, points, 2)
#             # 和轨迹图基本一样，只不过是闭合的，因为会覆盖，所以这里注释了
#             #if len(points) >= 3:
#             #    pygame.draw.polygon(screen, (0, 155, 155), points, 2)
#             # 把每个点画明显一点
#             for p in points:
#                 PYG.draw.circle(screen, (155, 155, 155), p, 3)

    
