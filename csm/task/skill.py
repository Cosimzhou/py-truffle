# -*- coding:UTF-8 -*-

import re

with open("/Users/zhouzhichao/tmp/skll.txt") as f:
#     data = f.read()
    exec f.read() #data

ptn = re.compile(r'DSK\("([^"]*)"\, ([^,]*), ([^,]*), "([^"]*)"([^;]*)\);')

with open("/Users/zhouzhichao/workspace/wsg/wsg/core/skill-funcitem.h", 'r') as f:
    for l in  f.readlines():
        if l.startswith('DSK('):
            m = ptn.match(l).groups()
            nm = SKLL.get(m[0])
            if m[3] or nm is None:
                print l,
            else:
                print 'DSK("%s", %s, %s, "%s"%s);'%(m[:3]+(nm,)+m[4:])
        else:
            print l,