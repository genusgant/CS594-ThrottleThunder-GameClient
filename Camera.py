from panda3d.core import NodePath, PandaNode

class Camera:
    def __init__(self, vehicle):
        base.camera.reparentTo(vehicle)
        base.camera.setPos(0, -30, 10)
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

    def update(self, vehicle):
        self.floater.setPos(vehicle.getPos())
        self.floater.setZ(vehicle.getZ() + 2.0)
        base.camera.setPos(0, -30, 8)
        base.camera.setZ(self.floater, 6)
        base.camera.lookAt(self.floater)