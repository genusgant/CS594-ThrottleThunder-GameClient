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
 

    def __init__(self,gameEngine,vehicleContainer):
        self.gameEngine = gameEngine
        self.vehicleContainer = vehicleContainer
        self.bar_text= loader.loadTexture("tex/bar_text.jpg")
        self.bar = DirectWaitBar(text = str(vehicleContainer.username),
                            value = 100,
                            scale =2,
                            range=100,
                            pos = (0,.4,.4),
                            barRelief=1,
                            relief = 1,
                            barColor=(0,0.8,0,1),
                            barTexture =(self.bar_text))
        self.bar.reparentTo(vehicleContainer.chassisNP)
        actualz = int(self.bar.getZ())
        self.bar.setZ(actualz + 3)
        self.bar.setBillboardPointEye()
        self.bar.setShaderOff()
        self.bar.setBin('fixed', 0)
        self.bar.setDepthWrite(False)
       # taskMgr.add(self.incbar,"healthchange")

    def setVal(self,val):
        #print "setting bar to: ", val
        self.bar['value'] = val
        self.checkcolor()
        #self.checkdead()

    def updateRange(self, m):
        self.bar['range'] = m
		
# def incbar(self,task):
#    if (keyMap["health-minus"]!=0):
#       self.bar['value']+= -1
#  if (keyMap["health-plus"]!=0):
#     self.bar['value']+= 1
#
#       self.checkcolor()
#      self.checkdead()
#     return task.cont

    def checkcolor(self):
        if(self.bar['value']<=2):
            self.bar ["barColor"]=(0.8,0,0,1) #red
            if (self.bar['value'] <=0):
                self.bar['value']=0  # block to zero

        elif(self.bar['value']>2 and self.bar['value']<=99):
            self.bar ["barColor"]=(0.8,0.8,0,1) #yellow
        else:
            self.bar ["barColor"]=(0,0.8,0,1) #green
            if (self.bar['value'] >=100):
                self.bar['value'] =100    #block to a hundred


    def checkdead(self):
        if (self.bar['value']<=0):
            # here you should block the player 
            # then at the end it should call revival fonction 
            self.revival()

    def revival(self):
        self.bar['value']=100
        self.bar ["barColor"]=(0,0.8,0,1)
        
        
