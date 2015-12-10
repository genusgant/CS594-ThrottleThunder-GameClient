from panda3d.core                       import *
from pandac.PandaModules                import *
from direct.actor.Actor                 import Actor
from Models3D.BaseModel3D               import BaseModel3D

class StaticModelVenus(BaseModel3D):
    def __init__(self,World, render,base,loader):
        BaseModel3D.__init__(self,World, render,base,loader)
        self.isVenusRotate = False

        #Load Venus
        self.orbit_root_venus = render.attachNewNode('orbit_root_venus')
        self.venus = loader.loadModel("models/planet_sphere")
        self.venus_tex = loader.loadTexture("models/venus_1k_tex.jpg")
        self.venus.setTexture(self.venus_tex, 1)
        self.venus.reparentTo(self.orbit_root_venus)
        self.venus.setPos( 10, -20, .8)
        self.venus.setScale(0.923 * 0.6)

        self.venusCNode = CollisionNode('venus')
        self.venusCNode.addSolid(CollisionSphere(0, 0, 0.01, 1.5))
        self.venusC = self.venus.attachNewNode(self.venusCNode)
        base.cTrav.addCollider(self.venusC, self.World.pusher)
        self.World.pusher.addCollider(self.venusC, self.venus, base.drive.node())

        self.day_period_venus = self.venus.hprInterval((60/365.0)*5, Vec3(360,0,0))

    def getVenus(self):
        return self.venus

    def rotateVenus(self, task):
        if self.getDistance()<10 and not self.isVenusRotate:
            self.isVenusRotate = True
            self.day_period_venus.loop()
        return task.cont

    def stopRotateVenus(self, task):
        if self.getDistance() > 10 and self.isVenusRotate:
            self.isVenusRotate = False
            self.day_period_venus.pause()
        return task.cont

    def getDistance(self):
        self.venus.setPos( 10, -20, .8)
        distanceVector = self.World.Character.actor.getPos()-self.venus.getPos()
        for model in self.World.CharacterManager.getCharacters():
            temp = model.actor.getPos()-self.venus.getPos()
            if temp.length() < distanceVector.length():
                distanceVector = temp
        return distanceVector.length()
