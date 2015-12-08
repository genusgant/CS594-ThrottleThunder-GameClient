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

class OtherPlayersUsername():
 

    def __init__(self, gameEngine,vehicleContainer):
        
        print "OtherPlayersUsername"
        self.gameEngine = gameEngine
        self.vehicleContainer = vehicleContainer
        #self.bar_text= loader.loadTexture("models/dashb/bar_text.jpg")
        #self.frame = DirectFrame(frameColor=(0,0,0,1),
                                         #frameSize=(-1,1,-1,1),parent=vehicleContainer.chassisNP)
        

        self.otherIdentity = DirectWaitBar(value=100,barColor= (0,0,0,0), frameSize = (-.8,.8,0.1,0.3))
        OnscreenText(parent=self.otherIdentity,text = str(vehicleContainer.username),fg=(1,1,1,1))
        print vehicleContainer.username
        self.otherIdentity.setPos(0, 0, 2)
    
        self.otherIdentity.setBillboardPointEye()
        self.otherIdentity.setBin('fixed', 0)
        self.otherIdentity.setDepthWrite(False)
        self.otherIdentity.reparentTo(vehicleContainer.chassisNP)

