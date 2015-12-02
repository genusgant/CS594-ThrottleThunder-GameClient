import direct.directbase.DirectStart
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import LVecBase3
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import Filename

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletVehicle
from panda3d.bullet import ZUp
import time
from direct.particles.ParticleEffect import ParticleEffect
from common.Constants import Constants

import math

def getDimensions(nPath):
    pt1, pt2 = nPath.getTightBounds()
    xDim = pt2.getX() - pt1.getX()
    yDim = pt2.getY() - pt1.getY()
    zDim = pt2.getZ() - pt1.getZ()
    return [xDim,yDim,zDim]

class VehicleProps():
    def __init__(self, type):
        self.constants = Constants()
        self.velocity = 0
        self.type = type
        self.armor = 0
        self.boost = 1

        if type == 2:
            self.weight = self.health = self.maxHealth = 400
            self.maxArmor = 300
        elif type == 1:
            self.weight = self.health = self.maxHealth = 200
            self.maxArmor = 200
        else:
            self.weight = self.health = self.maxHealth = 100
            self.maxArmor = 100

    def setVelocity(self, velocity):
        self.velocity = velocity

    def getHealthStatus(self):
        additionalHealth = 0
        health = (self.health/self.weight) * 100
        if health > 100:
            additionalHealth = health - 100

        result = {
            "health": health,
            "additionalHealth": additionalHealth
        }

        return result

    def setHealthStatus(self, health):
        self.health += health
        if self.health > self.props. self.constants.MAX_HEALTH[self.type]:
            self.armor = self.health - self.props. self.constants.MAX_HEALTH[self.type]
            self.health = self.props. self.constants.MAX_HEALTH[self.type]

class Vehicle(object):
    COUNT = 0

    def __init__(self, main, username, pos = LVecBase3(-5, -5, 1), isCurrentPlayer = False, carId=1):
        self.username = username
        self.isCurrentPlayer = isCurrentPlayer
        self.boostCount = 0
        self.boostActive = False
        self.boostStep = 2
        self.boostDuration = 0
        self.startTime = self.boostStartTime = time.time()
        self.pos = pos
        self.boostFactor = 1.2
        self.specs = {"mass": 800.0,
                    "maxWheelForce": 2000.0,
                    "brakeForce": 100.0,
                    "steeringLock": 45.0,
                    "maxSpeed": 33.0,
                    "maxReverseSpeed": 10.0}
        self.vehicleControlState = {"throttle": 0, "reverse": False, "brake": 0.0, "steering": 0.0, "health": 1}

        # Steering change per second, normalised to steering lock
        # Eg. 45 degrees lock and 1.0 rate means 45 degrees per second
        self.steeringRate = 0.8
        self.centreingRate = 1.2
        self.speed = 0

        self.setupVehicle(main)

        self.props = VehicleProps(type)

        self.currentPowerups = {"powerup1": None, "powerup2": None, "powerup3": None}
        # if isCurrentPlayer:
        #     #This command is required for Panda to render particles
        #     base.enableParticles()
        #     self.p = ParticleEffect()
        #     self.loadParticleConfig('steam.ptf')

    def loadParticleConfig(self, file):
        #Start of the code from steam.ptf
        self.p.cleanup()
        self.p = ParticleEffect()
        self.p.loadConfig(Filename(file))
        # print type(main.worldNp)
        self.p.softStart()
        self.p.start(self.yugoNP)
        # self.p.setPos(0.000, -0.700, 0.250)
        self.p.setPos(0.000, -0.700, 0)

        #self.setupVehicle(bulletWorld)
        self.startTime = time.time()
        #COUNT = 1

    def move(self, steering, wheelForce, brakeForce, x, y, z, h, p, r):
        self.applyForcesAndSteering(steering, wheelForce, brakeForce)
        self.endTime = time.time()
        #print self.endTime
        elapsed = self.endTime - self.startTime
        #self.startTime = self.endTime
        #if elapsed > 1:
        self.startTime = self.endTime
        if not self.isCurrentPlayer:
            self.setVehiclePos(x, y, z, h, p, r)

        #print "Do Move"

    def applyForcesAndSteering(self, steering, wheelForce, brakeForce):
        # Apply steering to front wheels
        self.vehicle.setSteeringValue(steering, 0);
        self.vehicle.setSteeringValue(steering, 1);
        # Apply engine and brake to rear wheels
        self.vehicle.applyEngineForce(wheelForce, 2);
        self.vehicle.applyEngineForce(wheelForce, 3);
        self.vehicle.setBrake(brakeForce, 2);
        self.vehicle.setBrake(brakeForce, 3);
    def addBoost(self):
        if self.boostCount > 0:
            self.boostCount -= 1
            if not self.boostActive:
                self.boostStartTime = time.time()
                self.boostActive = True
            self.boostDuration += self.boostStep
    def checkDisableBoost(self):
        if time.time() - self.boostStartTime > self.boostDuration:
            self.boostActive = False

    def reset(self):
        self.chassisNP.setP(0)
        self.chassisNP.setR(0)

    def processInput(self, inputState, dt):
        # print self.chassisNP.getPos()
        #print self.chassisNP.getH()
        """Use controls to update the player's car"""
        # For keyboard throttle and brake are either 0 or 1
        self.checkDisableBoost()
        if inputState.isSet('forward'):
            self.vehicleControlState["throttle"] = 1.0
        else:
            self.vehicleControlState["throttle"] = 0.0

        velocity = self.chassisNode.getLinearVelocity()
        speed = math.sqrt(sum(v ** 2 for v in velocity))
        self.speed = speed
        # Update braking and reversing
        if inputState.isSet('brake'):
            if speed < 0.5 or self.vehicleControlState["reverse"]:
                # If we're stopped, then start reversing
                # Also keep reversing if we already were
                self.vehicleControlState["reverse"] = True
                self.vehicleControlState["throttle"] = 1.0
                self.vehicleControlState["brake"] = 0.0
            else:
                self.vehicleControlState["reverse"] = False
                self.vehicleControlState["brake"] = 1.0
        else:
            self.vehicleControlState["reverse"] = False
            self.vehicleControlState["brake"] = 0.0

        # steering is normalised from -1 to 1, corresponding
        # to the steering lock right and left
        steering = self.vehicleControlState["steering"]
        if inputState.isSet('left'):
            steering += dt * self.steeringRate
            steering = min(steering, 1.0)
        elif inputState.isSet('right'):
            steering -= dt * self.steeringRate
            steering = max(steering, -1.0)
        else:
            # gradually re-center the steering
            if steering > 0.0:
                steering -= dt * self.centreingRate
                if steering < 0.0:
                    steering = 0.0
            elif steering < 0.0:
                steering += dt * self.centreingRate
                if steering > 0.0:
                    steering = 0.0
        self.vehicleControlState["steering"] = steering

        # """Updates acceleration, braking and steering
        # These are all passed in through a controlState dictionary
        # """
        # Update acceleration and braking
        self.reversing = self.vehicleControlState["reverse"]
        brakeForce = self.vehicleControlState["brake"] * self.specs["brakeForce"]

        if self.reversing and self.speed > self.specs["maxReverseSpeed"]:
            self.applyForcesAndSteering(steering, 0, brakeForce)
            return
        if not self.reversing and self.speed > self.specs["maxSpeed"]:
            self.applyForcesAndSteering(steering, 0, brakeForce)
            return

        wheelForce = self.vehicleControlState["throttle"] * self.specs["maxWheelForce"]

        if self.reversing:
            # Make reversing a bit slower than moving forward
            wheelForce *= -0.5

        # Update steering
        # Steering control state is from -1 to 1
        steering = self.vehicleControlState["steering"] * self.specs["steeringLock"]
        if self.boostActive:
            wheelForce *= self.boostFactor
        self.applyForcesAndSteering(steering, wheelForce, brakeForce)
        return [steering, wheelForce, brakeForce]

    def getSpeed(self):
        velocity = self.chassisNode.getLinearVelocity()
        speed = math.sqrt(sum(v ** 2 for v in velocity))
        return speed, speed/self.specs["maxSpeed"]

    def updateHealth(self, damage):
        self.vehicleControlState["health"] -= 0.25
        if self.vehicleControlState["health"] < 0.0:
            self.killVehicle("Lost health")

    def killVehicle(self, resaon = ""):
        print "Sent request to server for killing this player because: ", resaon

    def updateMovement(self, move, dt):
        """Use controls to update the player's car"""
        # For keyboard throttle and brake are either 0 or 1
        if move == 'f':
            self.vehicleControlState["throttle"] = 1.0
        else:
            self.vehicleControlState["throttle"] = 0.0

        velocity = self.chassisNode.getLinearVelocity()
        speed = math.sqrt(sum(v ** 2 for v in velocity))
        # Update braking and reversing
        if move == 'b':
            if speed < 0.5 or self.vehicleControlState["reverse"]:
                # If we're stopped, then start reversing
                # Also keep reversing if we already were
                self.vehicleControlState["reverse"] = True
                self.vehicleControlState["throttle"] = 1.0
                self.vehicleControlState["brake"] = 0.0
            else:
                self.vehicleControlState["reverse"] = False
                self.vehicleControlState["brake"] = 1.0
        else:
            self.vehicleControlState["reverse"] = False
            self.vehicleControlState["brake"] = 0.0

        # steering is normalised from -1 to 1, corresponding
        # to the steering lock right and left
        steering = self.vehicleControlState["steering"]
        if move == 'l':
            steering += dt * self.steeringRate
            steering = min(steering, 1.0)
        elif move == 'r':
            steering -= dt * self.steeringRate
            steering = max(steering, -1.0)
        else:
            # gradually re-center the steering
            if steering > 0.0:
                steering -= dt * self.centreingRate
                if steering < 0.0:
                    steering = 0.0
            elif steering < 0.0:
                steering += dt * self.centreingRate
                if steering > 0.0:
                    steering = 0.0
        self.vehicleControlState["steering"] = steering

        # """Updates acceleration, braking and steering
        # These are all passed in through a controlState dictionary
        # """
        # Update acceleration and braking
        wheelForce = self.vehicleControlState["throttle"] * self.specs["maxWheelForce"]
        self.reversing = self.vehicleControlState["reverse"]
        if self.reversing:
            # Make reversing a bit slower than moving forward
            wheelForce *= -0.5

        brakeForce = self.vehicleControlState["brake"] * self.specs["brakeForce"]

        # Update steering
        # Steering control state is from -1 to 1
        steering = self.vehicleControlState["steering"] * self.specs["steeringLock"]

        self.applyForcesAndSteering(steering, wheelForce, brakeForce)

        return [steering, wheelForce, brakeForce]

    def setVehiclePos(self, x,y, z, h, p, r):
        #self.chassisNP.setX(x)
        #self.chassisNP.setY(y)
        #self.chassisNP.setP(p)
        #self.chassisNP.setR(r)
        self.chassisNP.setPosHpr(x, y, z, h, p, r)
        return

    def setupVehicle(self, main):
        # Chassis
        shape = BulletBoxShape(Vec3(0.6, 1.4, 0.5))
        ts = TransformState.makePos(Point3(0, 0, 0.5))
        name = "vehicle"
        if self.isCurrentPlayer:
            name = self.username
        self.chassisNode = BulletRigidBodyNode(name)
        self.chassisNode.setTag('username', str(name))
        self.chassisNP = main.worldNP.attachNewNode(self.chassisNode)
        self.chassisNP.setName(str(name))
        self.chassisNP.node().addShape(shape, ts)
        self.chassisNP.setScale(.5,.5,.5)

        self.chassisNP.setPos(self.pos)
        if self.isCurrentPlayer:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(800.0)
        else:
            self.chassisNP.node().notifyCollisions(False)
            self.chassisNP.node().setMass(400.0)
        self.chassisNP.node().setDeactivationEnabled(False)

        main.world.attachRigidBody(self.chassisNP.node())

        #np.node().setCcdSweptSphereRadius(1.0)
        #np.node().setCcdMotionThreshold(1e-7)

        # Vehicle
        self.vehicle = BulletVehicle(main.world, self.chassisNP.node())
        self.vehicle.setCoordinateSystem(ZUp)
        main.world.attachVehicle(self.vehicle)

        self.yugoNP = loader.loadModel('models/yugo/yugo.egg')
        self.yugoNP.reparentTo(self.chassisNP)

        #self.carNP = loader.loadModel('models/batmobile-chassis.egg')
        #self.yugoNP.setScale(.7)
        #self.carNP.reparentTo(self.chassisNP)

        # Right front wheel
        np = loader.loadModel('models/yugo/yugotireR.egg')
        np.reparentTo(main.worldNP)
        self.addWheel(Point3( 0.70,  1.05, 0.3), True, np)

        # Left front wheel
        np = loader.loadModel('models/yugo/yugotireL.egg')
        np.reparentTo(main.worldNP)
        self.addWheel(Point3(-0.70,  1.05, 0.3), True, np)

        # Right rear wheel
        np = loader.loadModel('models/yugo/yugotireR.egg')
        np.reparentTo(main.worldNP)
        self.addWheel(Point3( 0.70, -1.05, 0.3), False, np)

        # Left rear wheel
        np = loader.loadModel('models/yugo/yugotireL.egg')
        np.reparentTo(main.worldNP)
        self.addWheel(Point3(-0.70, -1.05, 0.3), False, np)

    def addWheel(self, pos, front, np):
        wheel = self.vehicle.createWheel()

        wheel.setNode(np.node())
        wheel.setChassisConnectionPointCs(pos)
        wheel.setFrontWheel(front)

        wheel.setWheelDirectionCs(Vec3(0, 0, -1))
        wheel.setWheelAxleCs(Vec3(1, 0, 0))
        wheel.setWheelRadius(0.25)
        wheel.setMaxSuspensionTravelCm(40.0)

        wheel.setSuspensionStiffness(40.0)
        wheel.setWheelsDampingRelaxation(2.3)
        wheel.setWheelsDampingCompression(4.4)
        wheel.setFrictionSlip(100.0);
        wheel.setRollInfluence(0.1)


    def reset(self):
        #self.chassisNP.setP(0)
        #self.chassisNP.setR(0)
        print "kegwe", self.chassisNP.getX(),self.chassisNP.getY(),self.chassisNP.getZ(),self.chassisNP.getH(),0,0
        self.chassisNP.setPosHpr(self.chassisNP.getX(),self.chassisNP.getY(),self.chassisNP.getZ(),self.chassisNP.getH(),0,0)


    def pickedPowerup(self, powerup):
        if not powerup.pickable:
            powerup.useAbility()
        else:
            if self.currentPowerups["powerup1"] is None:
                self.currentPowerups["powerup1"] = powerup
            elif self.currentPowerups["powerup2"] is None:
                self.currentPowerups["powerup2"] = powerup
            elif self.currentPowerups["powerup3"] is None:
                self.currentPowerups["powerup3"] = powerup


    def canPickUpPowerup(self):
        return (self.currentPowerups["powerup1"] is None or
                self.currentPowerups["powerup2"] is None or
                self.currentPowerups["powerup3"] is None)


    def usePowerup(self, powerupIndex):
        # Move usePowerupN to this function
        if powerupIndex == 0 and self.currentPowerups["powerup1"] is not None:
            self.currentPowerups["powerup1"].useAbility()
            self.currentPowerups["powerup1"] = None
        elif powerupIndex == 1 and self.currentPowerups["powerup2"] is not None:
            self.currentPowerups["powerup2"].useAbility()
            self.currentPowerups["powerup2"] = None
        elif powerupIndex == 2 and self.currentPowerups["powerup3"] is not None:
            self.currentPowerups["powerup3"].useAbility()
            self.currentPowerups["powerup3"] = None
