#coding: UTF-8

import sqlite3

conn = sqlite3.connect('/Users/zhouzhichao/Documents/ci.sqlite')
cu = conn.cursor()
sql = 'select * from cipainew'
cu.execute(sql)
r = cu.fetchall()
print len(r)

for e in r:
    print e[2]