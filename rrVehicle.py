from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import BitMask32
from panda3d.core import TransformState
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletVehicle
from panda3d.bullet import ZUp
import time
import math
from panda3d.core import TransparencyAttrib


class Vehicle(object):
    COUNT = 0

    def __init__(self, world, username, vehicleType, pos=[0, 0, 0, 0, 0, 0], isCurrentPlayer=False):
        self.isDead = False
        self.isCurrentPlayer = isCurrentPlayer
        self.world = world
        self.acceleration = 1.5
        self.brakeForce = 100.0
        self.mass = 800
        self.max_speed = 150
        self.reverse_limit = -40
        self.mass = 800.0  # kg
        self.max_speed = 150  # km
        self.armor = 100
        self.health = 100
        self.friction = 0.2  # slows the car when not accelerating (based on the brakes)
        self.maxWheelForce = 2000.0
        self.maxWheelForce = 2000.0  # acceleration
        self.power_ups = [0, 0, 0]
        self.speed = 0.0
        self.startTime = time.time()

        self.specs = {"mass": self.mass, "maxWheelForce": self.maxWheelForce, "brakeForce": self.brakeForce,
                      "steeringLock": 45.0}
        self.vehicleControlState = {"throttle": 0, "reverse": False, "brake": 0.0, "steering": 0.0}
        self.username = username
        # Steering change per second, normalised to steering lock
        # Eg. 45 degrees lock and 1.0 rate means 45 degrees per second
        self.steeringRate = 0.7
        self.centreingRate = 5.0

        self.pos = pos

        self.type = vehicleType         # Indicate the type of the car 

        self.currentPowerups = {"powerup1": None, "powerup2": None, "powerup3": None}

        self.setupVehicle(world)

        COUNT = 1

    def processInput(self, inputState, dt):
        self.speed = self.vehicle.getCurrentSpeedKmHour()
        # print self.chassisNP.getPos()
        # print self.chassisNP.getH()
        """Use controls to update the player's car"""
        # For keyboard throttle and brake are either 0 or 1
        if inputState.isSet('forward') and self.vehicle.getCurrentSpeedKmHour() <= self.max_speed:
            self.vehicleControlState["throttle"] = 1.0
        else:
            self.vehicleControlState["throttle"] = 0.0

        velocity = self.chassisNode.getLinearVelocity()
        speed = math.sqrt(sum(v ** 2 for v in velocity))
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
        wheelForce = self.vehicleControlState["throttle"] * self.specs["maxWheelForce"]
        self.reversing = self.vehicleControlState["reverse"]
        if self.reversing:
            # Make reversing a bit slower than moving forward
            wheelForce *= -0.5

        brakeForce = self.vehicleControlState["brake"] * self.specs["brakeForce"]

        # slows down vehicle when no key pressed
        if self.vehicleControlState["throttle"] != 1.0 and self.vehicleControlState["reverse"] != 1.0 and \
                        self.vehicleControlState["brake"] != 1.0:
            brakeForce = self.friction * self.specs["brakeForce"]

        # Update steering
        # Steering control state is from -1 to 1
        steering = self.vehicleControlState["steering"] * self.specs["steeringLock"]

        # Apply steering to front wheels
        self.vehicle.setSteeringValue(steering, 0);
        self.vehicle.setSteeringValue(steering, 1);
        # Apply engine and brake to rear wheels
        self.vehicle.applyEngineForce(wheelForce, 2);
        self.vehicle.applyEngineForce(wheelForce, 3);
        self.vehicle.setBrake(brakeForce, 2);
        self.vehicle.setBrake(brakeForce, 3);
        return [steering, wheelForce, brakeForce]

    def setupVehicle(self, world):
        # Chassis
        shape = BulletBoxShape(Vec3(1, 2.2, 0.5))
        ts = TransformState.makePos(Point3(0, 0, .7))
        self.chassisNode = BulletRigidBodyNode('Vehicle')
        self.chassisNP = render.attachNewNode(self.chassisNode)
        # collision bit mesh
        self.chassisNP.setCollideMask(BitMask32(0x80))
        self.chassisNP.node().addShape(shape, ts)
        self.chassisNP.node().notifyCollisions(True)
        self.chassisNP.setPosHpr(self.pos[0], self.pos[1], self.pos[2], self.pos[3], self.pos[4], self.pos[5])
        # self.chassisNP.setPos(-5.34744, 114.773, 6)
        # self.chassisNP.setPos(49.2167, 64.7968, 10)
        self.chassisNP.node().setMass(800.0)
        self.chassisNP.node().setDeactivationEnabled(False)

        world.attachRigidBody(self.chassisNP.node())

        # np.node().setCcdSweptSphereRadius(1.0)
        # np.node().setCcdMotionThreshold(1e-7)

        # Vehicle
        self.vehicle = BulletVehicle(world, self.chassisNP.node())
        self.vehicle.setCoordinateSystem(ZUp)
        world.attachVehicle(self.vehicle)



        # switch the car type : 
         #1 Bruiser
                #2 swisftstar
                #3 stalion 
                #4 batmobile
                #5 Hovercraft
        print "vechile created type: ",self.type
        if self.type == 1:
            self.LoadBruiser()
        elif self.type == 2:
            self.LoadSwiftstar()
        elif self.type == 3:
            self.LoadStalion()
        elif self.type == 4:
            self.LoadBatmobile()
        #elif self.type ==  :
        else:
            self.LoadHoverboard()

        # self.LoadSwiftstar()

    def LoadBatmobile(self):                                                # Load the batmobile! 
        self.carNP = loader.loadModel('models/batmobile-chassis.egg')
        # self.yugoNP.setScale(.7)
        self.carNP.reparentTo(self.chassisNP)

        # Right front wheel
        self.rfnp = loader.loadModel('models/batmobile-wheel-right.egg')
        self.rfnp.reparentTo(self.carNP)
        self.addWheel(Point3(1, 1.1, .7), True, self.rfnp, .7)

        # Left front wheel
        self.lfnp = loader.loadModel('models/batmobile-wheel-left.egg')
        self.lfnp.reparentTo(self.carNP)
        self.addWheel(Point3(-1, 1.1, .7), True, self.lfnp, .7)

        # Right rear wheel
        self.rrnp = loader.loadModel('models/batmobile-wheel-right.egg')
        self.rrnp.reparentTo(self.carNP)
        self.addWheel(Point3(1, -2, .7), False, self.rrnp, .7)

        # Left rear wheel
        self.lrnp = loader.loadModel('models/batmobile-wheel-left.egg')
        self.lrnp.reparentTo(self.carNP)
        self.addWheel(Point3(-1, -2, .7), False, self.lrnp, .7)

    def LoadStalion(self):                       # Load the Stalion ! 
        self.carNP = loader.loadModel('models/stallion.egg')
        self.carNP.setScale(0.9)
        self.carNP.reparentTo(self.chassisNP)

        # Right front wheel
        np = loader.loadModel('models/stallion-right-tire.egg')
        np.reparentTo(self.carNP)
        self.addWheel(Point3(0.85, 1.40, .6), True, np, .6)

        # Left front wheel
        np = loader.loadModel('models/stallion-left-tire.egg')
        np.reparentTo(self.carNP)
        self.addWheel(Point3(-0.85, 1.40, .6), True, np, .6)
        # Right rear wheel
        np = loader.loadModel('models/stallion-right-tire.egg')
        np.reparentTo(self.carNP)
        self.addWheel(Point3(0.85, -1.3, .6), False, np, .6)

        # Left rear wheel
        np = loader.loadModel('models/stallion-left-tire.egg')
        np.reparentTo(self.carNP)
        self.addWheel(Point3(-0.85, -1.3, .6), False, np, .6)

    def LoadBruiser(self):                             # Load the bruiser ! 
        self.carNP = loader.loadModel('models/bruiser.egg')
        self.carNP.reparentTo(self.chassisNP)

        # Right front wheel
        np = loader.loadModel('models/bruiser-right-tire.egg')
        np.reparentTo(self.carNP)
        self.addWheel(Point3(1.2, 1.7, 0.8), True, np, 0.8)

        # Left front wheel
        np = loader.loadModel('models/bruiser-left-tire.egg')
        np.reparentTo(self.carNP)
        self.addWheel(Point3(-1.2, 1.7, 0.8), True, np, 0.8)

        # Right rear wheel
        np = loader.loadModel('models/bruiser-right-tire.egg')
        np.reparentTo(self.carNP)
        self.addWheel(Point3(1.2, -1.95, 0.8), False, np, 0.8)

        # Left rear wheel
        np = loader.loadModel('models/bruiser-left-tire.egg')
        np.reparentTo(self.carNP)
        self.addWheel(Point3(-1.2, -1.95, 0.8), False, np, 0.8)

    def LoadSwiftstar(self):                         # Load the swiftstar ! 
        self.carNP = loader.loadModel('models/swiftstar-chassis.egg')
        self.carNP.setScale(.5)
        self.carNP.reparentTo(self.chassisNP)

        # Right front wheel
        np = loader.loadModel('models/swiftstar-fr-tire.egg')
        np.reparentTo(self.carNP)
        self.addWheel(Point3(.7, 1, 0.65), True, np, 0.65)

        # Left front wheel
        np = loader.loadModel('models/swiftstar-fl-tire.egg')
        np.reparentTo(self.carNP)
        self.addWheel(Point3(-.7, 1, 0.65), True, np, 0.65)

        # Right rear wheel
        np = loader.loadModel('models/swiftstar-rr-tire.egg')
        np.reparentTo(self.carNP)
        self.addWheel(Point3(0.7, -1.4, .8), False, np, 0.9)

        # Left rear wheel
        np = loader.loadModel('models/swiftstar-rl-tire.egg')

        np.reparentTo(self.carNP)
        self.addWheel(Point3(-0.7, -1.4, 0.8), False, np, 0.9)

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
        self.chassisNP.setP(0)
        self.chassisNP.setR(0)

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

    def setVehiclePos(self, x,y, z, h, p, r):
        self.chassisNP.setPosHpr(x, y, z, h, p, r)
        return


    def applyForcesAndSteering(self, steering, wheelForce, brakeForce):
        # Apply steering to front wheels
        self.vehicle.setSteeringValue(steering, 0)
        self.vehicle.setSteeringValue(steering, 1)
        # Apply engine and brake to rear wheels
        self.vehicle.applyEngineForce(wheelForce, 2)
        self.vehicle.applyEngineForce(wheelForce, 3)
        self.vehicle.setBrake(brakeForce, 2)
        self.vehicle.setBrake(brakeForce, 3)


    def remove(self):
        """ Remove the whole vehicle. chassis and 4 wheels. """
        # main.world.removeVehicle(self.vehicle)
        self.chassisNP.remove()
        # self.lfnp.removeNode()
        # self.rfnp.removeNode()
        # self.rrnp.removeNode()
        # self.lrnp.removeNode()