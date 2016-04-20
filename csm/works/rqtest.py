#! /usr/bin/python
# coding: utf-8
'''
Created on 2014Äê7ÔÂ22ÈÕ

@author: zhouzhichao
'''

import random
from PIL import Image, ImageDraw


INF = float('inf')
CHARN, CHARB ='¡ö', '¡õ'
NBP, BBP = -1,0#False, True
BPARR=(BBP, NBP)

testdata=''

dataCoding = 'utf-8'


def xbin(value, bit=0):
    return ('0'*bit+bin(int(value))[2:])[-bit:]


class polynome(object):
    def __init__(self, **kwargs):
        order = kwargs.get('order')
        value = kwargs.get('value')
        if not order or order < 0: order = 0
        if type(value) is str:
            self.assign(value)
        elif type(value) is int:
            self.assign(bin(value)[2:])
        else:
            self.rates = [False]*order
    def assign(self, value):
        if type(value) is int: value = bin(value)[2:]
        self.rates = map(lambda x: x != '0', value)
        self.rates.reverse()
    def order(self):
        if len(self.rates) <= 0:
            return 0
        for i in xrange(len(self.rates)):
            if self.rates[-1-i]:
                return len(self.rates)-i
        return 0
    def mul(self, poly):
        result = polynome(order=self.order()+poly.order()-1)
        for i in xrange(poly.order()):
            if poly.rates[i]:
                for j in xrange(self.order()):
                    result.rates[i] ^= self.rates[j]
                    i += 1 
        return result
    def clone(self):
        poly = polynome()
        poly.rates = map(lambda x:x, self.rates)
        return poly
    def mod(self, poly):
        if type(poly) is not polynome:
            if type(poly) is not int :
                data = eval('0b'+''.join(map(lambda x: '0' if not x or x=='0' else '1', poly)))
            if data == 0:
                raise Exception('polynome divided by zero')
            data = bin(data)[::-1][:-2]
            poly = polynome(value=data)
        sord, pord = self.order(), poly.order()
        if pord == 0:
            raise Exception('polynome divided by zero')
        if sord < pord:
            return self.clone()
        memory = map(lambda x: x, self.rates[:sord])
        
        assert memory[-1]
        top, genlen = sord, pord

        while top >= genlen:
            for i in xrange(genlen):
                memory[top-i-1] ^= poly.rates[genlen-i-1]
            
            for i in xrange(1,sord):
                if memory[-i]:
                    top = sord-i+1
                    break
            if not memory[top-1]:
                break
        
        for i in xrange(len(memory)):
            if memory[-1-i]:
                top = len(memory)-i
                break
        return polynome(value=''.join(map(lambda x: '1' if x else '0', memory[:top][::-1])))
    def getValue(self):
        value, key = 0, 1
        for i in xrange(len(self.rates)):
            if self.rates[i]:
                value += key
            key *= 2
        return value

    def printf(self, **kFormat):
        if kFormat.get('polynome'):
            result = []
            for i in xrange(len(self.rates)):
                if self.rates[i]:
                    result.append('x^%s'%i)
            if kFormat.get('desc'): result.reverse()
            return '+'.join(result)
        elif kFormat.get('binary'):
            result = (''.join(map(lambda x: '1' if x else '0', self.rates)))
            if kFormat.get('desc'): result = result[::-1]
            return result

class GaloisField(object):
    def __init__(self, bottom, exp=1):
        self.top = bottom**exp
        self.gtop = self.top - 1
        self.gen = 1
        self.module = 2
        self.ord2val = {}
        self.val2ord = {}
    def generate(self, gen, module):
        self.gtop = self.top - 1
        self.gen = gen % self.top
        a, c = polynome(value=gen), polynome(value=gen)
        m = polynome(value=module)
        a2n, uniq = {0:1}, set([1])        
        order = 0
        while order < len(uniq) and len(a2n) < self.gtop:
            order = (order + 1) % self.gtop
            a2n[order] = val = c.getValue()
            c = a.mul(c).mod(m)
            uniq.add(val)
        self.gtop = len(uniq-set([0]))
        self.ord2val = tuple(map(lambda x:a2n[x], xrange(len(a2n))))
        n2a = {v:k for k, v in a2n.items()}
        if n2a.get(self.gtop): n2a[0] = n2a[self.gtop]
        self.val2ord = n2a
    def getOrder(self, value):
        return self.val2ord.get(value%self.top)
    def getValue(self, order):
        return self.ord2val[order%self.gtop]
    def mod(self, value):
        return value % self.gtop
    def mul(self, a, b):
        oa, ob = self.getOrder(a), self.getOrder(b)
        so = (oa+ob) % self.gtop
        return self.getValue(so)
    def add(self, a, b):
        return (a^b)%self.gtop

  




class QR_DataEncoder(object):
    def __init__(self, version = 1):
        self.version = version
        self.mode    = '8-bit'
        self.GF      = GaloisField(2,8)
        self.GF.generate(2, 0x11d)
        self.error   = 0 if 1<=version<=40 else 101        
    def getModeMark(self, name=None):
        dataList = {'eci':'0111', 'digit':'0001', 'alphadigit':'0010',
                    '8-bit':'0100', 'kanji':'1101', 'link':'0011',
                    'fnc1':'0101', 'fnc1.':'1001', 'end':'0000',
                    'chinese':'1101'
                    }
        if not name:
            name = self.mode 
        name = name.lower()
        return dataList.get(name)
    def isFitVersion(self, ver):
        if 1<=ver<=40:
            ver = (ver+7)/17
            versec = (self.version+7)/17
            return ver-versec
        return None
    def shiftVersion(self,verdiff):
        self.version += 17*verdiff
    def fillContent(self, data, length):
        ldata = len(data)
        rest = ldata % 8
        ldata /= 8
        if rest != 0: 
            data += '0'*(8-rest)
            ldata += 1
        if length > ldata:
            length -= ldata
            ll = length / 2
            data += '1110110000010001' * ll
            if length % 2: data += '11101100'
        return data
    @staticmethod
    def getLenOfMarkLen(version, mode):
        mode = mode.lower()
        if mode in ('digit', 'alphadigit', 'chinese','kanji'):
            return int((version+7)/17)*2 + {'d':10,'a':9,'c':8,'k':8}[mode[0]]
        if mode == '8-bit':
            return 8 if version<10 else 16
        else:
            return 0
    def getLengthMarkLen(self, mode=None):
        if not mode: 
            mode = self.mode
        return QR_DataEncoder.getLenOfMarkLen(self.version, mode)
    def encodeInDigitMode(self, content):
        mode = 'digit'
        # add check
        leng = len(content)
        gumi, data = leng/3, ''
        for i in xrange(gumi):
            i = i*3
            text = content[i:i+3]
            data += xbin(text,10)
        rest = leng % 3
        if rest > 0:
            data += xbin(content[-rest:], 3*rest+1)
        # byte counter begin
        lml = self.getLengthMarkLen(mode)
        data = xbin(leng, lml) +data
        data = self.getModeMark(mode)+ data
        assert len(data) == 4+lml+10*gumi+3*rest+(1 if rest else 0)
        return data
    def assertLenDigitMode(self, content):
        leng = len(content)
        gumi, rest = leng / 3, leng % 3         
        return 4+self.getLengthMarkLen('digit')+10*gumi+(0,4,7)[rest]
    def encodeInAlphaDigitMode(self, content):
        def getADIndex(char):
            asc = ord(char)
            if 0x30<=asc<0x39:
                value = asc-0x30
            elif 0x41<=asc<=0x5A:
                value = asc-0x37 #asc-0x41+10
            else:
                value = ' $%*+-./'.index(char) + 36
            return value
        mode = 'alphadigit'
        # add check
        leng, content = len(content), content.upper()
        gumi, lml = leng/2, self.getLengthMarkLen(mode)
        data = self.getModeMark(mode)+xbin(leng, lml) 
        for i in xrange(gumi):
            i *= 2
            text = content[i:i+3]
            value = getADIndex(text[0]) * 45 + getADIndex(text[1])
            data += xbin(value,11)
        rest = leng % 2
        if rest > 0:
            data += xbin(getADIndex(content[-1]), 6)
        assert len(data) == 4+lml+11*gumi+6*rest
        return data 
    def assertLenAlphaDigitMode(self, content):
        leng = len(content)
        gumi, rest = leng / 2, leng % 2  
        return 4+self.getLengthMarkLen('alphadigit')+11*gumi+6*rest
    def encodeIn8BitMode(self, content):
        mode = '8-bit'
        leng, lml = len(content), self.getLengthMarkLen(mode)
        data = self.getModeMark(mode) + xbin(leng, lml)
        for i in content:
            data += xbin(ord(i), 8)        
        assert len(data) == 4+lml+8*leng
        return data
    def assertLen8BitMode(self, content):
        return 4+self.getLengthMarkLen('8-bit')+8*len(content)
    def encodeInKanjiMode(self, content):
        def translate(char):
            ochar = char.encode('gbk')
            char = [ord(ochar[0]), ord(ochar[1])]
            if 0xA1<=char[0]<=0xAA and 0xA1<=char[1]<=0xFE:
                value = (char[0]-0xA1)*0x60+(char[1]-0xA1) 
            elif 0xB0<=char[0]<=0xFA and 0xA1<=char[1]<=0xFE:
                value = (char[0]-0xA6)*0x60+(char[1]-0xA1)
            else:
                value = 64
            return xbin(value, 13) 
        mode, content = 'kanji', content.decode(dataCoding)
        leng, lml = len(content), self.getLengthMarkLen(mode)
        data = self.getModeMark(mode) +'0001'+ xbin(leng, lml) 
        for i in content:
            data += translate(i)
        assert len(data) == 8+lml+13*leng
        return data
    def assertLenKanjiMode(self, content):
        return 8+self.getLengthMarkLen('kanji')+13*len(content.decode(dataCoding))
    def assertLength(self, content):
        funcs= {'alphadigit': self.assertLenAlphaDigitMode, 
                '8-bit':      self.assertLen8BitMode,
                'digit':      self.assertLenDigitMode,
                'kanji':      self.assertLenKanjiMode,
                'chinese':    self.assertLenKanjiMode
                }
        return funcs[self.mode](content)
    #@staticmethod
    def encodeData(self, content):
        funcs= {'alphadigit': self.encodeInAlphaDigitMode, 
                '8-bit':      self.encodeIn8BitMode,
                'digit':      self.encodeInDigitMode,
                'kanji':      self.encodeInKanjiMode,
                'chinese':    self.encodeInKanjiMode
                }
        return funcs[self.mode](content)
    def encode(self, content):
        pass
    
    def getRates(self,pn):#Galois field  
        def add(a, b):
            va, vb = self.GF.getValue(a), self.GF.getValue(b)
            assert va and vb
            vab = va ^ vb
            return self.GF.getOrder(vab)
        if pn <1: return    
        result = [0]*(pn+1)
    
        for k in xrange(1, pn):
            for i in xrange(k, 0, -1):
                result[i] = add(result[i]+k, result[i-1])
            result[0] += k
        result[0]  = self.GF.mod(result[0])
        return result          
    
    def encodeCheckCode(self, data, length):
        rates = map(lambda x: self.GF.getValue(x), self.getRates(length))
        buf = [0] * length
        ldata = len(data) / 8        
        for i in xrange(ldata):
            elem = eval('0b'+data[8*i: 8*i+8])
            xxoo = buf[-1] ^ elem
            for j in xrange(length):
                j = length-1-j
                tmp = self.GF.mul(xxoo, rates[j])
                if j > 0:
                    buf[j] = buf[j-1] ^ tmp
                else:
                    buf[j] = tmp 
        chkcode = ''#reduce(lambda x,y: )
        for elem in buf:
            chkcode = xbin(elem, 8) +chkcode    
        return chkcode
    def encodeBlocksCheckCode(self, data, pieces):
        idx, result = 0, []
        for pair in pieces:
            datalen = pair[0]-pair[2]
            i = 0
            while i < pair[1]:
                msg = data[idx*8: 8*(idx+datalen)]
                result.append(msg + self.encodeCheckCode(msg, pair[2]))
                idx += datalen
                i += 1
        return result 
    

class BCH_Coder(object):
    def __init__(self, m, n, gen = None):
        assert type(m) is int and type(n) is int
        self.error, self.M, self.N = 0, m, n
        self.generator = gen
        if type(self.generator) in (list, tuple):
            self.generator = ''.join(map(lambda x: '1' if x else '0', gen))
        elif type(self.generator) is str:
            self.generator = filter(lambda x: x in '01', gen)
        elif type(self.generator) is int:
            self.generator = bin(gen)[2:]
        else:
            self.error = -1
        if self.error == 0:
            if (len(self.generator) < 2 or '1' not in self.generator):
                self.error = 100
            elif self.M <= self.N or self.N < 1:
                self.error = 101
            self.generator = bin(eval('0b'+self.generator))[::-1][:-2]
    def encode(self, data):
        if self.error or type(data) not in (list, tuple, str, int): return None
        if type(data) is not int:
            data = eval('0b'+''.join(map(lambda x: '0' if not x or x=='0' else '1', data)))
        data = bin(data)[::-1][:-2]
        DMN = self.M-self.N
        memory = ([False]*DMN) + map(lambda x: True if x=='1' else False, data)
        assert memory[-1] or data=='0'
        top = len(memory)
        genlen = len(self.generator)
        while top >= genlen:
            for i in xrange(-1, -(genlen+1), -1):
                if self.generator[i] == '1':
                    memory[top+i] = not memory[top+i]
            top = 0
            for i in xrange(len(memory),0,-1):
                if memory[i-1]:
                    top = i
                    break
        return ''.join(map(lambda x: '1' if x else '0', memory[:DMN][::-1]))
    @staticmethod
    def strXor(str1, str2):
        assert len(str1) == len(str2)
        result = ''
        for i in xrange(len(str1)):
            result += '1' if str1[i]!=str2[i] else '0'
        return result



class QR_Master(object):
    LMQH_BlockList=((0,0,0,0),
                    (1,1,1,1),
                    (1,1,1,1),
                    (1,1,2,2),
                    (2,1,4,2),
                    (2,1,4,4),
                    (4,2,4,4),
                    (4,2,5,6),
                    (4,2,6,6),
                    (5,2,8,8),
                    (5,4,8,8),
                    (5,4,11,8),
                    (8,4,11,10),
                    (9,4,16,12),
                    (9,4,16,16),
                    (10,6,18,12),
                    (10,6,16,17),
                    (11,6,19,16),
                    (13,6,21,18),
                    (14,7,25,21),
                    (16,8,25,20),
                    (17,8,25,23),
                    (17,9,34,23),
                    (18,9,30,25),
                    (20,10,32,27),
                    (21,12,35,29),
                    (23,12,37,34),
                    (25,12,40,34),
                    (26,13,42,35),
                    (28,14,45,38),
                    (29,15,48,40),
                    (31,16,51,43),
                    (33,17,54,45),
                    (35,18,57,48),
                    (37,19,60,51),
                    (38,19,63,53),
                    (40,20,66,56),
                    (43,21,70,59),
                    (45,22,74,62),
                    (47,24,77,65),
                    (49,25,81,68))
    Check_Length = ((0,0,0,0),
                    (10,7,17,13),
                    (16,10,28,22),
                    (26,15,22,18),
                    (18,20,16,26),
                    (24,26,22,18),
                    (16,18,28,24),
                    (18,20,26,18),
                    (22,24,26,22),
                    (22,30,24,20),
                    (26,18,28,24),
                    (30,20,24,28),
                    (22,24,28,26),
                    (22,26,22,24),
                    (24,30,24,20),
                    (24,22,24,30),
                    (28,24,30,24),
                    (28,28,28,28),
                    (26,30,28,28),
                    (26,28,26,26),
                    (26,28,28,30),
                    (28,30,28,26),
                    (28,28,24,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,26,30,30),
                    (28,28,30,28),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30),
                    (28,30,30,30))

    def __init__(self):
        pass
    @staticmethod 
    def size(version):
        return 4*version+17 if 1<=version<=40 else 0
    @staticmethod 
    def size2version(size):
        return (size-17)/4 if 21<=size<=177 and size%4==1 else 0
    @staticmethod 
    def anchorLevel(version):
        return int(version/7)+2 if 1 < version <= 40 else 0
    @staticmethod 
    def funcpatBlock(version):
        if 1 <= version <= 40:
            al = QR_Master.anchorLevel(version)
            counter = 25*(al**2-3) if al > 0 else 0
            if al > 2:
                counter -= 10*(al-2)
            counter += (QR_Master.size(version)-16)*2
            return counter + 192
        return 0
    @staticmethod
    def dataAreaBlock(version):
        if 1<=version<=40:
            return QR_Master.size(version)**2-31-(36 if version>6 else 0)-QR_Master.funcpatBlock(version)
        return 0
    @staticmethod 
    def getVersionAndQualityByDataLength(length, qualevel='L'):
        qualevel = qualevel.upper()
        if qualevel not in 'LMQH': qualevel = 'L'
        qualevels = {'L':(2,3,0,1), 'M':(2,3,0), 'Q':(2,3), 'H':(2,)}[qualevel] 
        for i in xrange(40):
            ver = i+1
            for j in qualevels:
                if length <= QR_Master.dataCaps(ver, j):
                    return (ver, j)
        return None
    @staticmethod 
    def getInfo(version, quality = None):
        info = {'forblock': 31,
                'size':QR_Master.size(version),
                'version': version,
                'verblock': 36 if version >6 else 0,
                'block': QR_Master.funcpatBlock(version),
                'anchor level': QR_Master.anchorLevel(version),
                'content': None,
                'datablock':{'L':QR_Master.splitBlocks(version,1),
                             'M':QR_Master.splitBlocks(version,0),
                             'Q':QR_Master.splitBlocks(version,3),
                             'H':QR_Master.splitBlocks(version,2)
                             }
                }
        
        info['quality'] = 'MLHQ-'[quality%4 if quality is not None else 4]
        info['anchors'] = info['anchor level']**2-3 if info['anchor level'] > 1 else 0
        info['fvsize'] = info['verblock'] + info['forblock']
        info['data'] = info['size']**2 - info['fvsize'] - info['block']
        info['rest'] = info['data'] % 8
        info['capacity'] = info['data'] / 8
        return info
    @staticmethod
    def dataCaps(version, quality):
        if 1<=version<=40 and 0<=quality<4:
            return QR_Master.dataAreaLength(version) - QR_Master.checkCodeLength(version, quality)
        else: return 0
    @staticmethod
    def dataAreaLength(version): 
        return QR_Master.dataAreaBlock(version)/8   
    @staticmethod
    def checkCodeLength(version, quality):
        return QR_Master.LMQH_BlockList[version][quality]*QR_Master.Check_Length[version][quality]
    @staticmethod
    def splitBlocks(version, quality):
        if 1<=version<=40 and 0<=quality<4:
            total = QR_Master.dataAreaBlock(version)/8
            tn = QR_Master.LMQH_BlockList[version][quality]
            chkcode = QR_Master.Check_Length[version][quality]
            num, last = total / tn, total % tn
            if last == 0:
                return ((num, tn, chkcode),)
            else:
                return ((num, tn-last, chkcode),(num+1, last, chkcode)) 
        else:
            return None


class QR_Coder(QR_Master):
    def __init__(self):
        self.version   = 1
        self.versionToSize()
        self.producing = False
        self.matrix    = None
        self.matrix_buf= None
        self.error     = 0
        self.quality   = 0
        self.mask      = 0
    def changeVersion(self, ver):
        self.version   = ver
        self.versionToSize()
        self.producing = False
        self.matrix    = None
        self.matrix_buf= None
        self.error     = 0
        self.quality   = 0
        self.mask      = 0
    def changeQuality(self, qua):
        if type(qua) is str and len(qua):
            qua = qua.upper()
            if qua in 'LMQH':
                qua = {'L':1,'M':0,'H':2,'Q':3}[qua]
            else:
                return 
        self.quality   = qua % 4
    def changeMask(self, mask):
        self.mask      = mask % 8
    def fitData(self, length, level='L'):
        ver_qua = super(QR_Coder, self).getVersionAndQualityByDataLength(length, level)
        self.setVersionQuality(ver_qua)
    def setVersionQuality(self, ver_qua):
        if ver_qua and len(ver_qua) == 2:
            self.changeVersion(ver_qua[0])
            self.changeQuality(ver_qua[1])
    def checkCodeLength(self):
        return super(QR_Coder, self).checkCodeLength(self.version, self.quality)
    def dataCaps(self):
        return super(QR_Coder, self).dataCaps(self.version, self.quality)
    def piecesInfo(self):
        return self.splitBlocks(self.version, self.quality)
    def prepare(self):
        if self.error or self.matrix: return
        self.matrix = self.initBlankMatrix()
    def swapMatrix(self):
        self.matrix, self.matrix_buf = self.matrix_buf, self.matrix
    def showMatrix(self):
        if self.error or not self.matrix: return
        for i in self.matrix:
            print ''.join(map(lambda x: CHARB if x else CHARN, i))
    def outputMatrixPicture(self, path, unit):
        if self.error or not self.matrix: return
        img = Image.new("RGB", (self.size*unit,self.size*unit), 0xFFFFFF)
        draw= ImageDraw.Draw(img)
        for i in xrange(self.size):
            for j in xrange(self.size):
#                 if self.matrix[j][i] == BBP:
                draw.rectangle(((i*unit,j*unit),((i+1)*unit,(j+1)*unit)), self.matrix[j][i])
        img.save(path)        
    def versionToSize(self):
        if 1 <= self.version <= 40:
            self.size = self.version*4+17
            return self.size 
        else:
            self.error = 132
    def sizeToVersion(self):
        if 21 <= self.size <= 177 and self.size % 4 == 1:
            self.version = (self.size-17)/4
            return self.version
        else:
            self.error = 133
    def capacityInfo(self, level):
        if level.upper() not in 'LMQH': return
        
#     def getInfo(self):
#         info = {'forblock': 31,
#                 'size':self.size,
#                 'version': self.version,
#                 'verblock': 36 if self.version >6 else 0,
#                 'block': self.functionPatternAreaBlock(),
#                 'anchor level': self.anchorLevel(),
#                 'content': None
#                 }
#         info['anchors'] = info['anchor level']**2-3 if info['anchor level'] > 1 else 0
#         info['fvsize'] = info['verblock'] + info['forblock']
#         info['data'] = info['size']**2 - info['fvsize'] - info['block']
#         info['rest'] = info['data'] % 8
#         info['capacity'] = info['data'] / 8
#         return info
    def anchorLevel(self):
        if self.error: return None
        if 1 < self.version <= 40:
            return int(self.version/7)+2
        return 0
    def functionPatternAreaBlock(self):
        if self.error: return None
        if 1 <= self.version <= 40:
            al = self.anchorLevel()
            counter = 25*(al**2-3) if al > 0 else 0
            if al > 2:
                counter -= 2*5*(al-2)
            counter += (self.size - 16)*2
            return counter + 64 * 3
        return 0
    def _isOnAnchor(self, x, y):
        al = self.anchorLevel()
        if al < 2 or x<4 or y<4: return False
        disArr = self._anchorDistritionList(al-1)
        lx, ly = 0, 0
        x -= 4        
        if x >= disArr[0]:
            x -= disArr[0]
            lx = 1
        y -= 4        
        if y >= disArr[0]:
            y -= disArr[0]
            ly = 1
        unit = disArr[-1]
        x, lx = x%unit, lx+x/unit
        y, ly = y%unit, ly+y/unit    
        al -= 1
        if (lx == 0 and ly == al) or (lx == al and ly == 0):
            return False
        else:
            return x<5 and y<5
    def isDataArea(self, x, y):
        if self.error: return False
        if self.size <= y or 0 > y: return False
        if self.size <= x or 0 > x: return False
        if x == 6 or y == 6: return False
        if x < 9 and (y < 9 or y >= self.size-8): return False
        if x >= self.size-8 and y < 9: return False
        if self.version > 6:  #°æ±ŸÐÅÏ¢
            if x < 6 and y >= self.size-11: return False
            if y < 6 and x >= self.size-11: return False
            return not self._isOnAnchor(x,y)
        if self.version > 1:
            if self.size-10< x <=self.size-5 and self.size-10< y <=self.size-5: return False
        return True
    def dataAreaPosition(self): #ÊýŸÝÇøÎ»ÖÃ×ø±êµÄÉú³ÉÆ÷
        if self.error: return
        x = y = self.size - 1
        column = self.size -2
        ydir = -1
        while column >= 0:
            yield (y, x)
            if x > column:
                x -= 1
            else:
                y += ydir
                x += 1
            while not self.isDataArea(x, y) and column >= 0:
                if x > column:
                    x -= 1
                else:
                    y += ydir
                    x += 1
                    if y < 0: 
                        ydir = 1
                        column -= 2
                        if column == 5: column = 4
                        x, y= column+1, 0
                    elif y >= self.size:
                        ydir = -1
                        column -= 2
                        if column == 5: column = 4
                        x, y = column+1, self.size-1
    def _anchorDistritionList(self, anchor=None):
        if not anchor: anchor = self.anchorLevel()-1
        sideLength = self.size-13
        unit = float(sideLength)/anchor
        iunit = int(unit)
        anchor -= 1
        if unit == 26.4: unit = 26
        if unit > iunit: iunit+=1
        unit = iunit + iunit % 2
        sf = sideLength - unit*anchor
        return [sf]+[unit]*anchor
    def versionAnchorDistrition(self):  #Ð£ÕýÍŒÐÎÎ»ÖÃ×ø±êµÄÉú³ÉÆ÷
        if self.error: return
        anchor = self.anchorLevel()-1
        if anchor < 1: return
        diffarr = self._anchorDistritionList(anchor)
        x = 6
        for i in xrange(anchor):
            y = 6 
            for j in xrange(anchor):
                if not(i == 0 and j ==0):
                    yield (x,y)
                y += diffarr[j]
            if i != 0:
                yield (x,y)
            x += diffarr[i]
        y = 6
        for i in xrange(anchor):
            y += diffarr[i]
            yield (x,y)
    def checkMatrix(self):
        if type(self.matrix) is not list or type(self.matrix[0]) is not list:
            self.error = 101
            return False
        if len(self.matrix) != len(self.matrix[0]):
            self.error = 102
            return False
        if self.size != len(self.matrix):
            self.error = 150
            return False
        if self.size*4+17 != self.version:
            self.error = 151
            return False
        return True    
    def copyMatrix(self):
        assert self.checkMatrix()
        if self.error: return None
        cpy_mat = []
        for i in xrange(self.size):
            cpy_mat[i] = [NBP] * self.size
            for j in xrange(self.size):
                cpy_mat[i][j] = self.matrix[i][j]
        return cpy_mat
    def initBlankMatrix(self):
        return [[NBP]*self.size for _ in xrange(self.size)]
    def setCorner_sng(self,x,y):
        for i in xrange(7):
            self.matrix[x][y+i] = BBP
            self.matrix[x+6][y+i] = BBP
        for i in xrange(1, 6):
            self.matrix[x+i][y] = BBP
            self.matrix[x+i][y+6] = BBP
            self.matrix[x+i][y+1] = NBP
            self.matrix[x+i][y+5] = NBP
        for i in xrange(2, 5):
            self.matrix[x+1][y+i] = NBP
            self.matrix[x+2][y+i] = BBP
            self.matrix[x+3][y+i] = BBP
            self.matrix[x+4][y+i] = BBP
            self.matrix[x+5][y+i] = NBP
    def setCorner(self):
        if self.error or not self.matrix: return
        leng = lsize = self.size -1
        lsize -= 6
        self.setCorner_sng(0,0)
        self.setCorner_sng(lsize,0)
        self.setCorner_sng(0,lsize)
        lsize -= 1
        for i in xrange(8):
            self.matrix[7][i] = NBP 
            self.matrix[lsize][i] = NBP
            self.matrix[7][leng-i] = NBP 
        for i in xrange(7):
            self.matrix[i][7] = NBP 
            self.matrix[i][lsize] = NBP
            self.matrix[leng-i][7] = NBP        
    def setAnchor_sng(self, x, y):
        x -=2
        y -=2
        for i in xrange(5):
            self.matrix[x][y+i] = BBP
            self.matrix[x+4][y+i] = BBP
        for i in xrange(1, 4):
            self.matrix[x+i][y] = BBP
            self.matrix[x+i][y+4] = BBP
            self.matrix[x+i][y+1] = NBP
            self.matrix[x+i][y+3] = NBP
        self.matrix[x+1][y+2] = self.matrix[x+3][y+2] = NBP
        self.matrix[x+2][y+2] = BBP
    def setAnchor(self):
        if self.error or not self.matrix: return
        vad = self.versionAnchorDistrition()
        if vad:
            for i in vad:
                self.setAnchor_sng(i[0], i[1])
    def setRuler(self):
        if self.error or not self.matrix: return
        for i in xrange(8, self.size-8):
            self.matrix[i][6] = self.matrix[6][i] = BPARR[i%2] 
    def setFormatInfo(self):
        if self.error or not self.matrix: return
        data =  xbin(self.quality,2) + xbin(self.mask,3)  # '00111' #{LMQH->'01','00','11','10'} + masktype
        bch = BCH_Coder(15, 5, '10100110111')
        data += bch.encode(data)
        data = bch.strXor(data, '101010000010010')
        data = map(lambda x: x!='0', data) 
        for i in xrange(8):
            self.matrix[8][i if i<6 else i+1] = BBP if data[i] else NBP
            self.matrix[self.size-i-1][8] = BBP if data[i] else NBP
        for i in xrange(7):
            i += 8
            self.matrix[15-(i if i<9 else i+1)][8] = BBP if data[i] else NBP
            self.matrix[8][self.size-15+i] = BBP if data[i] else NBP
        self.matrix[self.size-8][8] = BBP
    def setVersionInfo(self):
        if self.error or not self.matrix: return
        if self.version < 7: return
        data = xbin(self.version, 6)
        bch = BCH_Coder(18, 6, '1111100100101')
        chkcode = bch.encode(data)
        data = map(lambda x: x!='0', (data+chkcode)[::-1])
        startColumn = self.size-11 
        for i in xrange(18):
            self.matrix[startColumn+i%3][i/3] =  BBP if data[i] else NBP
            self.matrix[i/3][startColumn+i%3] =  BBP if data[i] else NBP       
    def randMatrix(self):
        for i in xrange(self.size):
            for j in xrange(self.size):
                self.matrix[i][j] ^= BPARR[random.randint(0,10)%2]
    @staticmethod
    def generateMask(race):
        maskList = ((lambda x,y: (x+y)%2==0),
                    (lambda x,y: x%2==0),
                    (lambda x,y: y%3==0),
                    (lambda x,y: (x+y)%3==0),
                    (lambda x,y: (x/2+y/3)%2==0),
                    (lambda x,y: (x*y)%2+(x*y)%3==0),
                    (lambda x,y: ((x*y)%2+(x*y)%3)%2==0),
                    (lambda x,y: ((x*y)%3+(x+y)%2)%2==0)
                    )
        return maskList[race]
    def fillData(self, datas):
        pieceInfo = self.piecesInfo()
        totalGumi = pieceInfo[0][1]
        dataRest, dataNotFix = -1, True
        if len(pieceInfo) == 2:
            totalGumi += pieceInfo[1][1]
            dataRest = totalGumi * (pieceInfo[0][0] - pieceInfo[0][2]) * 8
        assert totalGumi == len(datas)
        idx, ibyte, igroup, gidx = 0, 0, 0, 0
        func = self.generateMask(self.mask)
        for i in self.dataAreaPosition():
            x, y = i
            if ibyte*8+gidx >= len(datas[igroup]):
                cdata = '0'
            else:
                cdata = datas[igroup][ibyte*8+gidx]
            self.matrix[x][y] = BBP if (cdata=='1')^func(x,y) else NBP
            idx += 1
            gidx += 1
            if idx % 8 == 0: 
                igroup += 1
                gidx = 0
                if 0 < dataRest < idx and igroup == pieceInfo[0][1]:
                    ibyte += 1
                if igroup == totalGumi:
                    igroup = 0
                    if dataNotFix:
                        ibyte += 1
                    if dataNotFix and dataRest == idx:
                        igroup = pieceInfo[0][1]
                        dataRest += pieceInfo[1][1] * 8
                        dataNotFix = False

                     
                
    def evaluateMatrix(self):
        N=(0,3,3,40,10) 
        avalst=(BBP,NBP,BBP,BBP,BBP,NBP,BBP)
        goback=(0,  1,  0,  2,  2,  1,  0)   
        total = 0.0
        for i in xrange(self.size):
            score = [0.0]*4
            same = [0] * 6
            if self.matrix[i][0]:same[2] = same[4] = 1
            if self.matrix[0][i]:same[3] = same[5] = 1
            for j in xrange(1, self.size):
                if j+1 < self.size:
                    if self.matrix[i][j] == self.matrix[i][j+1]:
                        same[0] += 1
                    else:
                        if same[0] >= 5:
                            score[0] += same[0]-5+N[1]
                        same[0] = 0
        
                    if self.matrix[j][i] == self.matrix[j+1][i]:
                        same[0] += 1
                    else:
                        if same[0] >= 5:
                            score[0] += same[0]-5+N[1]
                        same[0] = 0    
                    
                if self.matrix[i][j] == avalst[same[2]]:
                    same[2] += 1
                    if same[2] == 7:
                        score[2] += 1
                        same[2] = 1
                else:
                    same[2] = goback[same[2]]
                if self.matrix[i][j] == avalst[same[4]]:
                    same[4] += 1
                    if same[4] == 7:
                        score[2] += 1
                        same[4] = 1
                else:
                    same[4] = 0
                
                if self.matrix[j][i] == avalst[same[3]]:
                    same[3] += 1
                    if same[3] == 7:
                        score[3] += 1
                        same[3] = 1
                else:
                    same[3] = goback[same[3]]
                if self.matrix[j][i] == avalst[same[5]]:
                    same[5] += 1
                    if same[5] == 7:
                        score[3] += 1
                        same[5] = 1
                else:
                    same[5] = 0  
                    
                score[3] *= N[3]                          
                score[2] *= N[3]            
            total += sum(score)
    
        for i in xrange(self.size-1):
            for j in xrange(self.size-1):
                if self.matrix[i][j] == self.matrix[i][j+1] and self.matrix[i][j] == self.matrix[i+1][j+1] and self.matrix[i][j] == self.matrix[i+1][j]:
                    #find one
                    pass
                   
        total += sum(score)        
        return total




    
if __name__ == '__main__':    
    raw = '一对来自加拿大的夫妻间谍隐秘窃取中国国家机密被隶属于中国国家安全部辽宁丹东安全局带走审查，信息显示，这两个人在中国有年的生活经历，这已足够了解，评估中国发展情况，追踪测绘中国境况，其所在边境的咖啡馆已成为向外输出情报的据点，在中国境内他们是否还有联络人，这需要等待审查结果。'
    #raw = 'aaaaaaaaaaaaajiewjoirwjeoijrwoiejijsvkaknkjneuifujewifjkdsjkjasdifjwoiejfoiwjeoifaaaaaaaaaaaaaaaaaaaaajiewjoirwjeoijrwoiejijsvkaknkjneuifujewifjkdsjkjasdifjwoiejfoiwjeoifaaaaaaaaaaaaaaaaaaaaajiewjoirwjeoijrwoiejijsvkaknkjneuifujewifjkdsjkjasdifjwoiejfoiwjeoif'
    #raw = 'Hello world!\nHello world!\nHello world!\nHello world!\nHello world!\nHello world!\nHello world!\nHello world!\nHello world!\nHello world!\nHello world!\nHello world!\nHello world!\nHello world!\n'
    print len(raw)
    level, mode = 'L', '8-bit'#'kanji'#
    qrd = QR_DataEncoder()
    qrc = QR_Coder()
    qrd.mode = mode
    while True:
        ldata = qrd.assertLength(raw)
        lbyte = ldata / 8 + (1 if ldata % 8 else 0)
        vq = qrc.getVersionAndQualityByDataLength(lbyte, level)
        vdiff = qrd.isFitVersion(vq[0])
        if vdiff == 0:
            qrc.setVersionQuality(vq)
            break
        qrd.shiftVersion(vdiff)
         
    data = qrd.encodeData(raw)
 
     
    pinfo = qrc.piecesInfo()
    print qrc.dataCaps(), qrc.checkCodeLength()
    data = qrd.fillContent(data, qrc.dataCaps())
    datas = qrd.encodeBlocksCheckCode(data, pinfo)
    print datas
    print data+qrd.encodeCheckCode(data, 10)
     
    minscore, minmask = INF, 0
    qrc.prepare()
     
    qrc.setCorner()
    qrc.setAnchor()
    qrc.setRuler()
    qrc.setVersionInfo()
     
    for mask in xrange(8):
        qrc.changeMask(mask)
        qrc.fillData(datas) 
        qrc.setFormatInfo()
         
#         qrc.setCorner()
#         qrc.setAnchor()
#         qrc.setRuler()
#         qrc.setVersionInfo()
         
                     
        score = qrc.evaluateMatrix()
        if score < minscore:
            minscore, minmask = score, mask
         
        qrc.outputMatrixPicture('/home/zhouzhichao/test-%s.png'%mask, 3)
         
    print 'Best index: %s, %s'%(minmask, minscore)
 
    info = qrc.getInfo(qrc.version, qrc.quality)
    for key in info:
        print '%s: %s'%(key, info[key])
 
    import shutil
    shutil.copy('/home/zhouzhichao/test-%s.png'%minmask, '/home/zhouzhichao/test.png')

#     qrc = QR_Coder()
#     qrc.changeVersion(13)
#     qrc.prepare()
#     qrc.setCorner()
#     qrc.setAnchor()
#     qrc.setRuler()
#     qrc.setVersionInfo()  
#     qrc.changeMask(4)  
#     qrc.setFormatInfo()
#     
#     idx = 0
#     for pos in qrc.dataAreaPosition():
#         x, y = pos
#         if idx/8 in (356, 390):
#             qrc.matrix[x][y] = 0xff
#         idx += 1
#         
#     qrc.outputMatrixPicture('/home/zhouzhichao/test-x.png', 3)    
