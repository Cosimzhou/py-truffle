# -*- coding: UTF-8 -*-

try:
    import Image, ImageDraw, ImageFont
except ImportError as e:
    from PIL import Image, ImageDraw, ImageFont
from math import sin, cos


font = ImageFont.truetype("/Library/Fonts/华文细黑.ttf",180)

def textdraw(dest, txt, n, theta):
    im = Image.new("RGBA", (200,200), (0,0,0,0))
    ImageDraw.Draw(im).text((10,10), txt.decode("UTF-8"), font=font, fill=(255,0,0))
    im = im.resize((100,200))
    
    img = Image.new("RGBA", (282,282), (0,0,0,0))
    img.paste(im, (91,41))
    
    theta *= n
    theta += 120
    otheta = 45 # 240-theta
    
    im = img.rotate(145)

    cx, cy, r = 200, 200, 300
    
    x = int(cx+r*cos(theta))
    y = int(cy+r*sin(theta))
    
    dest.paste(im, (x,y))
    
n = 7
txt = '你'
a = 240.0 / n
img = Image.new("RGBA", (800,800), (0,0,0,0))

for i in xrange(n+1):
    textdraw(img, txt, i, a)

img.save("/Users/zhouzhichao/tmp/img.png", "PNG")