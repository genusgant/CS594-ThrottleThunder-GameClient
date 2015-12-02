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
from panda3d.core import TextureStage
from panda3d.core import Texture
from SkyDome import SkyDome


class Track(object):
    def __init__(self, bulletWorld):

        self.sky = SkyDome()

        # model used as collision mesh
        collisionModel = loader.loadModel('models/walledTrack')
        # model used as display model
        model = loader.loadModel('models/FullTrack')

        tex = loader.loadTexture("models/tex/Main.png")
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MBlend)
        model.setTexture(ts, tex, 2)
        #model.setTexScale(ts, 70)
        # renders track from two camera views
        model.setTwoSided(True)

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

        model.reparentTo(np)
        np.setScale(70)
        np.setPos(0, 0, -5)
        np.setCollideMask(BitMask32(0xf0))
        np.node().notifyCollisions(False)
        bulletWorld.attachRigidBody(np.node())

        self.hf = np.node()  # To enable/disable debug visualisation
