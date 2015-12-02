# Roaming-Ralph was modified to remove collision part.

import direct.directbase.DirectStart
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from panda3d.core import Vec3, Vec4, BitMask32, TransformState
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from panda3d.core import Point3, Plane
from panda3d.core import CollisionTraverser, CollisionNode, CollisionSphere
from panda3d.core import CollisionHandlerQueue, CollisionRay, CollisionHandlerPusher, CollisionPlane
from direct.interval.IntervalGlobal import Sequence
from direct.task import Task
from panda3d.bullet import (
    BulletPlaneShape, BulletCylinderShape,
    BulletBoxShape, BulletHeightfieldShape)
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode
from panda3d.bullet import BulletVehicle, BulletSphereShape
from panda3d.bullet import BulletTriangleMeshShape, BulletTriangleMesh
from panda3d.bullet import XUp, YUp, ZUp
import time


class Character:
    playerId = 1
    type = 0

    def __init__(self, tempworld, bulletWorld, type, playerId):
        self.world = tempworld
        self.speed = 0
        self.acceleration = 1.5
        self.brakes = .7
        self.min_speed = 0
        self.max_speed = 150
        self.reverse_speed = 20
        self.reverse_limit = -40
        self.armor = 100
        self.health = 100
        self.a_timer_start = time.time()
        self.a_timer_end = time.time()
        self.power_ups = [0, 0, 0]
        self.playerId = playerId

        if type == 0:
            self.actor = Actor("models/batmobile-chassis")
            self.actor.setScale(0.7)
            carRadius = 3
        elif type == 1:
            self.actor = Actor("models/policecarpainted", {})
            self.actor.setScale(0.30)
            self.actor.setH(180)  # elif type == 2:
        # self.actor = loader.loadModel("knucklehead.egg")
        #     self.tex = loader.loadTexture("knucklehead.jpg")
        #     self.actor.setTexture(self.car_tex, 1)


        shape = BulletBoxShape(Vec3(1.0, 1.5, 0.4))
        ts = TransformState.makePos(Point3(0, 0, 0.6))

        self.chassisNP = render.attachNewNode(BulletRigidBodyNode('Vehicle'))
        self.chassisNP.node().addShape(shape, ts)
        self.chassisNP.setPos(50 * random.random(), 50 * random.random(), 1)
        self.chassisNP.setH(180)
        self.chassisNP.node().setMass(800.0)
        self.chassisNP.node().setDeactivationEnabled(False)

        bulletWorld.attachRigidBody(self.chassisNP.node())

        self.actor.reparentTo(self.chassisNP)
        self.actor.setH(180)

        # Vehicle
        self.vehicle = BulletVehicle(bulletWorld, self.chassisNP.node())
        self.vehicle.setCoordinateSystem(ZUp)
        bulletWorld.attachVehicle(self.vehicle)

        for fb, y in (("F", 1.1), ("B", -1.1)):
            for side, x in (("R", 0.75), ("L", -0.75)):
                np = loader.loadModel("models/tire%s.egg" % side)
                np.reparentTo(render)
                isFront = fb == "F"
                self.addWheel(Point3(x, y, 0.55), isFront, np)

    def addWheel(self, position, isFront, np):
        wheel = self.vehicle.createWheel()

        wheel.setNode(np.node())
        wheel.setChassisConnectionPointCs(position)
        wheel.setFrontWheel(isFront)

        wheel.setWheelDirectionCs(Vec3(0, 0, -1))
        wheel.setWheelAxleCs(Vec3(1, 0, 0))
        wheel.setWheelRadius(0.2)
        wheel.setMaxSuspensionTravelCm(0.4 * 100.0)
        wheel.setSuspensionStiffness(40.0)
        wheel.setWheelsDampingRelaxation(2.3)
        wheel.setWheelsDampingCompression(4.4)
        wheel.setFrictionSlip(100)
        wheel.setRollInfluence(0.1)

    def getActor(self):
        return self.actor

    def get_speed(self):
        return self.speed

    def accelerate(self):
        # check how long you were accelerating
        time_elapsed = time.time() - self.a_timer_end
        if time_elapsed > 1:  # in seconds last accelerated
            self.a_timer_start = time.time()

        if self.speed < self.max_speed:
            self.speed += self.acceleration * (time.time() - self.a_timer_start)
            # print(time_elapsed)
        else:
            self.speed = self.max_speed
        # reset timer
        self.a_timer_end = time.time()

    def friction(self, friction):
        if self.speed > 0:
            self.speed -= friction
        else:
            self.speed = 0

    def brake(self):
        if self.speed > self.min_speed:
            self.speed -= self.brakes
            # reset acceleration timer
            self.a_timer_start = time.time()

    def reverse(self):
        if self.speed > self.reverse_limit:
            self.speed -= self.reverse_speed

    def walk(self):
        self.actor.stop()
        self.actor.pose("walk", 5)
        self.isMoving = False

    def run(self):
        self.actor.loop("run")
        self.isMoving = True
