#coding: utf-8

#from PIL import Image, ImageDraw




from PIL import Image, ImageDraw, ImageChops
# from PIL import ImageEnhance, ImageFont


#import os, math
# import Image
# import ImageDraw
# 1 头像图片剪成圆形的，其他为透明
# 搜索了好久，没有找到比较好的方法，有个博客(不好意思，忘记博客地址了)用了一个比较诡异的方法，我试了一下，除了处理jpg图片没有格式转换，其他的都没有问题，我当时就先按照那个方法来了


def circle():
    ima = Image.open("/home/zhouzhichao/下载/dougao.jpg").convert("RGBA")
    size = ima.size

    # 因为是要圆形，所以需要正方形的图片
    r2 = min(size)
    if size != size:
        ima = ima.resize((r2, r2), Image.ANTIALIAS)
    imb = Image.new('RGBA', (r2, r2), 0xffffff)
    pima = ima.load()
    pimb = imb.load()

    cnt = 0
    r = float(r2/2) #圆心横坐标
    rx2 = r**2
    for i in range(r2):
        for j in range(r2):
            lx = abs(i-r+0.5) #到圆心距离的横坐标
            ly = abs(j-r+0.5)#到圆心距离的纵坐标
            l  = lx**2 + ly**2
            if l <= rx2:
                if cnt < 100:
                    print pima[i,j]
                    cnt += 1
                pimb[i,j] = pima[i,j]

    imb.save("/home/zhouzhichao/test_circle.png")

# 这个方法是 计算每个像素到原点（就是图片中心点）的距离来画圆形的
# 
# 下载/dougao.jpg
# 2、给图片的4个角加椭圆


def circle_corder_image():
    im = Image.open("/home/zhouzhichao/choppa.png").convert("RGBA")
    rad = 50  # 设置半径 
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    im.save('/home/zhouzhichao/test_circle_corder.png')

#用了这个方法后，想了一想，头像图片剪成圆形的，其他为透明，用这个方法也是可以的，于是画圆形有了下面的方法：


def circle_new():
    ima = Image.open("/home/zhouzhichao/下载/dougao.jpg").convert("RGBA")
    size = ima.size
    r2 = min(size)
#     if size != size:
    ima = ima.resize((r2, r2), Image.ANTIALIAS)
    circle = Image.new('L', (r2, r2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, r2, r2), fill=255)
    alpha = Image.new('L', (r2, r2), 255)
    alpha.paste(circle, (0, 0))
    ima.putalpha(alpha)
    ima.save('/home/zhouzhichao/test_circle.png')


# #import aggdraw
# 
# 
# 
# #--------------------------------
# 
# #批量处理照片的函数
# 
# #--------------------------------
# 
# 
# 
# #将照片变成圆角边
# 
# def RoundCorner(image, radius):
#     """
#     Generate the rounded corner image for orgimage.
#     """
# 
#     image = image.convert('RGBA')
#     #generate the mask image
#     mask = Image.new('RGBA', image.size, (0,0,0,0))
# 
#     draw = aggdraw.Draw(mask)
#     brush = aggdraw.Brush('black')
# 
#     width, height = mask.size
#     draw.rectangle((0, 0, mask.size[0], mask.size[1]), aggdraw.Brush('white'))
# 
#     #north-west corner
#     draw.pieslice((0,0,radius*2,radius*2), 90, 180, None, brush)
# 
#     #north-east corner
#     draw.pieslice((width-radius*2, 0, width, radius*2), 0, 90, None, brush)
# 
#     #south-west corner
#     draw.pieslice((0, height-radius*2, radius*2, height), 180, 270, None, brush)
# 
#     #south-east corner
#     draw.pieslice((width-radius*2, height-radius*2, width, height), 270, 360, None, brush)
# 
# 
# 
#     #center rectangle
#     draw.rectangle((radius, radius, width-radius, height-radius), brush)
# 
#     #four edge rectangle
#     draw.rectangle((radius, 0, width-radius, radius), brush)
#     draw.rectangle((0, radius, radius, height-radius), brush)
#     draw.rectangle((radius, height-radius, width-radius, height), brush)
#     draw.rectangle((width-radius, radius, width, height-radius), brush)
# 
#     draw.flush()
#     del draw
# 
#     return ImageChops.add(mask, image)
# 
# 
# 
# #加圆角线条边框
# def RoundCornerFrame(image, radius, line_width, line_color, opacity=1.0):
#     width, height = image.size
# 
#     draw = aggdraw.Draw(image)
#     pen = aggdraw.Pen(line_color, line_width, int(255 * opacity))
# 
#     #注意: aggdraw对角度的解释与PIL有区别！
# 
#     #aggdraw画线的位置是线的中线，因此，需要减除半条线宽
# 
#     halfwidth = int(line_width / 2)
# 
#     #north-west corner 
# 
#     draw.arc((halfwidth, halfwidth, radius*2-halfwidth, radius*2-halfwidth), 90, 180, pen)
# 
#     #north-east corner
# 
#     draw.arc((width-radius*2+halfwidth, halfwidth, width-halfwidth, radius*2-halfwidth), 0, 90, pen)
# 
#     #south-west corner
# 
#     draw.arc((halfwidth, height-radius*2+halfwidth, radius*2-halfwidth, height-halfwidth), 180, 270, pen)
# 
#     #south-east corner
# 
#     draw.arc((width-radius*2+halfwidth, height-radius*2+halfwidth, width-halfwidth, height-halfwidth), 270, 360, pen)
# 
#     
# 
#     #four edge line
# 
#     draw.line((halfwidth, radius, halfwidth, height-radius), pen)
# 
#     draw.line((radius, halfwidth, width-radius, halfwidth), pen)
# 
#     draw.line((width-halfwidth, radius, width-halfwidth, height-radius), pen)
# 
#     draw.line((radius, height-halfwidth, width-radius, height-halfwidth), pen)
# 
#     
# 
#     draw.flush()
# 
#     del draw
# 
#     
# 
#     return image 
# 
#     
# 
# 
# 
# def reduce_opacity(im, opacity):
# 
#     """Returns an image with reduced opacity."""
# 
#     assert opacity >= 0 and opacity <= 1
# 
#     if im.mode != 'RGBA':
# 
#         im = im.convert('RGBA')
# 
#     else:
# 
#         im = im.copy()
# 
#     alpha = im.split()[3]
# 
#     alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
# 
#     im.putalpha(alpha)
# 
#     return im
# 
# 
# 
# #为照片加水印
# 
# def Watermark(image, markimage, position, opacity=1):
# 
#     """Adds a watermark to an image."""
# 
#     im = image
# 
#     mark = markimage
# 
#     if opacity < 1:
# 
#         mark = reduce_opacity(mark, opacity)
# 
#     if im.mode != 'RGBA':
# 
#         im = im.convert('RGBA')
# 
#     # create a transparent layer the size of the image and draw the
# 
#     # watermark in that layer.
# 
#     layer = Image.new('RGBA', im.size, (0,0,0,0))
# 
#     if position == 'tile':
# 
#         for y in range(0, im.size[1], mark.size[1]):
# 
#             for x in range(0, im.size[0], mark.size[0]):
# 
#                 layer.paste(mark, (x, y))
# 
#     elif position == 'scale':
# 
#         # scale, but preserve the aspect ratio
# 
#         ratio = min(
# 
#             float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
# 
#         w = int(mark.size[0] * ratio)
# 
#         h = int(mark.size[1] * ratio)
# 
#         mark = mark.resize((w, h))
# 
#         layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
# 
#     else:
# 
#         layer.paste(mark, position)
# 
#     # composite the watermark with the layer
# 
#     return Image.composite(layer, im, layer)
# 
# 
# 
# 
# 
# #为照片增加文字
# 
# def Signature(image, text, position, font=None, color=(255, 0, 0)):
# 
#     """
# 
#     imprints a PIL image with the indicated text in lower-right corner
# 
#     """
# 
#     if image.mode != "RGBA":
# 
#         image = image.convert("RGBA")
# 
#     textdraw = ImageDraw.Draw(image)
# 
#     textsize = textdraw.textsize(text, font=font)
# 
#     textpos = [image.size[i]-textsize[i]-position[i] for i in [0,1]]
# 
#     textdraw.text(textpos, text, font=font, fill=color)
# 
# 
# 
#     del textdraw
# 
# 
# 
#     return image



if __name__ == '__main__':
#     unit = 100
#     im = Image.new('RGB', (unit,unit), 0)
#     draw = ImageDraw.Draw(im)
# #     draw.ellipse(((-0.05*unit, -0.05*unit),(1.2*unit, 1.2*unit)), 0xffffff)
# #     draw.rectangle(((0.5*unit, 0),(unit, unit)), 0xffffff)
# #     draw.rectangle(((0, 0.5*unit),(unit, unit)), 0xffffff)
# #     im.save('/home/zhouzhichao/arc.png')
# # 
# #     imarc = im.copy()
# #     im = im.transpose(Image.FLIP_LEFT_RIGHT)
# #     im = ImageChops.multiply(im, imarc)
# #     im.save('/home/zhouzhichao/arcx2.png')
# 
#     draw.arc((0,0,unit,unit), 0, 90, fill=0xff)
#     
#     im.save('/home/zhouzhichao/arc.png')
    circle()
    circle_corder_image()
    circle_new()