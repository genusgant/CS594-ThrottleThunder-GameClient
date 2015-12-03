# Roaming-Ralph was modified to remove collision part.

# import direct.directbase.DirectStart
import sys
import math
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import PointLight
from panda3d.core import Vec2
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import LVecBase3
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32
from panda3d.core import PandaNode
from panda3d.core import NodePath
from panda3d.core import TextNode
from panda3d.core import CollisionNode
from panda3d.core import NodePath
from panda3d.bullet import BulletWorld, BulletTriangleMesh, BulletTriangleMeshShape, BulletDebugNode, BulletPlaneShape, \
    BulletRigidBodyNode, BulletBoxShape
from Track import Track
from rrVehicle import Vehicle
from Camera import Camera
from SkyDome import SkyDome
from Powerups import PowerupManager
from panda3d.bullet import BulletHeightfieldShape
from panda3d.bullet import ZUp
from Terrain import Terrain
from Obstruction import Obstruction
from LoadingScreen import LoadingScreen
from VehicleAttributes import VehicleAttributes
from rrTrack import Track
from rrAudio import Audio
# """ Custom Imports """
# import your modules
from common.Constants import Constants
from net.ConnectionManager import ConnectionManager
from rrDashboard import *
from threading import Thread
from time import sleep
import re
from pandac.PandaModules import loadPrcFileData
from helper.RaceMaster import RaceMaster
from rrCheckpoint import Checkpoint

loadPrcFileData('', 'bullet-enable-contact-events true')

SPEED = 0.5


def getDimensions(nPath):
    pt1, pt2 = nPath.getTightBounds()
    xDim = pt2.getX() - pt1.getX()
    yDim = pt2.getY() - pt1.getY()
    zDim = pt2.getZ() - pt1.getZ()
    return [xDim, yDim, zDim]


path = ['f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f',
        # 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f',
        # 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',
        # 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b','b', 'b', 'b', 'b', 'b', 'b',
        'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',
        'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f',
        'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']


# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale=.05)


# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1),
                        pos=(1.3, -0.95), align=TextNode.ARight, scale=.07)


class RRWorldManager():
    def __init__(self, lobby):
        self.playerList = {}
        self.userList = []
        self.otherPlayersDataAvailable = False
        self.lobby = lobby
        self.gameWorld = World(self)
        self.loadinScreen = LoadingScreen(self.gameWorld)
        self.lobby.World.ServerConnection.activeStatus = False
        self.cManager = ConnectionManager(self, self.lobby.World.ServerConnection)
        self.cManager.startConnection()
        self.gameWorld.cManager = self.cManager
        self.cManager.sendRequest(Constants.CMSG_REQ_TEST)
        self.addVehicleProps(self.lobby.World.username, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        # self.cManager.sendRequest(Constants.CMSG_SET_POSITION)
        # while not self.otherPlayersDataAvailable:
        # print "Wait for respponse"
        # sleep(1)
        # Fake player creation for the time being
        # x = 10
        # y = 10
        # z = 0
        # print "LOBBY LIST: ", self.lobby.playerList
        # if len(self.lobby.playerList) > 0:
        #     for idx, player in enumerate(self.lobby.playerList):
        #         if player != None:
        #             print "Creating -", player
        #             self.addPlayer(player, 1, 0, 0, x, y, z, 0, 0, 0)
        #             x += 10
        #             y += 10
        taskMgr.add(self.startGameTask, "startGameTask")

    def startGameTask(self, task):

        if self.otherPlayersDataAvailable:
            self.startGameSequence()
            self.gameWorld.startGameNow()
            return task.done
        else:
            return task.cont

    def addVehicleProps(self, username, carId, carPaint, carTires, x, y, z, h, p, r):
        if username in self.playerList.keys():
            vehicle = self.playerList[username]
            vehicle.carId = carId
            vehicle.carPaint = carPaint
            vehicle.carTires = carTires
            vehicle.x = x
            vehicle.y = y
            vehicle.z = z
            vehicle.h = h
            vehicle.p = p
            vehicle.r = r
            self.playerList[username] = vehicle
        else:
            vehicle = VehicleAttributes(username, carId, carPaint, carTires, x, y, z, h, p, r)
            print "Adding to list player: ", username
            self.playerList[username] = vehicle

    def modifyPlayerPos(self, username, x, y, z, h, p, r):
        if username in self.playerList.keys():
            vehicle = self.playerList[username]
            vehicle.x = x
            vehicle.y = y
            vehicle.z = z
            vehicle.h = h
            vehicle.p = p
            vehicle.r = r
            self.playerList[username] = vehicle

        else:
            VehicleAttributes(username, 0, 0, 0, x, y, z, h, p, r)

    def startGameSequence(self):
        self.loadinScreen.finish()
        self.gameWorld.initializeGameWorld()


class World(DirectObject):
    gameStateDict = {"Login": 0, "CreateLobby": 4, "EnterGame": 1, "BeginGame": 2, "InitializeGame": 3}
    gameState = -1
    # Login , EnterGame , BeginGame
    responseValue = -1
    currentTime = 0
    idleTime = 0
    mySequence = None
    pandaPace = None
    jumpState = False
    isWalk = False
    previousPos = None  # used to store the mainChar pos from one frame to another
    host = ""
    port = 0
    characters = []

    def __init__(self, manager):
        # Stores the list of all the others players characters
        self.vehiclelist = {}
        self.isActive = False
        self.nodeFilterList = []
        self.collisionThreadSet = []
        self.otherPlayer = None
        self.manager = manager
        self.lobby = manager.lobby
        self.login = self.lobby.World.username
        # self.cManager = self.manager.cManager
        self.isDebug = False

    def initializeGameWorld(self):

        base.setFrameRateMeter(True)
        self.setupLights()
        self.accept('escape', self.doExit)
        self.keyMap = {"reset": 0}
        # input states
        self.accept('f1', self.toggleWireframe)
        self.accept('f2', self.toggleTexture)
        self.accept('f3', self.toggleDebug)
        self.accept('f5', self.doScreenshot)
        self.accept("r", self.resetCar)
        self.accept('1', self.activateBoost)
        # Network Setup
        # self.cManager.startConnection()
        # taskMgr.add(self.usePowerup, "usePowerUp")
        self.accept('bullet-contact-added', self.onContactAdded)
        # Physics -- Terrain
        self.setup()  # Create Players
        self.createPlayers()

        # Camera
        self.setupCamera()
        # Create Powerups
        self.createPowerups()
        # taskMgr.add(self.powerups.checkPowerPickup, "checkPowerupTask")

        # Load Audio
        self.audio = Audio(base, self)

        # Dashboard
        self.dashboard = Dashboard(self, taskMgr, self.rm)

        # checkpoints for tracking positions
        #     self.cself.rm.getCheckpointMarkers()
        taskMgr.doMethodLater(.1, self.rm.updateCheckpoints, 'updateRace')

    def activateKeys(self):
        inputState.watchWithModifiers('boostUp', '1-up')
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('brake', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('turnLeft', 'q')
        inputState.watchWithModifiers('turnRight', 'e')

        self.world.setGravity(Vec3(0, 0, -9.81))

    def activateBoost(self):
        self.vehicleContainer.addBoost()

    def resetCar(self):
        if self.vehicleContainer.chassisNP.getZ() > -30 : self.vehicleContainer.reset()
        else: self.rm.resetCar()
        

    def createPowerups(self):
        self.powerups = PowerupManager(self, self.vehicleContainer)

    def setTime(self):
        self.cManager.sendRequest(Constants.CMSG_TIME)

    def doExit(self):
        self.cleanup()
        sys.exit(1)

    def cleanup(self):
        self.cManager.sendRequest(Constants.CMSG_DISCONNECT)
        self.cManager.closeConnection()
        self.world = None
        self.outsideWorldRender.removeNode()

    def doReset(self):
        self.mainCharRef.reset()

    def enterGame(self, task):
        self.startGameNow()
        return task.done
        if self.gameState == self.gameStateDict["Login"]:
            # responseValue = 1 indicates that this state has been finished
            if self.responseValue == 1:
                print "Authentication succeeded"
                # Authentication succeeded
                self.cManager.sendRequest(Constants.CMSG_CREATE_LOBBY, ["raceroyal", "0", "1"])
                self.gameState = self.gameStateDict["CreateLobby"]
                self.responseValue = -1
        elif self.gameState == self.gameStateDict["CreateLobby"]:
            if self.responseValue == 1:
                # Lobby Created and we are already in
                print "Lobby Created and we are already in"
                self.gameState = self.gameStateDict["EnterGame"]
                self.responseValue = -1
                self.cManager.sendRequest(Constants.CMSG_READY)

            elif self.responseValue == 0:
                # Game already created, let's join it
                print "Game already created, let's join it"
                self.cManager.sendRequest(Constants.CMSG_ENTER_GAME_NAME, "raceroyal")
                # self.gameState = self.gameStateDict["EnterGame"]
                # self.responseValue = -1
                self.responseValue = -1
                self.gameState = self.gameStateDict["InitializeGame"]
                #               Everyone is in the game, we send ReqReady, and the server will send positions when every client did
                self.cManager.sendRequest(Constants.CMSG_READY)

        elif self.gameState == self.gameStateDict["EnterGame"]:
            if self.responseValue == 1:
                #                 When the positions are sent, an acknowledgment is sent and we begin the InitializeGame
                print "When the positions are sent, an acknowledgment is sent and we begin the InitializeGame"
                self.responseValue = -1
                self.gameState = self.gameStateDict["InitializeGame"]
                #               Everyone is in the game, we send ReqReady, and the server will send positions when every client did
                self.cManager.sendRequest(Constants.CMSG_READY)

        elif self.gameState == self.gameStateDict["InitializeGame"]:
            if self.responseValue == 1:
                print "Set up the camera"
                # Set up the camera
                self.camera = Camera(self.mainChar)
                self.gameState = self.gameStateDict["BeginGame"]
                self.cManager.sendRequest(Constants.CMSG_READY)
                self.responseValue = -1

        elif self.gameState == self.gameStateDict["BeginGame"]:
            if self.responseValue == 1:
                print "Begin Game"
                # taskMgr.doMethodLater(.1, self.updateMove, 'updateMove')
                taskMgr.add(self.update, "moveTask")
                return task.done

        return task.cont

    def startGameNow(self):
        # self.camera = Camera(self.mainChar)
        taskMgr.doMethodLater(.1, self.update, 'updateMove')
        # taskMgr.add(self.update, "moveTask")

    def createEnvironment(self):
        self.environ = loader.loadModel("models/square")
        self.environ.reparentTo(render)
        self.environ.setPos(0, 0, 0)
        self.environ.setScale(500, 500, 1)
        self.moon_tex = loader.loadTexture("models/moon_1k_tex.jpg")
        self.environ.setTexture(self.moon_tex, 1)

        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
        node = BulletRigidBodyNode('Ground')
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(0, 0, 0)

        self.bulletWorld.attachRigidBody(node)

        self.visNP = loader.loadModel('models/track.egg')
        self.tex = loader.loadTexture("models/tex/Main.png")
        self.visNP.setTexture(self.tex)

        geom = self.visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
        mesh = BulletTriangleMesh()
        mesh.addGeom(geom)
        trackShape = BulletTriangleMeshShape(mesh, dynamic=False)

        body = BulletRigidBodyNode('Bowl')
        self.visNP.node().getChild(0).addChild(body)
        bodyNP = render.anyPath(body)
        bodyNP.node().addShape(trackShape)
        bodyNP.node().setMass(0.0)
        bodyNP.setTexture(self.tex)

        self.bulletWorld.attachRigidBody(bodyNP.node())

        self.visNP.reparentTo(render)

        self.bowlNP = bodyNP
        self.visNP.setScale(70)

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

    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def getDist(self):
        mainCharX = self.mainChar.getPos().x
        mainCharY = self.mainChar.getPos().y
        pandaX = self.pandaActor2.getPos().x
        pandaY = self.pandaActor2.getPos().y
        dist = math.sqrt(abs(mainCharX - pandaX) ** 2 + abs(mainCharY - pandaY) ** 2)
        return dist

    def removeCollisionSet(self, arg):
        sleep(2)
        self.nodeFilterList.pop(0)

    # _____HANDLER_____
    def onContactAdded(self, node1, node2):
        isMyCarColliding = False
        if node1.notifiesCollisions() and node2.notifiesCollisions():
            # play collision sound with another player
            self.audio.play_collision()
            isEnable = True
            list2 = [node1.getName(), node2.getName()]
            for nodeSet in self.nodeFilterList:
                if (list2[0] == nodeSet[0]) or (list2[0] == nodeSet[1]):
                    if (list2[1] == nodeSet[0]) or (list2[1] == nodeSet[1]):
                        isEnable = False

            if isEnable:
                isMyCarColliding = False
                npA = NodePath.anyPath(node1)
                npB = NodePath.anyPath(node2)
                message = ""
                if node1.getName() == self.login:
                    nodeA = node1
                    nodeB = node2
                    isMyCarColliding = True
                elif node2.getName() == self.login:
                    nodeA = node2
                    nodeB = node1
                    isMyCarColliding = True

            if isMyCarColliding:
                print "isMyCarColliding: True"
                name1 = node1.getTag("username")
                vehicle1 = self.vehicleList[name1]
                vehicle1.props.setVelocity(node1.getLinearVelocity().length())
                name2 = node2.getTag("username")
                vehicle2 = self.vehicleList[name2]
                vehicle2.props.setVelocity(node2.getLinearVelocity().length())
                self.calculateDamage(vehicle1, vehicle2)

            self.nodeFilterList.append((node1.getName(), node2.getName()))
            thread = Thread(target=self.removeCollisionSet, args=(1,))
            self.collisionThreadSet.append(thread)
            thread.start()

    def doExit(self):
        self.cleanup()
        sys.exit(1)

    def doReset(self):
        self.cleanup()
        self.setup()

    def toggleWireframe(self):

        base.toggleWireframe()

    def toggleTexture(self):

        base.toggleTexture()

    def toggleDebug(self):
        if self.debugNP.isHidden() and self.isDebug:
            self.debugNP.show()
        else:
            self.debugNP.hide()

    def calculateDamage(self, fromCar, toCar, fromCollisionSection=2, toCollisionSection=2):
        # toCar takes more damage than fromCar
        fromWeight = fromCar.props.weight
        toWeight = toCar.props.weight
        fromSpeed = fromCar.props.velocity
        toSpeed = toCar.props.velocity

        # Speed Max = 100
        # Weights Max = 10
        # Front collisionSection = 3, mid = 2, back = 1
        damageFactor = (((fromWeight + toWeight) * (fromSpeed + toSpeed)) / 100)

        fromDamage = .5 * damageFactor / fromCollisionSection
        toDamage = .5 * damageFactor / toCollisionSection

        print "From Damage: ", fromDamage
        print "To Damage: ", toDamage

        fromCar.props.armor -= fromDamage
        if fromCar.props.armor < 0:
            fromCar.props.armor = 0
            fromCar.props.health -= fromCar.props.armor

        toCar.props.armor -= toDamage
        if toCar.props.armor < 0:
            toCar.props.armor = 0
            toCar.props.health -= toCar.props.armor

    def doScreenshot(self):

        base.screenshot('Bullet')

    def toggleHeightfield(self):

        self.terrainContainer.setDebugEnabled()

    # ____TASK___
    def update(self, task):
        dt = globalClock.getDt()
        # print "Type: ", type(self.vehicleContainer)
        forces = self.vehicleContainer.processInput(inputState, dt)
        self.audio.process_input(inputState)
        moving = self.vehicleContainer.chassisNP.getPos()
        if forces != None and forces[0] != None and forces[1] != None and forces[2] != None:
            # fake move for other playera
            # self.otherPlayer.move(forces[0], forces[1], forces[2], moving.getX()+10, moving.getY(), moving.getZ(),
            #                            self.vehicleContainer.chassisNP.getH(), self.vehicleContainer.chassisNP.getP(), self.vehicleContainer.chassisNP.getR())
            # print"sending move: ", self.login, forces[0], forces[1], forces[2], moving.getX(), moving.getY(), moving.getZ(), self.vehicleContainer.chassisNP.getH(), self.vehicleContainer.chassisNP.getP(), self.vehicleContainer.chassisNP.getR()
            self.cManager.sendRequest(Constants.CMSG_MOVE,
                                      [forces[0], forces[1], forces[2], moving.getX(), moving.getY(), moving.getZ(),
                                       self.vehicleContainer.chassisNP.getH(), self.vehicleContainer.chassisNP.getP(),
                                       self.vehicleContainer.chassisNP.getR()])

        # self.moveCrazyCar(dt)
        self.world.doPhysics(dt, 10, 0.008)

        # if inputState.isSet('step'):
        #     self.vehicleContainer.processInput(inputState, dt)
        #     self.moveCrazyCar(dt)
        #     self.stepPhysicsWorld()

        self.updateCamera(self.vehicleContainer.speed)
        return task.again

    def updateCamera(self, speed=0.0, initial=False):
        # """Reposition camera depending on the vehicle speed"""
        minDistance = 8.0
        maxDistance = 13.0
        minHeight = 1.5
        maxHeight = 3.0
        maxSpeed = 30.0  # m/s

        distance = (minDistance + (maxDistance - minDistance) * speed / maxSpeed)
        distance = min(maxDistance, distance)
        height = minHeight + (maxHeight - minHeight) * speed / maxSpeed
        height = min(maxHeight, height)

        vPos = self.vehicleContainer.chassisNP.getPos()
        headingRad = self.vehicleContainer.chassisNP.getH() * math.pi / 180.0

        targetPos = vPos + Vec3(distance * math.sin(headingRad), -distance * math.cos(headingRad), height)
        cameraPos = base.camera.getPos()

        base.camera.setPos(cameraPos + (targetPos - cameraPos) * 0.1)
        # Look slightly ahead of the car
        base.camera.lookAt(*vPos)
        base.camera.setP(base.camera.getP() + 7)

    def cleanup(self):
        self.world = None
        self.worldNP.removeNode()

    def setupCamera(self):
        base.disableMouse()
        base.camera.setPos(self.vehicleContainer.chassisNP.getX(), self.vehicleContainer.chassisNP.getY() + 10, 2)
        # Create a floater object.  We use the "floater" as a temporary
        # variable in a variety of calculations.
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

    def setupLights(self):
        base.setBackgroundColor(0.0, 0.0, 0.0, 1)
        base.setFrameRateMeter(True)
        # Add a light to the scene.
        self.lightpivot = render.attachNewNode("lightpivot")
        self.lightpivot.setPos(0, 0, 5)
        self.lightpivot.hprInterval(10, Point3(360, 0, 0)).loop()
        plight = PointLight('plight')
        plight.setColor(Vec4(1, 0, 0, 1))
        plight.setAttenuation(Vec3(0.37, 0.025, 0))
        plnp = self.lightpivot.attachNewNode(plight)
        plnp.setPos(45, 0, 0)
        plnp.lookAt(*Vec3(0, 0, 0, ))

        # Light
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        alightNP = render.attachNewNode(alight)

        #   dlight = DirectionalLight('directionalLight')
        #   dlight.setDirection(Vec3(1, 1, -1))
        #   dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        #   dlightNP = render.attachNewNode(dlight)



        render.clearLight()
        render.setLight(alightNP)
        #   render.setLight(dlightNP)
        render.setLight(plnp)

        # create a sphere to denote the light
        sphere = loader.loadModel("models/sphere")
        sphere.reparentTo(plnp)

        render.setShaderAuto()

        # directional light
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        directionalLight2 = DirectionalLight("directionalLight2")
        directionalLight2.setDirection(Vec3(5, 5, -5))
        directionalLight2.setColor(Vec4(1, 1, 1, 1))
        directionalLight2.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(directionalLight))
        render.setLight(render.attachNewNode(directionalLight2))

    def stepPhysicsWorld(self):
        dt = globalClock.getDt()
        self.world.doPhysics(dt, 10, 0.008)

    def setup(self):
        self.worldNP = render.attachNewNode('World')
        # World
        self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
        # self.debugNP.show()
        # self.debugNP.node().showNormals(True)

        self.world = BulletWorld()
        Track(self.world)
        self.world.setDebugNode(self.debugNP.node())

        # Obstruction
        # self.obstruction = Obstruction(self)

        # Heightfield (static)
        # self.terrainContainer = Terrain(self, base, render)

    def createPlayers(self):
        # Dynamic - moving bodies
        # Car
        for createPlayerUsername in self.manager.playerList.keys():
            if createPlayerUsername in self.vehiclelist.keys():
                print "Player Already rendered"
            else:
                # print "Creating main other player @ 100"
                vehicleAttributes = self.manager.playerList[createPlayerUsername]
                isCurrentPlayer = False
                if self.login == createPlayerUsername:
                    isCurrentPlayer = True

                pos=[vehicleAttributes.x, vehicleAttributes.y, vehicleAttributes.z,vehicleAttributes.h, vehicleAttributes.p,vehicleAttributes.r]

                playerVehicle = Vehicle(self.world, createPlayerUsername,pos, isCurrentPlayer)#,
                                       # pos=LVecBase3(vehicleAttributes.x, vehicleAttributes.y, vehicleAttributes.z),
                                    #    isCurrentPlayer=isCurrentPlayer, carId=vehicleAttributes.carId)
                if isCurrentPlayer:
                    self.vehicleContainer = playerVehicle
                    print "I AM: ", createPlayerUsername
                    # this will be set by the server
                    self.howmanyplayers = len(self.manager.playerList)
                    
                    self.rm = RaceMaster(self, self.vehicleContainer, 1, self.howmanyplayers, 0)
                    self.rm.setStartingPos(0)
                    
                
                # print "Creating other players: ", createPlayerUsername, "@ ", vehicleAttributes.x, vehicleAttributes.y, vehicleAttributes.z
                else:
                    print "Creating other players: ", createPlayerUsername, "@ ", vehicleAttributes.x, vehicleAttributes.y, vehicleAttributes.z

                    self.vehiclelist[createPlayerUsername] = playerVehicle


              

    def startConnection(self):
        """Create a connection to the remote host.

        If a connection cannot be created, it will ask the user to perform
        additional retries.

        """
        if self.cManager.connection == None:
            if not self.cManager.startConnection():
                return False

        return True

    def listFromInputState(self, inputState):
        # index 0 == forward
        # index 1 == brake
        # index 2 == right
        # index 3 == left
        result = [0, 0, 0, 0]
        if inputState.isSet('forward'):
            result[0] = 1
        if inputState.isSet('brake'):
            result[1] = 1
        if inputState.isSet('right'):
            result[2] = 1
        if inputState.isSet('left'):
            result[3] = 1

        return result

# w = WorldManager()
# run()
