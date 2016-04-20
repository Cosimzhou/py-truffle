import math

def trim(f):
    fl, cl = math.floor(f), math.ceil(f)
    
    if f-fl < 1e-7: return int(fl)
    if cl-f < 1e-7: return int(cl)
    return f
    
class Complex:
    def __init__(self, real=0.0, image=0.0):
        self.real = trim(real)
        self.image= trim(image)
    
    def __nonzero__(self):
        return 1 if self.real or self.image else 0
    
    def __abs__(self):
        return math.sqrt(self.real**2+self.image**2)
    
    def __invert__(self):
        return Complex(self.real, -self.image)
    
    def __add__(self, comp):
        if type(comp) is type(self):
            return Complex(self.real+comp.real,
                           self.image+comp.image)
        else:
            return Complex(self.real-comp, self.image)
        
    def __sub__(self, comp):
        if type(comp) is type(self):
            return Complex(self.real-comp.real,
                           self.image-comp.image)
        else:
            return Complex(self.real-comp, self.image)
        
    def __mul__(self, comp):
        if type(comp) is type(self):
            return Complex(self.real*comp.real-self.image*comp.image, 
                           self.real*comp.image+self.image*comp.real)
        else:
            return Complex(self.real*comp, self.image*comp)
        
    def __div__(self, comp):
        if not comp:
            raise Exception('Divided by zero.')
        if type(comp) is type(self):
            a, b, c, d = self.real, self.image, comp.real, comp.image
            return Complex(float(a*c+b*d)/(c*c+d*d), float(b*c-a*d)/(c*c+d*d))
        else:
            return Complex(float(self.real)/comp, float(self.image)/comp)
    
    def __pow__(self, comp):
        leng = self.__abs__()
        angl = self.arg()
        if type(comp) is type(self):
            nleng= leng**comp.real
            nangl= (angl*comp.real)%(math.pi*2)
            rr = Complex()
            rr.setMA(nleng, nangl)
            zs = self.log()*comp.image
            xc = Complex(zs.cos(), zs.sin())
            return rr*xc
        else:
            mod = leng**comp
            ang = (angl*comp)%(math.pi*2)
            return Complex(mod*math.cos(ang), mod*math.sin(ang))
    
    def __and__(self, comp):
        return self.__nonzero__() and bool(comp) 
    
    def __or__(self, comp):
        return self.__nonzero__() or bool(comp)
    
    def __repr__(self):
        sreal = str(self.real) if self.real != 0 else ''
        if int(self.image) == self.image and int(self.image) in (0,1,-1):
            simage= {0:'',1:'i',-1:'-i'}[int(self.image)]
        else:
            simage= "%si"%self.image 
        
        if sreal and self.image > 0:
            return sreal +'+'+ simage
        elif sreal or simage:
            return sreal + simage
        else:
            return '0'
            
    
    def setMA(self, m, a):
        self.real, self.image = m*math.cos(a), m*math.sin(a)
    
    def arg(self): 
        return math.atan2(self.image, self.real)
    
    def log(self):
        if not self.__nonzero__():
            raise Exception('Zero is not logarithm for any.')
        ang, mod = self.arg(), self.__abs__()
        return Complex(math.log(mod), ang)
    
    def exp(self):
        rr = math.exp(self.real)
        return Complex(rr*math.cos(self.image), rr*math.sin(self.image))
    
    def sin(self):
        return math.sin(self.real) * math.cosh(self.image) + \
                math.sinh(self.image) * math.cos(self.real)
    
    def cos(self):
        return math.cos(self.real) * math.cosh(self.image) - \
                math.sin(self.real) * math.sinh(self.image)
    
    def tan(self):
        cosval = self.cos()
        if cosval == 0:
            return float('inf')
        return self.sin() / cosval
    
if __name__ == '__main__':
    a = Complex(0.7071067811865476, 0.7071067811865476)
    b = a.log()
    print "ln(%s)=%s, %s"%(a, b, b.exp())
    print a**2
    a, b, o = Complex(5,3), Complex(2,-1), Complex()
    print abs(a), abs(b)
    print a+b, a-b, a/b, ~a,(a and b), (a or b), a**b
    
#     a = complex(1,2)
#     print math.log(a)
    