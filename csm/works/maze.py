#coding: UTF-8

from random import randint as rnd
from csm.svg.SVGGen import svgGraph

SPM, KBB = 10, -100

class maze(object):
    def __init__(self, cx=100, cy=100):
        self.bmap = None
        self.cx = cx
        self.cy = cy
        self.dirt = ((1,0),(0,1),(-1,0),(0,-1))
        self.fillBorder()
    
    def fillBorder(self):
        self.bmap = [[0]*self.cy for _ in xrange(self.cx)]
        self.bmap[0] = [KBB]*self.cy
        self.bmap[-1] = [KBB]*self.cy
        for i in xrange(self.cx):
            self.bmap[i][0] = self.bmap[i][-1] = KBB
        
    def s(self):
        for x in xrange(len(self.bmap)):
            for y in xrange(len(self.bmap[0])): 
                print 'X' if self.bmap[x][y] else ' ',
            print
    
    def genSqrMaze(self, sx=1, sy=1):
        x, y, z = sx, sy, SPM
        while True:
            if self.bmap[x - 1][y] == 0 or self.bmap[x][y - 1] == 0 or self.bmap[x][y + 1] == 0 or self.bmap[x + 1][y] == 0:
                while True:
                    XX, YY, r = x, y, rnd(0, 3)
                    XX += self.dirt[r][0]
                    YY += self.dirt[r][1]
                    if 0 == self.bmap[XX][YY]: break
                x, y = XX, YY
                z += 1
                self.bmap[x][y] = z
            else:
                for r in xrange(4):
                    XX = x + self.dirt[r][0]
                    YY = y + self.dirt[r][1]
                    if self.bmap[XX][YY] == z - 1: break
               
                if self.bmap[XX][YY] != z - 1: break
                x, y, z = XX, YY, self.bmap[XX][YY]
                
    def genHexMaze(self, sx=1, sy=1):
        x, y, z = sx, sy, SPM
        dirt = ((-1,0),(0,-1),(1,-1),(1,0),(0,1),(-1,1))
        while True:
            if self.bmap[x-1][y] == 0 or self.bmap[x][y-1] == 0 or self.bmap[x+1][y-1] == 0 or \
                self.bmap[x+1][y] == 0 or self.bmap[x][y+1] == 0 or self.bmap[x-1][y+1] == 0:
                while True:
                    XX, YY, r = x, y, rnd(0, 5)
                    XX += dirt[r][0]
                    YY += dirt[r][1]
                    if 0 == self.bmap[XX][YY]: break
                x, y = XX, YY
                z += 1
                self.bmap[x][y] = z
            else:
                for r in xrange(6):
                    XX = x + dirt[r][0]
                    YY = y + dirt[r][1]
                    if self.bmap[XX][YY] == z - 1: break
               
                if self.bmap[XX][YY] != z - 1: break
                x, y, z = XX, YY, self.bmap[XX][YY]
    
    def findSqrMazeWay(self, sx, sy, ex, ey):
        self.ma = [[0]*self.cy for _ in xrange(self.cx)]
        self.curX = sx
        self.curY = sy
        self.bmap[sx][sy-1] = self.bmap[sx][sy]+1
        self.aimX = ex
        self.aimY = ey
        self.bmap[ex][ey+1] = self.bmap[ex][ey]+1
        
        self.curZ = SPM
        self.Unf = False
        self.ma[sx][sy] = self.curZ
        self.findSqrWay()
        
    def findSqrWay(self):
        if self.curX == self.aimX and self.curY == self.aimY:
            self.Unf = True
            return    
        
        for i in xrange(4):
            if self.Unf: break
            nxtX, nxtY = self.curX + self.dirt[i][0], self.curY + self.dirt[i][1]
            nextB = self.bmap[nxtX][nxtY]
            T = abs(self.bmap[self.curX][self.curY] - nextB)
            
            if T <= 1 and self.ma[nxtX][nxtY] == 0:
                self.curX += self.dirt[i][0]
                self.curY += self.dirt[i][1]
                self.curZ += 1
                self.ma[self.curX][self.curY] = self.curZ
                self.findSqrWay()
                if self.Unf: break
                self.ma[self.curX][self.curY] = KBB
                self.curZ -= 1
                self.curX -= self.dirt[i][0]
                self.curY -= self.dirt[i][1]
        
    def makeImage(self):
        svg = svgGraph()
        svg.docname = 'test'
        
        unit = 12
        svg.width = self.cx* unit
        svg.height = self.cy* unit
        
        for x in xrange(1, self.cx):
            for y in xrange(1, self.cy):
                if abs(self.bmap[x][y] - self.bmap[x-1][y]) > 1:
                    svg.line(x*unit, y*unit-1, x*unit, (y+1)*unit+1)
                if abs(self.bmap[x][y] - self.bmap[x][y-1]) > 1:
                    svg.line(x*unit-1, y*unit, (x+1)*unit+1, y*unit)
        
        if self.__dict__.get('ma') is not None:
            for x in xrange(1, self.cx):
                for y in xrange(1, self.cy):
                    if self.ma[x][y] < 0: continue
                     
                    if abs(self.ma[x][y] - self.ma[x-1][y]) == 1:
                        svg.line((x+0.5)*unit, (y+0.5)*unit, (x-0.5)*unit, (y+0.5)*unit, strColor='#ff0000', strWidth='1')
                    if abs(self.ma[x][y] - self.ma[x][y-1]) == 1:
                        svg.line((x+0.5)*unit, (y+0.5)*unit, (x+0.5)*unit, (y-0.5)*unit, strColor='#ff0000', strWidth='1')
                    
        svg.output()

def readModel(si):        
    so = si.decode('UTF-8').encode('GBK')
    offset=((ord(so[0])-0xa1)*94+(ord(so[1])-0xa1))*32 #根据内码找出汉字在HZK16中的偏移位置 
    with open("/Users/zhouzhichao/mapdata/HZK16", "r") as fp:  
        fp.seek(offset) #文件指针偏移到要找的汉字处 
        return fp.read(32) #读取该汉字的字模 
    
def showWordChar(char):
    mchar = readModel(char)
    mark = '0123456789ABCDEF'
    line, odd, ln = '0   ', True, 0
    print 'x   ' + mark
    for c in mchar:
        cc, mask = ord(c), 0x80
        for _ in xrange(8):
            line += '@' if cc & mask else ' '
            mask >>= 1
        odd = not odd
        if odd:
            print line
            ln += 1
            if ln > 15: break
            line = mark[ln]+'   '
        
def setMapChar(bmap, sx, sy, char, model = None):
    odd = True
    x, y = sx, sy
    plain = readModel(char)
    for c in plain:
        cc, mask = ord(c), 0x80
        for _ in xrange(8):
            if cc & mask: bmap[x][y] = SPM
            mask >>= 1
            x += 1
            
        odd = not odd
        if odd:
            y += 1
            x = sx
            
    if model:
        for p in model[0]:
            bmap[sx+p[0]][sy+p[1]] = 0
        for p in model[1]:
            bmap[sx+p[0]][sy+p[1]] = SPM    


def showMap(bmap):
    for l in bmap:
        line = ''
        for i in l:
            line += ' ' if i else '@'
        print line
        
def setCharsToMap(bmap, sx, sy):
    modifyModel = {'超':(((8,8),(8,12)), ((0,13),(3,13),(4,14),(7,7),(8,6),(10,6),(12,6))),
                   '爱':(((1,7),(3,2),(7,9),(12,7)), ((0,5),(2,13),(3,11),(4,9),(6,11),(6,15),(7,12),(7,14),(8,0),(9,12),(10,2),(10,11),(10,14),(14,6))),
                   '莹':(((9,4),), ((0,6),(10,12),(14,7)))
                   }
    
    setMapChar(m.bmap, sx, sy, '超', modifyModel['超'])
    setMapChar(m.bmap, sx+16, sy, '爱', modifyModel['爱'])
    setMapChar(m.bmap, sx, sy+16, '莹', modifyModel['莹'])
    setMapChar(m.bmap, sx+16, sy+16, '莹', modifyModel['莹'])
    
    
if __name__ == '__main__':
    m = maze(60, 60)
#     setCharsToMap(m.bmap, 14, 14)
    m.genSqrMaze(17, 14)
    m.findSqrMazeWay(30, 1, 30, 58)
    m.makeImage()
