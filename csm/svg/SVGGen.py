#coding: UTF-8

svgFileHeader=\
'''<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: Adobe Illustrator 16.0.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1"
     id="Capa_1" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:cc="http://web.resource.org/cc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:svg="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" sodipodi:docbase="Z:\mysrc\optisvg" sodipodi:version="0.32" inkscape:version="0.44" sodipodi:docname="%(docname)s.svg"
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="%(width)spx"
     height="%(height)spx" viewBox="0 0 %(width)s %(height)s" enable-background="new 0 0 %(width)s %(height)s" xml:space="preserve">
'''


svgFileTailer='''
</svg>'''

#线 (l ine):显示两个坐标之间的连线。下面的例子绘制了一条从x,y 为16,63到x, y为 128, 63的线段。  
lineFormat = '''<line fill ="none" stroke="%(strColor)s" stroke-width="%(strWidth)s" x1="%(x1)s" y1="%(y1)s" x2="%(x2)s" y2 ="%(y2)s"/>
'''
#矩 形 (rect) :显示左上角在指定点并且高度和宽度为指定值的矩形(包括正方形)。 也可以通过指定边角圆的x和y半径画成圆角矩形。下面的例子显示了一个蓝色矩形。
rectFormat = '''<rect fill="%(fillColor)s" stroke="%(strColor)s" stroke-width="%(strWidth)s" x ="%(x)s" y ="%(y)s" width ="%(width)s" height="%(height)s"/>
'''

propertiesFormat = {
'line':    (('x1', 'y1', 'x2', 'y2'),
            ('fill','stroke','stroke-width',)),
'rect':    (('x', 'y', 'width', 'height'), 
            ('fill','stroke','stroke-width')),   
'circle':  (('x','y','r'),
            ('fill','stroke','stroke-width')),    
'ellipse': (('cx', 'cy', 'rx', 'ry'),
            ()),
'poly':    (('points'),()),    
'polygon': (('points'),()),    
'path':    (('d'),()),                     
}

#圆 ( circle):显示一个圆心在指定点、半径为指定长度的标准的圆。下面的例子绘制 了一个蓝色的实心圆，中心点在(x, y)为(100, 100)的位置，半径为500
'''<circlec x ="100"cy ="100"r= "50"fill="rgb(0,0,255)" />'''
#椭圆(ellipse):显示中心在指定点、长轴和短轴半径为指定长度的椭圆。 下面的例子显示了一个蓝色实心椭圆。  
'''<ellipse fill= "rgb(0,0,255) stroke= "rgb(0,0,0)" stroke-width="1" cx="100" cy="80" rx= "8" ry ="12"/>'''
  

#折 线 (polyline) :显示顶点在指定点的一组线。下面的例子绘制了一系列灰色线段。  
'''<poly line fill="none" stroke="rgb(128,128,128)” stroke-width="5" points=350,250 45 0,2 50 4 50 ,3756 50,1756 50,3757 50,375"/>'''
#多边 形 (polygon):类似于polyline，但增加了从最末点到第一点的连线，从而创建 了一个闭合形状。在下面的例子中，绘制了一个五角星。  
'''<polygon fill="rgb(0,0,255)" stroke="rgb(0,0,0)" stroke-width="1" points="350,75 379,161 469,161 397,215 423,301 350,250 277,301 301,215 231,161 321,161"/>'''

#
'''<path fill="#B3B3B3" d="M1324.01,227.96c-0.479,0.24-0.959,0.48-1.438,0.72c0.409,0.563,2.041,0.83,2.354-0.014
    C1325.133,228.142,1324.477,227.271,1324.01,227.96"/>'''
    
class svgGraph(object):
    def __init__(self, *args, **kwargs):
        self.width = 1024
        self.height = 786
        self.docname = 'test-doc'
        self.content = []
        self.strWidth = '2'
        self.strColor = '#000000'
        
    def output(self):
        with open('/Users/zhouzhichao/%s.svg'%self.docname, 'w+') as f:
            f.write(svgFileHeader % self.__dict__)
            for l in self.content:
                f.write(l+'\n')
            f.write(svgFileTailer)
    
    def line(self, x1, y1, x2, y2, **kwargs):
        locdict = {'x1':x1,'x2':x2,'y1':y1,'y2':y2}
        locdict.update(self.__dict__)
        if kwargs:locdict.update(kwargs)
        text = lineFormat % locdict
        self.content.append(text)
        
    def rect(self):
        self.addElement('rect', rect=0)
        
    def addElement(self, element, **kwargs):
        arrFormat = propertiesFormat.get(element)
        text = '<%s ' % element
        for f in (1,0):
            for i in arrFormat[f]:
                if i in kwargs:
                    
                    text += '%s="%s" '%(i, kwargs[i])
        text += '/>'
        self.content.append(text)
        
        
if __name__ == '__main__':
    s = svgGraph()
    print s.__dict__
    s.output()

    