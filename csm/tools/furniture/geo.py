# -*- coding: UTF-8 -*-

import math, re
from collections import namedtuple

INF = float('inf')

class ClipType: (Intersection, Union, Difference, Xor) = range(4)
class PolyType:    (Subject, Clip) = range(2)
class PolyFillType: (EvenOdd, NonZero, Positive, Negative) = range(4)
class JoinType: (Square, Round, Miter) = range(3)
class EndType: (Closed, Butt, Square, Round) = range(4)
class EdgeSide: (Left, Right) = range(2)
class Protects: (Neither, Left, Right, Both) = range(4)
class Direction: (LeftToRight, RightToLeft) = range(2)

Point = namedtuple('Point', 'x y')
FloatPoint = namedtuple('FloatPoint', 'x y')
Rect = namedtuple('FloatPoint', 'left top right bottom')

def xfloat(f):
    ff, cf = math.floor(f), math.ceil(f)
    if abs(ff-f) <= 1e-5: return ff
    if abs(cf-f) <= 1e-5: return cf
    return f

class Vector(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    def __nonzero__(self):
        return 1 if self.x or self.y or self.z else 0
    def __neg__(self):   # -
        return Vector(-self.x, -self.y, -self.z)
    def __abs__(self):  # abs
        return math.sqrt(self.x**2+self.y**2+self.z**2)
    def __add__(self, vec): # +
        return Vector(self.x+vec.x, self.y+vec.y, self.z+vec.z)
    def __sub__(self, vec): # -
        return Vector(self.x-vec.x, self.y-vec.y, self.z-vec.z)
    def __mul__(self, vec): # *
        if type(vec) is Vector:
            return self.x*vec.x + self.y*vec.y + self.z*vec.z
        else:
            return Vector(self.x*vec, self.y*vec, self.z*vec)
    def __div__(self, rate):   # / 
        return Vector(float(self.x)/rate, float(self.y)/rate, float(self.z)/rate)
    def __pow__(self, vec):     # **
        return Vector(self.y*vec.z-self.z*vec.y,
                      self.z*vec.x-self.x*vec.z,
                      self.x*vec.y-self.y*vec.x)
    def __xor__(self, vec):
        m = abs(self)*abs(vec)
        if m == 0: return 0
        if self.z==0 and vec.z ==0:
            a = self**vec
            sinm, cosm = a.z / m, self*vec
            if sinm>1:sinm=1
            elif sinm<-1:sinm=-1
            ang = math.asin(sinm) *180/math.pi
            if cosm < 0: ang = 180-ang 
            return ang
        else:
            cosm = self*vec/m
            if cosm>1: cosm=1
            elif cosm<-1: cosm=-1
            return math.acos(cosm)*180/math.pi
    def normal(self):
        return self / abs(self)
    def vectorLength(self, leng):
        return self / abs(self) * leng
    def rotate(self, rot, os=None):
        rot *= math.pi/180.0
        cos0, sin0 = math.cos(rot), math.sin(rot)
        if os is None:
            return Vector(self.x*cos0-self.y*sin0,
                          self.x*sin0+self.y*cos0,
                          self.z)
        else:
            o = os.normal()
            return Vector(self.x*((o.x**2)*(1-cos0)+cos0) + self.y*(o.x*o.y*(1-cos0)-o.z*sin0) + self.z*(o.x*o.z*(1-cos0)+o.y*sin0),
                          self.x*(o.y*o.x*(1-cos0)+o.z*sin0) + self.y*((o.y**2)*(1-cos0)+cos0) +self.z*(o.y*o.z*(1-cos0)-o.x*sin0),
                          self.x*(o.z*o.x*(1-cos0)-o.y*sin0) + self.y*(o.z*o.y*(1-cos0)+o.x*sin0) +self.z*((o.z**2)*(1-cos0)+cos0))
    def __eq__(self, vec):
        return self.x == vec.x and self.y == vec.y and self.z == vec.z
    def __ne__(self, vec):
        return self.x != vec.x or self.y != vec.y or self.z == vec.z
    def __and__(self, comp):
        return self.__nonzero__() and bool(comp) 
    def __or__(self, comp):
        return self.__nonzero__() or bool(comp)
    def __repr__(self):
        return "(%f, %f, %f)"%(self.x, self.y, self.z)
    def downDim(self, f=None):
        return Point(xfloat(self.x), xfloat(self.y))

class Contour(object):
    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.origin = Point(0,0)
        self.points = None
        if len(args) == 1: self.setInstruct(args[0])
    def setInstruct(self, instruct):
        origin, vec = Vector(), Vector(1)
        if '$' in instruct:
            s = instruct.split('$')
            header = s[0]
            instruct = s[1]
            p=re.compile(r'(.*),(.*):(.*)')
            m = p.match(header)
            if len(m.groups()) == 3:
                rot = float(m.groups()[2])
                vec = vec.rotate(rot)
                self.origin = Point(*map(float,m.groups()[:2]))
            
        arr = [origin.downDim()]
        ss = instruct.split(' ')
        for s in ss:
            so=s.split('@')
            if len(so) == 1:
                s = float(so[0])
                if s > 0:
                    vec = vec.rotate(90)
                elif s < 0:
                    vec = vec.rotate(-90)
                    s = -s
                else: continue
                origin += vec.vectorLength(s)
                arr.append(origin.downDim())
            else:
                s, a = float(so[0]), float(so[1])
                vec = vec.rotate(a)
                origin += vec.vectorLength(s)
                arr.append(origin.downDim())
        self.points = arr
    def getInstruct(self, fixed=True):
        if not self.points: return ''
        buff, ovec, rot = [], None, 0
        lp = Vector(*self.points[0])
        for i in xrange(1,len(self.points)):
            p = Vector(*self.points[i])
            vec = p-lp
            dis = str(xfloat(abs(vec)))
#             dis = str(int(abs(vec)))
            if i == 1:
                rot = Vector(0,1) ^ vec
            elif ovec:
                ang = xfloat(ovec^vec)
                if ang == -90:
                    dis = '-'+dis
                elif ang != 90:
                    dis+='@%s'%ang
            buff.append(dis)
            ovec, lp = vec, p
        prefix = ''
        if fixed and (self.origin.x or self.origin.y or rot):
            prefix = '%s,%s:%s$'%(self.origin.x, self.origin.y, rot) 
        return prefix+' '.join(buff)
    def getPoints(self):
        return map(lambda p:Point(self.origin.x+p.x, self.origin.y+p.y), self.points)
    def rotate(self, rot):
        self.points = list(map(lambda p: Vector(*p).rotate(rot).downDim(), self.points))
    def mirror(self):
        self.points = list(map(lambda p: Point(-p.x, p.y), self.points))
    def envelop(self):
        mx, my, maxx, maxy = INF, INF, -INF, -INF
        for p in self.points:
            if p.x>maxx: maxx=p.x
            if p.y>maxy: maxy=p.y
            if p.x<mx: mx=p.x
            if p.y<my: my=p.y
        return (mx, my, maxx-mx, maxy-my)
        

class Adaptor(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.contour = None
        self.sx = 1
        self.sy = 1
        self.cx = self.width/2
        self.cy = self.height/2
        self.ccx = 5
        self.ccy = 5
        self.processor=lambda p:Point(self.cx+(p.x-self.ccx)*self.sx, self.cy+(p.y-self.ccy)*self.sy)
        self.rossecorp=lambda p:Point((p.x-self.cx)/self.sx+self.ccx, (p.y-self.cy)/self.sy+self.ccy)
    def autofit(self):
        print self.contour
        env = self.contour.envelop()
        self.ccx = env[0]+env[2]/2
        self.ccy = env[1]+env[3]/2
        rx = (self.width-10)/env[2]
        ry = (self.height-10)/env[3]
        if rx > ry: rx = ry
        self.sx = self.sy = rx
    def size(self):
        return self.width, self.height
    def points(self, array = None, x=None,y=None):
        if array:
            if x is None: return map(self.processor, array)
            d = self.rossecorp(Point(x,y))
            return map(lambda p:Point(self.cx+(p.x+d.x-self.ccx)*self.sx, self.cy+(p.y+d.y-self.ccy)*self.sy), array)
        else:
            return map(self.processor, self.contour.points)
    

if __name__ == '__main__':
    p = Point(0,1)
    print p[1]
    
    v = Vector(0,1)
    vv= Vector(1,1)
    print v**vv, vv**v
    print v ^ vv, vv ^ v
    print v.rotate(90)
    z = Vector(0,0,-1)
    print v.rotate(90, z)
    
    cnt = Contour()
    cnt.points = [
# Point(284,12),
# Point(284,21),
# Point(272,21),
# Point(272,106),
# Point(283,106),
# Point(283,120),
# Point(268,120),
# Point(268,230),
# Point(228,230),
# Point(228,225),
# Point(257,225),
# Point(257,195),
# Point(229,195),
# Point(229,190),
# Point(256,190),
# Point(256,112),
# Point(198,112),
# Point(198,188),
# Point(203,188),
# Point(203,196),
# Point(199,196),
# Point(199,224),
# Point(202,224),
# Point(202,231),
# Point(189,231),
# Point(189,225),
# Point(193,225),
# Point(193,89),
# Point(142,89),
# Point(142,116),
# Point(98,116),
# Point(98,224),
# Point(160,224),
# Point(160,231),
# Point(151,231),
# Point(151,235),
# Point(143,235),
# Point(143,231),
# Point(98,231),
# Point(98,234),
# Point(91,234),
# Point(91,196),
# Point(88,196),
# Point(88,189),
# Point(91,189),
# Point(91,113),
# Point(23,113),
# Point(23,190),
# Point(64,190),
# Point(64,196),
# Point(23,196),
# Point(23,275),
# Point(92,275),
# Point(92,271),
# Point(98,271),
# Point(98,281),
# Point(23,281),
# Point(23,445),
# Point(57,445),
# Point(57,469),
# Point(118,469),
# Point(118,444),
# Point(144,444),
# Point(144,268),
# Point(150,268),
# Point(150,272),
# Point(154,272),
# Point(154,278),
# Point(150,278),
# Point(150,444),
# Point(172,444),
# Point(172,468),
# Point(233,468),
# Point(233,444),
# Point(257,444),
# Point(257,279),
# Point(180,279),
# Point(180,271),
# Point(266,271),
# Point(266,445),
# Point(290,445),
# Point(290,454),
# Point(265,454),
# Point(265,504),
# Point(389,504),
# Point(389,479),
# Point(416,479),
# Point(416,456),
# Point(383,456),
# Point(383,445),
# Point(414,445),
# Point(414,20),
# Point(338,20),
# Point(338,106),
# Point(376,106),
# Point(376,116),
# Point(316,116),
# Point(316,105),
# Point(330,105),
# Point(330,22),
# Point(321,22),
# Point(321,12)]#,
Point(423,12),
Point(423,512),
Point(256,512),
Point(256,455),
Point(240,455),
Point(240,479),
Point(51,479),
Point(51,455),
Point(14,455),
Point(14,105),
Point(92,105),
Point(92,80),
Point(199,80),
Point(199,107),
Point(268,107),
Point(268,12),
Point(284,12)]
    print cnt.envelop()
#     (14, 12, 409, 500)
    cnt.points=map(lambda p:Point((p.x-14)*11700.0/409,(p.y-12)*12800.0/500), cnt.points)
#     cnt.origin = Point(0,0)
#     cnt.setInstruct("50 70.710678118654755@45 50@45 100")#"5 5 -5 5 10")
    print cnt.getInstruct()
    
    v = Vector(1)
    vv = v.rotate(-100)
    print v^vv
    
    
    pass