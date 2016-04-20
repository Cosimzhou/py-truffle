#coding: UTF-8

from math import cos, sin, tan, pi, atan, sqrt
alpha = 1.3

def testLens(A, B, phi):
    x, y = A/cos(phi), B*tan(phi)
    print "point at (%f, %f)"%(x,y)
    ax, ay = A*tan(phi)/cos(phi), B/(cos(phi)**2)
    af = B/A/sin(phi)
    print "∂y/∂x=f':  %f = %f/%f = %f"%(af, ay, ax, ay/ax)
    nf = -1.0/af
    A_i = atan(nf)
    sA_i = sin(A_i)
    print "injected angle check: %f = %f"%(sA_i, nf/sqrt(1+nf**2))
    sA_o = sA_i*alpha
    tA_o = sA_o/sqrt(1-sA_o**2)
    nl = (nf-tA_o)/(1+nf*tA_o)
    print "outjected angle: %f"%(nl)
    b = y - nl*x
    xo = -b/nl
    print "xx ==== >>>>: %f"%xo 
    
def testLensEx(X, Y, aX, aY, phis):
    for phi in phis:
        x, y = X(phi), Y(phi)
        """
#         nf = -aX(phi)/aY(phi)
#         sA_o = nf/sqrt(1+nf**2)*alpha
#         tA_o = sA_o/sqrt(1-sA_o**2)
#         nl = (nf-tA_o)/(1+nf*tA_o)
#         xo = (nl*x-y) / nl
#         print "%.12f  from(%f, %f), nf=%f, nl=%f"%(xo, x, y, nf, nl)
        """
        
        """
#         nf = -aX(phi)/aY(phi)
#         tk = sqrt((1-alpha**2)*nf**2+1)
#         k = nf*(tk - alpha)/(tk+alpha*(nf**2))
#         xo = x-y/k
        """
        
        f, g = aX(phi), aY(phi)
        tk = sqrt((1-alpha**2)*f**2+g**2)
        k = (alpha*f*g-f*tk)/(alpha*f*f+g*tk)
        xo = x-y/k
        
        print "%.12f   from(%f, %f)"%(xo, x, y)     
    
def gen0():
#     for i in xrange(51, 101, 1):
#         yield pi*i/100.0
    for i in xrange(950, 1001, 1):
        yield pi*i/1000.0
        
def gen():
#     for i in xrange(51, 101, 1):
#         yield pi*i/100.0
    for i in xrange(1,51):
        yield pi*i/1000.0
        
A, B = 1, 2
dict_data = {'双曲线': (lambda x: A/cos(x), 
                      lambda y: B*tan(y), 
                      lambda ax: A*tan(ax)/cos(ax), 
                      lambda ay: B/(cos(ay)**2),
                      gen0()),
             '抛物线': (lambda x: -A*x*x,
                       lambda y: B*y,
                       lambda ax: -2*A*ax,
                       lambda ay: B,
                       gen()),
             '椭圆线': (lambda x: A*cos(x),
                       lambda y: B*sin(y),
                       lambda ax: -A*sin(ax),
                       lambda ay: B*cos(ay),
                       gen()),
             '正圆线': (lambda x: A*cos(x),
                       lambda y: A*sin(y),
                       lambda ax: -A*sin(ax),
                       lambda ay: A*cos(ay),
                       gen()),
             }

def showDetail(name):
    print "下面展示的是%s的聚集情况："%(name)
    testLensEx(*dict_data[name])
    
if __name__ == '__main__':
#     showDetail('双曲线')
    showDetail('抛物线')
#     showDetail('椭圆线')
#     showDetail('正圆线')
    pass