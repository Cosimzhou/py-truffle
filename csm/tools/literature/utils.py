#coding:UTF-8
'''
Created on 2016年3月17日

@author: zhouzhichao
'''
import sys
sys.path.append("/Users/zhouzhichao/workspace/python")
from csm.tools.literature.data import LD_Yun, LD_YunBu2YinDiao

def num2hz(num):
    txt = '零一二三四五六七八九'
    units = '个十百千万'
    result, unit = '', 0
    if type(num) is int and num >= 0:
        while num > 0:
            bit, num = num % 10, int(num / 10)
            if num == 0:
                unit = 0
            else:
                result = units[unit*3:unit*3+3] + txt[bit*3:bit*3+3] + result
            unit += 1
    return result

def yun2pz(yun): 
    yin = LD_YunBu2YinDiao.get(yun)
    if yin is None: return '@'
    return '_'if yin[-3:]=='平'else'*'

def pz4char(char, sentence, idx):
    yb = LD_Yun.get(char)
    if yb is None: return '@'
    if len(yb) > 1:
        print '“%s”中的第%d个字，‘%s’字没有找到适当的解释'%(sentence, idx+1, char)
        chc = 1
        for k, v in yb.items():
            print '%d. %s(%s韵)'%(chc, '其它' if k[0]=='*' else k, v)
            chc += 1
        chc = int(raw_input('选择适意(1~%d):'%len(yb)))
        yun = yb.items()[chc-1][1]
    else:
        yun = yb.get('*')
#     if yun is None: 
#     
#         exit(1)
    diao = LD_YunBu2YinDiao.get(yun)
    if diao is None: return '@'
    return '_' if diao[3:] == '平' else '*'
    
def yb4char(char, sentence, idx):
    yb = LD_Yun.get(char)
    if yb is None: return '@'
    if len(yb) > 1:
        print '“%s”中的第%d个字，“%s”字没有找到适当的解释'%(sentence, idx+1, char)
        chc = 1
        for k, v in yb.items():
            print '%d. %s(%s韵)'%(chc, '其它' if k[0]=='*' else k, v)
            chc += 1
        chc = int(raw_input('选择适意(1~%d):'%len(yb)))
        yun = yb.items()[chc-1][1]
    else:
        yun = yb.get('*')
    return yun
    
def pz4sentence(sentence):
    pzsentence = ''
    for i in range(0,len(sentence),3):
        char = sentence[i:i+3]
        pz = pz4char(char, sentence, i/3)
        if type(pz) is dict:
            pzsentence += '@'
            continue
        pzsentence += pz
    return pzsentence


def matchFormat(cur, fmt, text=None):
    idx, mistake = 0, 0
    for f in fmt:
        if f == '^':
            pass
        elif f == '@':
            pass
        elif idx < len(cur) and cur[idx] != f:
            mistake += 1
        idx += 1
    return mistake