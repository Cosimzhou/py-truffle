#coding: UTF-8

from csm.tools.geotool.geo import *



if __name__ == '__main__':
    mmx, mmy, mxx, mxy = 300, 300, 0, 0
    
    with open('/Users/zhouzhichao/Downloads/bou2-province.log') as f:
        lns = f.readlines()
        i = 2
        while i < len(lns):
            l = lns[i]
            i+= 1
            t = tile(0, 0)
            cnt = int(l.split(':')[1])#924
            for _ in xrange(cnt):
                l = lns[i]
                i+= 1
                b = block()
                b.code = int(l.split(':')[1].split(',')[0])
                check = b.code == 370000
                
                bnt = int(l.split(':')[2])#5784
                for _ in xrange(bnt):
                    l = lns[i]
                    i+= 1
                    ll = l.split(',')
                    p = pt(float(ll[0]), float(ll[1]))
                    b.linearr.append(p)
                    if check:
                        if mmx > p.x: mmx = p.x
                        if mmy > p.y: mmy = p.y
                        if mxy < p.x: mxx = p.x
                        if mxy < p.y: mxy = p.y
                    pass
                t.blocks.append(b)
#             print l
            
    print mmx, mmy, mxx, mxy
    pass