#coding: UTF-8

TianGan=tuple("甲,乙,丙,丁,戊,己,庚,辛,壬,癸".split(","))
DiZhi=tuple("子,丑,寅,卯,辰,巳,午,未,申,酉,戌,亥".split(","))
ShengXiao=tuple("鼠,牛,虎,兔,龙,蛇,马,羊,猴,鸡,狗,猪".split(","))
GanZhi=tuple("%s%s"%(TianGan[i%10], DiZhi[i%12]) for i in xrange(60))
txtnayin="海中金,炉中火,大林木,路旁土,剑锋金,山头火,"\
"涧下水,城头土,白蜡金,杨柳木,泉中水,屋上土,霹雳火,松柏木,"\
"长流水,砂石金,山下火,平地木,壁上土,金箔金,灯头火,天河水,"\
"大驿土,钗钏金,桑柘木,大溪水,沙中土,天上火,石榴木,大海水"
NaYin=tuple(txtnayin.split(","))

class scale(object):
    TextArray = None
    rev_TextArray = None
    def __init__(self, name=None, index=None):
        if name is not None:
            self.index = self.rev_TextArray[name]
        else:
            self.index = int(index)
            
    def __nonzero__(self):
        return type(self.index) is int and 0<=self.index<len(self.TextArray)
    
    def __repr__(self):
        return self.TextArray[self.index] if self.__nonzero__() else "<bad>"
    
    def __cmp__(self, obj):
        return self.index == object.index
     
    def __lt__(self, obj):# and 小于/小于或等于；对应<及<=操作符
        return self.index < obj.index
    def __le__(self,obj):
        return self.index <= obj.index
    def __gt__(self, obj):# and 大于/大于或等于；对应>及>=操作符
        return self.index > obj.index
    def __ge__(self,obj):
        return self.index >= obj.index
    def __hash__(self):  
        print "%s:%s"%(type(self), self.index)
        return hash("%s:%s"%(type(self), self.index))  
    def __eq__(self, obj):# and 等于/不等于；对应==,!=及<>操作符
        return type(self)==type(obj) and self.index == obj.index
    def __ne__(self,obj):
        return self.index != obj.index
    
    def set(self, text):
        tmp = self.rev_TextArray[text]
        if tmp is not None:
            self.index = tmp
    
    def add(self, val):
        if self.__nonzero__():
            self.index += val
            self.index %= len(self.TextArray)
            
    def sub(self, val):
        if self.__nonzero__():
            self.index -= val
            self.index %= len(self.TextArray)
        
    def legal(self, obj):
        return (type(obj) is type(self)) and obj.__nonzero__()
    
    @staticmethod
    def revArrayToDict(arr):
        return {arr[i]:i for i in range(len(arr))}

class wuxing(scale):
    TextArray = tuple("木,火,土,金,水".split(","))
    rev_TextArray = scale.revArrayToDict(TextArray)

    def __init__(self, name=None, index=None):
        super(wuxing, self).__init__(name=name, index=index)
    
    @property
    def sheng(self):
        if self.__nonzero__():
            return wuxing(index=(self.index+1)%5)
    @property
    def ke(self):
        if self.__nonzero__():
            return wuxing(index=(self.index+2)%5)
        
    def issheng(self, wx):    
        return self.legal(wx) and self.__nonzero__() and (self.index == (wx.index+4)%5)
    
    def iske(self, wx):    
        return self.legal(wx) and self.__nonzero__() and (self.index == (wx.index+3)%5)

    def xiangsheng(self, wx):
        return self.legal(wx) and (self.issheng(wx) or wx.issheng(self))

    def xiangske(self, wx):
        return self.legal(wx) and (self.iske(wx) or wx.iske(self))
    
    
class tiangan(scale):
    TextArray = TianGan
    rev_TextArray = scale.revArrayToDict(TextArray)
    def __init__(self, name=None, index=None):
        super(tiangan, self).__init__(name=name, index=index)
   
    @property
    def shu(self):
        if self.__nonzero__():
            return wuxing(index=int(self.index/2)%5)
        
class dizhi(scale):
    TextArray = DiZhi
    rev_TextArray = scale.revArrayToDict(TextArray)
    def __init__(self, name=None, index=None):
        super(dizhi, self).__init__(name=name, index=index)
   
    @property
    def shu(self):
        if self.__nonzero__():
            if self.index % 3 == 1:
                return wuxing("土")
            else:
                idx = (self.index+10) % 12
                if idx > 4:
                    idx += 3
                return wuxing(index=int(idx/3))
            
    @property
    def xiao(self):
        if self.__nonzero__():
            return shengxiao(index=self.index)

class shengxiao(scale):
    TextArray = ShengXiao
    rev_TextArray = scale.revArrayToDict(TextArray)
    def __init__(self, name=None, index=None):
        super(shengxiao, self).__init__(name=name, index=index)
    
    @property
    def zhi(self):
        if self.__nonzero__():
            return dizhi(index=self.index)
        
        
class ganzhi(scale):
    TextArray = GanZhi
    rev_TextArray = scale.revArrayToDict(TextArray)
    def __init__(self, name=None, index=None, gan=None, zhi=None):
        if name is None and gan is not None and zhi is not None:
            name = "%s%s"%(gan,zhi)
        super(ganzhi, self).__init__(name=name, index=index)
    
    @property
    def gan(self):
        if self.__nonzero__():
            return tiangan(index=self.index%10)

    @property
    def zhi(self):
        if self.__nonzero__():
            return dizhi(index=self.index%12)

    @property
    def yin(self):
        if self.__nonzero__():
            return nayin(index=self.index/2)

class nayin(scale):
    TextArray = NaYin
    rev_TextArray = scale.revArrayToDict(TextArray)
    def __init__(self, index=None, name=None, gan=None, zhi=None):
        if name is None and gan is not None and zhi is not None:
            gz = ganzhi("%s%s"%(gan,zhi))
            if gz:
                index = gz.index/2
        
        super(nayin, self).__init__(name=name, index=index)
    @property
    def wuxing(self):
        if self.__nonzero__():
            return wuxing(self.__repr__()[6:])
        
if __name__ == '__main__':
    from csm.gcal.celest.Shuoqi import Shuoqi
    from csm.gcal.Julian import JDate
    from math import floor
#     jnow = JDate(1987,9,6,8,15)#JDate.now()
    jnow = JDate(1987,11,20,21,30)
#     jnow = JDate(1954,1,31,17,30)#二舅
#     jnow = JDate(1933,6,3,10,30)#姥姥
#     jnow = JDate(1956,10,2,4,30)#三舅
#     jnow = JDate(1960,2,16,21,30)#姨
#     jnow = JDate(1963,3,13,23,30)#老妈
#     jnow = JDate(1961,11,2)
#     jnow = JDate(1961,12,20,0,30)#老爹
#     jnow = JDate(2014,11,6,22,50)
#     jnow = JDate(2015,8,20,13,58)

    s = JDate(2014,12,20)
    e = JDate(2016,3,7)

    print e.julian - s.julian
    s.julian +=500
    print s

    jnow = JDate(2015,8,4,4,58)
    today = JDate.now()
    
    a = Shuoqi(lunar='1987年九月廿九')
    print a.julian
    
    m1st = JDate(2014,12,20)
    print "今天是第%d天"%(int(today.julian - m1st.julian) + 1)
    
#     if a.julian:
#         jnow = a.julian
#     jnow = JDate(2015,8,27,12,30)
    
    days = today.julian - jnow.julian 
    print "今天是您出生的第%d天"%floor(days+1)
    ssq = Shuoqi(jnow)
    n = ssq.year-1984
    a, b = ganzhi(index=n%60), ganzhi(index=(12*n+ssq.getMonth(jnow)-1)%60)
    dt = jnow-JDate(2014,12,18,23)
    c, d = ganzhi(index=floor(dt.days)%60), ganzhi(index=floor(dt.hours/2)%60)
    
    wx8z = (a.gan.shu, a.zhi.shu, b.gan.shu, b.zhi.shu, c.gan.shu, c.zhi.shu, d.gan.shu, d.zhi.shu) 
    print ssq.dateDescription #"%d年%s%s"%(ssq.year, ssq.getMonth(jnow,True), ssq.day)
    
    print a, b, c, d
    print a.yin, b.yin, c.yin, d.yin
    print "%s%s %s%s %s%s %s%s"%wx8z
    allwx = set(list("金,木,水,火,土".split(",")))
    ass = set([])
    [ass.add(str(i)) for i in wx8z]
    for i in (a,b,c,d):
        ass.add(str(i.yin.wuxing))
    diff=allwx-ass
    
    if diff:
        print "命理缺%s"%reduce(lambda x,y:"%s,%s"%(x,y), list(diff))
    
    