from panda3d.core import AmbientLight
from panda3d.core import VBase4
from panda3d.core import BitMask32
from panda3d.core import Filename
from panda3d.core import PNMImage
from panda3d.core import GeoMipTerrain
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletHeightfieldShape, BulletTriangleMesh, BulletTriangleMeshShape, BulletHelper
from panda3d.bullet import ZUp
from panda3d.bullet import BulletPlaneShape
from panda3d.core import Vec3
from panda3d.core import NodePath

class Track(object):

  def __init__(self, bulletWorld):

    #model used as collision mesh VOLCANO
    collisionModel = loader.loadModel('models/VolcanoCollision2')

    tex = loader.loadTexture("models/mars_1k_tex.jpg")
    collisionModel.setTexture(tex)

    mesh = BulletTriangleMesh()
    for geomNP in collisionModel.findAllMatches('**/+GeomNode'):
        geomNode = geomNP.node()
        ts = geomNP.getTransform(collisionModel)
        for geom in geomNode.getGeoms():
            mesh.addGeom(geom, ts)

    shape = BulletTriangleMeshShape(mesh, dynamic=False)

    self.rigidNode = BulletRigidBodyNode('Heightfield')
    self.rigidNode.notifyCollisions(False)
    np = render.attachNewNode(self.rigidNode)
    np.node().addShape(shape)

    collisionModel.reparentTo(np)
    np.setScale(7)
    ###Ucomment next line for RAZOR map:
    #np.setHpr(0,90,0)
    np.setPos(0, 0, -2)
    np.setCollideMask(BitMask32.allOn())
    np.node().notifyCollisions(False)
    bulletWorld.attachRigidBody(np.node())

    self.hf = np.node() # To enable/disable debug visualization
