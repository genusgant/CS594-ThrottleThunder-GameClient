from panda3d.core                       import *
from pandac.PandaModules                import *
from direct.actor.Actor                 import Actor
from Models3D.BaseModel3D               import BaseModel3D

class StaticModelEarth(BaseModel3D):
    def __init__(self,World, render,base,loader):
        BaseModel3D.__init__(self,World, render,base,loader)
        self.isEarthRotate = False

        #Load Earth
        self.orbit_root_earth = render.attachNewNode('orbit_root_earth')
        self.earth = loader.loadModel("models/planet_sphere")
        self.earth_tex = loader.loadTexture("models/earth_1k_tex.jpg")
        self.earth.setTexture(self.earth_tex, 1)
        self.earth.reparentTo(self.orbit_root_earth)
        self.earth.setScale(1)
        self.earth.setPos( 30, 20, 1)

        self.earthCNode = CollisionNode('earth')
        self.earthCNode.addSolid(CollisionSphere(0, 0,0.10, 1.1))
        self.earthC = self.earth.attachNewNode(self.earthCNode)
        base.cTrav.addCollider(self.earthC, self.World.pusher)
        self.World.pusher.addCollider(self.earthC, self.earth, base.drive.node())
        self.day_period_earth = self.earth.hprInterval((60/365.0)*5, Vec3(360, 0, 0))

    def rotateEarth(self, task):
        if self.getDistance()<10 and not self.isEarthRotate:
            self.isEarthRotate = True
            self.day_period_earth.loop()
        return task.cont

    def stopRotateEarth(self, task):
        if self.getDistance() > 10 and self.isEarthRotate:
            self.isEarthRotate = False
            self.day_period_earth.pause()
        return task.cont

    def getEarth(self):
        return self.earth

    def getDistance(self):
        self.earth.setPos( 30, 20, 1)
        distanceVector = self.World.Character.actor.getPos()-self.earth.getPos()
        for model in self.World.CharacterManager.getCharacters():
            temp = model.actor.getPos()-self.earth.getPos()
            if temp.length() < distanceVector.length():
                distanceVector = temp
        return distanceVector.length()