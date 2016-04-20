#coding: utf-8
import thread, threading
import time
import random

class Course(object):
    def __init__(self, game, player, state = None):
        self.player = player
        self._state = state
        self._owner = game
        
    def goNext(self):
        pass
    
    def process(self):
        rblsks = self._owner.currentRunnableSkills(self._state)
        if rblsks:
            for sk in rblsks:
                if sk.timing(self._owner) and  \
                    sk.hint(self._owner) and   \
                    sk.operating(self._owner):
                    sk.effect(self._owner)
                    
                    pass 


class Skill(object):    #sk
    def __init__(self, skID, player=-1):
        self.playerIndex = player #所属角色排位号
        self.skillID = skID
        self.skillState = []

    @property
    def skillID(self):
        return self.skillID
        
    def install(self, game):
        return True
    
    def uninstall(self, game):
        return True
    def timing(self, game):
        return False
    def hint(self, game):
        return False
    def operating(self, game):
        return False
    def effect(self, game):
        return True
    def complete(self, game):
        pass

class SkillCollector(object):   #skc
    def __init__(self, game):
        self.skillMatrix = {}#{排位号:[(技能序号, 技能实体)]}
        self._owner = game
        
    def __contains__(self, pair):
        sks = self.skillMatrix.get(pair[0])
        if sks:
            for sk in sks:
                if sk[0] == pair[1]:
                    return True
        return False
    
    def discardSkill(self, pair):
        sks = self.skillMatrix.get(pair[0])
        if sks:
            for sk in sks:
                if sk[0] == pair[1]:
                    sk.uninstall(self._owner)
                    sks.remove(sk)
                    
            if len(sks):
                del self.skillMatrix[pair[0]]
                if len(self.skillMatrix) == 0:
                    return True # it means to kill this SkillCollector, it's no more useful
            else:
                self.skillMatrix[pair[0]] = sks
                
        return False
    
    def addSkill(self, plridx, sk):
        sk.install(self._owner)
        sks = self.skillMatrix.get(plridx)
        if not sks:
            sks = [(sk.skillID,sk)]
        else:
            sks.append(sk.skillID,sk)
        self.skillMatrix[plridx] = sks
            
    def getSkillIterator(self, rdx):#     入参为当前回合角色的排位号，返回一个SkillIterator实例
        for i in self._owner.alivePlayers():
            sks = self.skillMatrix.get(i[0])
            if sks: 
                yield map(lambda x: x[1], sks)
     
   
   
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
        print "Hey %s, %s"%(self._clientIdx, self._hint)
        self._answer = [0]
        return True

          
         

    
def echo(command):
    print 'Im here %s'%command   
    
    
class BaseGame(object):     #g
    def __init__(self):
        self.beforeGaming = True
        self.Gaming, self.afterGaming = False, False
        self.skillRegistry = {}# {stt: skc}
        self.players = []
        self.curRound= 0
        self.course  = None
        self._gameID = 88975
        self._accept = Acceptance()
        self._actSerial = 0
        
    @property
    def playerNum(self):
        return len(self.players)
    
    def currentRunnableSkills(self, stt = None):
        if not stt:
            stt = self.course._state
        skc = self.skillRegistry.get(stt)
        if skc:
            return skc.getSkillIterator(self.curRound)
        else:
            return None
        
    def addPlayer(self, plr):
        if self.beforeGaming and not self.Gaming and not self.afterGaming:
            if self.playerNum < 10:
                plr.index = self.playerNum
                self.players.append(plr)
            else:
                raise Exception('Too many players entered.')
        else:
            raise Exception('Wrong timing to add player in.')
        
    def alivePlayers(self, rdx = 0):
        for i in xrange(self.playerNum):
            idx = (i+rdx) % self.playerNum
            plr = self.players[idx]
            if plr.isAlive:
                yield (idx, plr)            
            
    def actionReceiver(self, plrs, hint, theshold = 1):#用于停顿等待用户输入
        self._accept.startAccept(self._actSerial)
        for cm in map(lambda p: 
                      ClientMessager(p, hint, 
                                     self._actSerial, 
                                     self._accept, 
                                     "plr_%04x@g%04x"%(p, self._gameID)),
                      plrs):
            cm.start()
        
        result = {}
        while theshold > 0:
            if self._accept.wait():
                result.update(self._accept.Receipt)   #add
                theshold -= 1
                self._accept.rewait()
            else:
                break # time up
            
        echo(result)
    
    def registrySkills(self, plridx, sk):
        for stt in sk.skillState:
            skc = self.skillRegistry[stt]
            if not skc:
                skc = SkillCollector(self)
            skc.addSkill(plridx, sk)
            self.skillRegistry[stt] = skc
    
    def discardSkill(self, plridx, skName):
        deleteList, pair = [], (plridx, skName)
        for stt in self.skillRegistry:
            skc = self.skillRegistry[stt]
            if pair in skc and skc.discardSkill(pair):
                deleteList.append(stt)
                
        for stt in deleteList:
            del self.skillRegistry[stt]
            
class ZZFN_Game(BaseGame):
    def __init__(self):
        super(ZZFN_Game, self).__init__()
        pass
    
    def assignStatus(self, nx2=False):
        plrnum = self.playerNum
        zzfn = [1, 2, 4, 1]
        
        self.players[0].status = 0
        for i in xrange(1, plrnum):
            sts = random.randint(1,3)
            while zzfn[sts] <= 0:
                sts = random.randint(1,3)
            zzfn[sts] -= 1
            self.players[i].status = sts
        
    def masterChooseHero(self):
        result = self.actionReciever([0])
        self.players[0].chooseHero(result)
        pass
    
    def otherChooseHero(self):
        result = self.actionReciever(range(1, self.playerNum))
        pass

class Player(object):   #plr
    def __init__(self):
        self.status= -1
        self.index = 0
        self._blood= (0, 0)
        self._alive= True
        self._owner= None
        self.skills= None
        self.serial="%04d"%random.randint(0,99999)
        pass
    
    @property
    def No(self):
        return self.serial
    
    @property
    def isAlive(self):
        return self._alive
    
    
    @property
    def blood(self):
        return self._blood[0]
    @blood.setter
    def blood(self, val):
        self._blood[0] = val
        if self._blood[0] > self._blood[1]:
            self._blood[0] = self._blood[1]
    
    @property
    def bloodSlot(self):
        return self._blood[1]
    @bloodSlot.setter
    def bloodSlot(self, val):
        self._blood[1] = val if val > 0 else 0
        if self._blood[0] > self._blood[1]:
            self._blood[0] = self._blood[1]
    
    
    def entranceGame(self, game):
        if not self._owner:
            self._owner = game
            self._owner.addPlayer(self)
        else:
            raise Exception('Player has been in one game.')
            
    def chooseHero(self, hrCard):
        if self.isAlive and self._owner:
            self._owner.registrySkills(self.index,)
        pass
    
    def die(self):
        if self.isAlive and self._owner:
            for sk in self.skills:
                self._owner.discardSkill(self.index, sk)
            self._alive = False
        else:
            raise Exception("Player dead illegally! It has dead or not in game.")
        
        
class Hero(object):     #hr
    def __init__(self, hrid):
        self._hrID = hrid
        self.name  = None
        self.gendar= False
        self.blood = 0
        self.nation= None
        self.skills= []
        
        
        
if __name__ == '__main__':
    g = ZZFN_Game()
    for _ in xrange(8):
        Player().entranceGame(g)
        
    g.assignStatus()
    g.masterChooseHero()
    g.otherChooseHero()
    
    
    print g.playerNum
    for pair in g.alivePlayers():
        plr = pair[1]
        print plr.No, plr.status 