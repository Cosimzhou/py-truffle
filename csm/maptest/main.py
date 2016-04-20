# coding: utf-8

import psycopg2, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

#font = ImageFont.truetype("/usr/share/fonts/truetype/fonts-japanese-gothic.ttf", 15)
font = ImageFont.truetype("/home/zhouzhichao/下载/SIMYOU.TTF", 25)

def getConn():
    return psycopg2.connect(host='192.168.11.88', port=5432, user='postgres', password='titps4gg', database='vecbaseSw13Aut')

def getData(conn, area):
    cur = conn.cursor()
#    cur.execute("""select AsText(the_geom) from building_110000a  limit 10;""")
    result = {}
    cur.execute("""select AsText(the_geom) from building_110000a where ST_Intersects(%s, the_geom) limit 1000;"""%polygon(area))
    
    array = []
    for row in cur.fetchall():
        res = row[0]
        print res
        sti = res.index('(')
        res = list(eval(res[sti:].replace(' ', ',')))
        array.append(res)
    result['building'] = array 
    

    cur.execute("""select AsText(the_geom) from jianchengqu_110000a where ST_Intersects(%s, the_geom) limit 1000;"""%polygon(area))
     
    array = []
    for row in cur.fetchall():
        res = row[0]
        print res
        sti = res.index('(')
        res = list(eval(res[sti:].replace(' ', ',')))
        array.append(res)
    result['jianchengqu'] = array 
    
    
    cur.execute("""select AsText(the_geom) from rails_110000a where ST_Intersects(%s, the_geom) limit 1000;"""%polygon(area))
     
    array = []
    for row in cur.fetchall():
        res = row[0]
        print res
        sti = res.index('(')
        res = list(eval(res[sti:].replace(' ', ',')))
        if type(res[0]) is tuple:
            for line in res:
                array.append(list(line))
        else:
            array.append(res)
    result['rails'] = array 


    cur.execute("""select AsText(the_geom), class from road_110000a where ST_Intersects(%s, the_geom) limit 1000;"""%polygon(area))
     
    array = []
    classes = []
    for row in cur.fetchall():
        res = row[0]
        print res, row[1]
        sti = res.index('(')
        res = list(eval(res[sti:].replace(' ', ',')))
        array.append(res)
        classes.append(row[1])
    result['road'] = (array, classes) 
    
    cur.execute("""select AsText(the_geom), name from point_110000a where level < 5 and ST_Intersects(%s, the_geom) limit 1000;"""%polygon(area))
     
    array = []
    names = []
    for row in cur.fetchall():
        res = row[0]
        name = row[1].decode('gbk')
        print res, type(name),name
        sti = res.index('(')
        res = list(eval(res[sti:].replace(' ', ',')))
        array.append(res)
        names.append(name)
    result['point'] = (array, names) 
    
    
    cur.close()
#     print res
    return result
    

    
def lst2plst(data):
    assert len(data) % 2 == 0
    result = []
    x, xx = 0, True
    for d in data:
        if xx:
            x = d
        else:
            result.append([x,d])
        xx = not xx
    return result

def findMaxArea(datas):
    area = [[180,0],[180,0]]
    for data in datas:
        xx = 0
        for d in data:
            if area[xx][0]>d: area[xx][0] = d
            if area[xx][1]<d: area[xx][1] = d
            xx = 1-xx
    
    return area

def fitAreaX(x, area, size):
    return (x-area[0][0])/float(area[0][1] - area[0][0]) * size[0]

def fitAreaY(y, area, size):
    return (1-(y-area[1][0])/float(area[1][1] - area[1][0])) * size[1]

def polygon(varea):
    return """'SRID=4326;POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))'"""%(varea[0][0],varea[1][0],
                                                                 varea[0][1],varea[1][0],
                                                                 varea[0][1],varea[1][1],
                                                                 varea[0][0],varea[1][1],
                                                                 varea[0][0],varea[1][0],
                                                                 )
def shift(area, vec):
    area[0][0] += vec[0]
    area[0][1] += vec[0]
    area[1][0] += vec[1]
    area[1][1] += vec[1]
    return area

def junhengbili(area, size):
    rate = [0,0]
    rate[0] = size[0]/(area[0][1]-area[0][0])
    rate[1] = size[1]/(area[1][1]-area[1][0])
    rate = min(rate)
    for i in (0,1):
        leng = size[i]/rate/2
        mid  = (area[i][1]+area[i][0])/2
        area[i] = [mid-leng, mid+leng]
    return area 


def drawRoad(draw, line, width):
    if width == 1:
        draw.line(line, fill=0xcfffff)
    if width <= 1:
        return

    width /= 2.0
    for i in xrange(2, len(line), 2):
        xx = line[i-2: i+2]
        dx, dy = xx[0] - xx[2], xx[1] - xx[3]
        dl = math.sqrt(dx**2 + dy**2)
        dx, dy = dy/dl*width, -dx/dl*width
        xx = [xx[0]+dx, xx[1]+dy, xx[0]-dx, xx[1]-dy, xx[2]-dx, xx[3]-dy, xx[2]+dx, xx[3]+dy, xx[0]+dx, xx[1]+dy]
        draw.line(xx, fill=0xcfffff)
        draw.polygon(xx, fill=0xffffff)

def drawRailway(draw, line, white=1, rest=0):
    width, step = 3, 32
    color = (0x404040,0xffffff)
    for i in xrange(2, len(line), 2):
        xx = line[i-2: i+2]
        dx, dy = xx[2] - xx[0], xx[3] - xx[1]
        dl = math.sqrt(dx**2 + dy**2)
        nx, ny = dx/dl, dy/dl
        sx, sy = xx[0], xx[1]
        dx, dy = dy/dl*width, -dx/dl*width

        secn = 0
        while dl > 0:
            if rest <= 0:
                white, rest = 1-white, float(step)
            
            if rest > dl:
                drl, rest, dl = dl, rest-dl, 0.0
            else:
                drl, dl, rest = rest, dl-rest, 0
                
            minxx = [sx+dx, sy+dy, sx-dx, sy-dy, sx+nx*drl-dx, sy+ny*drl-dy, sx+nx*drl+dx, sy+ny*drl+dy, sx+dx, sy+dy]
            draw.polygon(minxx, fill = color[white], outline=color[0])
            
            if secn == 0 and white == 1:
                minxx = [sx-width+1, sy-width+1, sx+width-1, sy+width-1]    
                draw.ellipse(minxx, fill = color[1])
                  
            sx += nx*drl
            sy += ny*drl  

            if dl == 0.0 and white == 1:
                minxx = [sx-width+1, sy-width+1, sx+width-1, sy+width-1]    
                draw.ellipse(minxx, fill = color[1])

            secn += 1

def text(image, pos, text):
    pos = tuple(pos)
    size = (len(text)*25, 25)
    #size = (pos[0]+size[0], pos[1]+size[1])
    pos = map(int, pos+size)
    
    img = Image.new('RGBA', size, 0)
    draw = ImageDraw.Draw(img)
    draw.font = font
    for i in xrange(-2,2):
        for j in xrange(-2,2):
            draw.text((i,j), text, fill=0xffffffff)
    draw.text((0,0), text, fill=0xff000000)
    img.save('/home/zhouzhichao/ditu/text.png')
    
    paste(image, img, pos, (0,0), size)
    #image.paste(img, pos)#list(pos+size))

def blend(front, back):
    return tuple(map(lambda i: int((back[i]*(255-front[3])+front[i]*front[3])/255.0+0.5), [0,1,2])) 

def paste(dest, src, destpos, srcpos, srcsize, color=(255,0,255)):
    pdest = dest.load()
    psrc  = src .load()
    for i in xrange(srcsize[0]):
        for j in xrange(srcsize[1]):
            curcolor = psrc[srcpos[0]+i,srcpos[1]+j]
            if curcolor[3] != 0:#color:
                if 0 <= destpos[0]+i < dest.size[0] and 0 <= destpos[1]+j < dest.size[1]:
                    tmpcolor = pdest[destpos[0]+i, destpos[1]+j]
                    pdest[destpos[0]+i, destpos[1]+j] = blend(curcolor, tmpcolor) 

if __name__ == '__main__':
    39.86406, 116.37283
    varea = [[116.33, 116.35], [39.86, 39.88]]
    varea = shift(varea, [0.04,-0.01])
    
    size = (2000,1600)
    img = Image.new('RGB', size, 0xffffff)
    draw = ImageDraw.Draw(img)
    conn = getConn()
    datas = getData(conn, varea)
    conn.close()

    area = junhengbili(varea, size)
    
    color = {'building': 0xc0c5c5, 'jianchengqu':0xb9dcc1, 'rail': 0x0, 'road':0xff}
    
    
    for key in ('jianchengqu', 'building'):
        ardata = datas.get(key)
        if not ardata:
            continue
        for data in ardata:
            i = 0
            for d in data:
                if i % 2 == 0:
                    data[i] = fitAreaX(d, area, size)
                else:
                    data[i] = fitAreaY(d, area, size)
                i += 1
            draw.polygon(data, fill = color[key])


    ardata = datas.get('road')
    if ardata:        
        no = 0
        for data in ardata[0]:
            i = 0
            for d in data:
                if i % 2 == 0:
                    data[i] = fitAreaX(d, area, size)
                else:
                    data[i] = fitAreaY(d, area, size)
                i += 1
            drawRoad(draw, data, (6-ardata[1][no])*2)
            no += 1

    
    
    ardata = datas.get("rails")
    if ardata:
        for data in ardata:
            i = 0
            for d in data:
                if i % 2 == 0:
                    data[i] = fitAreaX(d, area, size)
                else:
                    data[i] = fitAreaY(d, area, size)
                i += 1
              
            drawRailway(draw, data)
            

    ardata = datas.get('point')
    if ardata:
        data = ardata[0]
        xy, xx, i = [0, 0], True, 0
        for d in data:
            if xx:
                xy[0] = fitAreaX(d[0], area, size)
            else:
                xy[1] = fitAreaY(d[1], area, size)    
                text(img, xy, ardata[1][i])
                i += 1
            xx = not xx
            
    img = img.resize((1000,800), Image.ANTIALIAS)
    img.save('/home/zhouzhichao/ditu/test.png')
    