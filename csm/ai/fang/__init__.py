#coding: UTF-8

# xc={'契税':1.5,'契税':}

class Fang(object):
    def __init__(self):
        self.area = 0
        self.danjia = 100
        self.new = 0 
        self.md = {}
    
    #面积
    @property 
    def MianJi(self):
        return self.area
    
    #交易费
    @property
    def JiaoYiFei(self):
        return 3*self.MianJi
    
    #成交价格
    @property
    def ChengJiaoJiaGe(self):
        return 0
    
    #印花税
    @property
    def YinHuaShui(self):
        return self.ChengJiaoJiaGe/2000.0
    
    #登记费
    @property
    def DengJiFei(self):
        return 80
    
    #核档费
    @property
    def HeDangFei(self):
        return 50
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def parse(self, aa):
        lmbd = self.md.get(aa)
        
        if type(lmbd) is float or type(lmbd) is int:
            return str(lmbd)
        else:
            return lmbd
    
    def aaa(self, s):
        ss, key = '', ''
        for c in s:
            if c == ' ':
                pass
            elif c in '+-*/^.0123456789':
                if key:
                    ss += self.parse(key)
                    key = ''
                ss += c
            else:
                key += c
                
        return eval(ss)
    
    
    
def trans(txt):
    cmd = ''
    i = 0
    while i < len(txt):
        c = txt[i]
        if ord(c) > 127:
            for k in 0,1,2: 
                cmd += "_%02X" % ord(txt[i+k])
            i += 3
        else:
            cmd += c
            i += 1
    return cmd
    
def setValue(name, value):
#     dc
    pass

def Eval(txt):
    algo = ''
    for c in txt:
        if ord(c) > 127:
            algo += hex(ord(c))
        else:
            algo += c
    
    
    
    
if __name__ == '__main__':
#     import sys
#     dc = sys._getframe(0).f_locals
#     dc['price']=50
#     print sys._getframe(0).f_locals
#     print eval('price*3')
#     

    cmd = """
单价,面积=3,80
# 总价 = 单价*面积

def 总价():
    return 单价*面积
print 总价()
    """
    
    scmd = trans(cmd)
    print scmd
    exec(scmd)
    

    
    