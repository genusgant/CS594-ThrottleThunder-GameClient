from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
import datetime
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
import math


class Dashboard():
    def __init__(self, gameEngine, taskMgr):
        self.gameEngine = gameEngine
        self.font_digital = loader.loadFont('models/font/SFDigitalReadout-Heavy.ttf')
        self.start_time = datetime.datetime.now()
        self.time_elapsed = datetime.timedelta(milliseconds=0)
        self.countdown_time = datetime.timedelta(minutes=8)
        # insert total time
        self.game_time = self.countdown_time - self.time_elapsed
        # print self.game_time

        # Timer
        self.display_timer = OnscreenText(text=str(self.game_time), style=1, fg=(1, 1, 1, 1), pos=(0, .9), scale=.1,
                                          font=self.font_digital)
        self.mini_map = OnscreenImage(image="models/dashb/speedometer.png", scale=.2, pos=(-1.15, 0, .8))
        self.mini_map.setTransparency(TransparencyAttrib.MAlpha)
        self.char = OnscreenImage(image='models/triangle.png', scale=.1, parent=self.mini_map,pos=(-1.15, 0, .8) )
        self.otherchar = OnscreenImage(image='models/power_ups/pow1.png', scale=.1,
                                          parent=self.mini_map ,pos=(-1.15, 0, .8))
        self.setupSpeedImages()
        self.setupStatusBars()
        taskMgr.doMethodLater(.1, self.updateSpeed, 'updateSpeed')
        taskMgr.doMethodLater(.1, self.updateTimer, 'updateTimer')
        taskMgr.doMethodLater(.1, self.updateStatusBars, 'updateStatusBars')
        taskMgr.doMethodLater(.1, self.show_map, 'updateminimap')

    def updateStatusBars(self, task):
        maxScale = 0.15
        totalWidthScaled = 163.0 * 0.15
        currentHealth = self.gameEngine.vehicleContainer.vehicleControlState["health"]
        # print "Current Health: ", currentHealth
        length = currentHealth * maxScale
        halfLengthScaled = (maxScale - length)
        self.healthBar.destroy()
        self.healthBar = OnscreenImage(image="models/dashb/seekBar.png", scale=(length, 1.0, 0.08), pos=(-1.125 - halfLengthScaled, 0, -.85))
        self.healthBar.setTransparency(TransparencyAttrib.MAlpha)
        # self.healthBar.setColorScale(1,0,0, 1-currentHealth)
        return task.cont

    def updateSpeed(self, task):
        speed, normalizedSpeed = self.gameEngine.vehicleContainer.getSpeed()
        self.speed = str(format(speed, '0.2f'))
        # print self.speed

        # Update Speed Display
        self.display_speed.destroy()
        self.display_speed = OnscreenText(text=self.speed, style=3, fg=(1, 1, 1, 1),
                                          pos=(1.2, -0.95), align=TextNode.ARight, scale=.15, font=self.font_digital)
        # Needle
        self.speedNeedleAngle = self.MaxNeedleAngle * normalizedSpeed
        self.speedNeedle_img.destroy()
        self.speedNeedle_img = OnscreenImage(image="models/dashb/meterNeedle.png", scale=.25, pos=(0.9, 0, -.65), hpr = (0,0,self.speedNeedleAngle))
        self.speedNeedle_img.setTransparency(TransparencyAttrib.MAlpha)
        # Meter Top
        self.speedTop.destroy()
        self.speedTop = OnscreenImage(image="models/dashb/meterTop.png", scale=.25, pos=(0.9, 0, -.65))
        self.speedTop.setTransparency(TransparencyAttrib.MAlpha)
        return task.cont

    def updateTimer(self, task):
        self.time_elapsed = datetime.datetime.now() - self.start_time
        game_time = str(self.countdown_time - self.time_elapsed)[2:11]
        self.display_timer.destroy()
        self.display_timer = OnscreenText(text=game_time, style=3, fg=(1, 1, 1, 1), pos=(0, .9), scale=.15,
                                          font=self.font_digital)
        return task.cont

    def setupSpeedImages(self):
        self.display_speed = OnscreenText(text="0", style=1, fg=(1, 1, 1, 1),
                                          pos=(1.3, -0.95), align=TextNode.ARight, scale=.07, font=self.font_digital)
        # Speedometer
        self.speed_img = OnscreenImage(image="models/dashb/meterBG.png", scale=.25, pos=(0.9, 0, -.65))
        self.speed_img.setTransparency(TransparencyAttrib.MAlpha)
        # Needle
        self.MaxNeedleAngle = 260
        self.speedNeedleAngle = 0
        self.speedNeedle_img = OnscreenImage(image="models/dashb/meterNeedle.png", scale=.25, pos=(0.9, 0, -.65), hpr = (0,0,self.speedNeedleAngle))
        self.speedNeedle_img.setTransparency(TransparencyAttrib.MAlpha)
        # Meter Top
        self.speedTop = OnscreenImage(image="models/dashb/meterTop.png", scale=.25, pos=(0.9, 0, -.65))
        self.speedTop.setTransparency(TransparencyAttrib.MAlpha)

    def setupStatusBars(self):
        # Health-Bar
        self.healthBarBG = OnscreenImage(image="models/dashb/seekBarBG.png", scale=(0.15, 1.0, 0.08), pos=(-1.125, 0, -.85))
        self.healthBarBG.setTransparency(TransparencyAttrib.MAlpha)
        self.healthBar = OnscreenImage(image="models/dashb/seekBar.png", scale=(0.15, 1.0, 0.08), pos=(-1.125, 0, -.85))
        self.healthBar.setTransparency(TransparencyAttrib.MAlpha)
        
    def show_map(self, task):
       
        main_char=self.gameEngine.vehicleContainer
        x=main_char.chassisNP.getX()
        y=main_char.chassisNP.getY()
        h=main_char.chassisNP.getH()
        #temporary value
        size=200
        bound=80
        # connected player
        for i in  self.gameEngine.vehiclelist:
            car= self.gameEngine.vehiclelist[i]
            i_x=car.chassisNP.getX()
            i_y=car.chassisNP.getY()
            i_h=car.chassisNP.getH()
            if(i_x<bound and i_y<bound and i_y>(bound*-1) and i_x>(bound*-1) ):
                self.otherchar.destroy()
                
            
                self.otherchar = OnscreenImage(image='models/power_ups/pow1.png', scale=.07, parent=self.mini_map ,
                                           pos=(i_x/size, 0, i_y/size),color=(1,1,0,1))
          
                self.otherchar.setR(-i_h)
        #powerup
        if(x<bound and y<bound and x>(bound*-1) and x>(bound*-1)): 
            self.char.destroy()
            self.char = OnscreenImage(image='models/triangle.png', scale=.1, parent=self.mini_map ,pos=(x/size, 0, y/size))
            self.char.setR(-h)
        return task.cont

