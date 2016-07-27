# -*- coding: UTF-8 -*-

import urllib2, re
from HTMLParser import HTMLParser

cardurl="http://gw.sanguosha.com/data/newsDetail.asp?id=47&CategoryID=5010"
herourl="http://www.sanguosha.com/data/newsDetail.asp?id=96&CategoryID=5004"
# herourl="http://gw.sanguosha.com/data/newsDetail.asp?id=%d&CategoryID=5004"#5001

ptn=re.compile(".*['\"](.*newsDetail\.asp\?id=\d+&CategoryID=\d+).*")
pid=re.compile(".*(id=\d+&CategoryID=\d+).*")
# m = ptn.match("<li><a href='newsDetail.asp?id=35&CategoryID=5015' title='[89期]&nbsp;三国杀大讲堂虎牢关篇之玩家心得(四)' target='_blank'>[89期]&nbsp;三国杀大讲堂虎牢关篇之玩家心得(四)</a></li>")
# print m.groups()
 

class HTML_node(object):
    def __init__(self, tag = None, attrs = None):
        self.tag = tag
        self.attrs = dict(attrs) if attrs else None
        self.children = None
        self.parent = None
    def addChild(self, node):
        if self.children is None:
            self.children = []
        if self.children and type(self.children[-1]) is str and type(node) is str:
            self.children[-1] += node
        self.children.append(node)
        if type(node) is HTML_node: node.parent = self 
    def __repr__(self):
        buff = "<%s" % self.tag
        if self.attrs:
            buff += ' '+ ' '.join(map(lambda x:'%s="%s"'%x, self.attrs.items()))
        if self.children is None:
            buff +='/>'
        else:
            buff += '>' + '\n'.join(map(str, self.children))
            buff += '</%s>'%self.tag
        return buff
    
    def string(self):
        buff = ''
        if self.children:
            for c in self.children:
                if type(c) is str:
                    buff += ' '+c
                elif type(c) is HTML_node:
                    buff += ' '+ c.string()
        return buff
    def find(self, filt, result):
        if filt(self):
            result.append(self)
        elif self.children:
            for c in self.children:
                if type(c) is HTML_node:
                    c.find(filt, result)


class HTML_Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.root = HTML_node('DOM')
        self.cn = self.root
 
#     def handle_decl(self, decl):
#         cnn = HTML_node(tag, attrs)
#         self.cn.addChild(cnn)
    def handle_starttag(self, tag, attrs):
        cnn = HTML_node(tag, attrs)
        self.cn.addChild(cnn)
        self.cn = cnn
    def handle_startendtag(self, tag, attrs):
        cnn = HTML_node(tag, attrs)
        self.cn.addChild(cnn)
    def handle_endtag(self, tag):
        if self.cn:
            self.cn = self.cn.parent 
    def handle_data(self, data):
        text = data.strip(' \t\r\n')
        if text:
            self.cn.addChild(text)            


# with open('/Users/zhouzhichao/tmp/skl.txt', 'r') as f:
#     of = open('/Users/zhouzhichao/tmp/sko.txt', 'w')
#     for l in f.readlines():
#         of.write(l[:6]+ "\t" +l[6:])
#     of.close()
# exit(0)


g_set = set()
g_queue=[herourl]


def filtr(node):
    if node.attrs:
        style = node.attrs.get('style')
        if style:
            dc = {}
            ss = style.split(';')
            for s in ss:
                si = s.split(':') 
                if len(si) != 2: continue
                dc[si[0].strip(' \t\r\n')] = si[1].strip(' \t\r\n')
            c = dc.get('color')
            if c:
                c = c.replace(' ','').lower()
                return c in ("rgb(255,0,0)", '#ff0000')
    return False 
def filta(node):
    if node.tag == 'a' and node.attrs:
        var = node.attrs.get('href')
        if var:
            m = pid.match(var)
            if m:
                g_queue.append("http://www.sanguosha.com/data/newsDetail.asp?"+m.groups()[0])
#                 g_set.add("http://www.sanguosha.com/data/newsDetail.asp?"+m.groups()[0])
    return False

i = 0
while i < len(g_queue):
    q = g_queue[i]
    if q in g_set: 
        i += 1
        continue
    g_set.add(q)
    
    data = urllib2.urlopen(q).read() 

    try:
        sd = data.decode('GBK').encode('UTF-8')
    except UnicodeDecodeError as e:
        sd = ''
        for l in data.split('\n'):
            try:
                sd += l.decode('GBK').encode('UTF-8')
            except UnicodeDecodeError as e:
                pass

    hp = HTML_Parser()
    hp.feed(sd)
    hp.close()
    bf = []
    
    hp.root.find(filtr, bf)
    hp.root.find(filta, [])
    for e in bf:
        txt = e.string()
        if len(txt) > 10 and ord(txt[0])>125: 
            print e
    
    i += 1
# 
exit(0)

# #     for l in sd.split('\n'):
# #         if """\"——""" in l:
# # print "(< %d >)" % i
#  
# with open('/Users/zhouzhichao/tmp/test.html', 'w') as f:
#     f.write(sd)
# exit(0) 



with open('/Users/zhouzhichao/tmp/test.html', 'r') as f:
    sd = f.read()
    
hp = HTML_Parser()
hp.feed(sd)
hp.close()
bf = []

hp.root.find(filtr, bf)
hp.root.find(filta, [])
