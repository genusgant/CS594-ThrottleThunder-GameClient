# Roaming-Ralph was modified to remove collision part.
from __future__ import division
import direct.directbase.DirectStart
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32, Point3
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from math import pi, sin, cos
from direct.interval.IntervalGlobal import *

from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from panda3d.core import *
import time

class OtherPlayersHealth():
 

    def __init__(self, gameEngine,vehicleContainer):
        
        print "OtherPlayersHealth"
        self.gameEngine = gameEngine
        self.vehicleContainer = vehicleContainer
        
        self.bar_text= loader.loadTexture("tex/bar_text.jpg")
        self.HealthBar = DirectWaitBar(text = str(vehicleContainer.username),
                            value = 100,
                            scale =2,
                            range=self.vehicleContainer.props.health,
                            pos = (0,.4,.4),
                            barRelief=1,
                            relief = 1,
                            barColor=(0,0.8,0,1),
                            barTexture =(self.bar_text))

        
        self.HealthBar.reparentTo(vehicleContainer.chassisNP)
        actualz = int(self.HealthBar.getZ())
        self.HealthBar.setZ(actualz + 3)
        self.HealthBar.setBillboardPointEye()
        self.HealthBar.setShaderOff()
        self.HealthBar.setBin('fixed', 0)
        self.HealthBar.setDepthWrite(False)

