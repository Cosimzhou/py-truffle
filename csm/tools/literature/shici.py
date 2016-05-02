#coding: UTF-8
'''
Created on 2016年3月17日

@author: zhouzhichao
'''
import argparse
import sys

sys.path.append('/Users/zhouzhichao/workspace/python')
from csm.tools.literature.utils import yb4char, yun2pz, num2hz#, pz4sentence, matchFormat
from csm.tools.literature.data import LD_Yun, LD_CiPai, LD_ShiXing, LD_JuXing, LD_JuXing7, LD_PingShuiYunBiao

def genShiFormat(yan=5, lvjue=False, yun=None):
    if yun == True:
        shixing = filter(lambda x:x[-1]=='_', LD_ShiXing)
    elif yun == False:
        shixing = filter(lambda x:x[-1]=='*', LD_ShiXing)
    else:
        shixing = LD_ShiXing
    
    juxing = LD_JuXing7 if yan==7 else LD_JuXing
    
    possibles = []
    for sx in shixing:
        jx, que = [], (2 if lvjue else 1)
        while que:
            for i in xrange(0,8,2):
                jxl = juxing[sx[i:i+2]]
                if jxl[-1] == sx[-1]: jxl += '^'
                jx.append(jxl)
            sx = sx[0] + ('*' if sx[-1] == '_' else '_') + sx[2:]
            que -= 1
        possibles.append(jx)
    return possibles


def matchFormat(cur, fmt, text=None):
    idx, mistake = 0, 0
    for f in fmt:
        if f in '^':
            pass
        elif f == '@':
            pass
        elif idx < len(cur) and cur[idx] != f:
            mistake += 1
        idx += 1
    return mistake

def yunbu4sentence(sentence):
    ysentence = []
    for i in range(0,len(sentence),3):
        char = sentence[i:i+3]
        pz = yb4char(char, sentence, i/3)
        ysentence.append(pz)
    return ysentence

class shiciAnalysis(object):
    def __init__(self, content, cipai):
        self.arrGL = []
        self.arrZ = []
        self.arrY = []
        self.txtCP = ''
        for i in content:
            self.arrY.append(yunbu4sentence(i))
            line = []
            for c in xrange(0,len(i),3):
                line.append(i[c:c+3])
            self.arrZ.append(line)
        
            self.arrGL.append(map(yun2pz, self.arrY[-1]))
        
        self.subtitle, self.yunBu = '', ''
        self.arrGS, self.bestGS = None, None
        if cipai is None:
            pass
        elif cipai in ('5j','五绝','五言绝句'):
            self.arrGS = genShiFormat(yan=5)#, yun=True)
            self.txtCP = '五言绝句'
        elif cipai in ('7j','七绝','七言绝句'):
            self.arrGS = genShiFormat(yan=7, yun=True)
            self.txtCP = '七言绝句'
        elif cipai in ('5l','五律','五言律诗'):
            self.arrGS = genShiFormat(yan=5, lvjue=True, yun=True)
            self.txtCP = '五言律诗'
        elif cipai in ('7l','七律','七言律诗'):
            self.arrGS = genShiFormat(yan=7, lvjue=True, yun=True)
            self.txtCP = '七言律诗'
        elif cipai in LD_CiPai:
            self.subtitle = []
            gs = LD_CiPai[cipai]
            self.arrGS = []
            for g in gs:
                garr = g.split(':') 
                self.subtitle.append(garr[0])
                garr = garr[1].replace(';',',').split(',')
                self.arrGS.append(garr)
        else:
            print '“%s”不是一个可用的诗格或词牌' % cipai
            
    def check(self):
        maxerr, mis, idx, best = 1e5, 0, 0, None
        for p in self.arrGS:
            mis, idx = 0, 0
            for l in p:
                mis += matchFormat(self.arrGL[idx], l)
                idx += 1
            if maxerr > mis:
                best, maxerr = p, mis
        self.bestGS = best
        
        print '\n%s\n' % self.txtCP
        mis, lno = 0, 0
        for l in self.bestGS:
            mis += self.checkFormat(l, lno)
            lno += 1
        
        if mis:
            print '共%d处错误' % mis
        else:
            print '格律通过'   

    def printSentence(self, line):
        markDict = {'@':' ⦿', '_':' ○', '*':' ●', '^':'▵'}
        sbuffer = ''
        for c in self.arrZ[line]:
            sbuffer += c
        print sbuffer, '   ', self.arrY[line][-1] if '^' in self.bestGS[line] else ''
        sbuffer = ''
        for f in self.bestGS[line]:
            sbuffer += markDict[f] if f in markDict else '  '
        print sbuffer
        
    def printGelv(self):
        markDict = {'@':'⦿', '_':'○','*':'●', '^':'▵'}
        
        print '%s\n' % self.txtCP
        for gs in self.arrGS:
            for l in gs:
                sbuffer = ''
                for f in l:
                    sbuffer += markDict[f] if f in markDict else ''
                print sbuffer
            print '\n--------------\n'

    # cur, fmt, yun
    def checkFormat(self, fmt, line):
        self.printSentence(line)
        
        idx, mistake = 0, 0
        for f in fmt:
            if f == '(':
                pass
            elif f == '^':
                if self.yunBu:
                    if self.arrY[line][-1] != self.yunBu:
                        mistake += 1
                        print '\t错韵：'
                else:
                    self.yunBu = self.arrY[line][-1]
                continue
            elif f == '@':
                pass
            elif idx < len(self.arrGL[line]) and self.arrGL[line][idx] != f:
                mistake += 1
                print idx, len(self.arrGL[line]), self.arrGL[line][idx], f
                print '\t“%s”字声%s,平仄不合'%(self.arrZ[line][idx], '平'if self.arrGL[line][idx]=='_'else'仄')
            idx += 1
        mistake += abs(len(self.arrZ[line])-idx)
        return mistake          


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''诗词格律检查
    诗词检查
    ''')
    
    parser.add_argument('content', metavar='N', type=str, nargs='*', help='诗句的内容，每句以空格分隔')
    parser.add_argument('--sourceCode', '-s', default='GBK', help='输入文件的编码方式，默认为“GBK”')
    parser.add_argument('--cipai', '-c', default=None, help='词牌名，新体诗也自作词牌，如“五绝”、“七律”等')
    parser.add_argument('--yun', '-y', default=None, help='提示汉字所属韵部')
    parser.add_argument('--yunbu', '-Y', default=None, help='查找韵部所属内容')
    args = parser.parse_args()
    
    if args.sourceCode != 'GBK':
        gbkContent = map(lambda x:x.decode(args.sourceCode).encode('GBK'), args.content)
    else:
        gbkContent = args.content
    
    if args.yun is not None:
        yunb = LD_Yun.get(args.yun)
        if yunb:
            if len(yunb) == 1:
                yunb = yunb.items()[0][1]
                print '%s: %s\n\n%s'%(args.yun, yunb, LD_PingShuiYunBiao[yunb].replace(args.yun,'>\033[0;31m%s\033[m<'%args.yun).replace(':','\n\n'))
            else:
                no = 1
                for k,v in yunb.items():
                    print '%d. %s: %s(%s韵)'%(no, args.yun, '原意'if k[0]=='*'else k, v)
                    no += 1
        else:
            print '平水韵表中不存在这个文字“%s”'%args.yun

    if args.yunbu is not None:
        yunb = LD_PingShuiYunBiao.get(args.yunbu)
        if yunb:
            yunbs = yunb.split(':')
            print yunbs[0][:6] + num2hz(int(yunbs[0][6:])) + args.yunbu
            print
            print yunbs[1]
        else:
            print '不存在的韵部，如果查找汉字所属韵部可以使用--yun或-y'
    
    if args.content and args.cipai is None:
        args.cipai = '7j'
    
    sca = shiciAnalysis(args.content, args.cipai)
    if args.cipai is not None and not args.content:
        sca.printGelv()
    
    if args.content:
        sca.check()
        
"""
五言诗的八病：平头、上尾、蜂腰、鹤膝、大韵、小韵、旁纽、正纽。
平头：第一字与第六字同声，第二字与第七字同声
上尾：第五字与第十字同声
蜂腰：第二字与第四字同声
鹤膝：第五字与第十五字同声
大韵：与韵相犯，一联中有与韵同音者
小韵：除韵外，一联中有相犯同音者
旁纽：一联中有同韵母而同声调者，如田延连
正纽：一联中有同韵母而不同声调者，如壬荏衽
"""
    