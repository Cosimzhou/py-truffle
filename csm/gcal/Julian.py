#coding: UTF-8

import datetime 
from math import floor

J2000 = 2451545

class JDate(object): #日期元件
    
    def __init__(self, y=None, m=0, d=0, h=0, n=0, s=0, ms=0):
        if y is None:
            if m is None and d is None:
                return
            y = -4712
        if m == 0 or d == 0:
            if m == 0: m = 1
            if d == 0: d = 1
        
        assert 0<=h<24 and 0<=n<60 and 0<=s<60 and 0<=ms<1000
        self.date = (y, m, d, h, n, s, ms)
        self.julianWorked = False
        d += (((ms/1000.0+s)/60.0+n)/60.0+h)/24.0
        self.jd = JDate.JulianDate(y,m,d)
        
    def __repr__(self):
        if 0 <= self.jd < 1:
            return "%d:%.2d:%.2d.%.3d"%self.date[3:]
        else:
            if self.date[3] == 0 and self.date[4] == 0 and self.date[5] == 0 and self.date[6] == 0:
                return "%d-%d-%d"%self.date[0:3]
            else:
                return "%d-%d-%d %d:%.2d:%.2d.%.3d"%self.date
        
    def __sub__(self, j):
        obj = JDate(None, None, None)
        obj.jd = self.jd-(j.jd if type(j) is JDate else j)
        obj.julianWorked = True
        obj.date = JDate.DateJulian(obj.jd)
        return obj
    def __add__(self, j):
        obj = JDate(None, None, None)
        obj.jd = self.jd+(j.jd if type(j) is JDate else j)
        obj.julianWorked = True
        obj.date = JDate.DateJulian(obj.jd)
        return obj
        
    @property
    def julian(self):
        return self.jd-0.5
    @julian.setter
    def julian(self, j):
        if type(j) in (int, float):
            self.julianWorked = True
            self.jd = j+0.5
            self.date = JDate.DateJulian(j)
            
    @property
    def J2000(self):
        return self.jd-J2000#2451545#(0.5
    @J2000.setter
    def J2000(self, j):
        if type(j) in (int, float):
            j += J2000#2451545
            self.julianWorked = True
            self.jd = j+0.5
            self.date = JDate.DateJulian(j)
    
            
    @property
    def time(self):
        if not self.julianWorked:
            arr = (None,1,1)+self.date[3:]
            return JDate(*arr)
        else:
            obj = JDate(None, None, None)
            obj.jd = self.jd-floor(self.jd)
            obj.julianWorked = True
            obj.date = JDate.DateJulian(obj.jd)
            return obj
    @property
    def week(self):
        return int(floor(self.jd+1)%7)
    
    @property
    def days(self):
        return self.jd
    @property
    def hours(self):
        return self.jd*24
    @property
    def minutes(self):
        return self.jd*24*60
    @property
    def seconds(self):
        return self.jd*24*60*60
    @property
    def milliseconds(self):
        return self.jd*24*60*60*1000
    
    @staticmethod
    def JulianDate(y, m, d):
        return JDate.julianDate(y,m,d)+0.5
    
    @staticmethod
    def julianDate(y, m, d): #公历转儒略日
        n=0
        Gregoryl = False
        if(y*372+m*31+floor(d)>=588829):
            Gregoryl=True #判断是否为格里高利历日1582*372+10*31+15
        if(m<=2): 
            m+=12
            y-=1
        if(Gregoryl):
            n=floor(y/100)
            n=2-n+floor(n/4) #加百年闰
        return floor(365.25*(y+4716)) + floor(30.6001*(m+1))+d+n - 1524.5;

    @staticmethod
    def DateJulian(jd): #儒略日数转公历
        return JDate.dateJulian(jd-0.5)
    
    @staticmethod
    def now(): #儒略日数转公历
        tnow = datetime.datetime.now()
        tdate, ttime = tnow.date(), tnow.time()
#         print (tdate.year, tdate.month, tdate.day, ttime.hour, ttime.minute, ttime.second, ttime.microsecond)
        return JDate(tdate.year, tdate.month, tdate.day, ttime.hour, ttime.minute, ttime.second, ttime.microsecond/1000.0)
    
    @staticmethod
    def dateJulian(jd): #儒略日数转公历
        jd+=0.5        
        D=floor(jd)
        F=jd-D  #取得日数的整数部份A及小数部分F
        if(D>=2299161): 
            c = floor((D-1867216.25)/36524.25)
            D += 1+c-floor(c/4)
        D += 1524
        Y = floor((D-122.1)/365.25)   #年数
        D -= floor(365.25*Y)
        M = floor(D/30.601)    #月数
        D -= floor(30.601*M) #日数
        if(M>13):
            M -= 13
            Y -= 4715
        else:
            M -= 1
            Y -= 4716
        #日的小数转为时分秒
        F*=24;h=floor(F);F-=h
        F*=60;m=floor(F);F-=m
        F*=60;s=floor(F);F-=s
        F*=1000
        return (Y, M, D, h, m, s, int(F))


if __name__ == '__main__':
    j=JDate(2015, 2, 11, 8, 45)
    print j.J2000
    
    print j, j.julian, j.time, j.week
    j=j+j.time
    print j
    
    j.J2000 = 0
    print j

    print JDate.now().J2000
    j = JDate()
    j.J2000= 5543.246366439924#5558.280284798731#5530
    print j
    
    
    m1st = JDate(2014,12,20)
    print "今天是第%d天"%(int(today.julian - m1st.julian) + 1)
    
    
#     print datetime.datetime.now().date().year
#  
#   DD2str:function(r){ #日期转为串
#    Y="     "+r.Y, M="0"+r.M, D="0"+r.D;
#    h=r.h, m=r.m, s=int2(r.s+.5);
#    if(s>=60) s-=60,m+=1;
#    if(m>=60) m-=60,h+=1;
#    h="0"+h; m="0"+m; s="0"+s;
#    Y=Y.substr(Y.length-5,5); M=M.substr(M.length-2,2); D=D.substr(D.length-2,2);
#    h=h.substr(h.length-2,2); m=m.substr(m.length-2,2); s=s.substr(s.length-2,2);
#    return Y+"-"+M+"-"+D+" "+h+":"+m+":"+s;
#   },
#   JD2str:function(jd){ #JD转为串
#    r=this.DD( jd );
#    return this.DD2str( r );
#   },
# 
# 
#   Y:2000, M:1, D:1, h:12, m:0, s:0,
#   toJD:function(){ return this.JDate( this.Y, this.M, this.D+((this.s/60+this.m)/60+this.h)/24 ); }, #公历转儒略日
#   setFromJD:function(jd){  r=this.DD(jd); this.Y=r.Y, this.M=r.M, this.D=r.D, this.m=r.m, this.h=r.h, this.s=r.s;  }, #儒略日数转公历
# 
#   timeStr:function(jd){ #提取jd中的时间(去除日期)
#    h,m,s;
#    jd+=0.5; jd = (jd - int2(jd));
#    s=int2(jd*86400+0.5);
#    h=int2(s/3600); s-=h*3600;
#    m=int2(s/60);   s-=m*60;
#    h="0"+h; m="0"+m; s="0"+s;
#    return h.substr(h.length-2,2)+':'+m.substr(m.length-2,2)+':'+s.substr(s.length-2,2);
#   },
#   #星期相关
#   Weeks : new Array('日','一','二','三','四','五','六','七'),
#   getWeek:function(jd){ return int2(jd+1.5+7000000)%7; }, #星期计算
#   nnweek:function(y,m,n,w){ #求y年m月的第n个星期w的儒略日数
#    jd = JDate.JDate(y,m,1.5); #月首儒略日
#    w0 = (jd+1+7000000)%7;       #月首的星期
#    r  = jd-w0+7*n+w;    #jd-w0+7*n是和n个星期0,起算下本月第一行的星期日(可能落在上一月)。加w后为第n个星期w
#    if(w>=w0) r-=7; #第1个星期w可能落在上个月,造成多算1周,所以考虑减1周
#    if(n==5){
#     m+=1; if(m>12) m=1, y+=1;   #下个月
#     if(r>=JDate.JDate(y,m,1.5)) r-=7; #r跑到下个月则减1周
#    }
#    return r;
#   }
# };