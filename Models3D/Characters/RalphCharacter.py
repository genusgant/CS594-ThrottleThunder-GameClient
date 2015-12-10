from Models3D.Characters.BaseCharacter  import BaseCharacter
from panda3d.core                       import *
from pandac.PandaModules                import *
from direct.actor.Actor                 import Actor
import math

class RalphCharacter(BaseCharacter):
    count = 0    
    def __init__(self,World, render,base,loader):
        BaseCharacter.__init__(self,World, render,base,loader)
        RalphCharacter.count += 1
        self.id = RalphCharacter.count

        self.taskName = 'ralph'+str(RalphCharacter.count)
        self.node = render.attachNewNode('ralph'+str(RalphCharacter.count))
        self.actor = Actor("models/ralph/ralph",
                         {"run":"models/ralph/ralph-run",
                          "walk":"models/ralph/ralph-walk"})
        self.actor.reparentTo(self.node)
        self.actor.setScale(.2)
        self.actor.name = "Ralph"

        # Create a collsion node for this object.
        self.cNode = CollisionNode('ralph')
        # Attach a collision sphere solid to the collision node.
        self.cNode.addSolid(CollisionSphere(0, 0, 3, 3))
        # Attach the collision node to the object's model.
        self.smileyC = self.actor.attachNewNode(self.cNode)
        base.cTrav.addCollider(self.smileyC, World.pusher)
        World.pusher.addCollider(self.smileyC, self.actor, base.drive.node())
        
    def getActor(self):
        return self.actor

    def getRalphCount(self):
        return RalphCharacter.count

    def getMyRalphId(self):
        return self.id
    
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
            self.actor.setY(self.actor, -25 * globalClock.getDt())
        if (self.World.keyMap["forward"]!=0 and self.World.keyMap["mag"]!=1):
            self.actor.setY(self.actor, -100 * globalClock.getDt())
            
        if (self.World.keyMap["backward"]!=0 and self.World.keyMap["mag"]!=5):
            self.actor.setY(self.actor, 25 * globalClock.getDt())
        if (self.World.keyMap["backward"]!=0 and self.World.keyMap["mag"]!=1):
            self.actor.setY(self.actor, 100 * globalClock.getDt())
    
        list = self.actor.getPos()
        pos = Vec4(list[0],list[1],list[2],self.actor.getH())
        self.World.MoveManager.appendAction(pos)

        #self.actor.stop()

        #if (self.World.keyMap["backward"]!=0):
        #    self.actor.setY(self.actor, 25 * globalClock.getDt())

        if (self.World.keyMap["forward"]!=0) or (self.World.keyMap["left"]!=0) or (self.World.keyMap["right"]!=0) or (self.World.keyMap["backward"]!=0):
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