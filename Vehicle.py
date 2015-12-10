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
from Audio import Audio

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
        self.isInvincible = False
        self.type = str(type)
        self.armor = 0
        self.boost = 1
        #print "VehicleProps for Type: ", self.type
        #print "VEHICLE_HEALTH", self.constants.VEHICLE_HEALTH
        self.weight = self.health = self.constants.VEHICLE_HEALTH[self.type]

    def setVelocity(self, velocity):
        self.velocity = velocity

    def getHealthStatus(self):
        additionalHealth = 0
        if self.health > self.constants.VEHICLE_HEALTH[self.type]:
            additionalHealth = self.health - self.constants.VEHICLE_HEALTH[self.type]
        health = self.health - additionalHealth
        #if additionalHealth >0:
            #print health, additionalHealth
        result = {
            "health": health,
            "additionalHealth": additionalHealth
        }
        return result

    def getArmorStatus(self):
        return self.armor

    def getBarDetails(self):
        #print "getBarDetails"
        healthRange = self.constants.VEHICLE_HEALTH[self.type]
        maxHealthRange = self.constants.MAX_HEALTH[self.type]
        armorRange = self.constants.MAX_ARMOR[self.type]

        result = {
            "health": healthRange,
            "additionalHealth": maxHealthRange - healthRange,
            "armor": armorRange
        }
        return result


    def getHitPoint(self):
        hitPoint = self.health + self.armor
        return hitPoint

    def setDamage(self, damage):
        if not self.isInvincible:
            self.armor -= damage
            if self.armor < 0:
                self.health += self.armor
                self.armor = 0

        if self.health < 0:
            return False
        else:
            return True

    def setHealth(self, health):
        self.health = health
        if self.health > self.constants.MAX_HEALTH[self.type]:
            self.armor = self.health - self.constants.MAX_HEALTH[self.type]
            self.health = self.constants.MAX_HEALTH[self.type]

    def setHealthStatus(self, health):
        self.health += health
        if self.health > self.constants.MAX_HEALTH[self.type]:
            self.armor = self.health - self.props. self.constants.MAX_HEALTH[self.type]
            self.health = self.props. self.constants.MAX_HEALTH[self.type]

class Vehicle(object):
    COUNT = 0

    def __init__(self, main, username, pos = LVecBase3(-5, -5, 1), isCurrentPlayer = False, carId=3):
        self.isDead = False
        self.username = username
        self.main = main
        self.isCurrentPlayer = isCurrentPlayer
        self.boostCount = 0
        self.boostActive = False
        self.boostStep = 2
        self.boostDuration = 0
        self.moveStartTime = self.startTime = self.boostStartTime = time.time()
        self.Audio = Audio(self)
        self.pos = pos
        self.boostFactor = 1.2
        self.props = VehicleProps(carId)
                
        self.specs = {
            "mass": self.props.constants.MAX_WEIGHT[self.props.type],
            "maxWheelForce": self.props.constants.MAX_WHEEL[self.props.type],
            "brakeForce": self.props.constants.MAX_BRAKE[self.props.type],
            "steeringLock": 45,
            "maxSpeed": self.props.constants.MAX_SPEED[self.props.type],
            "maxReverseSpeed": 10.0
        }

        print self.specs["mass"], ": 100"
        print self.specs["maxWheelForce"], ": 3000"
        print self.specs["brakeForce"], ": 100"
        print self.specs["maxSpeed"], "30"

        self.vehicleControlState = {"throttle": 0, "reverse": False, "brake": 0.0, "steering": 0.0, "health": 1}

        self.vehicleType = carId;

        # Steering change per second, normalised to steering lock
        # Eg. 45 degrees lock and 1.0 rate means 45 degrees per second
        self.steeringRate = 0.8
        self.centreingRate = 1.2
        self.speed = 0

        self.setupVehicle(main)        

        self.currentPowerups = {"powerup1": None, "powerup2": None, "powerup3": None}
        if isCurrentPlayer:
            #This command is required for Panda to render particles
            base.enableParticles()
            self.p = ParticleEffect()
        #     self.loadParticleConfig('steam.ptf')

    def setPropHealth(self, health):
        self.props.setHealth(health)
        if not self.isCurrentPlayer:
            self.main.updateStatusBars(self.username, self.props.health)

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
        elapsed = self.endTime - self.moveStartTime
        #self.startTime = self.endTime
        #if elapsed > 1:
        self.moveStartTime = self.endTime
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
            # self.Audio.play_brake()
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

    def getBoost(self):
        maxBoost = 3.0
        currentScaledBoost = self.boostCount / maxBoost
        return currentScaledBoost

    def updateHealth(self, damage):
        self.vehicleControlState["health"] -= 0.25
        if self.vehicleControlState["health"] <= 0.0:
            self.killVehicle("Lost health")

    def killVehicle(self, reason = ""):
        print "Sent request to server for killing this player because: ", reason

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


    def setupVehicleOld(self, main):
        scale = 0.5
        # Chassis
        shape = BulletBoxShape(Vec3(0.6, 1.4, 0.5))
        ts = TransformState.makePos(Point3(0, 0, 0.5 * scale))

        name = self.username
        self.chassisNode = BulletRigidBodyNode(name)
        self.chassisNode.setTag('username', str(name))
        self.chassisNP = main.worldNP.attachNewNode(self.chassisNode)
        self.chassisNP.setName(str(name))
        self.chassisNP.node().addShape(shape, ts)
        self.chassisNP.setScale(scale)

        self.chassisNP.setPos(self.pos)
        if self.isCurrentPlayer:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(800.0)
        else:
            self.chassisNP.node().notifyCollisions(True)
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
        self.rfnp = loader.loadModel('models/yugo/yugotireR.egg')
        self.rfnp.reparentTo(main.worldNP)
        self.addWheel(Point3( 0.70 * scale,  1.05 * scale, 0.3), True, self.rfnp)

        # Left front wheel
        self.lfnp = loader.loadModel('models/yugo/yugotireL.egg')
        self.lfnp.reparentTo(main.worldNP)
        self.addWheel(Point3(-0.70 * scale,  1.05 * scale, 0.3), True, self.lfnp)

        # Right rear wheel
        self.rrnp = loader.loadModel('models/yugo/yugotireR.egg')
        self.rrnp.reparentTo(main.worldNP)
        self.addWheel(Point3( 0.70 * scale, -1.05 * scale, 0.3), False, self.rrnp)

        # Left rear wheel
        self.lrnp = loader.loadModel('models/yugo/yugotireL.egg')
        self.lrnp.reparentTo(main.worldNP)
        self.addWheel(Point3(-0.70 * scale, -1.05 * scale, 0.3), False, self.lrnp)

    # load the vehicle
    def setupVehicle(self, main):
        # Choose the car type here
            #1 Bruiser
            #2 swisftstar
            #3 stallion
            #4 batmobile
            #5 Hovercraft
        if self.vehicleType == 1:
            self.loadBruiser(main)
        if self.vehicleType == 2:
            self.loadSwiftstar(main)
        if self.vehicleType == 3:
            self.loadStallion(main)
            # self.loadDefaultVehicle(main)
        if self.vehicleType == 4:
            # self.loadDefaultVehicle(main)
            self.loadBatMobile(main)


    # instantiating Bruser car type 1
    def loadBruiser(self, main):
        scale = 0.85
        # Chassis
        shape = BulletBoxShape(Vec3(0.95, 1.8, 0.8)) # change the vehicle size here
        ts = TransformState.makePos(Point3(0, -0.1, 0.67))

        name = self.username
        self.chassisNode = BulletRigidBodyNode(name)
        self.chassisNode.setTag('username', str(name))
        self.chassisNP = main.worldNP.attachNewNode(self.chassisNode)
        self.chassisNP.setName(str(name))
        self.chassisNP.node().addShape(shape, ts)
        self.chassisNP.setScale(scale)

        self.chassisNP.setPos(self.pos)
        if self.isCurrentPlayer:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(800.0)
        else:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(400.0)
        self.chassisNP.node().setDeactivationEnabled(False)

        main.world.attachRigidBody(self.chassisNP.node())

        # Vehicle
        self.vehicle = BulletVehicle(main.world, self.chassisNP.node())
        self.vehicle.setCoordinateSystem(ZUp)
        main.world.attachVehicle(self.vehicle)

        self.yugoNP = loader.loadModel('models/bruiser.egg')
        self.yugoNP.reparentTo(self.chassisNP)
        self.yugoNP.setScale(scale)
        # bring the model down to fit the wheel
        self.yugoNP.setZ(self.chassisNP, -0.05)

        xWheelLeft = -1.1
        xWheelRight = 1.1
        yWheelFront = 1.6
        yWheelRear = -1.7
        zWheel = 0.58
        radius = 0.45

        # Right front wheel
        self.rfnp = loader.loadModel('models/bruiser-dd-rt.egg')
        self.rfnp.reparentTo(main.worldNP)
        self.addWheel(Point3( xWheelRight * scale,  yWheelFront * scale, zWheel), True, self.rfnp, radius)

        # Left front wheel
        self.lfnp = loader.loadModel('models/bruiser-dd-lt.egg')
        self.lfnp.reparentTo(main.worldNP)
        self.addWheel(Point3(xWheelLeft * scale,  yWheelFront * scale, zWheel), True, self.lfnp, radius)

        # Right rear wheel
        self.rrnp = loader.loadModel('models/bruiser-dd-rt.egg')
        self.rrnp.reparentTo(main.worldNP)
        self.addWheel(Point3( xWheelRight * scale, yWheelRear * scale, zWheel), False, self.rrnp, radius)

        # Left rear wheel
        self.lrnp = loader.loadModel('models/bruiser-dd-lt.egg')
        self.lrnp.reparentTo(main.worldNP)
        self.addWheel(Point3(xWheelLeft * scale, yWheelRear * scale, zWheel), False, self.lrnp, radius)

    # instantiating Swisftstar car type 2
    def loadSwiftstar(self, main):
        scale = 0.65
        # Chassis
        shape = BulletBoxShape(Vec3(0.95, 2.4, 0.82)) # change the vehicle size here
        ts = TransformState.makePos(Point3(0, 0, 0.35)) #

        name = self.username
        self.chassisNode = BulletRigidBodyNode(name)
        self.chassisNode.setTag('username', str(name))
        self.chassisNP = main.worldNP.attachNewNode(self.chassisNode)
        self.chassisNP.setName(str(name))
        self.chassisNP.node().addShape(shape, ts)
        self.chassisNP.setScale(scale)

        self.chassisNP.setPos(self.pos)
        if self.isCurrentPlayer:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(800.0)
        else:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(400.0)
        self.chassisNP.node().setDeactivationEnabled(False)

        main.world.attachRigidBody(self.chassisNP.node())

        # Vehicle
        self.vehicle = BulletVehicle(main.world, self.chassisNP.node())
        self.vehicle.setCoordinateSystem(ZUp)
        main.world.attachVehicle(self.vehicle)

        self.yugoNP = loader.loadModel('models/swiftstar-chassis.egg')
        self.yugoNP.reparentTo(self.chassisNP)
        self.yugoNP.setScale(scale)
        self.yugoNP.setZ(self.chassisNP, -0.30)

        xWheelLeft = -1.01
        xWheelRight = 1.01
        yWheelFront = 1.55
        yWheelRear = -1.55
        zWheel = 0.48
        radious = 0.45

        # Right front wheel
        self.rfnp = loader.loadModel('models/swiftstar-fr-tire.egg')
        self.rfnp.reparentTo(main.worldNP)
        self.addWheel(Point3( xWheelRight * scale,  yWheelFront * scale, zWheel), True, self.rfnp, radious)

        # Left front wheel
        self.lfnp = loader.loadModel('models/swiftstar-fl-tire.egg')
        self.lfnp.reparentTo(main.worldNP)
        self.addWheel(Point3(xWheelLeft * scale,  yWheelFront * scale, zWheel), True, self.lfnp, radious)

        # Right rear wheel
        self.rrnp = loader.loadModel('models/swiftstar-rr-tire.egg')
        self.rrnp.reparentTo(main.worldNP)
        self.addWheel(Point3( xWheelRight * scale, yWheelRear * scale, zWheel), False, self.rrnp, radious)

        # Left rear wheel
        self.lrnp = loader.loadModel('models/swiftstar-rl-tire.egg')
        self.lrnp.reparentTo(main.worldNP)
        self.addWheel(Point3(xWheelLeft * scale, yWheelRear * scale, zWheel), False, self.lrnp, radious)


    # instantiating Stallion car type 3
    def loadStallion(self, main):
        scale = 1
        # Chassis

        shape = BulletBoxShape(Vec3(.98 * scale, 2.2 * scale, 0.71 * scale)) # change the vehicle size here
        ts = TransformState.makePos(Point3(0  * scale, -0.22  * scale, 0.35  * scale)) #

        name = self.username
        self.chassisNode = BulletRigidBodyNode(name)
        self.chassisNode.setTag('username', str(name))
        self.chassisNP = main.worldNP.attachNewNode(self.chassisNode)
        self.chassisNP.setName(str(name))
        self.chassisNP.node().addShape(shape, ts)
        self.chassisNP.setScale(scale)

        self.chassisNP.setPos(self.pos)
        if self.isCurrentPlayer:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(800.0)
        else:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(400.0)
        self.chassisNP.node().setDeactivationEnabled(False)

        main.world.attachRigidBody(self.chassisNP.node())

        # Vehicle
        self.vehicle = BulletVehicle(main.world, self.chassisNP.node())
        self.vehicle.setCoordinateSystem(ZUp)
        main.world.attachVehicle(self.vehicle)

        self.yugoNP = loader.loadModel('models/stallion.egg')
        self.yugoNP.reparentTo(self.chassisNP)
        self.yugoNP.setZ(self.chassisNP, -0.45)

        xWheelLeft = -0.9
        xWheelRight = 0.9
        yWheelFront = 1.55
        yWheelRear = -1.45
        zWheel = 0.25
        radius = 0.45

        # Right front wheel
        self.rfnp = loader.loadModel('models/stallion-right-tire.egg')
        self.rfnp.reparentTo(main.worldNP)
        self.addWheel(Point3( xWheelRight * scale,  yWheelFront * scale, zWheel), True, self.rfnp, radius)

        # Left front wheel
        self.lfnp = loader.loadModel('models/stallion-left-tire.egg')
        self.lfnp.reparentTo(main.worldNP)
        self.addWheel(Point3(xWheelLeft * scale,  yWheelFront * scale, zWheel), True, self.lfnp, radius)

        # Right rear wheel
        self.rrnp = loader.loadModel('models/stallion-right-tire.egg')
        self.rrnp.reparentTo(main.worldNP)
        self.addWheel(Point3( xWheelRight * scale, yWheelRear * scale, zWheel), False, self.rrnp, radius)

        # Left rear wheel
        self.lrnp = loader.loadModel('models/stallion-left-tire.egg')
        self.lrnp.reparentTo(main.worldNP)
        self.addWheel(Point3(xWheelLeft * scale, yWheelRear * scale, zWheel), False, self.lrnp, radius)

    # instantiating Mystery car type 4
    def loadBatMobile(self, main):
        scale = 0.73
        # Chassis

        shape = BulletBoxShape(Vec3(.98, 1.85, 0.71)) # change the vehicle size here
        ts = TransformState.makePos(Point3(0, -0.22, 0.35)) #

        name = self.username
        self.chassisNode = BulletRigidBodyNode(name)
        self.chassisNode.setTag('username', str(name))
        self.chassisNP = main.worldNP.attachNewNode(self.chassisNode)
        self.chassisNP.setName(str(name))
        self.chassisNP.node().addShape(shape, ts)
        self.chassisNP.setScale(scale)

        self.chassisNP.setPos(self.pos)
        if self.isCurrentPlayer:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(800.0)
        else:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(400.0)
        self.chassisNP.node().setDeactivationEnabled(False)

        main.world.attachRigidBody(self.chassisNP.node())

        # Vehicle
        self.vehicle = BulletVehicle(main.world, self.chassisNP.node())
        self.vehicle.setCoordinateSystem(ZUp)
        main.world.attachVehicle(self.vehicle)


        self.yugoNP = loader.loadModel('models/batmobile-chassis.egg')
        self.yugoNP.reparentTo(self.chassisNP)
        self.yugoNP.setScale(scale)
        self.yugoNP.setZ(self.chassisNP, -0.25)

        xWheelLeft = -0.8
        xWheelRight = 0.8
        yWheelFront = 1.25
        yWheelRear = -1.7
        zWheel = 0.25
        radious = 0.45
        # radious = 0.75

        # Right front wheel
        self.rfnp = loader.loadModel('models/batmobile-wheel-right.egg')
        self.rfnp.reparentTo(main.worldNP)
        self.addWheel(Point3( xWheelRight * scale,  yWheelFront * scale, zWheel), True, self.rfnp, radious)

        # Left front wheel
        self.lfnp = loader.loadModel('models/batmobile-wheel-left.egg')
        self.lfnp.reparentTo(main.worldNP)
        self.addWheel(Point3(xWheelLeft * scale,  yWheelFront * scale, zWheel), True, self.lfnp, radious)

        # Right rear wheel
        self.rrnp = loader.loadModel('models/batmobile-wheel-right.egg')
        self.rrnp.reparentTo(main.worldNP)
        self.rrnp.setScale(.25)
        self.addWheel(Point3( xWheelRight * scale, yWheelRear * scale, zWheel), False, self.rrnp, radious)

        # Left rear wheel
        self.lrnp = loader.loadModel('models/batmobile-wheel-left.egg')
        self.lrnp.reparentTo(main.worldNP)
        self.lrnp.setScale(.25)
        self.addWheel(Point3(xWheelLeft * scale, yWheelRear * scale, zWheel), False, self.lrnp, radious)


    # instantiating Default car type, Not being used for now. Only used for Testing
    def loadDefaultVehicle(self, main):
        scale = 0.5
        # Chassis

        shape = BulletBoxShape(Vec3(0.6, 1.4, 0.5)) # change the vehicle size here
        ts = TransformState.makePos(Point3(0, 0, 0.5 * scale)) #

        name = self.username
        self.chassisNode = BulletRigidBodyNode(name)
        self.chassisNode.setTag('username', str(name))
        self.chassisNP = main.worldNP.attachNewNode(self.chassisNode)
        self.chassisNP.setName(str(name))
        self.chassisNP.node().addShape(shape, ts)
        self.chassisNP.setScale(scale)

        self.chassisNP.setPos(self.pos)
        if self.isCurrentPlayer:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(800.0)
        else:
            self.chassisNP.node().notifyCollisions(True)
            self.chassisNP.node().setMass(400.0)
        self.chassisNP.node().setDeactivationEnabled(False)

        main.world.attachRigidBody(self.chassisNP.node())

        # Vehicle
        self.vehicle = BulletVehicle(main.world, self.chassisNP.node())
        self.vehicle.setCoordinateSystem(ZUp)
        main.world.attachVehicle(self.vehicle)

        radius = 0.25
        scale = .5

        self.yugoNP = loader.loadModel('models/yugo/yugo.egg')
        self.yugoNP.reparentTo(self.chassisNP)

        # Right front wheel
        self.rfnp = loader.loadModel('models/yugo/yugotireR.egg')
        self.rfnp.reparentTo(main.worldNP)
        self.addWheel(Point3( 0.70 * scale,  1.05 * scale, 0.3), True, self.rfnp, radius)

        # Left front wheel
        self.lfnp = loader.loadModel('models/yugo/yugotireL.egg')
        self.lfnp.reparentTo(main.worldNP)
        self.addWheel(Point3(-0.70 * scale,  1.05 * scale, 0.3), True, self.lfnp, radius)

        # Right rear wheel
        self.rrnp = loader.loadModel('models/yugo/yugotireR.egg')
        self.rrnp.reparentTo(main.worldNP)
        self.addWheel(Point3( 0.70 * scale, -1.05 * scale, 0.3), False, self.rrnp, radius)

        # Left rear wheel
        self.lrnp = loader.loadModel('models/yugo/yugotireL.egg')
        self.lrnp.reparentTo(main.worldNP)
        self.addWheel(Point3(-0.70 * scale, -1.05 * scale, 0.3), False, self.lrnp, radius)


    def addWheel(self, pos, front, np, radius):
        wheel = self.vehicle.createWheel()

        wheel.setNode(np.node())
        wheel.setChassisConnectionPointCs(pos)
        wheel.setFrontWheel(front)

        wheel.setWheelDirectionCs(Vec3(0, 0, -1))
        wheel.setWheelAxleCs(Vec3(1, 0, 0))
        wheel.setWheelRadius(radius)
        wheel.setMaxSuspensionTravelCm(40.0)

        wheel.setSuspensionStiffness(40.0)
        wheel.setWheelsDampingRelaxation(2.3)
        wheel.setWheelsDampingCompression(4.4)
        wheel.setFrictionSlip(100.0)
        wheel.setRollInfluence(0.1)


    def reset(self):
        #self.chassisNP.setP(0)
        #self.chassisNP.setR(0)
        #print "kegwe", self.chassisNP.getX(),self.chassisNP.getY(),self.chassisNP.getZ(),self.chassisNP.getH(),0,0
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

            
    def remove(self, main):
        """ Remove the whole vehicle. chassis and 4 wheels. """
        main.world.removeVehicle(self.vehicle)
        self.chassisNP.remove()
        self.lfnp.removeNode()
        self.rfnp.removeNode()
        self.rrnp.removeNode()
        self.lrnp.removeNode()

