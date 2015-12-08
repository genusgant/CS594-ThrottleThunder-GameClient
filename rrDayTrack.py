from panda3d.core import AmbientLight
from panda3d.core import VBase4
from panda3d.core import BitMask32
from panda3d.core import Filename
from panda3d.core import PNMImage
from panda3d.core import GeoMipTerrain
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletHeightfieldShape, BulletTriangleMesh, BulletTriangleMeshShape, BulletHelper
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import ZUp
from panda3d.bullet import BulletPlaneShape, BulletDebugNode
from panda3d.core import Vec3
from panda3d.core import NodePath
from rrDayDome import SkyDome


class Track(object):
    def __init__(self, bulletWorld):

        self.world = bulletWorld

        self.addCollisionPlane(5)

        self.sky = SkyDome()

        # model used as collision mesh
        collisionModel = loader.loadModel('models/flatTrackCollisionModel')

        mesh = BulletTriangleMesh()
        for geomNP in collisionModel.findAllMatches('**/+GeomNode'):
            geomNode = geomNP.node()
            ts = geomNP.getTransform(collisionModel)
            for geom in geomNode.getGeoms():
                mesh.addGeom(geom, ts)

        shape = BulletTriangleMeshShape(mesh, dynamic=False)

        self.rigidNode = BulletRigidBodyNode('Track')
        self.rigidNode.notifyCollisions(False)
        np = render.attachNewNode(self.rigidNode)
        np.node().addShape(shape)

        np.setScale(.6 * self.sky.SCALE_MOD, .6 * self.sky.SCALE_MOD, 10 * self.sky.SCALE_MOD)
        np.setPos(0, 0, -2.8)
        np.setCollideMask(BitMask32.allOn())
        np.node().notifyCollisions(False)
        bulletWorld.attachRigidBody(np.node())

        self.hf = np.node()  # To enable/disable debug visualisation
        #self.enableDebugging()


    def addCollisionPlane(self, z):
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)

        node = BulletRigidBodyNode('Ground')
        node.addShape(shape)

        np = render.attachNewNode(node)
        np.setPos(0, 0, z)

        self.world.attachRigidBody(node)

    def enableDebugging(self):
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        debugNP = render.attachNewNode(debugNode)
        debugNP.show()

        self.world.setDebugNode(debugNP.node())