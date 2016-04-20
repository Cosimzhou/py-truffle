#coding: UTF-8

from math import *
from eph0 import *
import math
"""****************************************
以下是天文计算部分,包含有：
物件 SZJ   : 用来计算日月的升起、中天、降落
注意，上述函数或物件是纯天文学的，根据实际需要组合使用可以得到所需要的各种日月坐标，计算精度及计算速度也是可以根据需要有效控制的。
*****************************************"""

#=========日月升降物件=============
class SZJ(object):#日月的升中天降,不考虑气温和气压的影响
    def __init__(self):
        self.L = 0  #站点地理经度,向东测量为正
        self.fa = 0  #站点地理纬度
        self.dt = 0  #TD-UT
        self.E = 0.409092614 #黄赤交角
        self.rts=[]#多天的升中降
        
    def getH(self, h,w): #h地平纬度,w赤纬,返回时角
        c = ( sin(h) - sin(self.fa)*sin(w) ) / cos(self.fa)/cos(w)
        
        return pi if(abs(c)>1)else acos(c)
 

    def Mcoord(self,jd,H0,r): #章动同时影响恒星时和天体坐标,所以不计算章动。返回时角及赤经纬
        z = m_coord( (jd+self.dt)/36525, 40,30,8 )  #低精度月亮赤经纬
        z = llrConv( z, self.E ) #转为赤道坐标
        r.H = rad2rrad( pGST(jd,self.dt) + self.L - z[0] )  #得到此刻天体时角

        if(H0): r.H0 = self.getH( 0.7275*cs_rEar/z[2]-34*60/rad, z[1] )  #升起对应的时角
 
    def Mt(self,jd):     #月亮到中升降时刻计算,传入jd含义与St()函数相同
        self.dt = dt_T(jd)
        self.E  = hcjj(jd/36525)
        jd -= mod2(0.1726222 + 0.966136808032357*jd - 0.0366*self.dt + self.L/pi2, 1)   #查找最靠近当日中午的月上中天,mod2的第1参数为本地时角近似值
        
        r = []
        sv = pi2*0.966
        r.z = r.x = r.s = r.j = r.c = r.h = jd
        self.Mcoord(jd,1,r)     #月亮坐标
        r.s += (-r.H0 - r.H )/sv
        r.j += ( r.H0 - r.H )/sv
        r.z += (    0 - r.H )/sv
        r.x += ( pi - r.H )/sv
        self.Mcoord(r.s,1,r)
        r.s += rad2rrad( -r.H0 - r.H )/sv
        self.Mcoord(r.j,1,r)
        r.j += rad2rrad( +r.H0 - r.H )/sv
        self.Mcoord(r.z,0,r)
        r.z += rad2rrad(     0 - r.H )/sv
        self.Mcoord(r.x,0,r)
        r.x += rad2rrad( pi - r.H )/sv
        return r;

    def Scoord(self,jd,xm,r): #章动同时影响恒星时和天体坐标,所以不计算章动。返回时角及赤经纬
        z = [ E_Lon( (jd+self.dt)/36525, 5 ) + pi - 20.5/rad, 0,1]  #太阳坐标(修正了光行差)
        z = llrConv( z, self.E ) #转为赤道坐标
        r.H = rad2rrad( pGST(jd,self.dt) + self.L - z[0] ) #得到此刻天体时角
    
        if(xm==10or xm==1): r.H1 = self.getH(-50*60/rad,  z[1]) #地平以下50分
        if(xm==10or xm==2): r.H2 = self.getH(-6*3600/rad, z[1]) #地平以下6度
        if(xm==10or xm==3): r.H3 = self.getH(-12*3600/rad,z[1]) #地平以下12度
        if(xm==10or xm==4): r.H4 = self.getH(-18*3600/rad,z[1]) #地平以下18度
 
    def St(self,jd): #太阳到中升降时刻计算,传入jd是当地中午12点时间对应的2000年首起算的格林尼治时间UT
        self.dt = dt_T(jd)
        self.E  = hcjj(jd/36525)
        jd -= mod2(jd + self.L/pi2, 1) #查找最靠近当日中午的日上中天,mod2的第1参数为本地时角近似值
        
        r = []
        sv = pi2
        r_z = r_x = r_s = r_j = r_c = r_h = r_c2 = r_h2 = r_c3 = r_h3 = jd; r_sm = '';
        self.Scoord(jd,10,r); #太阳坐标
        r_s += (-r_H1 - r_H )/sv; #升起
        r_j += ( r_H1 - r_H )/sv; #降落
        
        r_c += (-r_H2 - r_H )/sv; #民用晨
        r_h += ( r_H2 - r_H )/sv; #民用昏
        r_c2+= (-r_H3 - r_H )/sv; #航海晨
        r_h2+= ( r_H3 - r_H )/sv; #航海昏
        r_c3+= (-r_H4 - r_H )/sv; #天文晨
        r_h3+= ( r_H4 - r_H )/sv; #天文昏
        
        r_z += (    0 - r_H )/sv; #中天
        r_x += ( pi - r_H )/sv; #下中天
        self.Scoord(r_s,1,r);  r_s += rad2rrad( -r_H1 - r_H )/sv;  
        if(r_H1==pi): r_sm += '无升起.';
        self.Scoord(r_j,1,r);  r_j += rad2rrad( +r_H1 - r_H )/sv;  
        if(r_H1==pi): r_sm += '无降落.';
        
        self.Scoord(r_c, 2,r); r_c += rad2rrad( -r_H2 - r_H )/sv;  
        if(r_H2==pi): r_sm += '无民用晨.';
        self.Scoord(r_h, 2,r); r_h += rad2rrad( +r_H2 - r_H )/sv;  
        if(r_H2==pi): r_sm += '无民用昏.';
        self.Scoord(r_c2,3,r); r_c2+= rad2rrad( -r_H3 - r_H )/sv;  
        if(r_H3==pi): r_sm += '无航海晨.';
        self.Scoord(r_h2,3,r); r_h2+= rad2rrad( +r_H3 - r_H )/sv;  
        if(r_H3==pi): r_sm += '无航海昏.';
        self.Scoord(r_c3,4,r); r_c3+= rad2rrad( -r_H4 - r_H )/sv;  
        if(r_H4==pi): r_sm += '无天文晨.';
        self.Scoord(r_h3,4,r); r_h3+= rad2rrad( +r_H4 - r_H )/sv;  
        if(r_H4==pi): r_sm += '无天文昏.';
        
        self.Scoord(r_z,0,r);  r_z += (     0 - r_H )/sv;
        self.Scoord(r_x,0,r);  r_x += rad2rrad( pi - r_H )/sv;
        return r;


 
    def calcRTS(self,jd,n,Jdl,Wdl,sq): #多天升中降计算,jd是当地起始略日(中午时刻),sq是时区
        if len(self.rts)==0:
            for i in xrange(31):
                self.rts[i] = [] 
        self.L = Jdl; self.fa = Wdl
        sq /= 24 #设置站点参数
        for i in xrange(n):
            r=self.rts[i]
            r.Ms=r.Mz=r.Mj="--:--:--" 
        for i in xrange(-1, n+1):
            if(i>=0and i<n): #太阳
                r = SZJ.St(jd+i+sq);
                self.rts[i].s = JD.timeStr(r.s-sq); #升
                self.rts[i].z = JD.timeStr(r.z-sq); #中
                self.rts[i].j = JD.timeStr(r.j-sq); #降
                self.rts[i].c = JD.timeStr(r.c-sq); #晨
                self.rts[i].h = JD.timeStr(r.h-sq); #昏
                self.rts[i].ch = JD.timeStr(r.h-r.c-0.5); #光照时间,timeStr()内部+0.5,所以这里补上-0.5
                self.rts[i].sj = JD.timeStr(r.j-r.s-0.5); #昼长

            r = SZJ.Mt(jd+i+sq); #月亮
            c=floor(r.s-sq+0.5)-jd
            if(c>=0 and c<n): self.rts[c].Ms = JD.timeStr(r.s-sq);
            c=floor(r.z-sq+0.5)-jd;  
            if(c>=0 and c<n): self.rts[c].Mz = JD.timeStr(r.z-sq);
            c=floor(r.j-sq+0.5)-jd;  
            if(c>=0 and c<n): self.rts[c].Mj = JD.timeStr(r.j-sq);
        
        self.rts.dn = n;

szj = SZJ()
szj.St(2457066.5)

"""
#========行星天象及星历=============

#大距计算
function xingJJ(xt,t,jing){ #行星的距角,jing为精度控
 var a,z, ga,gz;
 a = p_coord(0, t,10,10,10);  #地球
 z = p_coord(xt,t,10,10,10);  #行星
 z = h2g(z,a); #转到地心
 if(jing==0); #低精度
 if(jing==1){ #中精度
  a = p_coord(0, t,60,60,60);  #地球
  z = p_coord(xt,t,60,60,60);  #行星
  z = h2g(z,a); #转到地心
 }
 if(jing>=2){ #高精度(补光行时)
  a = p_coord(0, t-a[2]*cs_Agx,-1,-1,-1); #地球
  z = p_coord(xt,t-z[2]*cs_Agx,-1,-1,-1); #行星
  z = h2g(z,a); #转到地心
 }
 a[0]+=pi, a[1]=-a[1]; #太阳
 return j1_j2(z[0],z[1],a[0],a[1]);
}
function daJu(xt,t,dx){ #大距计算超底速算法, dx=1东大距,t儒略世纪TD
 var a,b,c;
 if(xt==1) { a=115.8774777586/36525; c=new Array( 2, 0.2, 0.01, 46, 87 ); } #水星
 if(xt==2) { a=583.9213708245/36525; c=new Array( 4, 0.2, 0.01, 382,521); } #金星
 if(dx) b=c[3]/36525;
 else   b=c[4]/36525;
 t = b + a * int2((t-b)/a+0.5); #大距平时间
 var i,dt, r1,r2,r3;
 for(i=0;i<3;i++){
  dt=c[i]/36525;
  r1 = xingJJ(xt,t-dt,i);
  r2 = xingJJ(xt,t,   i);
  r3 = xingJJ(xt,t+dt,i);
  t += (r1-r3)/(r1+r3-2*r2)*dt/2;
 }
 r2+= (r1-r3)/(r1+r3-2*r2)*(r3-r1)/8;
 var re=new Array(t,r2);
 return re;
}

function xingLiu0(xt,t,n,gxs){ #行星的视坐标
 var a,z,E=hcjj(t),zd;
 a = p_coord(0, t-gxs,n,n,n);  #地球
 z = p_coord(xt,t-gxs,n,n,n);  #行星
 z = h2g(z,a); #转到地心
 if(gxs){ #如果计算了光行时，那么也计算章动
  zd=nutation2(t);  #章动计算
  z[0] += zd[0];
  E += zd[1];
 }
 z = llrConv(z,E);
 return z;
}

function xingLiu(xt,t,sn){ #留,sn=1顺留
 var i,y1,y2,y3, n, g;
 #先求冲(下合)
 var hh=cs_xxHH[xt-1]/36525; #会合周期
 var v = pi2/hh; if(xt>2) v = -v; #行星相对地球的黄经平速度
 for(i=0;i<6;i++) t -= rad2rrad( XL0_calc(xt,0,t,8)   -XL0_calc(0,0,t,8) ) / v;  #水星的平速度与真速度相差较多,所以多算几次

 var tt=new Array(5/36525,1/36525,0.5/36525,2e-6,2e-6), dt;
 var tc=new Array(17.4,28,52,82,86,88,89,90);
 tc = tc[xt-1]/36525;

 if(sn){ if(xt>2) t-=tc; else t+=tc; } #顺留
 else  { if(xt>2) t+=tc; else t-=tc; } #逆留
 for(i=0;i<4;i++){
   dt = tt[i], n = 8, g = 0;
   if(i>=3){
     g = y2[2]*cs_Agx;
     n = -1;
   }
   y1 = xingLiu0(xt,t-dt,n, g);
   y2 = xingLiu0(xt,t,   n, g);
   y3 = xingLiu0(xt,t+dt,n, g);
   t += (y1[0]-y3[0])/(y1[0]+y3[0]-2*y2[0])*dt/2;
 }
 return t;
}

#合月计算
function xingMP(xt,t,n,E, g){ #月亮行星视赤经差
  var a,p,m;
  a = p_coord( 0, t-g[1], n,n,n ); #地球
  p = p_coord( xt,t-g[1], n,n,n ); #行星
  m = m_coord(    t-g[0], n,n,n ); #月亮
  p = h2g( p, a );
  m[0] += g[2];  p[0] += g[2];
  m = llrConv( m, E+g[3] );
  p = llrConv( p, E+g[3] );
  var re = new Array( rad2rrad(m[0]-p[0]), m[1]-p[1], m[2]/cs_GS/86400/36525, p[2]/cs_GS/86400/36525*cs_AU ); #赤经差及光行时
  return re;
}
function xingHY(xt,t){ #行星合月(视赤经),t儒略世纪TD
 var i,d,d2,v,E, g=new Array(0,0,0,0);
 for(i=0;i<3;i++){
  d = xingMP(xt,t,8,0.4091, g);
  t -= d[0]/8192;
 }
 E = hcjj(t);
 var zd=nutation2(t);
 g=new Array(d[2], d[3], zd[0], zd[1]); #光行时,章动

 d = xingMP(xt,t,8,E, g);
 d2= xingMP(xt,t+1e-6,8,E, g);
 v = ( d2[0] - d[0] ) / 1e-6; #速度

 d = xingMP(xt,t,30,E, g); t -= d[0]/v;
 d = xingMP(xt,t,-1,E, g); t -= d[0]/v;
 var re = new Array(t,d[1]);
 return re;
}
#合冲日计算(视黄经合冲)
function xingSP(xt,t,n,w0,ts,tp){ #行星太阳视黄经差与w0的差
 var a,p,s;
 a = p_coord( 0, t-tp, n,n,n ); #地球
 p = p_coord( xt,t-tp, n,n,n ); #行星
 s = p_coord( 0, t-ts, n,n,n ); s[0]+=pi; s[1] = -s[1]; #太阳
 p = h2g( p, a );
 var re = new Array( rad2rrad(p[0]-s[0]-w0), p[1]-s[1], s[2]*cs_Agx, p[2]*cs_Agx ); #赤经差及光行时
 return re;
}

function xingHR(xt,t,f){ #xt星体号,t儒略世纪TD,f=1求冲(或下合)否则求合(或下合)
 var i, a,b,v,dt=2e-5;
 var w0=pi, w1=0; #合(或上合)时,日心黄经差为180，地心黄经差为0
 if(f){ #求冲(或下合)
   w0=0; #日心黄经差
   if(xt>2) w1=pi; #地心黄经差(冲)
 }
 v = pi2/cs_xxHH[xt-1]*36525; if(xt>2) v = -v; #行星相对地球的黄经平速度
 for(i=0;i<6;i++) t -= rad2rrad( XL0_calc(xt,0,t,8)   -XL0_calc(0,0,t,8)   -w0 ) / v;  #水星的平速度与真速度相差较多,所以多算几次
 #严格计算
 a = xingSP(xt,t,   8,w1,0,0);
 b = xingSP(xt,t+dt,8,w1,0,0);
 v = (b[0]-a[0])/dt;
 a = xingSP(xt,t,40,w1,a[2],a[3]); t -= a[0]/v;
 a = xingSP(xt,t,-1,w1,a[2],a[3]); t -= a[0]/v;
 var re = new Array(t,a[1]);
 return re;
}

#星历计算

function xingX(xt,jd,L,fa){ #行星计算,jd力学时
 #基本参数计算

 var T=jd/36525;
 var zd = nutation2(T);
 var dL = zd[0], dE = zd[1]; #章动
 var E = hcjj(T) + dE; #真黄赤交角
 var gstPing = pGST2(jd); #平恒星时
 var gst= gstPing + dL*cos(E); #真恒星时(不考虑非多项式部分)

 var z,a,z2,a2,s='';
 var ra,rb,rc,rfn=8;

 if(xt==10){ #月亮
  rfn = 2;
  #求光行时并精确求出地月距
  a = e_coord(T,15,15,15); #地球
  z = m_coord(T,1,1,-1); ra = z[2]; #月亮

  T -= ra*cs_Agx/cs_AU; #光行时计算

  #求视坐标
  a2 = e_coord(T,15,15,15);#地球
  z  = m_coord(T,-1,-1,-1); rc = z[2]; #月亮

  #求光行距
  a2 = h2g(a,a2); a2[2] *= cs_AU;
  z2 = h2g(z,a2); rb = z2[2];

  #地心黄道及地心赤道
  z[0] = rad2mrad(z[0]+dL); 
  s += '视黄经 ' +rad2str(z[0],0) +' 视黄纬 ' +rad2str(z[1],0) +' 地心距 ' +ra.toFixed(rfn)+'\r\n';
  z = llrConv(z,E); #转到赤道坐标
  s += '视赤经 ' +rad2str(z[0],1) +' 视赤纬 ' +rad2str(z[1],0) +' 光行距 ' +rb.toFixed(rfn)+'\r\n';

 }
 if(xt<10){ #行星和太阳
  a = p_coord(0, T,-1,-1,-1); #地球
  z = p_coord(xt,T,-1,-1,-1); #行星
  z[0] = rad2mrad(z[0]);
  s += '黄经一 ' +rad2str(z[0],0) +' 黄纬一 ' +rad2str(z[1],0) +' 向径一 ' +z[2].toFixed(rfn)+'\r\n';

  #地心黄道
  z = h2g(z,a); ra = z[2];  #ra地心距
  T -= ra*cs_Agx; #光行时

  #重算坐标
  a2 = p_coord(0, T,-1,-1,-1); #地球
  z2 = p_coord(xt,T,-1,-1,-1); #行星
  z = h2g(z2,a);  rb = z[2]; #rb光行距(在惯性系中看)
  z = h2g(z2,a2); rc = z[2]; #rc视距
  z[0] = rad2mrad(z[0]+dL); #补章动

  s += '视黄经 ' +rad2str(z[0],0) +' 视黄纬 ' +rad2str(z[1],0) +' 地心距 ' +ra.toFixed(rfn)+'\r\n';
  z = llrConv(z,E); #转到赤道坐标
  s += '视赤经 ' +rad2str(z[0],1) +' 视赤纬 ' +rad2str(z[1],0) +' 光行距 ' +rb.toFixed(rfn)+'\r\n';
 }

 var sj = rad2rrad(gst + L - z[0]); #得到天体时角
 parallax(z, sj,fa, 0); #视差修正
 s += '站赤经 ' +rad2str(z[0],1) +' 站赤纬 ' +rad2str(z[1],0) +' 视距离 ' +rc.toFixed(rfn)+'\r\n';

 z[0] += pi/2-gst-L;  #修正了视差的赤道坐标
 z = llrConv( z, pi/2-fa ); #转到时角坐标转到地平坐标
 z[0] = rad2mrad( pi/2-z[0] );

 if(z[1]>0) z[1] += MQC(z[1]); #大气折射修正
 s += '方位角 ' +rad2str(z[0],0) +' 高度角 ' +rad2str(z[1],0)+'\r\n';
 s += '恒星时 ' +rad2str(rad2mrad(gstPing),1) +'(平) ' +rad2str(rad2mrad(gst),1)+'(真)\r\n';

 return s;
}



#========日月食计算使用的一些函数=============

function lineEll(x1,y1,z1, x2,y2,z2, e,r){ #求空间两点连线与地球的交点(靠近点x1的交点)
  var dx=x2-x1, dy=y2-y1, dz=z2-z1, e2=e*e, A,B,C,D,R,t, p=new Object();
  A = dx*dx + dy*dy + dz*dz/e2;
  B = x1*dx + y1*dy + z1*dz/e2;
  C = x1*x1 + y1*y1 + z1*z1/e2 - r*r;
  p.D = B*B-A*C; if(p.D<0) return p; #判别式小于0无解
  D = sqrt(p.D); if(B<0) D = -D;     #只求靠近x1的交点
  t = (-B+D)/A;
  p.x=x1+dx*t, p.y=y1+dy*t, p.z=z1+dz*t;
  R = sqrt(dx*dx + dy*dy + dz*dz);
  p.R1 = R*abs(t), p.R2 = R*abs(t-1); #R1,R2分别为x1,x2到交点的距离
  return p;
}
function lineEar2(x1,y1,z1, x2,y2,z2, e,r, I){ #I是贝塞尔坐标参数
  var P=cos(I[1]), Q=sin(I[1]);
  var X1=x1, Y1=P*y1-Q*z1, Z1=Q*y1+P*z1;
  var X2=x2, Y2=P*y2-Q*z2, Z2=Q*y2+P*z2;
  var p=lineEll(X1,Y1,Z1, X2,Y2,Z2, e,r);
  p.J=p.W=100;
  if(p.D<0) return p;
  p.J = rad2rrad(atan2(p.y,p.x)+I[0]-I[2]);
  p.W = atan( p.z/e/e/sqrt(p.x*p.x+p.y*p.y) );
  return p;
}

function lineEar(P,Q,gst){ #在分点坐标中求空间两点连线与地球的交点(靠近点P的交点),返回地标
  var p=llr2xyz(P), q=llr2xyz(Q);
  var r=lineEll(p[0],p[1],p[2], q[0],q[1],q[2], cs_ba,cs_rEar);
  if(r.D<0) { r.J=r.W=100; return r; } #反回100表示无解
  r.W = atan( r.z/cs_ba2/sqrt(r.x*r.x+r.y*r.y) );
  r.J = rad2rrad( atan2(r.y,r.x)-gst );
  return r;
}

/****
function cirCir(R,R2,x0,y0){ #两圆的交点,R主圆半径,R2次圆半径,x0,y0次圆圆心
  var re = new Object();
  var d = sqrt(x0*x0+y0*y0);
  var sinB = y0/d, cosB = x0/d;
  var cosA = (R*R+d*d-R2*R2)/(2*d*R);
  if(abs(cosA)>1){ re.n=0; return re; } #无解
  var sinA=sqrt(1-cosA*cosA);
  var c1=R*cosA*cosB, c2=R*sinA*sinB;
  var c3=R*cosA*sinB, c4=R*sinA*cosB;
  re.A=[c1-c2,c3+c4]; #第一个交点
  re.B=[c1+c2,c3-c4]; #第二个交点
  re.n=2;
  return re;
}
****/
function cirOvl(R,ba,R2,x0,y0){ #椭圆与圆的交点,R椭圆长半径,R2圆半径,x0,y0圆的圆心
  var re = new Object();
  var d = sqrt(x0*x0+y0*y0);
  var sinB = y0/d, cosB = x0/d;
  var cosA = (R*R+d*d-R2*R2)/(2*d*R);
  if(abs(cosA)>1){ re.n=0; return re; } #无解
  var sinA = sqrt(1-cosA*cosA);
 
  var k,g,ba2=ba*ba, C,S;
  for(k=-1;k<2;k+=2){
   S = cosA*sinB + sinA*cosB*k;
   g= R - S*S*(1/ba2-1)/2;
   cosA = (g*g+d*d-R2*R2)/(2*d*g);
   if(abs(cosA)>1){ re.n=0; return re; } #无解
   sinA = sqrt(1-cosA*cosA);
   C = cosA*cosB - sinA*sinB*k;
   S = cosA*sinB + sinA*cosB*k;
   if(k==1) re.A=[g*C,g*S]; else re.B=[g*C,g*S];
  }
  re.n=2;
  return re;
}

function lineOvl(x1,y1,dx,dy,r,ba){
  var A,B,C,D,L,t1,t2, p=new Object();
  var f=ba*ba;
  A = dx*dx + dy*dy/f;
  B = x1*dx + y1*dy/f;
  C = x1*x1 + y1*y1/f - r*r;
  D = B*B-A*C; if(D<0) { p.n=0; return p; }#判别式小于0无解
  if(!D) p.n=1; else p.n=2;
  D = sqrt(D);
  t1 = (-B+D)/A, t2 = (-B-D)/A;
  p.A = [x1+dx*t1,y1+dy*t1];
  p.B = [x1+dx*t2,y1+dy*t2];
  L = sqrt(dx*dx + dy*dy);
  p.R1 = L*abs(t1); #x1到交点1的距离
  p.R2 = L*abs(t2); #x1到交点2的距离
  return p;
}

#========太阳月亮计算类=============

var msc={
 calc:function(T,L,fa,high){ #sun_moon类的成员函数。参数：T是力学时,站点经纬L,fa,海拔high(千米)
  #基本参数计算
  self.T=T, self.L=L, self.fa=fa;
  self.dt = dt_T(T); #TD-UT
  self.jd = T - self.dt;    #UT
  T/=36525;
  var zd = nutation2(T);
  self.dL = zd[0];   #黄经章
  self.dE = zd[1];   #交角章动
  self.E  = hcjj(T) + self.dE; #真黄赤交角
  self.gst= pGST(self.jd,self.dt) + self.dL*cos(self.E); #真恒星时(不考虑非多项式部分)
  var z=new Array();

  #=======月亮========
  #月亮黄道坐标
  z=m_coord(T,-1,-1,-1); #月球坐标
  z[0]  = rad2mrad( z[0]+gxc_moonLon(T)+self.dL );  z[1] += gxc_moonLat(T);  #补上月球光行差及章动
  self.mHJ = z[0]; self.mHW = z[1]; self.mR  = z[2]; #月球视黄经,视黄纬,地月质心距

  #月球赤道坐标
  z = llrConv( z, self.E ); #转为赤道坐标
  self.mCJ = z[0]; self.mCW = z[1]; #月球视赤经,月球赤纬

  #月亮时角计算
  self.mShiJ = rad2mrad(self.gst + L - z[0]); #得到此刻天体时角
  if( self.mShiJ>pi ) self.mShiJ -= pi2;

  #修正了视差的赤道坐标
  parallax(z, self.mShiJ,fa, high); #视差修正
  self.mCJ2 = z[0], self.mCW2 = z[1], self.mR2=z[2];

  #月亮时角坐标
  z[0] += pi/2-self.gst-L;  #转到相对于地平赤道分点的赤道坐标(时角坐标)

  #月亮地平坐标
  z = llrConv (z, pi/2-fa );    #转到地平坐标(只改经纬度)
  z[0] = rad2mrad( pi/2-z[0] );
  self.mDJ = z[0]; self.mDW = z[1]; #方位角,高度角
  if(z[1]>0) z[1] += MQC(z[1]); #大气折射修正
  self.mPJ = z[0]; self.mPW = z[1]; #方位角,高度角

  #=======太阳========
  #太阳黄道坐标
  z = e_coord(T,-1,-1,-1);   #地球坐标
  z[0]  = rad2mrad(z[0]+pi+gxc_sunLon(T)+self.dL);  #补上太阳光行差及章动
  z[1]  =-z[1] + gxc_sunLat(T); #z数组为太阳地心黄道视坐标
  self.sHJ = z[0]; self.sHW = z[1]; self.sR  = z[2]; #太阳视黄经,视黄纬,日地质心距

  #太阳赤道坐标
  z = llrConv( z, self.E ); #转为赤道坐标
  self.sCJ = z[0]; self.sCW = z[1]; #太阳视赤经,视赤纬

  #太阳时角计算
  self.sShiJ = rad2mrad(self.gst + L - z[0]); #得到此刻天体时角
  if( self.sShiJ>pi ) self.sShiJ -= pi2;

  #修正了视差的赤道坐标
  parallax(z,self.sShiJ,fa,high); #视差修正
  self.sCJ2=z[0], self.sCW2=z[1], self.sR2=z[2];

  #太阳时角坐标
  z[0] += pi/2-self.gst-L;  #转到相对于地平赤道分点的赤道坐标

  #太阳地平坐标
  z = llrConv( z, pi/2-fa );
  z[0] = rad2mrad( pi/2-z[0] );
  #z[1] -= 8.794/rad/z[2]*cos(z[1]); #直接在地平坐标中视差修正(这里把地球看为球形,精度比parallax()稍差一些)
  self.sDJ = z[0]; self.sDW = z[1]; #方位角,高度角

  if(z[1]>0) z[1] += MQC(z[1]); #大气折射修正
  self.sPJ = z[0]; self.sPW = z[1]; #方位角,高度角

  #=======其它========
  #时差计算
  var t=T/10, t2=t*t,t3=t2*t,t4=t3*t,t5=t4*t;
  var Lon = ( 1753470142 + 6283319653318*t + 529674*t2 + 432*t3 - 1124*t4 - 9*t5 )/1000000000 + pi - 20.5/rad; #修正了光行差的太阳平黄经
  Lon = rad2mrad( Lon - (self.sCJ-self.dL*cos(self.E)) ); #(修正了光行差的平黄经)-(不含dL*cos(E)的视赤经)
  if(Lon>pi) Lon-=pi2; #得到时差,单位是弧度
  self.sc  = Lon/pi2;   #时差(单位:日)

  #真太阳与平太阳
  self.pty = self.jd+L/pi2;  #平太阳时
  self.zty = self.jd+L/pi2+self.sc; #真太阳时

  #视半径
  #self.mRad = XL.moonRad(self.mR,self.mDW);  #月亮视半径(角秒)
  self.mRad = cs_sMoon/self.mR2; #月亮视半径(角秒)
  self.sRad = 959.63/self.sR2; #太阳视半径(角秒)
  self.e_mRad = cs_sMoon/self.mR; #月亮地心视半径(角秒)
  self.eShadow = (cs_rEarA/self.mR*rad-(959.63-8.794)/self.sR )*51/50; #地本影在月球向径处的半径(角秒),式中51/50是大气厚度补偿
  self.eShadow2= (cs_rEarA/self.mR*rad+(959.63+8.794)/self.sR )*51/50; #地半影在月球向径处的半径(角秒),式中51/50是大气厚度补偿
  self.mIll = XL.moonIll(T); #月亮被照面比例

  #中心食计算
  if( abs(rad2rrad(self.mCJ-self.sCJ))<50/180*pi ){
   var pp = lineEar( new Array(self.mCJ,self.mCW,self.mR), new Array(self.sCJ,self.sCW,self.sR*cs_AU), self.gst );
   self.zx_J = pp.J;
   self.zx_W = pp.W; #无解返回值是100
  } else self.zx_J=self.zx_W=100;
 },
 toHTML:function(fs){
  var s = '<table width="100%" cellspacing=1 cellpadding=0 bgcolor="#FFC0C0">';

  s += '<tr><td bgcolor=white align=center>';
  s += '平太阳 ' + JD.timeStr(self.pty) + ' 真太阳 <font color=red>' + JD.timeStr(self.zty) + '</font><br>';
  s += '时差 ' + m2fm(self.sc*86400,2,1) + " 月亮被照亮 " + (self.mIll*100).toFixed(2)+'% ';
  s += '</td></tr>';

  s += '<tr><td bgcolor=white><center><pre style="margin-top: 0; margin-bottom: 0"><font color=blue><b>表一       月亮            太阳</b></font>\r\n';
  s += '视黄经 ' + rad2str(self.mHJ,0) +'  '+ rad2str(self.sHJ,0) + '\r\n';
  s += '视黄纬 ' + rad2str(self.mHW,0) +'  '+ rad2str(self.sHW,0) + '\r\n';
  s += '视赤经 ' + rad2str(self.mCJ,1) +'  '+ rad2str(self.sCJ,1) + '\r\n';
  s += '视赤纬 ' + rad2str(self.mCW,0) +'  '+ rad2str(self.sCW,0) + '\r\n';
  s += '距离     ' + (self.mR).toFixed(2)  +'千米     '+ (self.sR).toFixed(8)+'AU'+'\r\n';
  s += '</pre></center></td></tr>';

  s += '<tr><td bgcolor=white><center><pre style="margin-top: 0; margin-bottom: 0"><font color=blue><b>表二       月亮            太阳</b></font>\r\n';
  s += '方位角 ' + rad2str(self.mPJ,0) +'  '+ rad2str(self.sPJ,0) + '\r\n';
  s += '高度角 ' + rad2str(self.mPW,0) +'  '+ rad2str(self.sPW,0) + '\r\n';
  s += '时角   ' + rad2str(self.mShiJ,0)+'  '+rad2str(self.sShiJ,0)+'\r\n';
  s += '视半径(观测点) ' + m2fm(self.mRad,2,0) +'     '+ m2fm(self.sRad,2,0)+'\r\n';
  s += '</pre></center></td></tr>';

  if(fs){
   s += '<tr><td bgcolor=white align=center>';
   s += '力学时 ' +JD.JD2str(self.T+J2000);
   s += ' ΔT=' + (self.dt*86400).toFixed(1) +'秒<br>';
   s += '黄经章 '+(self.dL/pi2*360*3600).toFixed(2) +'" ';
   s += '交角章 '+(self.dE/pi2*360*3600).toFixed(2) +'" ';
   s += 'ε='+rad2str(self.E,0);
   s += '</td></tr>';
  }
  s += '</table>';
  return s;
 }
};


#====================================
var ysPL={ #月食快速计算器
 lineT:function(G, v,u, r, n){#已知t1时刻星体位置、速度，求x*x+y*y=r*r时,t的值
  var b=G.y*v-G.x*u, A=u*u+v*v, B=u*b, C=b*b-r*r*v*v, D=B*B-A*C;
  if(D<0) return 0;
  D=sqrt(D); if(!n) D=-D;
  return G.t+((-B+D)/A-G.x)/v;
 },
 lecXY:function(jd,re){#日月黄经纬差转为日面中心直角坐标(用于月食)
  var T=jd/36525, zm=new Array(), zs=new Array();

  #=======太阳月亮黄道坐标========
  zs = e_coord(T,-1,-1,-1);   #地球坐标
  zs[0]  = rad2mrad(zs[0]+pi+gxc_sunLon(T));  zs[1]  =-zs[1] + gxc_sunLat(T); #补上太阳光行差
  zm = m_coord(T,-1,-1,-1); #月球坐标
  zm[0]  = rad2mrad( zm[0]+gxc_moonLon(T) );  zm[1] += gxc_moonLat(T);  #补上月球光行差就可以了

  #=======视半径=======
  re.e_mRad = cs_sMoon/zm[2]; #月亮地心视半径(角秒)
  re.eShadow = (cs_rEarA/zm[2]*rad-(959.63-8.794)/zs[2] )*51/50; #地本影在月球向径处的半径(角秒),式中51/50是大气厚度补偿
  re.eShadow2= (cs_rEarA/zm[2]*rad+(959.63+8.794)/zs[2] )*51/50; #地半影在月球向径处的半径(角秒),式中51/50是大气厚度补偿

  re.x = rad2rrad(zm[0]+pi-zs[0]) * cos((zm[1]-zs[1])/2);
  re.y = zm[1]+zs[1];
  re.mr= re.e_mRad/rad,  re.er=re.eShadow/rad, re.Er=re.eShadow2/rad;
  re.t = jd;
 },
 lecMax:function(jd){ #月食的食甚计算(jd为近朔的力学时,误差几天不要紧)
  self.lT=new Array();
  for(var i=0;i<7;i++) self.lT[i]=0; #分别是:食甚,初亏,复圆,半影食始,半影食终,食既,生光
  self.sf=0;
  self.LX='';

  jd = XL.MS_aLon_t2( floor((jd-4)/29.5306)*pi*2 +pi)*36525; #低精度的朔(误差10分钟),与食甚相差10分钟左右

  var g=new Object(), G=new Object(), u,v;

  #求极值(平均误差数秒)
  u = -18461 * sin(0.057109+0.23089571958*jd)*0.23090/rad; #月日黄纬速度差
  v = (XL.M_v(jd/36525)-XL.E_v(jd/36525))/36525; #月日黄经速度差
  self.lecXY(jd,G);
  jd -= (G.y*u+G.x*v)/(u*u+v*v); #极值时间

  #精密求极值
  var dt=60/86400;
  self.lecXY(jd,G); self.lecXY(jd+dt,g); #精密差分得速度,再求食甚
  u = (g.y-G.y)/dt;
  v = (g.x-G.x)/dt;
  dt= -(G.y*u+G.x*v)/(u*u+v*v); jd += dt; #极值时间

  #求直线到影子中心的最小值
  var x=G.x+dt*v, y=G.y+dt*u, rmin=sqrt(x*x+y*y);
  #注意,以上计算得到了极值及最小距rmin,但没有再次计算极值时刻的半径,对以下的判断造成一定的风险,必要的话可以再算一次。不过必要性不很大，因为第一次极值计算已经很准确了,误差只有几秒
  #求月球与影子的位置关系
  if(rmin<=G.mr+G.er){ #食计算
   self.lT[1] = jd; #食甚
   self.LX = '偏';
   self.sf=(G.mr+G.er-rmin)/G.mr/2; #食分

   self.lT[0] = self.lineT(G,v,u, G.mr+G.er, 0); #初亏
   self.lecXY(self.lT[0],g);
   self.lT[0] = self.lineT(g,v,u, g.mr+g.er, 0); #初亏再算一次

   self.lT[2] = self.lineT(G,v,u, G.mr+G.er, 1); #复圆
   self.lecXY(self.lT[2],g);
   self.lT[2] = self.lineT(g,v,u, g.mr+g.er, 1); #复圆再算一次
  }
  if(rmin<=G.mr+G.Er){ #半影食计算
   self.lT[3] = self.lineT(G,v,u, G.mr+G.Er, 0); #半影食始
   self.lecXY(self.lT[3],g);
   self.lT[3] = self.lineT(g,v,u, g.mr+g.Er, 0); #半影食始再算一次

   self.lT[4] = self.lineT(G,v,u, G.mr+G.Er, 1); #半影食终
   self.lecXY(self.lT[4],g);
   self.lT[4] = self.lineT(g,v,u, g.mr+g.Er, 1); #半影食终再算一次
  }
  if(rmin<=G.er-G.mr){ #全食计算
   self.LX = '全';
   self.lT[5] = self.lineT(G,v,u, G.er-G.mr, 0); #食既
   self.lecXY(self.lT[5],g);
   self.lT[5] = self.lineT(g,v,u, g.er-g.mr, 0); #食既再算一次

   self.lT[6] = self.lineT(G,v,u, G.er-G.mr, 1); #生光
   self.lecXY(self.lT[6],g);
   self.lT[6] = self.lineT(g,v,u, g.er-g.mr, 1); #生光再算一次
  }
 }
};

#====================================
/*****
ecFast()函数返回参数说明
r.jdSuo 朔时刻
r.lx    日食类型
*****/
function ecFast(jd){ #快速日食搜索,jd为朔时间(J2000起算的儒略日数,不必很精确)
 var re=new Object();
 var t,t2,t3,t4;
 var L,mB,mR,sR, vL,vB,vR;
 var W = floor((jd+8)/29.5306)*pi*2; #合朔时的日月黄经差

 #合朔时间计算,2000前+-4000年误差1小时以内，+-2000年小于10分钟
 t  = ( W + 1.08472 )/7771.37714500204; #平朔时间
 re.jd = re.jdSuo = t*36525;

 t2=t*t,t3=t2*t,t4=t3*t;
 L = ( 93.2720993+483202.0175273*t-0.0034029*t2-t3/3526000+t4/863310000 )/180*pi;
 re.ac=1, re.lx='N';
 if(abs(sin(L))>0.4) return re; #一般大于21度已不可能

 t -= ( -0.0000331*t*t + 0.10976 *cos( 0.785 + 8328.6914*t) )/7771;
 t2=t*t;
 L = -1.084719 +7771.377145013*t -0.0000331*t2 +
 (22640 * cos(0.785+  8328.6914*t +0.000152*t2)
  +4586 * cos(0.19 +  7214.063*t  -0.000218*t2)
  +2370 * cos(2.54 + 15542.754*t  -0.000070*t2)
  + 769 * cos(3.1  + 16657.383*t)
  + 666 * cos(1.5  +   628.302*t)
  + 412 * cos(4.8  + 16866.93*t)
  + 212 * cos(4.1    -1114.63*t)
  + 205 * cos(0.2  +  6585.76*t)
  + 192 * cos(4.9  + 23871.45*t)
  + 165 * cos(2.6  + 14914.45*t)
  + 147 * cos(5.5    -7700.39*t)
  + 125 * cos(0.5  +  7771.38*t)
  + 109 * cos(3.9  +  8956.99*t)
  +  55 * cos(5.6    -1324.18*t)
  +  45 * cos(0.9  + 25195.62*t)
  +  40 * cos(3.8    -8538.24*t)
  +  38 * cos(4.3  + 22756.82*t)
  +  36 * cos(5.5  + 24986.07*t)
  -6893 * cos(4.669257+628.3076*t)
  -  72 * cos(4.6261 +1256.62*t)
  -  43 * cos(2.67823 +628.31*t)*t
  +  21) / rad;
 t += ( W - L ) / ( 7771.38
  - 914 * sin( 0.7848 + 8328.691425*t + 0.0001523*t2 )
  - 179 * sin( 2.543  +15542.7543*t )
  - 160 * sin( 0.1874 + 7214.0629*t ) );
 re.jd = re.jdSuo = jd = t*36525; #朔时刻

 #纬 52,15 (角秒)
 t2=t*t/10000,t3=t2*t/10000;
 mB=
  18461*cos(0.0571+  8433.46616*t   -0.640*t2    -1*t3)
 + 1010*cos(2.413 + 16762.1576 *t +  0.88 *t2 +  25*t3)
 + 1000*cos(5.440    -104.7747 *t +  2.16 *t2 +  26*t3)
 +  624*cos(0.915 +  7109.2881 *t +  0    *t2 +   7*t3)
 +  199*cos(1.82  + 15647.529  *t   -2.8  *t2   -19*t3)
 +  167*cos(4.84    -1219.403  *t   -1.5  *t2   -18*t3)
 +  117*cos(4.17  + 23976.220  *t   -1.3  *t2 +   6*t3)
 +   62*cos(4.8   + 25090.849  *t +  2    *t2 +  50*t3)
 +   33*cos(3.3   + 15437.980  *t +  2    *t2 +  32*t3)
 +   32*cos(1.5   +  8223.917  *t +  4    *t2 +  51*t3)
 +   30*cos(1.0   +  6480.986  *t +  0    *t2 +   7*t3)
 +   16*cos(2.5     -9548.095  *t   -3    *t2   -43*t3)
 +   15*cos(0.2   + 32304.912  *t +  0    *t2 +  31*t3)
 +   12*cos(4.0   +  7737.590  *t)
 +    9*cos(1.9   + 15019.227  *t)
 +    8*cos(5.4   +  8399.709  *t)
 +    8*cos(4.2   + 23347.918  *t)
 +    7*cos(4.9     -1847.705  *t)
 +    7*cos(3.8    -16133.856  *t)
 +    7*cos(2.7   + 14323.351  *t);
 mB/=rad;

 #距 106, 23 (千米)
 mR = 385001
 +20905*cos(5.4971+  8328.691425*t+  1.52 *t2 +  25*t3)
 + 3699*cos(4.900 +  7214.06287*t   -2.18 *t2   -19*t3)
 + 2956*cos(0.972 + 15542.75429*t   -0.66 *t2 +   6*t3)
 +  570*cos(1.57  + 16657.3828 *t +  3.0  *t2 +  50*t3)
 +  246*cos(5.69    -1114.6286 *t   -3.7  *t2   -44*t3)
 +  205*cos(1.02  + 14914.4523 *t   -1    *t2 +   6*t3)
 +  171*cos(3.33  + 23871.4457 *t +  1    *t2 +  31*t3)
 +  152*cos(4.94  +  6585.761  *t   -2    *t2   -19*t3)
 +  130*cos(0.74    -7700.389  *t   -2    *t2   -25*t3)
 +  109*cos(5.20  +  7771.377  *t)
 +  105*cos(2.31  +  8956.993  *t +  1    *t2 +  25*t3)
 +   80*cos(5.38    -8538.241  *t +  2.8  *t2 +  26*t3)
 +   49*cos(6.24  +   628.302  *t)
 +   35*cos(2.7   + 22756.817  *t   -3    *t2   -13*t3)
 +   31*cos(4.1   + 16171.056  *t   -1    *t2 +   6*t3)
 +   24*cos(1.7   +  7842.365  *t   -2    *t2   -19*t3)
 +   23*cos(3.9   + 24986.074  *t +  5    *t2 +  75*t3)
 +   22*cos(0.4   + 14428.126  *t   -4    *t2   -38*t3)
 +   17*cos(2.0   +  8399.679  *t);
 mR/=6378.1366;

 t=jd/365250, t2=t*t, t3=t2*t;
 #误0.0002AU
 sR = 10001399 #日地距离
 +167070*cos(3.098464 +  6283.07585*t)
 +  1396*cos(3.0552   + 12566.1517 *t)
 + 10302*cos(1.10749  +  6283.07585*t)*t
 +   172*cos(1.064    + 12566.152  *t)*t
 +   436*cos(5.785    +  6283.076  *t)*t2
 +    14*cos(4.27     +  6283.08   *t)*t3;
 sR*=1.49597870691/6378.1366*10;

 #经纬速度
 t=jd/36525;
 vL = 7771 #月日黄经差速度
     -914*sin(0.785 + 8328.6914*t)
     -179*sin(2.543 +15542.7543*t)
     -160*sin(0.187 + 7214.0629*t);
 vB =-755*sin(0.057 + 8433.4662*t) #月亮黄纬速度
     - 82*sin(2.413 +16762.1576*t);
 vR =-27299*sin(5.497 + 8328.691425*t)
     - 4184*sin(4.900 + 7214.06287*t)
     - 7204*sin(0.972 +15542.75429*t);
 vL/=36525, vB/=36525, vR/=36525; #每日速度


 var gm = mR*sin(mB)*vL/sqrt(vB*vB+vL*vL), smR=sR-mR; #gm伽马值,smR日月距
 var mk = 0.2725076, sk = 109.1222;
 var f1 = (sk+mk)/smR, r1 = mk+f1*mR; #tanf1半影锥角, r1半影半径
 var f2 = (sk-mk)/smR, r2 = mk-f2*mR; #tanf2本影锥角, r2本影半径
 var b = 0.9972, Agm = abs(gm), Ar2 = abs(r2);
 var fh2 = mR-mk/f2, h = Agm<1 ? sqrt(1-gm*gm) : 0; #fh2本影顶点的z坐标
 var ls1,ls2,ls3,ls4;

 if(fh2<h) re.lx = 'T';
 else      re.lx = 'A';

 ls1 = Agm-(b+r1 ); if(abs(ls1)<0.016) re.ac=0; #无食分界
 ls2 = Agm-(b+Ar2); if(abs(ls2)<0.016) re.ac=0; #偏食分界
 ls3 = Agm-(b    ); if(abs(ls3)<0.016) re.ac=0; #无中心食分界
 ls4 = Agm-(b-Ar2); if(abs(ls4)<0.016) re.ac=0; #有中心食分界(但本影未全部进入)

 if     (ls1>0) re.lx  = 'N'; #无日食
 else if(ls2>0) re.lx  = 'P'; #偏食
 else if(ls3>0) re.lx += '0'; #无中心
 else if(ls4>0) re.lx += '1'; #有中心(本影未全部进入)
 else{ #本影全进入
  if(abs(fh2-h)<0.019) re.ac=0;
  if( abs(fh2)<h ){
    var dr = vR*h/vL/mR;
    var H1 = mR-dr-mk/f2;  #入点影锥z坐标
    var H2 = mR+dr-mk/f2;  #出点影锥z坐标
    if(H1>0) re.lx='H3';      #环全全
    if(H2>0) re.lx='H2';      #全全环
    if(H1>0 and H2>0) re.lx='H'; #环全环
    if(abs(H1)<0.019) re.ac=0;
    if(abs(H2)<0.019) re.ac=0;
  }
 }
 return re;
}


var rsGS={
 Zs   : new Array(),  #日月赤道坐标插值表
 Zdt  : 0.04,   #插值点之间的时间间距
 Zjd  : 0,      #插值表中心时间
 dT   : 0,      #deltatT
 tanf1: 0.0046, #半影锥角
 tanf2: 0.0045, #本影锥角
 srad : 0.0046, #太阳视半径
 bba  : 1,      #贝圆极赤比
 bhc  : 0,      #黄交线与赤交线的夹角简易作图用
 dyj  : 23500,  #地月距
 
 init:function(jd,n){ #创建插值表(根数表)
  if(suoN(jd)==suoN(self.Zjd)  and  self.Zs.length==n*9) return;
  self.Zs.length=0;
  self.Zjd  = jd = XL.MS_aLon_t2( suoN(jd)*pi*2 )*36525; #低精度的朔(误差10分钟)
  self.dT   = dt_T(jd); #deltat T

  var zd = nutation2(jd/36525); #章动
  var E = hcjj(jd/36525)+zd[1]; #黄赤交角

  var i,k,T, S,M,B, a=self.Zs;
  for(i=0;i<n;i++){ #插值点范围不要超过360度(约1个月)
   T=( self.Zjd + (i-n/2+0.5)*self.Zdt ) / 36525;

   if(n==7) S = e_coord(T,-1,-1,-1), M = m_coord(T,-1,-1,-1);    #地球坐标及月球坐标,全精度
   if(n==3) S = e_coord(T,65,65,65), M = m_coord(T,-1,150,150);  #中精度
   if(n==2) S = e_coord(T,20,20,20), M = m_coord(T,30,30,30);    #低精度


   S[0] = S[0]+zd[0]+gxc_sunLon(T)+pi;  S[1] = -S[1] + gxc_sunLat(T);  #补上太阳光行差及章动
   M[0] = M[0]+zd[0]+gxc_moonLon(T);         M[1] =  M[1] + gxc_moonLat(T); #补上月球光行差及章动
   S = llrConv( S, E );  M = llrConv( M, E ); S[2]*=cs_AU; #转为赤道坐标
   if(i  and  S[0]<a[0]) S[0]+=pi2;  #确保插值数据连续
   if(i  and  M[0]<a[3]) M[0]+=pi2;  #确保插值数据连续

   k = i*9;
   a[k+0]=S[0], a[k+1]=S[1], a[k+2]=S[2]; #存入插值表
   a[k+3]=M[0], a[k+4]=M[1], a[k+5]=M[2];


   #贝塞尔坐标的z轴坐标计算,得到a[k+6,7,8]交点赤经,贝赤交角,真恒星时
   S=llr2xyz(S), M=llr2xyz(M);
   B = xyz2llr( new Array(S[0]-M[0],S[1]-M[1],S[2]-M[2]) );
   B[0] = pi/2+B[0];
   B[1] = pi/2-B[1];
   if(i  and  B[0]<a[6]) B[0]+=pi2; #确保插值数据连续

   a[k+6]=B[0], a[k+7]=B[1], a[k+8]=pGST(T*36525-self.dT, self.dT)+zd[0]*cos(E); #真恒星时
  }
  #一些辅助参数的计算
  var p=a.length-9;
  self.dyj = (a[2]+a[p+2]-a[5]-a[p+5])/2/cs_rEar; #地月平均距离
  self.tanf1 = (cs_k0+cs_k )/self.dyj; #tanf1半影锥角
  self.tanf2 = (cs_k0-cs_k2)/self.dyj; #tanf2本影锥角
  self.srad = cs_k0/((a[2]+a[p+2])/2/cs_rEar);
  self.bba = sin( (a[1]+a[p+1])/2 );
  self.bba = cs_ba*(1+(1-cs_ba2)*self.bba*self.bba/2);
  self.bhc = -atan(tan(E)*sin( (a[6]+a[p+6])/2 )); #黄交线与赤交线的夹角

 },

 chazhi:function(jd,xt){#日月坐标快速计算(贝赛尔插值法),计算第p个根数开始的m个根数
  var p=xt*3,m=3; #计算第p个根数开始的m个根数
  var i, N=self.Zs.length/9, B=self.Zs, z=new Array();
  var w = B.length/N; #每节点个数
  var t = (jd-self.Zjd)/self.Zdt+N/2-0.5; #相对于第一点的时间距离

  if(N==2) { for(i=0; i<m; i++,p++) z[i] = B[p] + (B[p+w]-B[p])*t; return z; }
  var c=floor(t+0.5); if(c<=0) c=1; if(c>N-2) c=N-2; #确定c,并对超出范围的处理
  t-=c, p+=c*w; #c插值中心,t为插值因子,t再转为插值中心在数据中的位置
  for(i=0; i<m; i++,p++)
    z[i] = B[p] + ( B[p+w]-B[p-w] + (B[p+w]+B[p-w]-B[p]*2)*t ) * t/2;
  return z;
 },

 sun :function(jd){ return self.chazhi(jd,0); }, #传回值可能超过360度
 moon:function(jd){ return self.chazhi(jd,1); },
 bse :function(jd){ return self.chazhi(jd,2); },

 cd2bse:function(z,I){ #赤道转贝塞尔坐标
  var r=new Array(z[0]-I[0],z[1],z[2]);
  r = llrConv(r,-I[1]);
  return llr2xyz(r);
 },
 bse2cd:function(z,I){ #贝塞尔转赤道坐标
  var r = xyz2llr(z);
  r = llrConv(r,I[1]);
  r[0] = rad2mrad(r[0]+I[0]);
  return r;
 },
 bse2db:function(z,I,f){ #贝赛尔转地标(p点到原点连线与地球的交点,z为p点直角坐标),f=1时把地球看成椭球
  var r = xyz2llr(z);
  r = llrConv(r,I[1]);
  r[0] = rad2rrad(r[0]+I[0]-I[2]);
  if(f) r[1] = atan( tan(r[1])/cs_ba2 );
  return r;
 },
 bseXY2db:function(x,y,I,f){ #贝赛尔转地标(过p点垂直于基面的线与地球的交点,p坐标为(x,y,任意z)),f=1时把地球看成椭球
  var b=f?cs_ba:1;
  var F = lineEar2(x,y,2,  x,y,0,  b,1,I);#求中心对应的地标
  return [F.J,F.W];
 },

 bseM:function(jd){  #月亮的贝塞尔坐标
   var a=self.cd2bse(self.chazhi(jd,1),self.chazhi(jd,2));
   a[0]/=cs_rEar, a[1]/=cs_rEar, a[2]/=cs_rEar;
   return a;
 },

 #以下计算日食总体情况

 Vxy:function(x,y,s, vx,vy){ #地球上一点的速度，用贝塞尔坐标表达，s为贝赤交角
   var r = new Object();
   var h = 1-x*x-y*y;
   if(h<0) h = 0;  #越界置0，使速度场连续，置零有助于迭代时单向收敛
   else    h = sqrt(h);
   r.vx = pi2*( sin(s)*h-cos(s)*y );
   r.vy = pi2*x*cos(s);
   r.Vx = vx - r.vx;
   r.Vy = vy - r.vy;
   r.V = sqrt(r.Vx*r.Vx+r.Vy*r.Vy);
   return r;
 },
 rSM:function(mR){ #rm,rs单位千米
  var re = new Object();
  re.r1 = cs_k +self.tanf1*mR; #半影半径
  re.r2 = cs_k2-self.tanf2*mR; #本影半径
  re.ar2 = abs(re.r2);
  re.sf = cs_k2/mR/cs_k0*(self.dyj+mR); #食分
  return re;
 },
 qrd:function(jd,dx,dy, fs){ #求切入点
  var ba2 = self.bba*self.bba;
  var M = self.bseM(jd), x=M[0], y=M[1];
  var B = self.rSM(M[2]);
  var r = 0; if(fs==1) r = B.r1;
  var d = 1-(1/ba2-1)*y*y/(x*x+y*y)/2 + r;
  var t = (d*d-x*x-y*y)/(dx*x+dy*y)/2;
  x+=t*dx, y+=t*dy, jd+=t;

  var c=(1-ba2)*r*x*y/d/d/d;
  x += c*y;
  y -= c*x;
  var re=self.bse2db([x/d,y/d,0],self.bse(jd),1);
  #re[0] +=0.275/radd; #转为deltatT为66秒的历书经度
  re[2]=jd;
  return re;
 },
 feature:function(jd){#日食的基本特征
  jd = self.Zjd; #低精度的朔(误差10分钟)

  var tg=0.04,jd1=jd-tg/2, re=new Object(), ls;



  var tg=0.04, re=new Object(), ls;
  var a = self.bseM(jd-tg);
  var b = self.bseM(jd);
  var c = self.bseM(jd+tg);
  var vx = (c[0]-a[0])/tg/2;
  var vy = (c[1]-a[1])/tg/2;
  var vz = (c[2]-a[2])/tg/2;
  var ax = (c[0]+a[0]-2*b[0])/tg/tg;
  var ay = (c[1]+a[1]-2*b[1])/tg/tg;
  var v = sqrt(vx*vx+vy*vy), v2=v*v;

  #影轴在贝塞尔面扫线的特征参数
  re.jdSuo = jd;    #朔
  re.dT = self.dT;  #deltat T
  re.ds = self.bhc; #黄交线与赤交线的夹角
  re.vx = vx;       #影速x
  re.vy = vy;       #影速y
  re.ax = ax;
  re.ay = ay;
  re.v  = v;
  re.k  = vy/vx;    #斜率

  var t0 = -(b[0]*vx+b[1]*vy)/v2;
  re.jd = jd+t0;  #中点时间
  re.xc = b[0]+vx*t0;  #中点坐标x
  re.yc = b[1]+vy*t0;  #中点坐标y
  re.zc = b[2]+vz*t0-1.37*t0*t0;  #中点坐标z
  re.D  = (vx*b[1]-vy*b[0])/v;
  re.d  = abs(re.D);  #直线到圆心的距离
  re.I  = self.bse(re.jd); #中心点的贝塞尔z轴的赤道坐标及恒星时，(J,W,g)

  #影轴交点判断
  var F = lineEar2(re.xc,re.yc,2,  re.xc,re.yc,0,  cs_ba,1,re.I);#求中心对应的地标
  #四个关键点的影子半径计算
  var Bc,Bp,B2,B3,  dt,t2,t3,t4,t5,t6;
  Bc=Bp=B2=B3 = self.rSM(re.zc); #中点处的影子半径
  if(F.W!=100)  Bp = self.rSM(re.zc - F.R2);
  if(re.d<1){
    dt=sqrt(1-re.d*re.d)/v;  t2=t0-dt, t3=t0+dt; #中心始终参数
    B2 = self.rSM(t2*vz+b[2]-1.37*t2*t2);   #中心线始影半径
    B3 = self.rSM(t3*vz+b[2]-1.37*t3*t3);   #中心线终影半径
  }
  ls = 1;        dt=0; if(re.d<ls) dt=sqrt(ls*ls-re.d*re.d)/v; t2=t0-dt, t3=t0+dt; #偏食始终参数,t2,t3
  ls = 1+Bc.r1;  dt=0; if(re.d<ls) dt=sqrt(ls*ls-re.d*re.d)/v; t4=t0-dt, t5=t0+dt; #偏食始终参数,t4,t5
  t6 = -b[0]/vx; #视午参数l6
  re.gk1 = self.qrd(t2+jd,vx,vy,0); #中心始
  re.gk2 = self.qrd(t3+jd,vx,vy,0); #中心终
  re.gk3 = self.qrd(t4+jd,vx,vy,1); #偏食始
  re.gk4 = self.qrd(t5+jd,vx,vy,1); #偏食终
  re.gk5 = self.bseXY2db(t6*vx+b[0],t6*vy+b[1], self.bse(t6+jd), 1);  re.gk5[2]=t6+jd; #地方视午日食

  #日食类型、最大食地标、食分、太阳地平坐标
  if(F.W==100){ #无中心线
   #最大食地标及时分
   ls = self.bse2db([re.xc,re.yc,0],re.I, 0); re.zxJ=ls[0], re.zxW=ls[1]; #最大食地标
   re.sf = (Bc.r1-(re.d-0.9972))/(Bc.r1-Bc.r2); #0.9969是南北极区的平半径
   #类型判断
   if     (re.d>0.9972+Bc.r1)  { re.lx = 'N'; } #无食,半影没有进入
   else if(re.d>0.9972+Bc.ar2) { re.lx = 'P'; } #偏食,本影没有进入
   else                        { if(Bc.sf<1) re.lx = 'A0'; else re.lx = 'T0'; } #中心线未进入,本影部分进入(无中心，所以只是部分地入)
  }else{ #有中心线
   #最大食地标及时分
   re.zxJ=F.J, re.zxW=F.W;  #最大食地标
   re.sf = Bp.sf; #食分
   #类型判断
   if(re.d>0.9966-Bp.ar2) { if(Bp.sf<1) re.lx = 'A1'; else re.lx = 'T1'; } #中心进入,但本影没有完全进入
   else{ #本影全进入有中心日食
    if(Bp.sf>=1){
      re.lx = 'H';
      if(B2.sf>1) re.lx = 'H2'; #全环食,全始
      if(B3.sf>1) re.lx = 'H3'; #全环食,全终
      if(B2.sf>1  and  B3.sf>1) re.lx='T'; #全食
    } else re.lx = 'A'; #环食
   }
  }
  re.Sdp = CD2DP(self.sun(re.jd),re.zxJ,re.zxW,re.I[2]);  #太阳在中心点的地平坐标

  #食带宽度和时延
  if(F.W!=100){
    re.dw = abs(2*Bp.r2*cs_rEar) / sin(re.Sdp[1]); #食带宽度
    ls = self.Vxy(re.xc,re.yc,re.I[1], re.vx,re.vy); #求地表影速
    re.tt = 2*abs(Bp.r2)/ls.V; #时延
  } else re.dw = re.tt =0;
  return re;
 },

 #界线图
 push:function(z,p){ p[p.length]=z[0], p[p.length]=z[1]; }, #经度改为东经为正,所以有个负号
 elmCpy:function(a,n, b,m){ #数据元素复制
   if(!b.length) return;
   if(n==-2) n=a.length;
   if(m==-2) m=b.length;
   if(n==-1) n=a.length-2;
   if(m==-1) m=b.length-2;
   a[n]=b[m], a[n+1]=b[m+1];
 },
 nanbei:function(M,vx0,vy0, h, r,I){ #vx0,vy0为影足速度(也是整个影子速度),h=1计算北界,h=-1计算南界
   var x=M[0]-vy0/vx0*r*h, y=M[1]+h*r, z, i;
   var vx,vy,v,sinA,cosA, js=0;
   for(i=0;i<3;i++){
    z = 1 - x*x - y*y;
    if(z<0) { if(js) break;  z=0;js++; } #z小于0则置0，如果两次小于0，可能不收敛造成的，故不再迭代了
    z = sqrt(z);
    x -= (x-M[0])*z/M[2];
    y -= (y-M[1])*z/M[2];
    vx = vx0 - pi2*( sin(I[1])*z-cos(I[1])*y );
    vy = vy0 - pi2*  cos(I[1])*x;
    v  = sqrt(vx*vx+vy*vy);
    sinA = h*vy/v, cosA = h*vx/v;
    x = M[0] - r*sinA, y = M[1] + r*cosA;
   }
   var X = M[0] - cs_k*sinA, Y = M[1] + cs_k*cosA;
   var p = lineEar2(X,Y,M[2],  x,y,0,  cs_ba,1,I);
   return [p.J, p.W, x, y];
 },

 mQie:function(M,vx0,vy0, h, r,I, A){ #vx0,vy0为影足速度(也是整个影子速度),h=1计算北界,h=-1计算南界
   var p=self.nanbei(M,vx0,vy0,h,r,I);
   if(!A.f2) A.f2=0;   A.f = p[1]==100?0:1; #记录有无解
   if(A.f2!=A.f){ #补线头线尾
     var g=lineOvl(p[2],p[3],vx0,vy0,1,self.bba), dj, F;
     if(g.n){
      if(A.f) dj=g.R2, F=g.B;
      else    dj=g.R1, F=g.A;
      F[2]=0;
      var I2 = new Array( I[0], I[1], I[2] - dj/sqrt(vx0*vx0+vy0*vy0)*6.28 );  #也可以不重算计算恒星时，直接用I[2]代替，但线头不会严格落在日出日没食甚线上
      self.push( self.bse2db(F,I2,1), A);#有解补线头
     }
   }
   A.f2 = A.f; #记录上次有无解

   if(p[1]!=100) self.push(p,A);
 },
 mDian:function(M,vx0,vy0, AB, r,I, A){ #日出日没食甚
   var i, p,a=M, R,c=new Object();
   for(i=0;i<2;i++){ #迭代求交点
     c = self.Vxy(a[0],a[1],I[1], vx0,vy0);
     p = lineOvl(M[0],M[1],c.Vy,-c.Vx,1,self.bba);
     if(!p.n) break;
     if(AB) a=p.A, R=p.R1;
     else   a=p.B, R=p.R2;
   }
   if(p.n  and  R<=r){ #有交点
     a=self.bse2db([a[0],a[1],0], I,1); #转为地标
     self.push(a,A ); #保存第一食甚线A或B根
     return 1;
   }
   return 0;
 },
 jieX:function(jd){ #日出日没的初亏食甚复圆线，南北界线等
  var i, p, ls;
  var re=self.feature(jd);  #求特征参数

  re.p1=new Array(), re.p2=new Array(), re.p3=new Array(), re.p4=new Array();
  re.q1=new Array(), re.q2=new Array(), re.q3=new Array(), re.q4=new Array();
  re.L1=new Array(), re.L2=new Array(), re.L3=new Array(), re.L4=new Array();
  re.L5=new Array(), re.L6=new Array(); #0.5食分线
  re.L0=new Array(); #中心线

  var T = 1.7*1.7-re.d*re.d; if(T<0) T=0; T=sqrt(T)/re.v+0.01;
  var t=re.jd-T, N=200, dt=2*T/N;

  var n1=0, n4=0; #n1切入时序

  #对日出日没食甚线预置一个点
  var Ua=re.q1,Ub=re.q2;
  self.push([0,0],re.q2); self.push([0,0],re.q3); self.push([0,0],re.q4);

  for(i=0;i<=N;i++,t+=dt){
   var vx = re.vx+re.ax*(t-re.jdSuo);
   var vy = re.vy+re.ay*(t-re.jdSuo);
   var M = self.bseM(t);    #此刻月亮贝塞尔坐标(其x和y正是影足)
   var B = self.rSM(M[2]);  #本半影等
   var r = B.r1;            #半影半径
   var I = self.bse(t);     #贝塞尔坐标参数

   p=cirOvl(1,self.bba, r,M[0],M[1]); #求椭圆与圆交点
   if(n1%2) {if(!p.n) n1++;} else {if(p.n) n1++;}
   if(p.n) { #有交点
    p.A[2]=p.B[2]=0;  p.A=self.bse2db(p.A,I,1);  p.B=self.bse2db(p.B,I,1); #转为地标
    if(n1==1){ self.push(p.A,re.p1); self.push(p.B,re.p2); }#保存第一亏圆界线
    if(n1==3){ self.push(p.A,re.p3); self.push(p.B,re.p4); }#保存第二亏圆界线
   }

   #日出日没食甚线
   if( !self.mDian(M,vx,vy,0,r,I, Ua) ) { if(Ua.length>0) Ua=re.q3; };
   if( !self.mDian(M,vx,vy,1,r,I, Ub) ) { if(Ub.length>2) Ub=re.q4; };
   if(t>re.jd){
     if(Ua.length==0) Ua=re.q3;
     if(Ub.length==2) Ub=re.q4;
   }

   #求中心线
   p = self.bseXY2db(M[0],M[1],I,1);
   if( p[1]!=100 and n4==0 || p[1]==100 and n4==1 ){ #从无交点跳到有交点或反之
     ls=lineOvl(M[0],M[1],vx,vy,1,self.bba);
     var dj;
     if(n4==0) dj=ls.R2,ls=ls.B; #首坐标
     else      dj=ls.R1,ls=ls.A; #末坐标
     ls[2]=0;
     var I2 = new Array( I[0], I[1], I[2] - dj/sqrt(vx*vx+vy*vy)*6.28 );  #也可以不重算计算恒星时，直接用I[2]代替，但线头不会严格落在日出日没食甚线上
     self.push( self.bse2db(ls,I2,1), re.L0 );
     n4++;
   }
   if(p[1]!=100) self.push(p,re.L0); #保存中心线

   #南北界
   self.mQie(M,vx,vy, +1, r,          I, re.L1); #半影北界
   self.mQie(M,vx,vy, -1, r,          I, re.L2); #半影南界
   self.mQie(M,vx,vy, +1, B.r2,       I, re.L3); #本影北界
   self.mQie(M,vx,vy, -1, B.r2,       I, re.L4); #本影南界
   self.mQie(M,vx,vy, +1, (r+B.r2)/2, I, re.L5); #0.5半影北界
   self.mQie(M,vx,vy, -1, (r+B.r2)/2, I, re.L6); #0.5半影南界
  }


  #日出日没食甚线的线头连接
  self.elmCpy(re.q3, 0, re.q1,-1); #连接q1和a3,单边界必须
  self.elmCpy(re.q4, 0, re.q2,-1); #连接q2和a4,单边界必须

  self.elmCpy(re.q1,-2, re.L1, 0); #半影北界线西端
  self.elmCpy(re.q2,-2, re.L2, 0); #半影南界线西端
  self.elmCpy(re.q3, 0, re.L1,-1); #半影北界线东端
  self.elmCpy(re.q4, 0, re.L2,-1); #半影南界线东端

  self.elmCpy(re.q2, 0, re.q1, 0);
  self.elmCpy(re.q3,-2, re.q4,-1);

  return re;
 },
 jieX2:function (jd){ #jd力学时
  var re=new Object();
  var p1=new Array(), p2=new Array(), p3=new Array();

  if(abs(jd-self.Zjd)>0.5) return re;

  var i,s,p,x,y,X,Y;
  var S = self.sun(jd);   #此刻太阳赤道坐标
  var M = self.bseM(jd);  #此刻月亮
  var B = self.rSM(M[2]); #本半影等
  var I = self.bse(jd);   #贝塞尔坐标参数
  var Z = M[2];           #月亮的坐标的z量

  var a0=M[0]*M[0]+M[1]*M[1];
  var a1=a0-B.r2*B.r2;
  var a2=a0-B.r1*B.r1;
  var N = 200;
  for(i=0;i<N;i++){#第0和第N点是同一点，可形成一个环，但不必计算，因为第0点可能在界外而无效
    s=i/N*pi2;
    var cosS=cos(s), sinS=sin(s);
    X = M[0] + cs_k*cosS, Y = M[1] + cs_k*sinS;
    #本影
    x = M[0] + B.r2*cosS, y = M[1] + B.r2*sinS;
    p = lineEar2(X,Y,Z,  x,y,0,  cs_ba,1,I);
    if(p.W!=100) self.push( [p.J,p.W], p1 );
    else { if(sqrt(x*x+y*y)>a1) self.push( self.bse2db([x,y,0],I,1), p1 ); }
    #半影
    x = M[0] + B.r1*cosS, y = M[1] + B.r1*sinS;
    p = lineEar2(X,Y,Z,  x,y,0,  cs_ba,1,I);
    if(p.W!=100) self.push( [p.J,p.W], p2 );
    else { if(sqrt(x*x+y*y)>a2) self.push( self.bse2db([x,y,0],I,1), p2 ); }
    #晨昏圈
    p = llrConv([s,0,0],pi_2-S[1]);
    p[0] = rad2rrad( p[0]+S[0]+pi_2-I[2] );
    self.push(p, p3);
  }
  p1[p1.length]=p1[0], p1[p1.length]=p1[1];
  p2[p2.length]=p2[0], p2[p2.length]=p2[1];
  p3[p3.length]=p3[0], p3[p3.length]=p3[1];

  re.p1=p1, re.p2=p2, re.p3=p3;
  return re;
 },
 jieX3:function(jd){ #界线表
  var i,k, p, ls;
  var re=self.feature(jd);  #求特征参数

  var t = floor(re.jd*1440)/1440 -3/24;
  var N=360, dt=1/1440, s='',s2;

  for(i=0;i<N;i++,t+=dt){
   var vx = re.vx+re.ax*(t-re.jdSuo);
   var vy = re.vy+re.ay*(t-re.jdSuo);
   var M = self.bseM(t);    #此刻月亮贝塞尔坐标(其x和y正是影足)
   var B = self.rSM(M[2]);  #本半影等
   var r = B.r1;            #半影半径
   var I = self.bse(t);     #贝塞尔坐标参数
   s2 = JD.JD2str(t+J2000)+' ', k=0;
   #南北界
   p = self.nanbei(M,vx,vy, +1, r,     I); if(p[1]!=100) s2+=rad2str2(p[0])+' '+rad2str2(p[1])+'|', k++; else s2+='-------------------|'; #半影北界
   p = self.nanbei(M,vx,vy, +1, B.r2,  I); if(p[1]!=100) s2+=rad2str2(p[0])+' '+rad2str2(p[1])+'|', k++; else s2+='-------------------|'; #本影北界
   p = self.bseXY2db(M[0],M[1],I,1);       if(p[1]!=100) s2+=rad2str2(p[0])+' '+rad2str2(p[1])+'|', k++; else s2+='-------------------|'; #中心线
   p = self.nanbei(M,vx,vy, -1, B.r2,  I); if(p[1]!=100) s2+=rad2str2(p[0])+' '+rad2str2(p[1])+'|', k++; else s2+='-------------------|'; #本影南界
   p = self.nanbei(M,vx,vy, -1, r,     I); if(p[1]!=100) s2+=rad2str2(p[0])+' '+rad2str2(p[1])+' ', k++; else s2+='------------------- '; #半影南界
   if(k) s+=s2+'<br>';
  }
  return '<pre>时间(力学时) 半影北界限 本影北界线 中心线 本影南界线 半影南界线，(伪本影南北界应互换)<br>'+s+'</pre>';
 }
};




var rsPL={ #日食批量快速计算器
 nasa_r:0, #为1表示采用NASA的视径比
 sT:new Array(), #地方日食时间表

 secXY:function(jd,L,fa,high,re){ #日月xy坐标计算。参数：jd是力学时,站点经纬L,fa,海拔high(千米)
  #基本参数计算
  var deltat = dt_T(jd); #TD-UT
  var zd=nutation2(jd/36525);
  var gst= pGST(jd-deltat,deltat) + zd[0]*cos(hcjj(jd/36525) + zd[1]); #真恒星时(不考虑非多项式部分)

  var z;
  #=======月亮========
  z=rsGS.moon(jd); re.mCJ=z[0]; re.mCW=z[1]; re.mR=z[2]; #月亮视赤经,月球赤纬
  var mShiJ = rad2rrad(gst + L - z[0]); #得到此刻月亮时角
  parallax(z, mShiJ,fa, high); re.mCJ2=z[0], re.mCW2=z[1], re.mR2=z[2]; #修正了视差的赤道坐标

  #=======太阳========
  z=rsGS.sun(jd); re.sCJ=z[0]; re.sCW=z[1]; re.sR=z[2]; #太阳视赤经,太阳赤纬
  var sShiJ = rad2rrad(gst + L - z[0]); #得到此刻太阳时角
  parallax(z,sShiJ,fa,high); re.sCJ2=z[0], re.sCW2=z[1], re.sR2=z[2]; #修正了视差的赤道坐标

  #=======视半径========
  re.mr = cs_sMoon/re.mR2/rad;
  re.sr = 959.63/re.sR2/rad*cs_AU;
  if(self.nasa_r) re.mr*=cs_sMoon2/cs_sMoon; #0.99925;
  #=======日月赤经纬差转为日面中心直角坐标(用于日食)==============
  re.x = rad2rrad(re.mCJ2-re.sCJ2) * cos((re.mCW2+re.sCW2)/2);
  re.y = re.mCW2-re.sCW2;
  re.t = jd;
 },
 lineT:function(G, v,u, r, n){#已知t1时刻星体位置、速度，求x*x+y*y=r*r时,t的值
  var b=G.y*v-G.x*u, A=u*u+v*v, B=u*b, C=b*b-r*r*v*v, D=B*B-A*C;
  if(D<0) return 0;
  D=sqrt(D); if(!n) D=-D;
  return G.t+((-B+D)/A-G.x)/v;
 },
 secMax:function(jd,L,fa,high){ #日食的食甚计算(jd为近朔的力学时,误差几天不要紧)
  var i;
  for(i=0;i<5;i++) self.sT[i]=0; #分别是:食甚,初亏,复圆,食既,生光
  self.LX=''; #类型
  self.sf=0;  #食分
  self.b1=1;  #月日半径比(食甚时刻)
  self.dur = 0; #持续时间
  self.P1 = self.V1 = 0;  #初亏方位,P北点起算,V顶点起算
  self.P2 = self.V2 = 0;  #复圆方位,P北点起算,V顶点起算
  self.sun_s = self.sun_j = 0; #日出日没

  rsGS.init(jd,7);
  jd=rsGS.Zjd; #食甚初始估值为插值表中心时刻(粗朔)

  var G=new Object(), g=new Object();
  self.secXY(jd,L,fa,high,G);
  jd -= G.x/0.2128; #与食甚的误差在20分钟以内

  var u,v,dt=60/86400,dt2;
  for(i=0;i<2;i++){
   if( self.secXY(jd,L,fa,high,G)   =='err') return;
   if( self.secXY(jd+dt,L,fa,high,g)=='err') return;
   u = (g.y-G.y)/dt;
   v = (g.x-G.x)/dt;
   dt2 = -(G.y*u+G.x*v)/(u*u+v*v);
   jd += dt2; #极值时间
  }

  #求直线到太阳中心的最小值
  var x=G.x+dt2*v, y=G.y+dt2*u, rmin=sqrt(x*x+y*y);

  if(rmin<=G.mr+G.sr){ #食计算
   self.sT[1] = jd; #食甚
   self.LX='偏';
   self.sf=(G.mr+G.sr-rmin)/G.sr/2; #食分
   self.b1=G.mr/G.sr;

   self.sun_s = sunShengJ(jd-dt_T(jd)+L/pi2,L,fa,-1); #日出
   self.sun_j = sunShengJ(jd-dt_T(jd)+L/pi2,L,fa, 1); #日没

   self.sT[0] = self.lineT(G,v,u, G.mr+G.sr, 0); #初亏
   for(i=0;i<3;i++) { #初亏再算3次
    self.secXY(self.sT[0],L,fa,high,g);
    self.sT[0] = self.lineT(g,v,u, g.mr+g.sr, 0);
   }

   self.P1 = rad2mrad(atan2(g.x,g.y)); #初亏位置角
   self.V1 = rad2mrad(self.P1-shiChaJ(pGST2(self.sT[0]),L,fa,g.sCJ,g.sCW)); #这里g.sCJ与g.sCW对应的时间与sT[0]还差了一点，所以有一小点误差，不采用真恒星时也误差一点

   self.sT[2] = self.lineT(G,v,u, G.mr+G.sr, 1); #复圆
   for(i=0;i<3;i++) { #复圆再算3次
    self.secXY(self.sT[2],L,fa,high,g);
    self.sT[2] = self.lineT(g,v,u, g.mr+g.sr, 1);
   }
   self.P2 = rad2mrad(atan2(g.x,g.y));
   self.V2 = rad2mrad(self.P2-shiChaJ(pGST2(self.sT[2]),L,fa,g.sCJ,g.sCW)); #这里g.sCJ与g.sCW对应的时间与sT[2]还差了一点，所以有一小点误差，不采用真恒星时也误差一点
  }
  if(rmin<=G.mr-G.sr){ #全食计算
   self.LX='全';
   self.sT[3] = self.lineT(G,v,u, G.mr-G.sr, 0); #食既
   self.secXY(self.sT[3],L,fa,high,g);
   self.sT[3] = self.lineT(g,v,u, g.mr-g.sr, 0); #食既再算1次

   self.sT[4] = self.lineT(G,v,u, G.mr-G.sr, 1); #生光
   self.secXY(self.sT[4],L,fa,high,g);
   self.sT[4] = self.lineT(g,v,u, g.mr-g.sr, 1); #生光再算1次
   self.dur = self.sT[4]-self.sT[3];
  }
  if(rmin<=G.sr-G.mr){ #环食计算
   self.LX='环';
   self.sT[3] = self.lineT(G,v,u, G.sr-G.mr, 0); #食既
   self.secXY(self.sT[3],L,fa,high,g);
   self.sT[3] = self.lineT(g,v,u, g.sr-g.mr, 0); #食既再算1次

   self.sT[4] = self.lineT(G,v,u, G.sr-G.mr, 1); #生光
   self.secXY(self.sT[4],L,fa,high,g);
   self.sT[4] = self.lineT(g,v,u, g.sr-g.mr, 1); #生光再算1次
   self.dur = self.sT[4]-self.sT[3];
  }
 },

 #以下涉及南北界计算
 A:new Array(), B:new Array(), #本半影锥顶点坐标
 P : {S:new Array(), M:new Array(), g:0},#t1时刻的日月坐标,g为恒星时
 Q : {S:new Array(), M:new Array(), g:0},#t2时刻的日月坐标
 V : new Array(), #食界表
 Vc: '', Vb: '',  #食中心类型,本影南北距离

 zb0:function(jd){
  #基本参数计算
  var deltat = dt_T(jd); #TD-UT
  var E=hcjj(jd/36525);
  var zd=nutation2(jd/36525);

  self.P.g = pGST(jd-deltat, deltat) + zd[0]*cos(E+zd[1]); #真恒星时(不考虑非多项式部分)
  self.P.S=rsGS.sun(jd);
  self.P.M=rsGS.moon(jd);

  var t2=jd+60/86400;
  self.Q.g = pGST(t2-deltat,deltat) + zd[0]*cos(E+zd[1]);
  self.Q.S=rsGS.sun(t2);
  self.Q.M=rsGS.moon(t2);

  #转为直角坐标
  var z1=new Array(), z2=new Array();
  z1 = llr2xyz(self.P.S);
  z2 = llr2xyz(self.P.M);

  var k=959.63/cs_sMoon*cs_AU, F; #k为日月半径比
  #本影锥顶点坐标计算
  F = new Array(
   (z1[0]-z2[0])/(1-k)+z2[0],
   (z1[1]-z2[1])/(1-k)+z2[1],
   (z1[2]-z2[2])/(1-k)+z2[2]);
  self.A = xyz2llr(F);
  #半影锥顶点坐标计算
  F = new Array(
   (z1[0]-z2[0])/(1+k)+z2[0],
   (z1[1]-z2[1])/(1+k)+z2[1],
   (z1[2]-z2[2])/(1+k)+z2[2]);
  self.B = xyz2llr(F);
 },

 zbXY:function(p,L,fa){
  var s=new Array(p.S[0],p.S[1],p.S[2]);
  var m=new Array(p.M[0],p.M[1],p.M[2]);
  parallax(s, p.g+L-p.S[0],fa, 0); #修正了视差的赤道坐标
  parallax(m, p.g+L-p.M[0],fa, 0); #修正了视差的赤道坐标
  #=======视半径========
  p.mr = cs_sMoon/m[2]/rad;
  p.sr = 959.63/s[2]/rad*cs_AU;
  #=======日月赤经纬差转为日面中心直角坐标(用于日食)==============
  p.x = rad2rrad(m[0]-s[0]) * cos((m[1]+s[1])/2);
  p.y = m[1]-s[1];
 },
 p2p:function(L,fa,re,fAB,f){ #f取+-1
  var p=self.P, q=self.Q;
  self.zbXY(self.P,L,fa);
  self.zbXY(self.Q,L,fa);

  var u=q.y-p.y, v=q.x-p.x, a=sqrt(u*u+v*v),r=959.63/p.S[2]/rad*cs_AU;

  var W=p.S[1]+f*r*v/a, J=p.S[0]-f*r*u/a/cos((W+p.S[1])/2), R=p.S[2];

  var A = fAB ? self.A : self.B;

  var pp = lineEar( new Array(J,W,R), A, p.g );
  re.J = pp.J;
  re.W = pp.W;
 },
 pp0:function(re){ #食中心点计算
  var p=self.P;
  var pp = lineEar( p.M, p.S, p.g );
  re.J = pp.J;
  re.W = pp.W; #无解返回值是100
  
  if(re.W==100) { re.c = ''; return; }
  re.c='全';
  self.zbXY(p,re.J,re.W);
  if(p.sr>p.mr) re.c='环';
 },
 nbj:function(jd){ #南北界计算
  rsGS.init(jd,7);
  var i, G=new Object(), V=self.V;
  for(i=0;i<10;i++) V[i]=100; self.Vc='',self.Vb=''; #返回初始化,纬度值为100表示无解,经度100也是无解,但在以下程序中经度会被转为-PI到+pi

  self.zb0(jd);
  self.pp0(G); V[0]=G.J, V[1]=G.W, self.Vc=G.c; #食中心

  G.J=G.W=0; for(i=0;i<2;i++) self.p2p(G.J,G.W,G,1, 1); V[2]=G.J, V[3]=G.W; #本影北界,环食为南界(本影区之内,变差u,v基本不变,所以计算两次足够)
  G.J=G.W=0; for(i=0;i<2;i++) self.p2p(G.J,G.W,G,1,-1); V[4]=G.J, V[5]=G.W; #本影南界,环食为北界
  G.J=G.W=0; for(i=0;i<3;i++) self.p2p(G.J,G.W,G,0,-1); V[6]=G.J, V[7]=G.W; #半影北界
  G.J=G.W=0; for(i=0;i<3;i++) self.p2p(G.J,G.W,G,0, 1); V[8]=G.J, V[9]=G.W; #半影南界

  if(V[3]!=100 and V[5]!=100){ #粗算本影南北距离
    var x=(V[2]-V[4])*cos((V[3]+V[5])/2), y=V[3]-V[5];
    self.Vb = (cs_rEarA*sqrt(x*x+y*y)).toFixed(0)+'千米';
  }
 }
};







"""