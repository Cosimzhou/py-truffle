#coding: UTF-8



def normalCSV():
    def bigcode(men,da,zhong,xiao):
        if men == 'A':
            if 0<len(xiao)<=6:
                return 'A'+(xiao+'000000')[:6]
            elif 0<len(zhong)<=6:
                return 'A'+(zhong+'000000')[:6]
            elif 0<len(da)<=6:
                return 'A'+(da+'0000000')[:6]
            return 'A000000'
        else:
            if 0<len(xiao)<=6:
                return men+('000000'+xiao)[-6:]
            elif zhong:
                zhong+='00'
                xiao = ('000000'+zhong)[-6:]
            elif da:
                da+='0000'
                xiao=('000000'+da)[-6:]
            else:
                xiao='000000'
        return men+xiao
    of = open('/Users/zhouzhichao/workspace/mcdata/founders/typecode-1.csv', 'w')
    with open('/Users/zhouzhichao/workspace/mcdata/founders/typecode.csv', 'r') as f:
        no = 0
        men, da, zhong, xiao = '','','',''
        for l in f.readlines():
            if no:
                arr = l.split(';')
                if arr[0]:
                    men, da, zhong, xiao = arr[0:4]
                elif arr[1]:
                    da, zhong, xiao = arr[1:4]  
                elif arr[2]:
                    zhong, xiao = arr[2:4]                      
                elif arr[3]:
                    xiao = arr[3]
#                 else:
#                     if len(arr[3])<6:
                of.write(';'.join([bigcode(men, da, zhong, xiao)]+arr[4:]))
                print bigcode(men, da, zhong, xiao)        
                
            no += 1
    of.close()

def normalCSS():
    of = open('/Users/zhouzhichao/workspace/mcdata/founders/css-1.csv', 'w')
    with open('/Users/zhouzhichao/workspace/mcdata/founders/css.csv', 'r') as f:
        no = 0
        larr = []
        for l in f.readlines():
            if no:
                arr = l.split(';')
                if arr[2]:
                    of.write( ';'.join(larr))
                    larr = list(arr)
                else:
                    larr[3] = larr[3].strip('\n')+'`'+arr[3]     
            no+=1
    of.close()
            
def extractCSS():
    def cmyk2rgb(c,m,y,k):
        r = 255*(100-c)*(100-k)/10000
        g = 255*(100-m)*(100-k)/10000
        b = 255*(100-y)*(100-k)/10000
        return r, g, b

    of = open('/Users/zhouzhichao/workspace/mcdata/founders/css-2.csv', 'w')
    with open('/Users/zhouzhichao/workspace/mcdata/founders/css-1.csv', 'r') as f:
        no = 0
        for l in f.readlines():
            if no:
                property = []
                arr = l.strip('\n').split(';')
                colortype=''
                for s in arr[-1].split('`'):                    
                    ss = s.split(':')
                    if ss[0].endswith('olor'):
                        iss = ss[1].split(',')
                        iss[0] = iss[0][iss[0].index('(')+1:]
                        iss[-1]= iss[-1][:-1]
                        r,g,b = cmyk2rgb(int(iss[0]),int(iss[1]),int(iss[2]),int(iss[3]))
                        property.append('%s%s:0x%02X%02X%02XFF'%(colortype,ss[0],r,g,b))
                    elif ss[0] == 'fontName':
                        colortype='font'
                    elif ss[0] == 'fontSize':
                        colortype='font'
                        property.append(':'.join(ss))
                    elif ss[0] == 'icon' or ss[0]=='iconSize':
                        ss[1]=ss[1].replace(',','-')
                        colortype = 'icon'
                        property.append(':'.join(ss))
                    else:
                        colortype = ''
                        property.append(':'.join(ss))
                arr[-1] = ','.join(property)
                of.write(';'.join(arr) + '\n')
            no+=1
    of.close()
    
def css():
    fontSize=set()
    lineWidth=set()
    strokeWidth=set()
    icon=set()
    of = open('/Users/zhouzhichao/workspace/mcdata/founders/css-3.csv', 'w')
    with open('/Users/zhouzhichao/workspace/mcdata/founders/css-2.csv', 'r') as f:
        no = 0
        for l in f.readlines():
            if no:
                property = []
                arr = l.strip('\n').split(';')
                for s in arr[-1].split(','):      
                    if s.startswith('iconSize') or s.startswith('iconColor'):
                        continue
                    if s.startswith('icon:'):
                        aa=s[5:].split('-')
                        aa[1]=('0000'+aa[1])[-3:]
                        aa=''.join(aa)
                        icon.add(aa)
                        s=s[:5]+aa
                    elif s.startswith('fontSize:'):
                        fontSize.add(s[9:])
#                     elif s.startswith('fontSize:'):
#                         fontSize.add(s[9:])
                    elif s.startswith('lineWidth:'):
                        lineWidth.add(s[10:])
                    elif s.startswith('strokeWidth:'):
                        strokeWidth.add(s[12:])
                        
                    property.append(s)
                arr[-1] = ','.join(property)
                of.write(';'.join(arr) + '\n')
            else:
                of.write(l)
            no+=1
    of.close()
    
    print fontSize
    print lineWidth
    print strokeWidth
    print icon
    
def CSV2bigCode():
#     of = open('/Users/zhouzhichao/workspace/mcdata/founders/typetable.csv', 'w')
    of1 = open('/Users/zhouzhichao/workspace/mcdata/founders/typetable.xml', 'w')
    with open('/Users/zhouzhichao/workspace/mcdata/founders/typecode-1.csv', 'r') as f:
        no = 0
        for l in f.readlines():
            if no:
                aaa=[]
                arr=l.decode('GBK').decode('UTF-8').split(';')
                minl, maxl = 0, 0
                if arr[2] == '√': minl=17
                if arr[3] == '√': minl=12
                if arr[4] == '√': minl=8
                
                if arr[4] == '√': maxl=12
                if arr[3] == '√': maxl=17
                if arr[2] == '√': maxl=20
                
                if minl==0 or maxl==0: continue
                
                aaa.append(arr[0].rstrip('0'))
                aaa.append(arr[1])
                aaa.append(str(no/128+1))
                aaa.append(str(no%128))
                aaa.append(str(minl))
                aaa.append(str(maxl))
                
#                 of.write(';'.join(aaa)+'\n')
                of1.write("""<data k1="%s"><!-- %s -->
        <type>%s</type>
        <subtype>%s</subtype>
        <minDisplayLV>%s</minDisplayLV>
        <maxDisplayLV>%s</maxDisplayLV>
      </data>
      """%tuple(aaa))
#             else:
#                 of.write(l)
            no += 1
#     of.close()
    of1.close()
    
def iconConfig():
    ddict={}
    with open('/Users/zhouzhichao/workspace/mcdata/founders/css-3.csv', 'r') as f:
        for l in f.readlines():
            l = l.decode('GBK').encode('UTF-8').strip('\n')
            aa = l.split(';')
            aaa=aa[3].split(',')
            for a in aaa:
                if a.startswith('icon:'):
                    ddict[aa[2]] = a[5:]
                    break
    cnt = 0
    with open('/Users/zhouzhichao/workspace/mcdata/founders/translate.table', 'r') as f:
        for l in f.readlines():
            aa = l.strip('\n\r').split(',')
            k = aa[0][:-4]
            if k in ddict:
                cnt += 1
                print '<icon id="%s" name="ic_map_founder_%s.png"/>'%(ddict[k], aa[1])
                del ddict[k]
    print cnt,len(ddict)
    
    for k in ddict:
        print k, ddict[k]
        
def realUsed():
    dc = {}
    with open('/Users/zhouzhichao/workspace/mcdata/founders/typetable.csv', 'r') as f:
        for l in f.readlines():
            aa = l.strip('\n').split(';')
            dc[aa[0]] = aa[1:]
    
    with open('/Users/zhouzhichao/workspace/mcdata/founders/realUsed', 'r') as f:
        for l in f.readlines():
            aa = l.strip('\n').split(' ')
            if aa and aa[0]:
                a = dc.get(aa[0])
                if a:
                    print aa[0], a[0],a[3],a[4]


def makeGaiaConfig():
    context = """A420000;城际公路;8;20;2;16
A420100;国道;8;20;2;17
A420200;省道;8;20;2;18
A420300;县道;8;20;2;19
A420400;乡道;8;20;2;20
A420500;专用公路;8;20;2;21
A420600;匝道（连接道，交换道）;8;20;2;22
A420700;公路控制点;12;20;2;23
A429000;城际公路注记;8;20;2;24
A430000;城市道路;8;20;2;25
A430100;轨道交通;8;20;2;26
A430200;快速路;12;20;2;27
A430300;高架路;8;20;2;28
A430400;引道;12;20;2;29
A430500;街道;8;20;2;30
A430600;内部道路;12;20;2;31
A430700;阶梯路;17;20;2;32
A439000;城市道路注记;8;20;2;33
A440000;乡村道路;8;20;2;34
A440100;机耕路（大路）;8;20;2;35
A440200;乡村路;8;20;2;36
A440300;小路;8;20;2;37
A440400;时令路;12;17;2;38
A440500;山隘;8;17;2;39
A440600;栈道;12;17;2;40
A449000;乡村道路注记;8;20;2;41"""
    
    no = 12
    for l in context.split('\n'):
        aa = l.split(';')
        
        print """
      <data k1="%s"><!-- %s -->
        <type>75</type>
        <subtype>%d</subtype>
        <minDisplayLV>17</minDisplayLV>
        <maxDisplayLV>20/maxDisplayLV>
        <alias></alias>
        <funclass>99</funclass>
        <rank>8</rank>
        <direction>0</direction>
        <isCrossed>false</isCrossed>
        <rarefyDistanceNorm>1.0</rarefyDistanceNorm>
        <rarefyDistanceDevp>1.0</rarefyDistanceDevp>        
      </data>"""%(aa[0].strip('0'), aa[1], no)
        no+=1    



def makeRenderConfig():
    
    mrcBegin="""
  <!-- 默认(其他未定义类型) -->
  <dataset type="%s" geoType="GeoPoint">
    <render name="name">
      <default>
        <priority>20</priority>
      </default>
      <overide>"""
        
    cond="""        <cond subtype="%s"><values%s/></cond><!-- %s -->"""
        
    mrcEnd="""      </overide>
      <view name="vector" render="poi"></view>
      <view name="satellite" render="poi-S"></view>
    </render>
  </dataset>"""
    
    dcc, no = {}, 0
    with open('/Users/zhouzhichao/workspace/mcdata/founders/xxxxx.csv', 'r') as f:
        for l in f.readlines():
            aaa = l.strip('\n').split(';')
            if aaa[-1] and 0x41 <= ord(aaa[-1][0]) <= 0x45:
                dcc[no] = aaa[-1]
            no += 1

    css, no = {}, 0          
    with open('/Users/zhouzhichao/workspace/mcdata/founders/css-3.csv', 'r') as f:
        for l in f.readlines():
            aaa = l.strip('\n ').split(';')
            if no and dcc.get(no):
                css[dcc[no]] = aaa[-1]
            no += 1
    
    oldtype = ""
    tcc, no = {}, 0
    with open('/Users/zhouzhichao/workspace/mcdata/founders/typetable.csv', 'r') as f:
        for l in f.readlines():
            aaa = l.strip('\n ').split(';')
            if no and css.get(aaa[0]):
                if aaa[4] != oldtype:
                    if oldtype: print mrcEnd
                    oldtype = aaa[4]
                    print mrcBegin % oldtype

                cv = ''
                for v in css[aaa[0]].split(','):
                    aa = v.split(':')
                    if aa[0]=='fontSize':
                        aa[1] = str(int(round(float(aa[1])*4)))
                    cv += ' %s="%s"'%tuple(aa)
                
                print cond%(aaa[-1], cv, aaa[1])
            no += 1
        print mrcEnd

            
if __name__ == '__main__':
#     normalCSV()
#     normalCSS()
#     extractCSS()
#     css()
#     CSV2bigCode()
#     iconConfig()
    
#     realUsed()
#     makeGaiaConfig()
    
    makeRenderConfig()
    
    pass


