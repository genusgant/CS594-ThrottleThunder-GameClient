'''
Created on Nov 21, 2015

@author: saul
'''

from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState


from panda3d.bullet import BulletBoxShape
from panda3d.bullet import ZUp
from panda3d.bullet import BulletGhostNode

from panda3d.core import BitMask32


class Checkpoint(object):
    '''
    checkpoint object to track race posistions
    '''

    count = 0

    def __init__(self, main, pos, h):
        '''
        Constructor
        '''
        self.setupCheckpoint(main, pos, h)
        self.cid = Checkpoint.count
        Checkpoint.count += 1
        
        
    def setupCheckpoint(self, main, pos, h):
            # Chassis
            shape = BulletBoxShape(Vec3(1, 5, 1))
            ts = TransformState.makePos(Point3(0, 0, 0))
            self.cpnode = BulletGhostNode('CheckPoint')
            self.cpnode = render.attachNewNode(self.cpnode)
            self.cpnode.node().addShape(shape, ts)      
            self.cpnode.setCollideMask(BitMask32(0x0f))
#             self.cpnode.node().notifyCollisions(True)
            self.cpnode.setPos(pos.x, pos.y, pos.z)
            self.cpnode.setH(h)

            main.world.attachGhost(self.cpnode.node())
            

         
       
            
           
            
            