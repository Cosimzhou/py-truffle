#coding: UTF-8

with open('/Users/zhouzhichao/.simcity/items.csv') as f:
    for l in f.readlines():
        arr = l.strip('\n').split(';')
        arr[-1] = arr[-1].replace('x','*')
        ty = '1' if arr[0] and not arr[0].endswith('空运') else '0'
        arr = arr[:4]+[ty]+arr[4:]
        print ';'.join(arr)