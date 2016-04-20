#coding: UTF-8


from math import floor, cos, sin, pi
from csm.gcal.eph0 import dt_T, S_aLon_t, S_aLon_t2, MS_aLon_t, MS_aLon_t2
from csm.gcal.Julian import J2000, JDate

"""
*************************
  实气实朔计算器
  适用范围 -722年2月22日——1959年12月
  平气平朔计算使用古历参数进行计算
  定朔、定气计算使用开普勒椭圆轨道计算，同时考虑了光行差和力学时与UT1的时间差
  古代历算仅在晚期才使用开普勒方法计算，此前多采用一些修正表并插值得到，精度很低，与本程序中
的开普勒方法存在误差，造成朔日计算错误1千多个，这些错误使用一个修正表进行订正。同样，定气部分
也使用了相同的方法时行订正。
  平气朔表的算法(线性拟合)：
  气朔日期计算公式：D = k*n + b  , 式中n=0,1,2,3,...,N-1, N为该式适用的范围
  h表示k不变b允许的误差,如果b不变则k许可误差为h/N
  每行第1个参数为k,第2参数为b
  public中定义的成员可以直接使用
*************************
"""

class Shuoqi(object): #实朔实气计算器
#private成员定义
    SB=None #朔修正表
    QB=None #气修正表
    yueNames=('十一','十二','正','二','三','四','五','六','七','八','九','十') #月名称,建寅
    jieqiNames=('冬至','小寒','大寒','立春','雨水','惊蛰','春分','清明','谷雨','立夏','小满','芒种','夏至','小暑','大暑','立秋','处暑','白露','秋分','寒露','霜降','立冬','小雪','大雪')
    
    suoKB =( #朔直线拟合参数
            1457698.231017,29.53067166, # -721-12-17 h=0.00032 古历·春秋
            1546082.512234,29.53085106, # -479-12-11 h=0.00053 古历·战国
            1640640.735300,29.53060000, # -221-10-31 h=0.01010 古历·秦汉
            1642472.151543,29.53085439, # -216-11-04 h=0.00040 古历·秦汉
            
            1683430.509300,29.53086148, # -104-12-25 h=0.00313 汉书·律历志(太初历)平气平朔
            1752148.041079,29.53085097, #   85-02-13 h=0.00049 后汉书·律历志(四分历)
            1807665.420323,29.53059851, #  237-02-12 h=0.00033 晋书·律历志(景初历)
            1883618.114100,29.53060000, #  445-01-24 h=0.00030 宋书·律历志(何承天元嘉历)
            1907360.704700,29.53060000, #  510-01-26 h=0.00030 宋书·律历志(祖冲之大明历)
            1936596.224900,29.53060000, #  590-02-10 h=0.01010 隋书·律历志(开皇历)
            1939135.675300,29.53060000, #  597-01-24 h=0.00890 隋书·律历志(大业历)
            1947168.00)#  619-01-21

    qiKB = ( #气直线拟合参数
            1640650.479938,15.21842500, # -221-11-09 h=0.01709 古历·秦汉
            1642476.703182,15.21874996, # -216-11-09 h=0.01557 古历·秦汉
            
            1683430.515601,15.218750011, # -104-12-25 h=0.01560 汉书·律历志(太初历)平气平朔 回归年=365.25000
            1752157.640664,15.218749978, #   85-02-23 h=0.01559 后汉书·律历志(四分历) 回归年=365.25000
            1807675.003759,15.218620279, #  237-02-22 h=0.00010 晋书·律历志(景初历) 回归年=365.24689
            1883627.765182,15.218612292, #  445-02-03 h=0.00026 宋书·律历志(何承天元嘉历) 回归年=365.24670
            1907369.128100,15.218449176, #  510-02-03 h=0.00027 宋书·律历志(祖冲之大明历) 回归年=365.24278
            1936603.140413,15.218425000, #  590-02-17 h=0.00149 隋书·律历志(开皇历) 回归年=365.24220
            1939145.524180,15.218466998, #  597-02-03 h=0.00121 隋书·律历志(大业历) 回归年=365.24321
            1947180.798300,15.218524844, #  619-02-03 h=0.00052 新唐书·历志(戊寅元历)平气定朔 回归年=365.24460
            1964362.041824,15.218533526, #  666-02-17 h=0.00059 新唐书·历志(麟德历) 回归年=365.24480
            1987372.340971,15.218513908, #  729-02-16 h=0.00096 新唐书·历志(大衍历,至德历) 回归年=365.24433
            1999653.819126,15.218530782, #  762-10-03 h=0.00093 新唐书·历志(五纪历) 回归年=365.24474
            2007445.469786,15.218535181, #  784-02-01 h=0.00059 新唐书·历志(正元历,观象历) 回归年=365.24484
            2021324.917146,15.218526248, #  822-02-01 h=0.00022 新唐书·历志(宣明历) 回归年=365.24463
            2047257.232342,15.218519654, #  893-01-31 h=0.00015 新唐书·历志(崇玄历) 回归年=365.24447
            2070282.898213,15.218425000, #  956-02-16 h=0.00149 旧五代·历志(钦天历) 回归年=365.24220
            2073204.872850,15.218515221, #  964-02-16 h=0.00166 宋史·律历志(应天历) 回归年=365.24437
            2080144.500926,15.218530782, #  983-02-16 h=0.00093 宋史·律历志(乾元历) 回归年=365.24474
            2086703.688963,15.218523776, # 1001-01-31 h=0.00067 宋史·律历志(仪天历,崇天历) 回归年=365.24457
            2110033.182763,15.218425000, # 1064-12-15 h=0.00669 宋史·律历志(明天历) 回归年=365.24220
            2111190.300888,15.218425000, # 1068-02-15 h=0.00149 宋史·律历志(崇天历) 回归年=365.24220
            2113731.271005,15.218515671, # 1075-01-30 h=0.00038 李锐补修(奉元历) 回归年=365.24438
            2120670.840263,15.218425000, # 1094-01-30 h=0.00149 宋史·律历志 回归年=365.24220
            2123973.309063,15.218425000, # 1103-02-14 h=0.00669 李锐补修(占天历) 回归年=365.24220
            2125068.997336,15.218477932, # 1106-02-14 h=0.00056 宋史·律历志(纪元历) 回归年=365.24347
            2136026.312633,15.218472436, # 1136-02-14 h=0.00088 宋史·律历志(统元历,乾道历,淳熙历) 回归年=365.24334
            2156099.495538,15.218425000, # 1191-01-29 h=0.00149 宋史·律历志(会元历) 回归年=365.24220
            2159021.324663,15.218425000, # 1199-01-29 h=0.00149 宋史·律历志(统天历) 回归年=365.24220
            2162308.575254,15.218461742, # 1208-01-30 h=0.00146 宋史·律历志(开禧历) 回归年=365.24308
            2178485.706538,15.218425000, # 1252-05-15 h=0.04606 淳祐历 回归年=365.24220
            2178759.662849,15.218445786, # 1253-02-13 h=0.00231 会天历 回归年=365.24270
            2185334.020800,15.218425000, # 1271-02-13 h=0.00520 宋史·律历志(成天历) 回归年=365.24220
            2187525.481425,15.218425000, # 1277-02-12 h=0.00520 本天历 回归年=365.24220
            2188621.191481,15.218437494, # 1280-02-13 h=0.00015 元史·历志(郭守敬授时历) 回归年=365.24250
            2322147.76)# 1645-09-21
    
    @staticmethod
    def dateDay(d):
        d = int(d)
        chinnum = "一,二,三,四,五,六,七,八,九,十".split(",")
        if d<=10:
            return "初%s"%chinnum[d-1]
        elif d%10 == 0:
            return "%s%s"%(chinnum[int(d/10)-1], chinnum[9])
        elif d<20:
            return "%s%s"%(chinnum[9], chinnum[d-11])
        elif d<30:
            return "廿%s"%(chinnum[d-21])
        elif d<40:
            return "卅%s"%(chinnum[d-31])
        elif d<50:
            return "卌%s"%(chinnum[d-41])
        pass 
        
    
    @staticmethod
    def so_low(W): #低精度定朔计算,在2000年至600，误差在2小时以内(仍比古代日历精准很多)
        v = 7771.37714500204
        t  = ( W + 1.08472 )/v
        t -= (( -0.0000331*t*t
           + 0.10976 *cos( 0.785 + 8328.6914*t)
           + 0.02224 *cos( 0.187 + 7214.0629*t)
           - 0.03342 *cos( 4.669 +  628.3076*t ) )/v
           + (32*(t+1.8)*(t+1.8)-20)/86400/36525)
        return t*36525 + 8/24.0
    
    @staticmethod
    def qi_low(W): #最大误差小于30分钟，平均5分
        v= 628.3319653318
        t =  ( W - 4.895062166 )/v #第一次估算,误差2天以内
        t -= ( 53*t*t + 334116*cos( 4.67+628.307585*t) + 2061*cos( 2.678+628.3076*t)*t )/v/10000000 #第二次估算,误差2小时以内
        
        L = (48950621.66 + 6283319653.318*t + 53*t*t #平黄经
          +334166 * cos( 4.669257+  628.307585*t) #地球椭圆轨道级数展开
            +3489 * cos( 4.6261  + 1256.61517*t ) #地球椭圆轨道级数展开
          +2060.6 * cos( 2.67823 +  628.307585*t ) * t  #一次泊松项
            - 994 - 834*sin(2.1824-33.75705*t)) #光行差与章动修正
        
        t -= (L/10000000 -W )/628.332 + (32*(t+1.8)*(t+1.8)-20)/86400/36525
        return t*36525 + 8/24.0
    
    @staticmethod
    def qi_high(W): #较高精度气
        t = S_aLon_t2(W)*36525
        t = t - dt_T(t)+8/24.0
        v = ( (t+0.5) %1 ) * 86400.0
        if(v<1200 or v >86400-1200):
            t = S_aLon_t(W)*36525.0 - dt_T(t)+8/24.0
        return  t
    
    @staticmethod
    def so_high(W): #较高精度朔
        t = MS_aLon_t2(W)*36525.0
        t = t - dt_T(t)+8/24.0
        v = ( (t+0.5) %1 ) * 86400.0
        if(v<1800 or v >86400-1800):
            t = MS_aLon_t(W)*36525.0 - dt_T(t)+8/24.0
        return  t


    @staticmethod
    def jieya(s): #气朔解压缩
        o="0"*10
        o2=o*2
        s=s.replace('J','00');
        s=s.replace('I','000');
        s=s.replace('H','0000');
        s=s.replace('G','00000');
        s=s.replace('t','02');
        s=s.replace('s','002');
        s=s.replace('r','0002');
        s=s.replace('q','00002');
        s=s.replace('p','000002');
        s=s.replace('o','0000002');
        s=s.replace('n','00000002');
        s=s.replace('m','000000002');
        s=s.replace('l','0000000002');
        s=s.replace('k','01');
        s=s.replace('j','0101');
        s=s.replace('i','001');
        s=s.replace('h','001001');
        s=s.replace('g','0001');
        s=s.replace('f','00001');
        s=s.replace('e','000001');
        s=s.replace('d','0000001');
        s=s.replace('c','00000001');
        s=s.replace('b','000000001');
        s=s.replace('a','0000000001');
        s=s.replace('A',o2+o2+o2);
        s=s.replace('B',o2+o2+o);
        s=s.replace('C',o2+o2);
        s=s.replace('D',o2+o);
        s=s.replace('E',o2);
        s=s.replace('F',o);
        return s;
    
    def __init__(self, jd=None, lunar=None): #初使用化
        
        if self.SB is None:
            #  619-01-21开始16598个朔日修正表 d0=1947168
            suoS ="EqoFscDcrFpmEsF2DfFideFelFpFfFfFiaipqti1ksttikptikqckstekqttgkqttgkqteksttikptikq2fjstgjqttjkqttgkqt";
            suoS+="ekstfkptikq2tijstgjiFkirFsAeACoFsiDaDiADc1AFbBfgdfikijFifegF1FhaikgFag1E2btaieeibggiffdeigFfqDfaiBkF";
            suoS+="1kEaikhkigeidhhdiegcFfakF1ggkidbiaedksaFffckekidhhdhdikcikiakicjF1deedFhFccgicdekgiFbiaikcfi1kbFibef";
            suoS+="gEgFdcFkFeFkdcfkF1kfkcickEiFkDacFiEfbiaejcFfffkhkdgkaiei1ehigikhdFikfckF1dhhdikcfgjikhfjicjicgiehdik";
            suoS+="cikggcifgiejF1jkieFhegikggcikFegiegkfjebhigikggcikdgkaFkijcfkcikfkcifikiggkaeeigefkcdfcfkhkdgkegieid";
            suoS+="hijcFfakhfgeidieidiegikhfkfckfcjbdehdikggikgkfkicjicjF1dbidikFiggcifgiejkiegkigcdiegfggcikdbgfgefjF1";
            suoS+="kfegikggcikdgFkeeijcfkcikfkekcikdgkabhkFikaffcfkhkdgkegbiaekfkiakicjhfgqdq2fkiakgkfkhfkfcjiekgFebicg";
            suoS+="gbedF1jikejbbbiakgbgkacgiejkijjgigfiakggfggcibFifjefjF1kfekdgjcibFeFkijcfkfhkfkeaieigekgbhkfikidfcje";
            suoS+="aibgekgdkiffiffkiakF1jhbakgdki1dj1ikfkicjicjieeFkgdkicggkighdF1jfgkgfgbdkicggfggkidFkiekgijkeigfiski";
            suoS+="ggfaidheigF1jekijcikickiggkidhhdbgcfkFikikhkigeidieFikggikhkffaffijhidhhakgdkhkijF1kiakF1kfheakgdkif";
            suoS+="iggkigicjiejkieedikgdfcggkigieeiejfgkgkigbgikicggkiaideeijkefjeijikhkiggkiaidheigcikaikffikijgkiahi1";
            suoS+="hhdikgjfifaakekighie1hiaikggikhkffakicjhiahaikggikhkijF1kfejfeFhidikggiffiggkigicjiekgieeigikggiffig";
            suoS+="gkidheigkgfjkeigiegikifiggkidhedeijcfkFikikhkiggkidhh1ehigcikaffkhkiggkidhh1hhigikekfiFkFikcidhh1hit";
            suoS+="cikggikhkfkicjicghiediaikggikhkijbjfejfeFhaikggifikiggkigiejkikgkgieeigikggiffiggkigieeigekijcijikgg";
            suoS+="ifikiggkideedeijkefkfckikhkiggkidhh1ehijcikaffkhkiggkidhh1hhigikhkikFikfckcidhh1hiaikgjikhfjicjicgie";
            suoS+="hdikcikggifikigiejfejkieFhegikggifikiggfghigkfjeijkhigikggifikiggkigieeijcijcikfksikifikiggkidehdeij";
            suoS+="cfdckikhkiggkhghh1ehijikifffffkhsFngErD1pAfBoDd1BlEtFqA2AqoEpDqElAEsEeB2BmADlDkqBtC1FnEpDqnEmFsFsAFn";
            suoS+="llBbFmDsDiCtDmAB2BmtCgpEplCpAEiBiEoFqFtEqsDcCnFtADnFlEgdkEgmEtEsCtDmADqFtAFrAtEcCqAE1BoFqC1F1DrFtBmF";
            suoS+="tAC2ACnFaoCgADcADcCcFfoFtDlAFgmFqBq2bpEoAEmkqnEeCtAE1bAEqgDfFfCrgEcBrACfAAABqAAB1AAClEnFeCtCgAADqDoB";
            suoS+="mtAAACbFiAAADsEtBqAB2FsDqpFqEmFsCeDtFlCeDtoEpClEqAAFrAFoCgFmFsFqEnAEcCqFeCtFtEnAEeFtAAEkFnErAABbFkAD";
            suoS+="nAAeCtFeAfBoAEpFtAABtFqAApDcCGJ";
            
            #1645-09-23开始7567个节气修正表
            qiS ="FrcFs22AFsckF2tsDtFqEtF1posFdFgiFseFtmelpsEfhkF2anmelpFlF1ikrotcnEqEq2FfqmcDsrFor22FgFrcgDscFs22FgEe";
            qiS+="FtE2sfFs22sCoEsaF2tsD1FpeE2eFsssEciFsFnmelpFcFhkF2tcnEqEpFgkrotcnEqrEtFermcDsrE222FgBmcmr22DaEfnaF22";
            qiS+="2sD1FpeForeF2tssEfiFpEoeFssD1iFstEqFppDgFstcnEqEpFg11FscnEqrAoAF2ClAEsDmDtCtBaDlAFbAEpAAAAAD2FgBiBqo";
            qiS+="BbnBaBoAAAAAAAEgDqAdBqAFrBaBoACdAAf1AACgAAAeBbCamDgEifAE2AABa1C1BgFdiAAACoCeE1ADiEifDaAEqAAFe1AcFbcA";
            qiS+="AAAAF1iFaAAACpACmFmAAAAAAAACrDaAAADG0";
            
            self.SB = Shuoqi.jieya(suoS);  #定朔修正表解压
            self.QB = Shuoqi.jieya(qiS);   #定气修正表解压
            
        #排月序(生成实际年历),在调用calcY()后得到以下数据
        #时间系统全部使用北京时，即使是天象时刻的输出，也是使用北京时
        #如果天象的输出不使用北京时，会造成显示混乱，更严重的是无法与古历比对
        self.leap=0         #闰月位置
        self.ym=[0]*14 #各月名称
        self.ZQ=None #中气表,其中.liqiu是节气立秋的儒略日,计算三伏时用到
        self.HS=None #合朔表
        self.dx=[0]*14 #各月大小
        self.julian = None
        self.year, self.month, self.day = None, None, None
        if lunar is not None:
            sec = lunar.split('年')
            iyear = int(sec[0])
            jda, jdb = JDate(iyear), JDate(iyear+1) 
            sqa, sqb = Shuoqi(jda), Shuoqi(jdb)
            while sqa.year <= iyear and sqa.dateDescription != lunar:
                jda = jda+1
                sqa = Shuoqi(jda)
            if sqa.year == iyear:
                self.julian = jda
        if jd is None:
            jd = self.julian
        if jd is not None:
            self.julian = jd
            self.calcY(jd)
                
    @property
    def dateDescription(self):
        if self.julian:
            return "%d年%s%s"%(self.year, self.getMonth(self.julian,True), self.day)
#         else:
#             return
    
    #节气定月
    def getMonth(self, jd, moon=False):
        if type(jd) is JDate:
            jd = jd.J2000
        
        n = 0
        if moon:
            for i in self.HS:
                if i > jd:
                    n -= 1
                    break
                n += 1
            assert i > jd
            self.day = Shuoqi.dateDay(jd-self.HS[n]+1)
            self.month = n = self.ym[n]
        else:
            for i in xrange(1, 24, 2):
                n += 1
                if jd < self.ZQ[i]:
                    break
            self.month = n
            self.day = jd-self.ZQ[n]+1
        return n
 

    #public公有成员定义
    def calc(self, jd, isJieqi = False): #jd应靠近所要取得的气朔日,isJieqi=True时，算节气的儒略日
        jd += J2000#2451545
        fittingTable = self.qiKB if isJieqi else self.suoKB
        pc = 7 if isJieqi else 14
        
        f1=fittingTable[0]-pc
        f2=fittingTable[-1]-pc
        f3=2436935
    
        if jd<f1 or jd>=f3: #平气朔表中首个之前，使用现代天文算法。1960.1.1以后，使用现代天文算法 (这一部分调用了qi_high和so_high,所以需星历表支持)
            if isJieqi:
                return floor(self.qi_high ( floor((jd+pc-2451259)/365.2422*24) * pi/12 ) +0.5) # ) #2451259是1999.3.21,太阳视黄经为0,春分.定气计算
            else:
                return floor( self.so_high ( floor((jd+pc-2451551)/29.5306) * pi*2 )      +0.5) #2451551是2000.1.7的那个朔日,黄经差为0.定朔计算
        elif f1<=jd<f2: #平气或平朔
            for i in xrange(0, len(fittingTable),2):
                if jd+pc<fittingTable[i+2]:
                    break
            D = fittingTable[i] + fittingTable[i+1] * floor( (jd+pc-fittingTable[i])/fittingTable[i+1] )
            D = floor(D+0.5)
            if D==1683460: D+=1 #如果使用太初历计算-103年1月24日的朔日,结果得到的是23日,这里修正为24日(实历)。修正后仍不影响-103的无中置闰。如果使用秦汉历，得到的是24日，本行D不会被执行。
            return D-J2000#2451545
        elif f2<=jd<f3: #定气或定朔
            if isJieqi:
                D = floor( self.qi_low( floor((jd+pc-2451259)/365.2422*24) * pi/12 ) +0.5 ) #2451259是1999.3.21,太阳视黄经为0,春分.定气计算
                n = self.QB[int(floor((jd-f2)/365.2422*24))] #找定气修正值
            else:
                D = floor( self.so_low( floor((jd+pc-2451551)/29.5306) * pi*2 )     +0.5 ) #2451551是2000.1.7的那个朔日,黄经差为0.定朔计算
                n = self.SB[int(floor((jd-f2)/29.5306))] #找定朔修正值
            if(n=="1"): return D+1
            if(n=="2"): return D-1
            return D
        
    def calcY(self, jd): #农历排月序计算,可定出农历,有效范围：两个冬至之间(冬至一 <= d < 冬至二)
        if type(jd) is JDate:
            jd = jd.J2000
        jieqiTable=self.ZQ=[0]*25   #中气表(整日)
        heshuoTable=self.HS=[0]*15  #日月合朔表(整日)
        #该年的气
        preWinterSolstice = floor( (jd-355+183)/365.2422 )*365.2422+355  #355是2000.12冬至,得到较靠近jd的冬至估计值
        if self.calc(preWinterSolstice,True)>jd: 
            preWinterSolstice-=365.2422
        for i in xrange(25):
            jieqiTable[i]=self.calc(preWinterSolstice+15.2184*i,True) #25个节气时刻(北京时间),从冬至开始到下一个冬至以后
        
        #补算二气,确保一年中所有月份的“气”全部被计算在内    
        self.pe1 = self.calc(preWinterSolstice-15.2,True)
        self.pe2 = self.calc(preWinterSolstice-30.4,True) 
        
        #今年"首朔"的日月黄经差firstNewMoon
        firstNewMoon = self.calc(jieqiTable[0],False) #求较靠近冬至的朔日
        if firstNewMoon>jieqiTable[0]: firstNewMoon -= 29.53
        
        #该年所有朔,包含14个月的始末
        #并计算大小月（月内的天数）
        for i in xrange(15):
            heshuoTable[i]=self.calc(firstNewMoon+29.5306*i,False)
            if i>0:
                j = i-1
                self.dx[j] = heshuoTable[i]-heshuoTable[j]     #月大小
                self.ym[j] = j  #月序初始化
        self.leap = 0
        
        #-721年至-104年的后九月及月建问题,与朔有关，与气无关
        YY = floor( (self.ZQ[0]+10 +180)/365.2422) + 2000 #确定年份
        self.year = int(YY)
        if -721<=YY<=-104:
            ns = ()
            for i in xrange(3):
                yy = YY+i-1
                #颁行历年首, 闰月名称, 月建
                if(yy>=-721): 
                    ns[i]=self.calc(1457698-J2000+floor(0.342+(yy+721)*12.368422)*29.5306,False)
                    ns[i+3]='十三'
                    ns[i+6]=2  #春秋历,ly为-722.12.17
                if(yy>=-479): 
                    ns[i]=self.calc(1546083-J2000+floor(0.500+(yy+479)*12.368422)*29.5306,False)
                    ns[i+3]='十三'
                    ns[i+6]=2;  #战国历,ly为-480.12.11
                if(yy>=-220): 
                    ns[i]=self.calc(1640641-J2000+floor(0.866+(yy+220)*12.369000)*29.5306,False)
                    ns[i+3]='后九'
                    ns[i+6]=11; #秦汉历,ly为-221.10.31
            
            for i in xrange(14):
                for nn in (2,1,0):
                    if self.HS[i]>=ns[nn]:
                        break
                f1 = floor( (self.HS[i]-ns[nn]+15)/29.5306 ) #该月积数
                if(f1 < 12):
                    self.ym[i] = Shuoqi.yueNames[(f1+ns[nn+6])%12] 
                else:
                    self.ym[i] = ns[nn+3]
        else:        
            #无中气置闰法确定闰月,(气朔结合法,数据源需有冬至开始的的气和朔)
            if heshuoTable[13] <= jieqiTable[24]: #第13月的月末没有超过冬至(不含冬至),说明今年含有13个月
                i=1 #在13个月中找第1个没有中气的月份
                while heshuoTable[i+1]>jieqiTable[2*i]  and  i<13:
                    i+=1
                self.leap = i
                while i<14:
                    self.ym[i] -= 1
                    i+=1
            
            #名称转换(月建别名)
            for i in xrange(14):
                Dm = self.HS[i]+J2000
                v2=self.ym[i] #Dm初一的儒略日,v2为月建序号
                mc = Shuoqi.yueNames[v2%12] #月建对应的默认月名称：建子十一,建丑十二,建寅为正……
                if Dm>=1724360 and Dm<=1729794:
                    mc = Shuoqi.yueNames[(v2+1)%12] #  8.01.15至 23.12.02 建子为十二,其它顺推
                elif Dm>=1807724 and Dm<=1808699:
                    mc = Shuoqi.yueNames[(v2+1)%12] #237.04.12至239.12.13 建子为十二,其它顺推
                elif Dm>=1999349 and Dm<=1999467:
                    mc = Shuoqi.yueNames[(v2+2)%12] #761.12.02至762.03.30 建子为正月,其它顺推
                elif Dm>=1973067 and Dm<=1977052:
                    if v2%12==0: mc="正"
                    if v2==2: mc = '一' #689.12.18至700.11.15 建子为正月,建寅为一月,其它不变
                
                if Dm==1729794 or Dm==1808699:
                    mc='拾贰'   #239.12.13及23.12.02均为十二月,为避免两个连续十二月，此处改名
                
                self.ym[i]=mc;
        
        for i in xrange(len(self.ym)):
            if self.ym[i] == '正':
                if self.HS[i]>jd: self.year-=1
            self.ym[i] += '月'
            if i>0 and self.ym[i] == self.ym[i-1]:
                self.ym[i] = '闰'+self.ym[i]        
            
        
if __name__ == '__main__':
    jd = -4500#5531#5479#-95531#-655957#5156 #2457074#2456685#5522#2456693#(
    ssq= Shuoqi(jd)
    
    print jd
    print ssq.year
    print ssq.dx, ssq.leap
    print "合朔", ssq.HS
    print ssq.getMonth(jd)
    
    for i in ssq.ym: print i,
    print
    
    print "节气", ssq.ZQ
    
    ssq.calc(5143.531200)    