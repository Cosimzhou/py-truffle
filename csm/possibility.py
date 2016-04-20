# -*- coding: utf-8 -*-
# from __future__ import division  

'''
Created on 2014年6月20日

@author: zhouzhichao
'''

"""
    在一个暗盒中有大小形状相同三种颜色的小球，红色的3个，白色的2个，绿色的1个.
    从该暗盒中一个个的取出小球，首先把红球取光的概率是多少？
"""


his={}
def p(*args):
    larg = len(args)
    if larg < 2:
        return 1
    
    for i in range(larg):
        if args[i] <=0.0:
            return 0.0 if i else 1.0
    
    global his
    
    key = ','.join(map(lambda x: str(x), args))
    if his.get(key) is None:
        sumv = sum(args)
        poss = 0.0
        locargs = list(args)
        for i in xrange(larg):
            n = locargs[i]
            locargs[i] -= 1
            poss += n*p(*locargs)
            locargs[i] += 1
        poss /= sumv
        his[key] = poss
        return poss
    else:
        return his[key]
    
    
class CutLoopFloat(object):
    def __init__(self):
        super(CutLoopFloat, self).__init__()
        self.replen = 0
        self.repetend = ''
        self.repcnt = 0
        self.prerep = 0 
        self.prelen = 0
        self.exp    = 0
        self.frag   = ''
    
    def setclf(self, **kwargs):
        if kwargs.get('repetend'):
            self.repetend = kwargs['repetend']
            self.replen = len(self.repetend)
        
        if kwargs.get('repcnt'): self.repcnt = kwargs['repcnt']
        if kwargs.get('prerep'): 
            self.prerep = kwargs['prerep']
            self.prelen = len(self.prerep)
            self.prerep = int('0' + self.prerep) 
        if kwargs.get('exp'): self.exp = int(kwargs['exp'])
        if kwargs.get('frag'): self.frag = kwargs['frag']
    
    
def floatCheck(num):
    e, d, ei, di = False, False, 0, 0
    ii = 0
    flstr, exstr='', ''
    for i in num:
        if i == '.':
            if d or e: return None
            d, di = True, ii 
        elif i in 'eE':
            if e: return None
            if (not d and ii != 1) or not (d and di == 1):
                return None
            e, ei = True, ii
        elif i in '0123456789':
            if d and not e:
                flstr += i
            elif e:
                exstr += i
        elif i in '+-':
            if e and ii == ei+1:
                pass
            else:
                return None
        else:
            return None
        ii += 1 
        
    exp = int(exstr) if exstr != '' else 0
    return flstr, exp   
        
def cutLoopFloat(num):
    fltchk = floatCheck(num)
    if fltchk is None:
        return None
    
    flstr, exp = fltchk
    xstr=flstr[:-1]
    
    repcnt, replen, maxj = 1, 1, 0
    for i in range(1, len(flstr)/2+1):
        piece = xstr[-i:]
        cnt = 1
        for j in range(len(xstr)-i-i, -1, -i):
            if xstr[j:j+i] != piece:
                break
            cnt += 1
        if repcnt < cnt:
            repcnt, replen, maxj = cnt, i, len(xstr)-cnt*i
            
    for i in range(2, len(flstr)/2+1):
        piece = xstr[-i:]
        piece = piece[1:]+piece[0]
        cnt = 1
        for j in range(len(xstr)-i-i+1, -1, -i):
            if xstr[j:j+i] != piece:
                break
            cnt += 1
        if repcnt < cnt:
            repcnt, replen, maxj = cnt, i, len(xstr)-cnt*i+1
                        

    clf = CutLoopFloat()    
    if repcnt > 1 and (xstr[-replen] == flstr[-1] or 
                       (int(xstr[-replen]) == int(flstr[-1])-1 and 
                        int(xstr[-replen+(1%replen)]) >= 5)):
        prerep = xstr[:maxj]
        if replen == 1 and int(xstr[-replen]) == int(flstr[-1])-1:
            repcnt += 1
        clf.setclf(repetend=xstr[-replen:], repcnt=repcnt, prerep=prerep, exp=exp, frag=flstr)
        return clf
    
    repcnt, replen, maxj = 1, 1, 0
    for i in range(2, len(flstr)/2+1):
        piece = flstr[-i:]
        cnt = 1
        for j in range(len(flstr)-i-i, -1, -i):
            if flstr[j:j+i] != piece:
                break
            cnt += 1
    
        if repcnt < cnt:
            repcnt, replen, maxj = cnt, i, len(flstr)-cnt*i
    
    if repcnt == 1:
        clf.setclf(prerep=flstr,exp=exp, frag=flstr)
        return clf        
        
    prerep = flstr[:maxj]
    
    clf.setclf(repetend=xstr[-replen:], repcnt=repcnt, prerep=prerep, exp=exp, frag=flstr)
    return clf

    
def gcd(x, y):
    while y:
        z,x=x,y
        y=z%y
    return x
    
def yuefen(x, y):
    zdgys = gcd(x, y)
    return (x/zdgys, y/zdgys) if zdgys != 1 else (x, y)

def calcresult(clf):
    if clf is not None:
        if clf.replen > 0:
            x, y, z = int(clf.repetend),'9'*clf.replen, clf.prerep
            z *= int(y)
            y += '0'*clf.prelen
#            print x, y, z
            x += z
            y = int(y)
        else:
            x, y = clf.prerep, 10**clf.prelen
         
        return yuefen(x, y)
    else:
        return (0,0)

def gauss(clf):
    if clf is None:
        return {}
    if len(clf.frag) > 3 and clf.repcnt*clf.replen<6:
        loclf = CutLoopFloat()
        loclf.setclf(exp=clf.exp)
        
        optYF, loopI, bestPair = int(clf.frag)*10, 0, (0,0)
        for i in xrange(len(clf.frag)):
            loclf.setclf(repetend=clf.frag[-i:], repcnt=2, prerep=clf.frag[:-i], frag=clf.frag+clf.frag[-i:])
            elem = calcresult(loclf)
            if optYF > elem[0]+elem[1]:
                optYF = elem[0] + elem[1]
                bestPair = elem
                loopI = i
        
        print "%s/%s  "%bestPair, loopI
        print clf.frag
    else:
        big = calcresult(clf)
        return {}

    
if __name__ == '__main__':
#     txt = str(1.0/7)#p(4,2,1))#1000000000/12) #p(1,2,3))
#     print txt
#     clf = cutLoopFloat(txt)
#     print clf.__dict__
#     gauss(clf)
#     print "%s/%s"%calcresult(clf)
    
    
    print p(30,40,10), 40/70.0
