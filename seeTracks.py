# import direct.directbase.DirectStart
import sys
import math
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import PointLight
from panda3d.core import Vec2
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import LVecBase3
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32
from panda3d.core import PandaNode
from panda3d.core import NodePath
from panda3d.core import TextNode
from panda3d.core import CollisionNode
from panda3d.core import NodePath
from panda3d.bullet import BulletWorld, BulletTriangleMesh, BulletTriangleMeshShape, BulletDebugNode, BulletPlaneShape, \
    BulletRigidBodyNode, BulletBoxShape
from Track import Track
from rrVehicle import Vehicle
from rrCamera import Camera
from SkyDome import SkyDome
from Powerups import PowerupManager
from panda3d.bullet import BulletHeightfieldShape
from panda3d.bullet import ZUp
from Terrain import Terrain
from Obstruction import Obstruction
from LoadingScreen import LoadingScreen
from VehicleAttributes import VehicleAttributes
from rrTrack import Track
import rrDayTrack
from rrAudio import Audio
# """ Custom Imports """
# import your modules
from common.Constants import Constants
from net.ConnectionManager import ConnectionManager
from rrDashboard import *
from threading import Thread
from time import sleep
import re
from pandac.PandaModules import loadPrcFileData
from helper.RaceMaster import RaceMaster
from OtherPlayersUsername import OtherPlayersUsername
from rrCheckpoint import Checkpoint
from TopView import TopView
import atexit

class World(DirectObject):

    def __init__(self):
        self.world = BulletWorld()
        rrDayTrack.Track(self.world)

w = World()
run()
