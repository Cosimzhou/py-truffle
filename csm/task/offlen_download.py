#coding: UTF-8

oo = set()
orr = []
with open('/Users/zhouzhichao/tmp') as f:
    isum = 0
    for i in f.readlines():
        if "POST:at=td" in i:
            s = i.index("vs=1.0&")
            i = i[s+11:]
            arr = i.split('&off=')
            
            for e in arr:
                kr = e.split("&len=")
                ee = (int(kr[0]), int(kr[0])+int(kr[1]))
                for o in orr:
                    if o[0]<ee[0]<o[1] or o[0]<ee[1]<o[1]:
                        print o, ee
                        ee = None
                if ee is not None:
                    orr.append(ee)
#                 if e in oo:
#                     print e
#                 else:
#                     oo.add(e)
                    
#             print arr
            isum += 1
#             print i
        
    print isum