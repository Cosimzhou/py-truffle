#! /usr/bin/python
# -*- coding:UTF-8 -*-

from PIL import Image, ImageDraw, ImageChops

img = Image.open('/Users/zhouzhichao/Downloads/subway.jpg')
pix = img.load()
szimg = img.size
cnter = {}
pix[100,100]=(0,0,0)

for i in xrange(szimg[0]):
    for j in xrange(szimg[1]):
        color = "%02x%02x%02x"%pix[i,j]
        cnt = cnter.get(color, 0)
        cnter[color] = cnt+1
#         pix[i,j]=(0,0,0)        
# pix[101,101]=(0,0,0)        

# img.save('/tmp/xx.png')
array = sorted(cnter.items(), key=lambda x:x[1], reverse=True) 
limit = (szimg[0]*szimg[1] - array[0][1])/500
for i in xrange(len(array)):
    if array[i][1] < limit:
        break
limit = array[i][1]
    
for i in xrange(1,szimg[0]-1):
    for j in xrange(1,szimg[1]-1):
        color = "%02x%02x%02x"%pix[i,j]
        cnt = cnter[color]
        if cnt > limit:
            continue
        n = []
        n.append("%02x%02x%02x"%pix[i-1,j])
        n.append("%02x%02x%02x"%pix[i,j-1])
        n.append("%02x%02x%02x"%pix[i-1,j-1])
        
        cnter[color] = cnt+1
        
            
print len(cnter)

print i,array[:i]