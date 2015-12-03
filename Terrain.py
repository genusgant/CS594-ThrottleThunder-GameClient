from panda3d.core import loadPrcFileData
# Configure the parallax mapping settings (these are just the defaults)
loadPrcFileData("", "parallax-mapping-samples 30")
loadPrcFileData("", "parallax-mapping-scale 0.1")

from panda3d.core import BitMask32
from panda3d.core import Filename
from panda3d.core import PNMImage
from panda3d.core import GeoMipTerrain
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletHeightfieldShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import ZUp
from panda3d.core import TextureStage, Texture
from panda3d.core import NodePath
from panda3d.core import LVecBase3f
from panda3d.bullet import BulletPlaneShape
from panda3d.core import Vec3
from UniverseBackground import UniverseBackground

class Terrain(object):
    def __init__(self, main, base, render, type = "heightMap"):
        if type == "heightMap":
            self.terrainFromHeightMap(main)
        elif type == "model":
            self.terrainFromModel(main)

        # Plane
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        universeNode = BulletRigidBodyNode('UniverseNode')
        universeNode.notifyCollisions(True)
        universeNode.addShape(shape)
        np = self.parentNodePath.attachNewNode(universeNode)
        np.setPos(0, 0, -150)
        np.hide()
        main.world.attachRigidBody(universeNode)

        self.parentNodePath.reparentTo(main.worldNP)
        self.hf = self.rigidNodePath.node() # To enable/disable debug visualisation
        # Sky Dome
        universeBackground = UniverseBackground()

    def terrainFromModel(self, main):
        self.parentNodePath = NodePath("FloorNodePath")
        self.parentNodePath.setPos(0, 0, -1)
        self.parentNodePath.setScale(2.0, 2.0, 1.0)
        # self.parentNodePath.setP(90)

        self.loadModelAndTexture()
        self.setupCollisionMeshAndRigidNodeFromModel()

        main.world.attachRigidBody(self.rigidNodePath.node())

    def loadModelAndTexture(self, path={"model": "models/map", "texture": "models/tex/floor.jpg"}):
        self.floorModel = loader.loadModel(path["model"])
        # floor_tex = loader.loadTexture(path["texture"])
        # self.floorModel.setTexture(floor_tex)
        self.parentNodePath.attachNewNode(self.floorModel.node())

    def setupCollisionMeshAndRigidNodeFromModel(self):
        mesh = BulletTriangleMesh()
        for geomNP in self.floorModel.findAllMatches('**/+GeomNode'):
            geomNode = geomNP.node()
            ts = geomNP.getTransform(self.floorModel)
            for geom in geomNode.getGeoms():
                mesh.addGeom(geom, ts)

        shape = BulletTriangleMeshShape(mesh, dynamic=False)
        self.rigidNode = BulletRigidBodyNode('Floor')
        self.rigidNode.notifyCollisions(False)

        self.rigidNodePath = self.parentNodePath.attachNewNode(self.rigidNode)
        self.rigidNodePath.node().addShape(shape)
        self.rigidNodePath.setScale(12, 12, 1.5)
        self.rigidNodePath.setCollideMask(BitMask32.allOn())
        self.rigidNodePath.node().notifyCollisions(False)

    def toggleHeightfield(self):
        self.hf.setDebugEnabled(not self.hf.isDebugEnabled())

    def terrainFromHeightMap(self, main):
        self.parentNodePath = NodePath("FloorNodePath")
        self.parentNodePath.setPos(0, 0, -2)
        self.parentNodePath.setScale(5, 5, 0.75)
        # Heightfield (static)
        height = 8.0

        img = PNMImage(Filename('models/elevation.png'))
        xdim = img.getXSize()
        ydim = img.getYSize()
        shape = BulletHeightfieldShape(img, height, ZUp)
        shape.setUseDiamondSubdivision(True)
        self.rigidNode = BulletRigidBodyNode('Heightfield')
        self.rigidNode.notifyCollisions(False)
        self.rigidNodePath = self.parentNodePath.attachNewNode(self.rigidNode)
        self.rigidNodePath.node().addShape(shape)
        self.rigidNodePath.setPos(0, 0, 0)
        self.rigidNodePath.setCollideMask(BitMask32.allOn())
        self.rigidNodePath.node().notifyCollisions(False)

        main.world.attachRigidBody(self.rigidNodePath.node())

        self.hf = self.rigidNodePath.node() # To enable/disable debug visualisation

        self.terrain = GeoMipTerrain('terrain')
        self.terrain.setHeightfield(img)

        self.terrain.setBlockSize(32)
        self.terrain.setNear(50)
        self.terrain.setFar(100)
        self.terrain.setFocalPoint(base.camera)

        rootNP = self.terrain.getRoot()
        rootNP.reparentTo(self.parentNodePath)
        rootNP.setSz(8.0)

        offset = img.getXSize() / 2.0 - 0.5
        rootNP.setPos(-offset, -offset, -height / 2.0)

        self.terrain.generate()

        # Apply texture
        diffuseTexture = loader.loadTexture(Filename('models/diffuseMap.jpg'))
        diffuseTexture.setWrapU(Texture.WMRepeat)
        diffuseTexture.setWrapV(Texture.WMRepeat)
        rootNP.setTexture(diffuseTexture)

        # Normal map
        texStage = TextureStage('texStageNormal')
        texStage.setMode(TextureStage.MNormal)
        normalTexture = loader.loadTexture(Filename('models/normalMap.jpg'))
        rootNP.setTexture(texStage, normalTexture)

        # Glow map
        texStage = TextureStage('texStageNormal')
        texStage.setMode(TextureStage.MGlow)
        glowTexture = loader.loadTexture(Filename('models/glowMap.jpg'))
        rootNP.setTexture(texStage, glowTexture)
