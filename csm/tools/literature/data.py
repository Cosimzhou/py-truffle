#coding:UTF-8
'''
Created on 2016年3月16日

@author: zhouzhichao
'''
from csm.tools.literature.database import *

LD_BiHua = data_BiHua
LD_Yun=None
LD_YunBu = None 

LD_PingShuiYunBiao = data_PingShuiYunBiao
LD_YunBu2YinDiao = None

LD_JuXingName=data_JuXingName
LD_JuXingMark=None#{'__':'平', '**':'仄', '_*':'弯', '*_':'直',}

LD_JuXing = data_JuXing
LD_JuXing7 = None#{'__':'@_@**__', '**':'@*@__**', '_*':'@_@*__*', '*_':'@*__**_',}


LD_ShiXing=data_ShiXing#('__*_**__', '_**_**__', '**___**_', '*____**_', '__***__*', '_****__*', '**_*__**', '*__*__**', '_***__**', '_***_***')
LD_CiPai = data_CiPai

# init method
if True:
    def addPSY(psy, r, char, yb):
        cd = psy.get(char)
        if cd is None:
            psy[char] = cd = {}
        if r == '*':
            while r in cd:
                r += '*'
        cd[r] = yb
        
    def parseYunBiao(ybiao):
        yb, psy = {}, {}
        for k,v in ybiao.items():
            ybm, v = v.split(':')
            ybh, ybn = ybm[0:6], int(ybm[6:])
            if ybh not in yb:
                yb[ybh] = '   '*50
            yb[ybh] = yb[ybh][:(ybn-1)*3]+k+yb[ybh][ybn*3:]
            
            char, oldChar, inkh = '', '', False
            for c in v:
                if c == '(':
                    inkh = True
                elif c == ')':
                    inkh = False
                    addPSY(psy, char, oldChar, k)
                    char = oldChar = ''
                elif inkh:
                    char += c
                else:
                    char += c
                    if len(char) == 3:
                        if oldChar:
                            addPSY(psy, '*', oldChar, k)
                        oldChar = char
                        char = ''
            if oldChar:
                addPSY(psy, '*', oldChar, k)
        for y in yb:
            yb[y] = yb[y].strip(' ')
#         for k,v in psy.items():
#             print "'%s':{%s},"%(k, ', '.join(map(lambda x:"'%s': '%s'"%x, v.items())))
            
        return psy, yb
    
    LD_Yun, LD_YunBu = parseYunBiao(LD_PingShuiYunBiao)
    # LD_BiHua, LD_Yun, LD_YunBu
#     global LD_YunBu2YinDiao, LD_Yun
    y2d={}
    for d,y in LD_YunBu.items():
        for i in xrange(0, len(y), 3):
            y2d[y[i:i+3]] = d
    LD_YunBu2YinDiao = y2d
    
#     global LD_JuXing7
    jx7, fd = {}, {'*':'_','_':'*'}
    for k in LD_JuXing:
        jx7[k] = '@%s%s'%(k[0], LD_JuXing['%s%s'%(fd[k[0]], k[1])])
    LD_JuXing7 = jx7
    
#     global LD_JuXingMark
    LD_JuXingMark = dict(map(lambda x:(x[1],x[0]), LD_JuXingName.items()))
    
#     """
    
#     for k,v in tmp.items():  
#         if k not in LD_Yun:
#             print k," not found"
#             continue
#         psyv = LD_Yun[k]
#         if len(psyv) != len(v):
#             print k," has different yb"
#         for vk,vv in v.items():
#             if psyv.get(vk) == vv:
#                 continue
#             print psyv.get(vk), vv, vk, " xx"
            
    #"""

if __name__ == '__main__':
#     for z,dic in LD_Yun.items():
#         for p,y in dic.items():
#             d = y2d.get(y)
#             if d:
#                 pass
#             else:
#                 print "err:", z,p,y
#                 exit(1)
        
        
    pass