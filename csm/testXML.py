# -*- coding: utf-8 -*-

'''
Created on 2014年6月27日

@author: zhouzhichao
'''

import xml.etree.ElementTree as et
import xml.dom.minidom as dm



xmlfile = '/home/zhouzhichao/tag_graph.xml'
def kk():
    root = et.parse(xmlfile)
    for i in root.getiterator('word'):
        print i.attrib['name'], i.getparent().attrib['name']

def kkk():
    root = dm.parse(xmlfile).documentElement
    for n in root.getElementsByTagName('word'):
        print getPath(n)
#         p = n.parentNode
#         print n.getAttribute('name'), p.getAttribute('name')
        
def getPath(node):
    pchain, name = [], node.getAttribute('name')
    while name:
        pchain.append(name)
        node = node.parentNode
        name = node.getAttribute('name')
    
    if pchain:
        pchain.reverse()
        return "^/%s/"%('/'.join(pchain))
    else:
        return "^/"
     


if __name__ == '__main__':
    kkk()
    pass