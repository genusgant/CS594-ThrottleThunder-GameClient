from Models3D.Characters.BaseCharacter  import BaseCharacter
from panda3d.core                       import *
from pandac.PandaModules                import *
from direct.actor.Actor                 import Actor
import math

class PandaCharacter(BaseCharacter):
    count=0
    def __init__(self,World, render,base,loader):
        BaseCharacter.__init__(self,World, render,base,loader)
        PandaCharacter.count += 1
        self.id = PandaCharacter.count

        self.taskName = 'panda'+str(PandaCharacter.count)
        self.node = render.attachNewNode('panda'+str(PandaCharacter.count))
        self.actor=Actor("models/panda-model",
                     {"walk": "models/panda-walk4"})
        self.actor.reparentTo(self.node)
        self.actor.setScale(0.002, 0.002, 0.002)
        self.actor.name = "Panda"

        self.cNode = CollisionNode('panda')
        self.cNode.addSolid(CollisionSphere(2, 0, 400, 500))
        self.frowneyC = self.actor.attachNewNode(self.cNode)
        base.cTrav.addCollider(self.frowneyC, World.pusher)
        World.pusher.addCollider(self.frowneyC, self.actor, base.drive.node())

    def getActor(self):
        return self.actor

    def getPandaCount(self):
        return PandaCharacter.count

    def getMyPandaId(self):
        return self.id  
    #def moveCharacterTo(self):
    
    def lookAt(self,model):
        self.actor.lookAt(model)
        hpr = self.actor.getHpr()
        self.actor.setHpr(hpr[0]+180,hpr[1],hpr[2])
     
     
    def setZofPlayer(self):
        self.actor.setZ(0)
    
        
    def move(self, task):

        self.base.camera.lookAt(self.actor)
        if (self.World.keyMap["cam-left"]!=0):
            self.base.camera.setX(self.base.camera, -20 * globalClock.getDt())
        if (self.World.keyMap["cam-right"]!=0):
            self.base.camera.setX(self.base.camera, +20 * globalClock.getDt())

        startpos = self.actor.getPos()

        self.setZofPlayer()
        if (self.World.keyMap["left"]!=0):
            self.actor.setH(self.actor.getH() + 300 * globalClock.getDt())
        if (self.World.keyMap["right"]!=0):
            self.actor.setH(self.actor.getH() - 300 * globalClock.getDt())
        if (self.World.keyMap["forward"]!=0 and self.World.keyMap["mag"]!=5):
            if not self.actor.getAnimControl("walk").isPlaying():
                self.actor.loop("walk")
            self.actor.setY(self.actor, -1000 * globalClock.getDt())
        if (self.World.keyMap["forward"]!=0 and self.World.keyMap["mag"]!=1):
            if not self.actor.getAnimControl("walk").isPlaying():
                self.actor.loop("walk")
            self.actor.setY(self.actor, -2000 * globalClock.getDt())
        
        if (self.World.keyMap["backward"]!=0 and self.World.keyMap["mag"]!=5):
            if not self.actor.getAnimControl("walk").isPlaying():
                self.actor.loop("walk")
            self.actor.setY(self.actor, 1000 * globalClock.getDt())
            
        if (self.World.keyMap["backward"]!=0 and self.World.keyMap["mag"]!=1):
            if not self.actor.getAnimControl("walk").isPlaying():
                self.actor.loop("walk")
            self.actor.setY(self.actor, 2000 * globalClock.getDt())   
           
        list = self.actor.getPos()
        pos = Vec4(list[0],list[1],list[2],self.actor.getH())
        self.World.MoveManager.appendAction(pos)

        #self.actor.stop()

        #if (self.World.keyMap["backward"]!=0):
        #    self.actor.setY(self.actor, 25 * globalClock.getDt())

        if (self.World.keyMap["forward"]!=0) or (self.World.keyMap["left"]!=0) or (self.World.keyMap["right"]!=0 or (self.World.keyMap["backward"]!=0)):
            if self.isMoving is False:
                self.actor.loop("run")
                self.isMoving = True
        else:
            if self.isMoving:
                self.actor.stop()
                self.actor.pose("walk",5)
                self.isMoving = False

        camvec = self.actor.getPos() - self.base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > 10.0):
            self.base.camera.setPos(self.base.camera.getPos() + camvec*(camdist-10))
            camdist = 10.0
        if (camdist < 5.0):
            self.base.camera.setPos(self.base.camera.getPos() - camvec*(5-camdist))
            camdist = 5.0

        self.floater.setPos(self.actor.getPos())
        self.floater.setZ(self.actor.getZ() + 2.0)
        self.base.camera.lookAt(self.floater)

        return task.cont
    
    def moveCharacterTo(self,pos,heading=None):
        self.World.taskMgr.remove(self.taskName)
        if heading == None:
            self.floater.setPos(float(pos[0]),float(pos[1]),float(pos[2]))
            self.lookAt(self.floater)
            self.actor.setPos(float(pos[0]),float(pos[1]),float(pos[2]))
        else:
            self.actor.setPos(float(pos[0]),float(pos[1]),float(pos[2]))
            self.actor.setH(float(heading))
        
        if not self.isMoving:
            self.isMoving = True
            self.actor.loop("walk")
        
        self.World.taskMgr.doMethodLater(0.3,self.stopAnimation,self.taskName)
        
    def stopAnimation(self, task):
        self.isMoving = False
        self.actor.stop()
        self.actor.pose("walk",5)