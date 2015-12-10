import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject      
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from Screen.AuthScreen import AuthScreen
from Screen.CharacterSelectScreen import CharacterSelectScreen
import random, sys, os, math
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from panda3d.core import Point3, Plane
from panda3d.core import CollisionTraverser,CollisionNode, CollisionSphere
from panda3d.core import CollisionHandlerQueue,CollisionRay, CollisionHandlerPusher, CollisionPlane
from direct.interval.IntervalGlobal import Sequence
from direct.task import Task
import time

SPEED = 0.5

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
                        pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)


class MyRalph:
    count = 0
    def __init__(self, tempworld):
        self.world = tempworld
        MyRalph.count += 1
        self.id = MyRalph.count

        self.actor = Actor("models/ralph/ralph",
                         {"run":"models/ralph/ralph-run",
                          "walk":"models/ralph/ralph-walk"})
        self.actor.reparentTo(render)
        self.actor.setScale(.2)
        self.actor.setPos(int(self.id)*20, 0, 0)

        # Create a collsion node for this object.
        self.cNode = CollisionNode('ralph')
        # Attach a collision sphere solid to the collision node.
        self.cNode.addSolid(CollisionSphere(0, 0, 3, 3))
        # Attach the collision node to the object's model.
        self.smileyC = self.actor.attachNewNode(self.cNode)
        base.cTrav.addCollider(self.smileyC, self.world.pusher)
        self.world.pusher.addCollider(self.smileyC, self.actor, base.drive.node())

    def getActor(self):
        return self.actor

    def getRalphCount(self):
        return MyRalph.count

    def getMyRalphId(self):
        return self.id

class MyPanda:
    count=0
    def __init__(self, tempworld):
        MyPanda.count += 1
        self.id = MyPanda.count
        self.world = tempworld

        self.pandaNode=render.attachNewNode('pandaNode')
        self.actor=Actor("models/panda-model",
                     {"walk": "models/panda-walk4"})
        self.actor.reparentTo(self.pandaNode)
        self.actor.setPos(int(self.id) * 30,0,0)
        self.actor.setScale(0.002, 0.002, 0.002)

        self.cNode = CollisionNode('panda')
        self.cNode.addSolid(CollisionSphere(2, 0, 400, 500))
        self.frowneyC = self.actor.attachNewNode(self.cNode)
        base.cTrav.addCollider(self.frowneyC, self.world.pusher)
        self.world.pusher.addCollider(self.frowneyC, self.actor, base.drive.node())

    def getActor(self):
        return self.actor

    def getPandaCount(self):
        return MyRalph.count

    def getMyPandaId(self):
        return self.id


class MyCar:
    count=0
    def __init__(self, tempworld):
        self.world = tempworld
        MyCar.count += 1
        self.carNode = render.attachNewNode('dummy_car')
        self.car = loader.loadModel("models/knucklehead")
        self.car_tex = loader.loadTexture("models/knucklehead.jpg")
    	self.car.setTexture(self.car_tex, 1)
        self.car.reparentTo(self.carNode)
        self.car.setPos(20,20,0)
        self.car.setScale(.08)
        self.car.setP(-90)
        self.car.setColor(0.6, 0.6, 1.0, 1.0)
        self.car.setColorScale(0.6, 0.6, 1.0, 1.0)

        self.carCNode = CollisionNode('car')
        self.carCNode.addSolid(CollisionSphere(0, 0, 3, 3))
        self.carC = self.car.attachNewNode(self.carCNode)
        base.cTrav.addCollider(self.carC, self.world.pusher)
        self.world.pusher.addCollider(self.carC, self.car, base.drive.node())

        #self.actor = self.car

    def getMyCar(self):
        return self.car


class StaticModelSun:

    def __init__(self,tempworld):

        self.world = tempworld
        self.isSunRotate = False

        #Load the Sun
        self.orbit_root_sun = render.attachNewNode('orbit_root_sun')
        self.sun = loader.loadModel("models/planet_sphere")
        self.sun_tex = loader.loadTexture("models/sun_1k_tex.jpg")
        self.sun.setTexture(self.sun_tex, 1)
        self.sun.reparentTo(self.orbit_root_sun)
        self.sun.reparentTo(render)
        self.sun.setPos(-30,20,1)
        self.sun.setScale(2 * 0.4)

        self.sunCNode = CollisionNode('sun')
        self.sunCNode.addSolid(CollisionSphere(0, 0, 5, 5))
        self.sunC = self.sun.attachNewNode(self.sunCNode)
        base.cTrav.addCollider(self.sunC, self.world.pusher)
        self.world.pusher.addCollider(self.sunC, self.sun, base.drive.node())

        self.day_period_sun = self.sun.hprInterval((60/365.0)*5, Vec3(360, 0, 0))

    def getSun(self):
        return self.sun

    def rotateSun(self, task):
        if self.getDistance()<10 and not self.isSunRotate:
            self.isSunRotate = True
            self.day_period_sun.loop()
        return Task.cont

    def stopRotateSun(self, task):
        if self.getDistance() > 10 and self.isSunRotate:
            self.isSunRotate = False
            self.day_period_sun.pause()
        return Task.cont

    def getDistance(self):
        distanceVector = self.world.ralph.getPos()-self.sun.getPos()
        return distanceVector.length()



class StaticModelVenus:

    def __init__(self,tempworld):

        self.world = tempworld
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
        self.venusCNode.addSolid(CollisionSphere(0, 0, 3, 3))
        self.venusC = self.venus.attachNewNode(self.venusCNode)
        base.cTrav.addCollider(self.venusC, self.world.pusher)
        self.world.pusher.addCollider(self.venusC, self.venus, base.drive.node())

        self.day_period_venus = self.venus.hprInterval((60/365.0)*5, Vec3(360,0,0))

    def getVenus(self):
        return self.venus

    def rotateVenus(self, task):
        if self.getDistance()<10 and not self.isVenusRotate:
            self.isVenusRotate = True
            self.day_period_venus.loop()
        return Task.cont

    def stopRotateVenus(self, task):
        if self.getDistance() > 10 and self.isVenusRotate:
            self.isVenusRotate = False
            self.day_period_venus.pause()
        return Task.cont

    def getDistance(self):
        distanceVector = self.world.ralph.getPos()-self.venus.getPos()
        return distanceVector.length()


class StaticModelEarth:

    def __init__(self,tempworld):

        self.world = tempworld
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
        self.earthCNode.addSolid(CollisionSphere(0, 0, 4, 4))
        self.earthC = self.earth.attachNewNode(self.earthCNode)
        base.cTrav.addCollider(self.earthC, self.world.pusher)
        self.world.pusher.addCollider(self.earthC, self.earth, base.drive.node())
        self.day_period_earth = self.earth.hprInterval((60/365.0)*5, Vec3(360, 0, 0))

    def rotateEarth(self, task):
        if self.getDistance()<10 and not self.isEarthRotate:
            self.isEarthRotate = True
            self.day_period_earth.loop()
        return Task.cont

    def stopRotateEarth(self, task):
        if self.getDistance() > 10 and self.isEarthRotate:
            self.isEarthRotate = False
            self.day_period_earth.pause()
        return Task.cont

    def getEarth(self):
        return self.earth

    def getDistance(self):
        distanceVector = self.world.ralph.getPos()-self.earth.getPos()
        return distanceVector.length()

class World(DirectObject):

    def __init__(self):

        self.keyMap = {"left":0, "right":0, "forward":0, "backward":0,"cam-left":0, "cam-right":0}
        base.win.setClearColor(Vec4(0,0,0,1))

        # Post the instructions

        self.title = addTitle("Panda3D Tutorial: Multiplayer (Walking on the Moon)")
        self.inst1 = addInstructions(0.95, "[ESC]: Quit")
        self.inst2 = addInstructions(0.90, "[a]: Rotate Player Left")
        self.inst3 = addInstructions(0.85, "[d]: Rotate Player Right")
        self.inst4 = addInstructions(0.80, "[w]: Move Player Forward")
        self.inst5 = addInstructions(0.75, "[s]: Move Player Backward")
        self.inst6 = addInstructions(0.70, "[shift+w]: Move Player Fast")
        self.inst7 = addInstructions(0.65, "[q]: Rotate Camera Left")
        self.inst8 = addInstructions(0.60, "[e]: Rotate Camera Right")


        # Set up the environment
        self.environ = loader.loadModel("models/square")
        self.environ.reparentTo(render)
        self.environ.setPos(0,0,0)
        self.environ.setScale(100,100,1)
        self.moon_tex = loader.loadTexture("models/moon_1k_tex.jpg")
        self.environ.setTexture(self.moon_tex, 1)

        #Collision Code
        # Initialize the collision traverser.
        base.cTrav = CollisionTraverser()
        # Initialize the Pusher collision handler.
        self.pusher = CollisionHandlerPusher()


        #Load Players and Models in GameWorld
        self.ralphRef = MyRalph(self)
        self.ralph = self.ralphRef.getActor()

        self.pandaRef = MyPanda(self)
        self.panda = self.pandaRef.getActor()

        self.carRef = MyCar(self)
        self.car = self.carRef.getMyCar()

        self.staticRefSun = StaticModelSun(self)
        self.staticRefVenus = StaticModelVenus(self)
        self.staticRefEarth = StaticModelEarth(self)

        self.sun = self.staticRefSun.getSun()
        self.venus = self.staticRefVenus.getVenus()
        self.earth = self.staticRefEarth.getEarth()

        taskMgr.add(self.staticRefSun.rotateSun,"rotateSun")
        taskMgr.add(self.staticRefVenus.rotateVenus,"rotateVenus")
        taskMgr.add(self.staticRefEarth.rotateEarth,"rotateEarth")
        taskMgr.add(self.staticRefEarth.stopRotateEarth,"stopRotateEarth")
        taskMgr.add(self.staticRefSun.stopRotateSun,"stopRotateSun")
        taskMgr.add(self.staticRefVenus.stopRotateVenus,"stopRotateVenus")


        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        floorNode = render.attachNewNode("Floor NodePath")
        # Create a collision plane solid.
        collPlane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        # Call our function that creates a nodepath with a collision node

        floorCollisionNP = self.makeCollisionNodePath(floorNode, collPlane)

        # Accept the control keys for movement and rotation
        self.accept("escape", sys.exit)
        self.accept("a", self.setKey, ["left",1])
        self.accept("d", self.setKey, ["right",1])
        self.accept("w", self.setKey, ["forward",1])
        self.accept("q", self.setKey, ["cam-left",1])
        self.accept("e", self.setKey, ["cam-right",1])
        self.accept("a-up", self.setKey, ["left",0])
        self.accept("d-up", self.setKey, ["right",0])
        self.accept("w-up", self.setKey, ["forward",0])
        self.accept("q-up", self.setKey, ["cam-left",0])
        self.accept("e-up", self.setKey, ["cam-right",0])
        self.accept("shift-w",self.setKey, ["forward",5])
        #self.accept("s",self.setKey, ["backward",1])


        taskMgr.add(self.move,"moveTask")

        # Game state variables
        self.isMoving = False

        # Set up the camera

        base.disableMouse()
        #Change Camera Position Later
        base.camera.setPos(self.ralph.getX(),self.ralph.getY()+10,2)

        # Create some lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

    def makeCollisionNodePath(self, nodepath, solid):
        '''
        Creates a collision node and attaches the collision solid to the
        supplied NodePath. Returns the nodepath of the collision node.
        '''
        # Creates a collision node named after the name of the NodePath.
        collNode = CollisionNode("%s c_node" % nodepath.getName())
        collNode.addSolid(solid)
        collisionNodepath = nodepath.attachNewNode(collNode)
        return collisionNodepath

    #Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value
        print key, value

    def move(self, task):

        base.camera.lookAt(self.ralph)
        if (self.keyMap["cam-left"]!=0):
            base.camera.setX(base.camera, -20 * globalClock.getDt())
        if (self.keyMap["cam-right"]!=0):
            base.camera.setX(base.camera, +20 * globalClock.getDt())

        startpos = self.ralph.getPos()

        if (self.keyMap["left"]!=0):
            self.ralph.setH(self.ralph.getH() + 300 * globalClock.getDt())
        if (self.keyMap["right"]!=0):
            self.ralph.setH(self.ralph.getH() - 300 * globalClock.getDt())
        if (self.keyMap["forward"]!=0 and self.keyMap["forward"]!=5):
            self.ralph.setY(self.ralph, -25 * globalClock.getDt())
        if (self.keyMap["forward"]!=0 and self.keyMap["forward"]!=1):
            self.ralph.setY(self.ralph, -100 * globalClock.getDt())
        #if (self.keyMap["backward"]!=0):
        #    self.ralph.setY(self.ralph, 25 * globalClock.getDt())

        if (self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or (self.keyMap["right"]!=0):
            if self.isMoving is False:
                self.ralph.loop("run")
                self.isMoving = True
        else:
            if self.isMoving:
                self.ralph.stop()
                self.ralph.pose("walk",5)
                self.isMoving = False

        camvec = self.ralph.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > 10.0):
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-10))
            camdist = 10.0
        if (camdist < 5.0):
            base.camera.setPos(base.camera.getPos() - camvec*(5-camdist))
            camdist = 5.0

        self.floater.setPos(self.ralph.getPos())
        self.floater.setZ(self.ralph.getZ() + 2.0)
        base.camera.lookAt(self.floater)

        return task.cont

w = World()
run()