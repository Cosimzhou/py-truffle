#coding: UTF-8

from os.path import getsize

def changeSngFile2Code(filename):
    with open(filename, 'r') as f:
        for r in f.readlines():
            yield changeSngLine2Code(r)

def changeSngLine2Code(strline):
    resultArray = []
    for char in strline:
        resultArray.append(hex(ord(char)))
        
    return ', '.join(resultArray)

if __name__ == '__main__':
    # filelist = ['citylist', 'env.dat', 'regionlist', 'render.cfg', 'render_n.cfg', 'SPI.dat', 'subwaycolor']
    filelist = ['SPI.dat', 'env.dat', 'subwaycolor', 'border.dat', 'regionlist', 'citylist', 'render_config.xml']
    for fn in filelist:
#         filename = '/Users/zhouzhichao/workspace/tigerknows-mapcore/tigermap/'+ fn
        filename = '/Users/zhouzhichao/workspace/tkmap-api/tkmap-api/tigermapres/'+ fn
        fn = fn.replace('.','_')
        with open(filename + '.m', 'wb') as f:
            startline = True
            f.write('const unsigned long long %s_length = %s;\n' %(fn, getsize(filename)))
            for l in changeSngFile2Code(filename):
                if not startline:
                    f.write(',\n')
                    f.write(l)
                else:
                    f.write('const unsigned char ')
                    f.write(fn)
                    f.write('[] = {')
                    f.write(l)
                startline = False
            f.write('};')
            
#     print changeSngLine2Code('安康 ankang 陕西 shan3xi 109.028885 32.68472 293 20 13 209\r\n')
    pass