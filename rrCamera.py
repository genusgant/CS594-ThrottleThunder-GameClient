from panda3d.core import NodePath, PandaNode, LPoint3f

class Camera:
    def __init__(self, vehicle, world):
        self.vehicle = vehicle
        self.world = world
        base.camera.reparentTo(vehicle)
        base.camera.setPos(0, -30, 10)
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)
        self.pos = LPoint3f(0, -30, 6)
        self.cFloater = NodePath(PandaNode("cFloater"))
        self.cFloater.reparentTo(vehicle)
        self.cFloater.setPos(0, -30, 6)
        self.floater.setPos(vehicle.getPos())
        self.floater.setZ(vehicle.getZ() + 2.0)
        base.camera.setPos(self.pos)
        base.camera.setZ(self.floater, self.pos.getZ())
        base.camera.lookAt(self.floater)

    def update(self):
        self.floater.setPos(self.vehicle.getPos())
        self.floater.setZ(self.vehicle.getZ() + 2.0)
        base.camera.setPos(self.pos)
        base.camera.setZ(self.floater, self.pos.getZ())
        base.camera.lookAt(self.floater)
        if self.pos.getY() < -30 or self.pos.getZ() > 6 or self.pos.getY() > -6 or self.pos.getZ() < 1:
            self.pos = LPoint3f(0, -30, 6)
        elif self.rayTest() == 1 and self.pos.getY() < -9 and self.pos.getZ() > 1.5:
            self.pos.setY(self.pos.getY() + 0.2)
            self.pos.setZ(self.pos.getZ() - 0.04)
        elif self.rayTest() == 0 and self.pos.getY() > -30 and self.pos.getZ() < 6:
            self.pos.setY(self.pos.getY() - 0.2)
            self.pos.setZ(self.pos.getZ() + 0.04)

    def rayTest(self):
        frontResult = self.world.rayTestClosest(base.camera.getPos(render), self.floater.getPos())
        rearResult = self.world.rayTestClosest(base.camera.getPos(render), self.cFloater.getPos(render))

        if frontResult.hasHit() and frontResult.getNode().getName() == 'Track':
            return 1
        elif rearResult.hasHit() and rearResult.getNode().getName() == 'Track':
            return -1
        else:
            return 0
