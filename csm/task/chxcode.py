#coding: UTF-8



# started, ended = False, False
# of = open('/Users/zhouzhichao/workspace/tigerknows-mapcore/x86_64-macosx-clang-debug.xcode.build/tkengine-1.xcodeproj','w')

with open('/Users/zhouzhichao/workspace/tigerknows-mapcore/x86_64-macosx-clang-debug.xcode.build/tkengine.xcodeproj','r') as f:
    probj = {}
    for l in f.readlines():
        l = l.strip('\n')
        for c in l:
            pass
#         
#         if started and not ended:
#             
#             
#             continue
#         elif "/* End PBXGroup section */" in l:
#             ended = True
#             
#             pass
#             
#         elif "/* Begin PBXGroup section */" in l:
#             started = True
#         of.write(l)
        
exec '''
b={ 'asd' """b """: 4}
'''
# b = _

print b