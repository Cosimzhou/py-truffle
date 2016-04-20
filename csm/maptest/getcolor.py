#coding: utf-8
from PIL import Image
szfile = '/home/zhouzhichao/图片/2014-08-27 18:50:54的屏幕截图.png'
szoutfile = '/home/zhouzhichao/ditu/color.png'

img = Image.open(szfile)
# img = img.crop((500, 400,300,300))
# img.save(szoutfile)

print img.load()[500, 300]#0xb9dcc1
#(245, 243, 240) = 0xf0f3f5