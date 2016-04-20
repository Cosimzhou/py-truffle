#coding:UTF-8
import math

def Luma_ITU_R_601_2(R,G,B):
    return (R * 299 + G * 587 + B * 114)/1000.0
def Luma_ITU_R_601_2_4rgb(r,g,b):
    return (r * 299 + g * 587 + b * 114)/255000.0

def rgb2hsb(rgbR, rgbG, rgbB):  
#     assert 0 <= rgbR <= 255  
#     assert 0 <= rgbG <= 255  
#     assert 0 <= rgbB <= 255  
    minV, _, maxV = sorted([ rgbR, rgbG, rgbB ])
  
    delta = maxV - minV
    hsbB = maxV / 255.0  
    hsbS = 0.0 if maxV == 0 else delta / float(maxV)  
  
    hsbH = 0.0  
    if delta > 0:
        if maxV == rgbR and rgbG >= rgbB:  
            hsbH = (rgbG - rgbB) * 60.0 / delta + 0  
        elif maxV == rgbR and rgbG < rgbB:  
            hsbH = (rgbG - rgbB) * 60.0 / delta + 360  
        elif maxV == rgbG:  
            hsbH = (rgbB - rgbR) * 60.0 / delta + 120  
        elif maxV == rgbB:  
            hsbH = (rgbR - rgbG) * 60.0 / delta + 240  

    return [hsbH, hsbS, hsbB]  

  
def hsb2rgb(hsbH, hsbS, hsbB):  
#     assert Float.compare(hsbH, 0.0f) >= 0 && Float.compare(hsbH, 360.0f) <= 0  
#     assert Float.compare(hsbS, 0.0f) >= 0 && Float.compare(hsbS, 1.0f) <= 0  
#     assert Float.compare(hsbB, 0.0f) >= 0 && Float.compare(hsbB, 1.0f) <= 0  
  
    r = g = b = 0  
    i = int(hsbH / 60.0) % 6
    f = (hsbH / 60.0) - i  
    p = hsbB * (1.0 - hsbS)  
    q = hsbB * (1.0 - f * hsbS)  
    t = hsbB * (1.0 - (1.0 - f) * hsbS)  
    if i == 0:  
        r, g, b = hsbB, t, p 
    elif i == 1:  
        r, g, b = q, hsbB, p  
    elif i == 2:  
        r, g, b = p, hsbB, t
    elif i == 3:  
        r, g, b = p, q, hsbB  
    elif i == 4:  
        r, g, b = t, p, hsbB
    elif i == 5:  
        r, g, b = hsbB, p, q  
        
    return [int(r * 255.0), int(g * 255.0), int(b * 255.0)]  

def rgb2lab(R, G, B):
    X = 0.412453*R + 0.357580*G + 0.180423*B
    Y = 0.212671*R + 0.715160*G + 0.072169*B
    Z = 0.019334*R + 0.119193*G + 0.950227*B 
    
    X = X/(255*0.950456)
    Y = Y/255
    Z = Z/(255*1.088754)
    
    if Y > 0.008856:
        fY = Y**(1/3.0)
        fX = X**(1/3.0)
        fZ = Z**(1/3.0)
        L= 116*fY - 16    
    if Y < 0.008856:
        fY = 7.787*Y + 16/116.0
        fX = 7.787*X + 16/116.0
        fZ = 7.787*Z + 16/116.0
        L= 903.3*Y
    
    a = 500.0*(fX - fY) +128
    b = 200.0*(fY - fZ) +128
    return [L,a,b]

def lab2rgb(L, a, b):
    a-=128
    b-=128
    fY = ((L + 16) / 116.0)**3
    if fY < 0.008856: fY = L / 903.3
    Y = fY
    if fY > 0.008856: fY = fY**(1/3.0) 
    if fY < 0.008856: fY = 7.787 * fY + 16/116    
    fX = a / 500.0 + fY
    if fX > 0.206893: X = fX**(1/3.0) 
    if fX < 0.206893: X = (fX - 16/116.0) / 7.787
    fZ = fY - b /200.0
    if fZ > 0.206893: Z = fZ**(1/3.0)
    if fX < 0.206893: Z = (fZ - 16/116.0) / 7.787
    
    X, Y, Z = X * 0.950456 * 255,  Y * 255.0, Z * 1.088754 * 255  

    R = 3.240479*X - 1.537150*Y - 0.498535*Z 
    G =-0.969256*X + 1.875992*Y + 0.041556*Z
    B = 0.055648*X - 0.204043*Y + 1.057311*Z
    
    return [int(R), int(G), int(B)]



# def kline(k): 
#     k/=100.0   
#     if k <= 0.3:
#         k*=0.75
#     elif k <= 0.7:
#         k=k*0.875 - 0.0375
#     elif k <= 0.8:
#         k*=1.0625 - 0.1688
#     elif k <= 0.92:
#         k*=1.3125 - 0.3688
#     else:
#         k=k*k
#     return k
#   
#    
# def cmyk2rgb(c,m,y,k):
# #     if (CMYKColor.C == 0 && CMYKColor.M == 0.5 && CMYKColor.Y == 0 && CMYKColor.K == 0.5)
# #      cout<<"";
#       
#     colorMix = math.sqrt(math.pow(kline(c),2) + math.pow(kline(k),2))
#     r = 255*max((0,1 - colorMix))
#     colorMix=math.sqrt(math.pow(kline(m),2) + math.pow(kline(k),2)) + 0.25*c;
#     g = 255*max((0,1 - colorMix))
#     colorMix=math.sqrt(math.pow(kline(y),2) + math.pow(kline(k),2)) + 0.25*m;
#     b = 255*max((0,1 - colorMix))
#     return r,g,b

# 
# def cymk2rgb(c,y,m,k):
#     m1 = c if c>y else y
#     m2 = m if m>k else k
#     maxval = m1 if m1>m2 else m2
#     r = (k*c)/maxval
#     g = (k*m)/maxval
#     b = (k*y)/maxval
#     
def rgb2cmyk(r,g,b): 
    c, m, y = 255-r, 255-g, 255-b
    k = 0
    temp = min((c, m, y))
    if temp != 0:
        temp2 = round((1-(r+g+b)/3.0/255) * temp)
        k = round((temp2 / 255.0) * 100)
        c = round(((c - temp2) / 255.0) * 100)
        m = round(((m - temp2) / 255.0) * 100)
        y = round(((y - temp2) / 255.0) * 100)
    else:
        c = round((c / 255.0) * 100)
        m = round((m / 255.0) * 100)
        y = round((y / 255.0) * 100)
    return c, m, y, k
        
def cmyk2rgb(c,m,y,k):
    r = 255*(100-c)*(100-k)/10000
    g = 255*(100-m)*(100-k)/10000
    b = 255*(100-y)*(100-k)/10000
    return r, g, b
 

if __name__ == '__main__':
# 
# rgb=(142,52,201)
# hsb=rgb2hsb(*rgb)
# lab=rgb2lab(*rgb)
# rgb2=lab2rgb(*lab)
# print rgb, Luma_ITU_R_601_2(*rgb), hsb, lab, rgb2
    hsb=[0]*3
    hsb[0]=120
    hsb[2]=1
    for s in xrange(101):
        hsb[1] = s/100.0
        rgb = hsb2rgb(*hsb)
        print s, Luma_ITU_R_601_2(*rgb)
    for s in xrange(101):
        hsb[2] = (100-s)/100.0
        rgb = hsb2rgb(*hsb)
        print hsb[2], Luma_ITU_R_601_2(*rgb)

    rgb = cmyk2rgb(95,10,50,33)
    print rgb
    cmyk = rgb2cmyk(*rgb)
    print cmyk
    rgb = cmyk2rgb(*cmyk)
    print rgb
    print
    cmyk = rgb2cmyk(0,200,0)
    print cmyk
    print cmyk2rgb(*cmyk)
    