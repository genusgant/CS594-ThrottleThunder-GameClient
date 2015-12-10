from panda3d.core import Vec3
from panda3d.core import LVecBase3
from panda3d.core import TransformState
from panda3d.core import BitMask32

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import ZUp
from panda3d.bullet import BulletGhostNode

class PowerUp(object):

  def __init__(self, main, pos =LVecBase3(0, 0, 0) ):
    shape = BulletBoxShape(Vec3(1, 1, 1))
    self.ghost = BulletGhostNode('Ghost')
    ghost.addShape(shape)
    ghostNP = main.worldNP.attachNewNode(ghost)
    ghostNP.setPos(0, 0, 0)
    ghostNP.setCollideMask(BitMask32(0x0f))
    main.world.attachGhost(ghost)
