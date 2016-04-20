# encoding: UTF-8
import thread, threading
import time
  
g_accept=None
g_debug=None

class debug_input(object):
    def __init__(self):
        self._lock = thread.allocate()

    def printinfo(self, txt):
        if self._lock.acquire(10):
            print txt
            self._lock.release()
            
    def getinput(self, prompt=None):
        if self._lock.acquire(10):
            if prompt:print prompt
            rst = raw_input()
            self._lock.release()
            return rst

class Acceptance(object):
    def __init__(self):
        self.Receipt = {}
        self._lock = thread.allocate()
        self._evtMailGot = threading.Event()
        self._eventSerial = 0
        self._timeOut = 15
        self._timeLimit = 0
        self._ready = False
        
    def startAccept(self, eventSerial):
        self._timeLimit = time.time() + self._timeOut
        self._eventSerial = eventSerial
        if self._lock.locked():
            self._lock.release()
        self._evtMailGot.clear()
        self._ready = True
        
    def wait(self):
        if self._ready:
            timerest = self._timeLimit - time.time()
            if self._evtMailGot.wait(timerest):
                return True
        return False

    def rewait(self):
        if self._ready:
            self._evtMailGot.clear()
            if self._lock.locked():
                self._lock.release()  
                      
    def dealMessage(self, cmMsger):
        if self._lock.acquire(10):
            if self._eventSerial == cmMsger._eventSerial:
                self.Receipt = {cmMsger._clientIdx: cmMsger._answer}
                self._evtMailGot.set()
                return True
            else:
                self._lock.release()
        return False

        
            

class ClientMessager(threading.Thread):
    def __init__(self, clientIndex, hint, eventSerial, acceptance, threadname):  
        threading.Thread.__init__(self, name = threadname)
        self._name        = threadname
        self._eventSerial = eventSerial
        self._clientIdx   = clientIndex
        self._acceptance  = acceptance
        self._hint        = hint
        self._answer      = []
        

    def run(self):  
        if self.talkWithClient():
            self._acceptance.dealMessage(self)
    
    # override this method to implement client-communicating
    def talkWithClient(self):
        result = [g_debug.getinput("Hey %s, %s"%(self._clientIdx, self._hint))]
        if result:
            self._answer = result
            return True
        else:
            return False

          
         
def addReceiver(plrs, hint, theshold = 1):
    g_accept.startAccept(1324)
    for cm in map(lambda p: ClientMessager(p, hint, 1324, g_accept, "plr_%04x"%p), plrs):
        cm.start()
    
    result = {}
    while theshold > 0:
        if g_accept.wait():
            result.update(g_accept.Receipt)   #add
            theshold -= 1
            g_accept.rewait()
        else:
            break # time up
        
    echo(result)
    
def echo(command):
    print 'Im here %s'%command
         
if __name__ == '__main__':
    global g_accept, g_debug
    g_accept = Acceptance()
    g_debug = debug_input()
    addReceiver((2,4,5,7), 'Are you ready?', 8)
    
    
#     # 启动一个线程，线程立即开始运行
#     # 这个方法与thread.start_new_thread()等价
#     # 第一个参数是方法，第二个参数是方法的参数
#     thread.start_new(func, ()) # 方法没有参数时需要传入空tuple
#       
#     # 创建一个锁（LockType，不能直接实例化）
#     # 这个方法与thread.allocate_lock()等价
#     lock = thread.allocate()
#       
#     # 判断锁是锁定状态还是释放状态
#     print lock.locked()
#       
#     # 锁通常用于控制对共享资源的访问
#     count = 0
#       
#     # 获得锁，成功获得锁定后返回True
#     # 可选的timeout参数不填时将一直阻塞直到获得锁定
#     # 否则超时后将返回False
#     if lock.acquire():
#         count += 1
#          
#         # 释放锁
#         lock.release()
#       
#     # thread模块提供的线程都将在主线程结束后同时结束
#     time.sleep(6)
"""
import threading  
class mythread(threading.Thread):  
    def __init__(self,threadname):  
        threading.Thread.__init__(self,name = threadname)  
    def run(self):  
        global event  
        if event.isSet():  
            event.clear()  
            event.wait()   #当event被标记时才返回  
            print self.getName()  
        else:  
            print "I set", self.getName()  
            event.set()  
event = threading.Event()  
event.set()  
t1 = []  
for i in range(10):  
    t = mythread(str(i))  
    t1.append(t)  
for i in t1:  
    i.start()  
"""