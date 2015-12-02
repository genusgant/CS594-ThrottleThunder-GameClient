from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletVehicle
from panda3d.bullet import ZUp

import math

class Obstruction(object):

  def __init__(self, main):
    # Chassis
    shape = BulletBoxShape(Vec3(0.6, 1.4, 0.5))
    ts = TransformState.makePos(Point3(0, 0, 0.5))
    self.chassisNode = BulletRigidBodyNode('Obstruction')
    self.chassisNP = main.worldNP.attachNewNode(self.chassisNode)
    self.chassisNP.setName("Obstruction")
    self.chassisNP.node().addShape(shape, ts)
    self.chassisNP.node().notifyCollisions(True)
    self.chassisNP.setPos(0, 5, 1)
    self.chassisNP.node().setMass(8000.0)
    self.chassisNP.node().setDeactivationEnabled(False)
    main.world.attachRigidBody(self.chassisNP.node())
