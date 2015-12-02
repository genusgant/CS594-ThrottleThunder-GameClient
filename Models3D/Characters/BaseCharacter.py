import sys, random
from panda3d.core               import *
from Models3D.BaseModel3D       import BaseModel3D

class BaseCharacter(BaseModel3D):
    floater = None
    def __init__(self, World, render, base,loader):
        BaseModel3D.__init__(self, World, render, base,loader)
        if self.floater == None:
            self.floater = NodePath(PandaNode("floater"))
            self.floater.reparentTo(self.render)
        self.isMoving = False

    def setControls(self):
        self.World.keyMap = {"left":0, "right":0, "forward":0, "backward":0,"cam-left":0, "cam-right":0,"mag":1}
        self.World.accept("escape", self.World.endSession)
        self.World.accept("a", self.setKey, ["left",1])
        self.World.accept("d", self.setKey, ["right",1])
        self.World.accept("w", self.setKey, ["forward",1])
        self.World.accept("s", self.setKey, ["backward",1])
        self.World.accept("q", self.setKey, ["cam-left",1])
        self.World.accept("e", self.setKey, ["cam-right",1])
        self.World.accept("a-up", self.setKey, ["left",0])
        self.World.accept("d-up", self.setKey, ["right",0])
        self.World.accept("w-up", self.setKey, ["forward",0])
        self.World.accept("s-up", self.setKey, ["backward",0])
        self.World.accept("q-up", self.setKey, ["cam-left",0])
        self.World.accept("e-up", self.setKey, ["cam-right",0])
        self.World.accept("shift",self.setKey, ["mag",5])
        self.World.accept("shift-a",self.setKey, ["left",1])
        self.World.accept("shift-d",self.setKey, ["right",1])
        self.World.accept("shift-w",self.setKey, ["forward",1])
        self.World.accept("shift-s",self.setKey, ["backward",1])
        self.World.accept("shift-up",self.setKey, ["mag",1])
        
        
    def blockControls(self):
        self.World.ignore("escape")
        self.World.ignore("a")
        self.World.ignore("d")
        self.World.ignore("w")
        self.World.ignore("s")
        self.World.ignore("q")
        self.World.ignore("e")
        self.World.ignore("a-up")
        self.World.ignore("d-up")
        self.World.ignore("w-up")
        self.World.ignore("s-up")
        self.World.ignore("q-up")
        self.World.ignore("e-up")
        self.World.ignore("shift-w")
        self.World.ignore("shift-s")
        self.World.ignore("shift-a")
        self.World.ignore("shift-d")
    
    def setCharacter(self, _Actor):
        self.actor = _Actor
    
    #Records the state of the arrow keys
    def setKey(self, key, value):
        self.World.keyMap[key] = value
        
    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
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
        if (self.World.keyMap["forward"]!=0 and self.World.keyMap["forward"]!=5 and self.actor.name =='Ralph'):
            self.actor.setY(self.actor, -25 * globalClock.getDt())
        if (self.World.keyMap["forward"]!=0 and self.World.keyMap["forward"]!=1 and self.actor.name == 'Ralph'):
            self.actor.setY(self.actor, -100 * globalClock.getDt())
        if (self.World.keyMap["forward"]!=0 and self.World.keyMap["forward"]!=5 and self.actor.name != 'Ralph'):
            self.actor.play("walk")
            self.actor.loop("walk")
            self.actor.setY(self.actor, -1000 * globalClock.getDt())
        if (self.World.keyMap["forward"]!=0 and self.World.keyMap["forward"]!=1 and self.actor.name != 'Ralph'):
            self.actor.play("walk")
            self.actor.loop("walk")
            self.actor.setY(self.actor, -2000 * globalClock.getDt())
            
            
        if self.World.keyMap["backward"]!=0 and self.actor.name == 'Ralph':
            self.actor.setY(self.actor, 25 * globalClock.getDt())
            
        if (self.World.keyMap["backward"]!=0 and self.actor.name != 'Ralph'):
            self.actor.play("walk")
            self.actor.loop("walk")
            self.actor.setY(self.actor, 1000 * globalClock.getDt())

        list = self.actor.getPos()
        pos = Vec4(list[0],list[1],list[2],self.actor.getH())
        self.World.MoveManager.appendAction(pos)
        #self.actor.stop()

        #if (self.World.keyMap["backward"]!=0):
        #    self.actor.setY(self.actor, 25 * globalClock.getDt())

        if (self.World.keyMap["forward"]!=0) or (self.World.keyMap["left"]!=0) or (self.World.keyMap["right"]!=0):
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
        if heading == None:
            self.floater.setPos(float(pos[0]),float(pos[1]),float(pos[2]))
            self.lookAt(self.floater)
            self.actor.setPos(float(pos[0]),float(pos[1]),float(pos[2]))
        else:
            self.actor.setPos(float(pos[0]),float(pos[1]),float(pos[2]))
            self.actor.setH(float(heading))
        
    def placeAt(self,pos):
        for model in self.World.CharacterManager.getCharacters():
            distance = Vec3(pos[0],pos[1],0) - model.actor.getPos()
            if( abs(distance.length()) < 5):
                self.placeAt((pos[0]+random.uniform(-5.0, 5.0), pos[1]+random.uniform(-5.0, 5.0), 0))
                return False
        
        self.actor.setPos(pos[0],pos[1],0)