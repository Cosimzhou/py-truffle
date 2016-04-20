#! /usr/bin/python
#coding: utf-8

'''
Created on 2014年8月20日

@author: zhouzhichao
'''

import random, guiutil
from qrtest import QR_Coder, NBP, BBP, simpleQREncode
from PIL import Image, ImageDraw, ImageChops

def Luma_ITU_R_601_2(R,G,B):
    return (R * 299 + G * 587 + B * 114)/1000.0

def isDarkGray(R,G,B):
    return (R*30+G*59+B*11+50) < 10000#12800
def isLightGray(R,G,B):
    return (R*30+G*59+B*11+50) > 18000#12800
def RGB(R,G,B):
    return int(R)+(int(G)<<8)+(int(B)<<16)

def fitGray(realRng, aimRng, color, luma):
    if realRng[1] > realRng[0]:
        rate = (aimRng[1]-aimRng[0])/(realRng[1]-realRng[0])
        aimLuma = (luma - realRng[0]) * rate + aimRng[0]
    else:
        aimLuma = aimRng[0 if aimRng[0] < 150 else 1]
    
#     result = list(color) 
#     if min(color) > 0:
#         xr = (aimLuma - luma)*1000.0/(299+587*(color[1]/color[0])+114*(color[2]/color[0]))
#         result[0] += xr
#         result[1] = result[0]*color[1]/color[0]
#         result[2] = result[0]*color[2]/color[0]
#         if max(result) <= 255 and min(result)>=0:
#             return tuple(map(int, result))
        
    hsb = guiutil.rgb2hsb(*color)
    if aimLuma > 180:
        hsb[1]=(255-aimLuma)/100.0
        hsb[2]=1
    elif aimLuma < 100:
        hsb[1]=1
        hsb[2]=aimLuma/149.2
    
    return tuple(guiutil.hsb2rgb(*hsb))

def makeDarkFace(box):
    # box := (width, height)
    img = Image.new("RGB", box, 0)
    width, height = box 
    draw= ImageDraw.Draw(img)
    x, y, r, g, b = 0, 0, 0, 0, 0
    count = 0
    while count < 40:
        while True:
            rest = 9999
            r = random.uniform(0,rest/30)
            rest -= r*30 
            g = random.uniform(0,rest/59)
            rest -= g*59
            b = random.uniform(0,rest/11)
            if rest >= b*11:
                break
                
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        xr= random.uniform(3, width/3)
        yr= random.uniform(3, height/3)
        draw.ellipse(((x-xr, y-yr), (x+xr, y+yr)), RGB(r,g,b))
        count += 1

    img.save('/home/zhouzhichao/dark.png')
    return img
     
     
def makeLightFace(box):
    # box := (width, height)
    img = Image.new("RGB", box, 0xffffff)
    width, height = box 
    draw= ImageDraw.Draw(img)
    x, y, r, g, b = 0, 0, 0, 0, 0
    count = 0
    while count < 40:
        while True:
            rest = 5000
            r = random.uniform(0,rest/30)
            rest -= r*30 
            g = random.uniform(0,rest/59)
            rest -= g*59
            b = random.uniform(0,rest/11)
            if rest >= b*11:
                break
        
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        xr= random.uniform(3, width/3)
        yr= random.uniform(3, height/3)
        draw.ellipse(((x-xr, y-yr), (x+xr, y+yr)), RGB(255-r,255-g,255-b))
        count += 1

    img.save('/home/zhouzhichao/light.png')
    return img     
     

def drawDotStyle(qrc, unit=10):
    box = (qrc.size*unit,qrc.size*unit)
    img = Image.new("RGB", box, 0xFFFFFF)
    draw= ImageDraw.Draw(img)
    for i in xrange(qrc.size):
        for j in xrange(qrc.size):
            if qrc.matrix[j][i] != NBP:
                draw.rectangle(((i*unit,j*unit),((i+1)*unit,(j+1)*unit)), 0)
                #draw.ellipse(((i*unit,j*unit),((i+1)*unit,(j+1)*unit)), 0)
    return img

def createNuruTile(unit):
    box = (512*unit,unit)
    cci =  Image.new("RGB", (unit, unit), 0)
    draw= ImageDraw.Draw(cci)
    draw.ellipse(((0,0),(unit,unit)), 0xFFFFFF)
    
    img = Image.new("RGB", box, 0xFFFFFF)
    draw= ImageDraw.Draw(img)
    
    for i in xrange(1,512,2):
        draw.ellipse(((i*unit,0),((i+1)*unit,unit)), 0)
      
    for i in xrange(512):
        if i % 2 == 1:
            if (i & 2) > 0:
                draw.rectangle(((i*unit,unit),(i*unit+unit/2,0)), 0)
        
            if (i & 4) > 0:
                draw.rectangle(((i*unit,0),(i*unit+unit,unit/2)), 0)
                
            if (i & 8) > 0:
                draw.rectangle(((i*unit+unit/2, 0),(i*unit+unit,unit)), 0)
                
            if (i & 16) > 0:
                draw.rectangle(((i*unit,unit/2),(i*unit+unit,unit)), 0)
        else:
            draw.rectangle(((i*unit,0),((i+1)*unit,unit)), 0xFFFFFF)

            if (i & 38) == 38:
                img.paste(cci.crop((0,0,unit/2,unit/2)), (i*unit,0))

            if (i & 280) == 280:
                img.paste(cci.crop((unit/2,unit/2,unit,unit)), (i*unit+unit/2,unit/2))

            if (i & 82) == 82:
                img.paste(cci.crop((0,unit/2,unit/2,unit)), (i*unit,unit/2))

            if (i & 140) == 140:
                img.paste(cci.crop((unit/2,0,unit,unit/2)), (i*unit+unit/2,0))
    
    return img

def drawNurunuruStyle(qrc, unit=10):
    box = (qrc.size*unit,qrc.size*unit)
    tiles=createNuruTile(unit)
    img = Image.new("RGB", box, 0xFFFFFF)
    #draw= ImageDraw.Draw(img)
    for i in xrange(qrc.size):
        for j in xrange(qrc.size):
            blocktype = 0
            if qrc.matrix[j][i] != NBP:
                blocktype += 1
            if i > 0 and qrc.matrix[j][i-1] != NBP:
                blocktype += 2
                if j > 0 and qrc.matrix[j-1][i-1] != NBP:
                    blocktype += 32
                if j < qrc.size-1 and qrc.matrix[j+1][i-1] != NBP:
                    blocktype += 64
                    
            if j > 0 and qrc.matrix[j-1][i] != NBP:
                blocktype += 4
                
            if i < qrc.size-1 and qrc.matrix[j][i+1] != NBP:
                blocktype += 8
                if j > 0 and qrc.matrix[j-1][i+1] != NBP:
                    blocktype += 128
                if j < qrc.size-1 and qrc.matrix[j+1][i+1] != NBP:
                    blocktype += 256
                    
            if j < qrc.size-1 and qrc.matrix[j+1][i] != NBP:
                blocktype += 16

            img.paste(tiles.crop((blocktype*unit, 0, (blocktype+1)*unit, unit)), (i*unit,j*unit))
            
    img.save('/home/zhouzhichao/nuru.png')
    return img

          
def paintRandomColor(img):
    dimg = makeDarkFace(img.size)
    limg = makeLightFace(img.size)
    
    paintFrontBackImage(img, dimg, limg)
    

def RGB_RaiseGray(rgb):
    r, g, b = rgb&0xff, (rgb&0xff00)>>8, rgb>>16
    luma = Luma_ITU_R_601_2(r, g, b)
    if luma >= 180:
        return rgb
    diff = (180 - luma)/1000
    r += diff*299
    g += diff*587
    b += diff*114
    return RGB(r,g,b)
     

# def paintPictureColor(img):
#     fimg = makeDarkFace(img.size)
#     
#     im = Image.open('/home/zhouzhichao/下载/ginsan.jpg')
#     bimg = im.resize(img.size, Image.ANTIALIAS)
#     
#     mask = bimg.convert('L').point(lambda x: x < 180 and 255)
#     bands = bimg.split()
#     R, G, B = 0, 1, 2
#     lr = bands[R].point()
#     #for point(RGB_RaiseGray)
#     #tmp.save('/home/zhouzhichao/tmpxx.jpg')
#     
#     
#     paintFrontBackImage(img, fimg, bimg) 
    
def paintPictureCode(img, unit):
    im = Image.open('/home/zhouzhichao/下载/image001.jpg').convert('RGB')#makeDarkFace(img.size)#
    face = im.resize(img.size, Image.ANTIALIAS)
    
    qrmk = img.convert('1').load()
    imgf = face.load()
    imgsize = img.size[0]/unit
    
    rrng = ((0, 50), (220, 255))
    for x in xrange(imgsize):
        ux =x * unit
        for y in xrange(imgsize):
            uy = y * unit
            crng = [[0, 255], [0, 255]]
            crng = [[255,0], [255,0]]
            for i in xrange(unit):
                for j in xrange(unit):
                    lm = Luma_ITU_R_601_2(*imgf[ux+i,uy+j])
                    dl = 1 if qrmk[ux+i,uy+j] else 0
                    if crng[dl][0]>lm: crng[dl][0] = lm
                    if crng[dl][1]<lm: crng[dl][1] = lm 
                    
            for i in xrange(unit):
                for j in xrange(unit):
                    lm = Luma_ITU_R_601_2(*imgf[ux+i,uy+j])
                    dl = 1 if qrmk[ux+i,uy+j] else 0
                    imgf[ux+i,uy+j] = fitGray(crng[dl], rrng[dl], imgf[ux+i,uy+j], lm)
                    
    face.save('/home/zhouzhichao/choppa.png')
    
def paintFrontBackImage(img, frontimg, backimg):
    invimg = ImageChops.invert(img)
    invimg.save('/home/zhouzhichao/imginv.png')
    
    img1 = ImageChops.lighter(img, frontimg)
    img1.save('/home/zhouzhichao/img1.png')
    
    img2 = ImageChops.lighter(invimg, backimg)
    img2.save('/home/zhouzhichao/img2.png')
     
    img = ImageChops.multiply(img1, img2)
    img.save('/home/zhouzhichao/dot.png')        
            
            
if __name__ == '__main__':
    raw = '赣A C9216'#'http://avi.blog.jp'
    qrc = simpleQREncode(raw, qrcode=True)
    img = drawNurunuruStyle(qrc, 14)
    
    #img = drawDotStyle(qrc, 14)
    paintRandomColor(img)
    #paintPictureCode(img, 14)
    
    Image.open('/home/zhouzhichao/下载/image001.jpg').convert('L').point(lambda x: x<180 and 255).save('/home/zhouzhichao/choppa.png')
    pass