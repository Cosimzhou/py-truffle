#coding: UTF-8

import urllib2, time

tmpDir = '/Users/zhouzhichao/tmp'
urlPattern = 'http://ilibrary.ru/text/1099/p.%d/index.html'
wordCode = 'windows-1251'

tagMark = set()

dictTag2Text={'larr':'←',
'egrave':'è',
'Ccedil':'Ç',
'auml':'ä',
'laquo':'«',
'ccedil':'ç',
'ecirc':'ê',
'mdash':'—',
'uuml':'ü',
'#8470':'№',
'raquo':'»',
'rarr':'→',
'nbsp':' ',
'agrave':'à',
'eacute':'é',
'ldquo':'“',
'#769':'́',
'bdquo':'„',
'acirc':'â',
'icirc':'î'}




def url_iter():
    for i in xrange(1,240):
        yield urlPattern%i

def tmpfile_path(idx, prefix=None):
    prefix = '%s' if (prefix is None) else (prefix+'%s')
    return '/'.join((tmpDir, (prefix % idx)))        

def pull_files_from_web():
    counter = 1 
    for url in url_iter():
        wp = urllib2.urlopen(url) #打开连接
        content = wp.read() #获取页面内容
        with open(tmpfile_path(counter),'w') as fp: #打开一个文本文件
            fp.write(content) #写入数据
        time.sleep(0.5)
        print 'download file finished............%d'%counter
        counter += 1
        
def encode_middle_file():
    for i in range(1,240):
        fp = open(tmpfile_path(i),'r')
        ofp = open(tmpfile_path(i,'u'),'w')
        for l in fp.readlines():
            ofp.write(l.decode(wordCode).encode('UTF-8'))    
        fp.close()
        ofp.close()

def extract_text():
    ofp = open(tmpfile_path(0,'Ahha'),'w')
    for i in range(1,240):
        fp = open(tmpfile_path(i,'u'),'r')
        for l in fp.readlines():
            if '<span class=fi></span>' in l:
                text = remove_tag_mark(l)
                ofp.write(text)
        fp.close()
        ofp.write("\n\n")
    ofp.close()
    
def remove_tag_mark(text):
    a, tag='', ''
    inner = False
    spetag = False
    for c in text:
        if inner:
            if c == '>':
                inner = False
        else:
            if c == '<':
                inner = True
                continue
            if spetag:
                if c == ';':
                    if dictTag2Text.get(tag) is None:
                        tagMark.add(tag)
                    else:
                        a+=dictTag2Text[tag]
                    tag=''
                    spetag = False
                    continue
                else:
                    tag += c
            else:
                if c == '&':
                    spetag = True
                    continue
                a+=c
    return a
        
if __name__ == '__main__':
    extract_text()
    
    print len(tagMark)
    for i in tagMark:
        print i
    pass