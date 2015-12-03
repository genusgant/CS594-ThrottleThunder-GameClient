from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
import datetime
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
import math
from direct.gui.DirectGui import *


class Dashboard():
    def __init__(self, gameEngine, taskMgr):
        self.gameEngine = gameEngine
        self.font_digital = loader.loadFont('models/font/SFDigitalReadout-Heavy.ttf')
        self.start_time = datetime.datetime.now()
        self.time_elapsed = datetime.timedelta(milliseconds=0)
        self.countdown_time = datetime.timedelta(minutes=8)
        #
        self.screenBtns = [] 

        self.isGameTimeOver = False

        # insert total time
        self.game_time = self.countdown_time - self.time_elapsed
        # print self.game_time

        # players is a map that holds all the players with their ranking and updates every second key= rank, value= username
        self.players={}

        self.lead1 = ""
        self.lead2 = ""
        self.lead3 = ""

        # Leaderboard Ranking
        self.leader1 = OnscreenText(text="1:", style=1, fg=(1, 1, 1, 1),
                                    pos=(-1.3, .5), align=TextNode.ALeft,
                                    scale=.07, font=self.font_digital)
        self.leader2 = OnscreenText(text="2:", style=1, fg=(1, 1, 1, 1),
                                    pos=(-1.3, .45), align=TextNode.ALeft,
                                    scale=.07, font=self.font_digital)
        self.leader3 = OnscreenText(text="3:", style=1, fg=(1, 1, 1, 1),
                                    pos=(-1.3, .4), align=TextNode.ALeft,
                                    scale=.07, font=self.font_digital)

        # Your Rank
        self.ranklabel = OnscreenText(text="Rank", style=1, fg=(1, 1, 1, 1), pos=(-.9, .89), align=TextNode.ALeft,
                     font=self.font_digital, scale=.06)
        # rank = str(self.rm.rank) + "/" + str(self.rm.racers)
        self.rank = "Rank placeholder1"
        self.display_rank = OnscreenText(text=self.rank, style=1, fg=(1, 1, 1, 1),
                                         pos=(-.8, .85), align=TextNode.ALeft,
                                         scale=.15, font=self.font_digital)
        self.playerlabel = OnscreenText(text="Players\nLeft", style=1, fg=(1, 1, 1, 1), pos=(-.5, .89), align=TextNode.ALeft,
                     font=self.font_digital, scale=.06)

        self.screenBtns.append(self.leader1)
        self.screenBtns.append(self.leader2)
        self.screenBtns.append(self.leader3)
        self.screenBtns.append(self.ranklabel)
        self.screenBtns.append(self.display_rank)
        self.screenBtns.append(self.playerlabel)



        def displayBars() :
            health = self.gameEngine.vehicleContainer.props.getHealthStatus()
            self.Health_bar['value'] = health['health']
            self.EHealth_bar['value'] = health['additionalHealth']
            armour = self.gameEngine.vehicleContainer.props.getArmorStatus()
            self.Armour_bar['value'] = armour

        # Timer
        self.display_timer = OnscreenText(text=str(self.game_time), style=1, fg=(1, 1, 1, 1), pos=(0, .9), scale=.1,
                                          font=self.font_digital)
        self.mini_map = OnscreenImage(image="models/dashb/speedometer.png", scale=.2, pos=(-1.15, 0, .8))
        self. mini_map.setTransparency(TransparencyAttrib.MAlpha)
        self.char = OnscreenImage(image='models/triangle.png', scale=.1, parent=self.mini_map,pos=(-1.15, 0, .8) )
        self.otherchar = OnscreenImage(image='models/power_ups/pow1.png', scale=.1,
                                          parent=self.mini_map ,pos=(-1.15, 0, .8))

        self.screenBtns.append(self.display_timer)
        self.screenBtns.append(self.mini_map)
        self.screenBtns.append(self.char)
        self.screenBtns.append(self.otherchar)

        self.offset = 0.13
        self.setupSpeedImages()
        self.setupBoostImages()
        self.setupStatusBars()
        taskMgr.doMethodLater(.1, self.updateSpeed, 'updateSpeed')
        taskMgr.doMethodLater(.1, self.updateBoost, 'updateBoost')
        taskMgr.doMethodLater(.1, self.updateTimer, 'updateTimer')
        taskMgr.doMethodLater(.1, self.updateStatusBars, 'updateStatusBars')
        taskMgr.doMethodLater(.1, self.show_map, 'updateminimap')
        displayBars()
        taskMgr.doMethodLater(.1, self.update_rank, 'updateRank')


    def updateStatusBars(self, task):

        health = self.gameEngine.vehicleContainer.props.getHealthStatus()
        self.Health_bar['value'] = health['health']
        self.EHealth_bar['value'] = health['additionalHealth']
        armour = self.gameEngine.vehicleContainer.props.getArmorStatus()
        self.Armour_bar['value'] = armour
        # maxScale = 0.15
        # totalWidthScaled = 163.0 * 0.15
        # currentHealth = self.gameEngine.vehicleContainer.vehicleControlState["health"]
        # # print "Current Health: ", currentHealth
        # length = currentHealth * maxScale
        # halfLengthScaled = (maxScale - length)
        # self.healthBar.destroy()
        # self.healthBar = OnscreenImage(image="models/dashb/seekBar.png", scale=(length, 1.0, 0.08), pos=(-1.125 - halfLengthScaled, 0, -.85))
        # self.healthBar.setTransparency(TransparencyAttrib.MAlpha)
        # # self.healthBar.setColorScale(1,0,0, 1-currentHealth)
        return task.cont

    def updateSpeed(self, task):
        speed, normalizedSpeed = self.gameEngine.vehicleContainer.getSpeed()
        self.speed = str(format(speed, '0.2f'))
        # print self.speed

        wheelRate = 0.75 * speed

        self.reversing = False

        self.gearSpacing = (self.gameEngine.vehicleContainer.specs['maxSpeed'] / 4)

        # Calculate which gear we're in, and what the normalised revs are
        if self.reversing:
            numberOfGears = 1
        else:
            numberOfGears = 4

        self.gear = min(int(wheelRate/ self.gearSpacing),
                    numberOfGears - 1)

        # Update Speed Display
        self.display_speed.destroy()
        self.display_speed = OnscreenText(text=self.speed, style=3, fg=(1, 1, 1, 1),
                                          pos=(1.15, -0.95), align=TextNode.ARight, scale=.13, font=self.font_digital)

        # print gear
        self.display_gear.destroy()
        self.display_gear = OnscreenText(text=str(self.gear+1), style=3, fg=(1, 1, 1, 1),
            pos=(0.917, -0.80), align=TextNode.ARight, scale=.10, font=self.font_digital)

        # Needle
        self.speedNeedleAngle = self.MaxNeedleAngle * normalizedSpeed
        self.speedNeedle_img.destroy()
        self.speedNeedle_img = OnscreenImage(image="models/dashb/meterNeedle.png", scale=.25, pos=(0.9, 0, -.65), hpr = (0,0,self.speedNeedleAngle))
        self.speedNeedle_img.setTransparency(TransparencyAttrib.MAlpha)
        # Meter Top
        self.speedTop.destroy()
        self.speedTop = OnscreenImage(image="models/dashb/meterTop.png", scale=.25, pos=(0.9, 0, -.65))
        self.speedTop.setTransparency(TransparencyAttrib.MAlpha)
        self.screenBtns.append(self.display_speed)
        self.screenBtns.append(self.display_gear)
        self.screenBtns.append(self.speedNeedle_img)
        self.screenBtns.append(self.speedTop)
        return task.cont

    def updateBoost(self, task):
        normalizedBoost = self.gameEngine.vehicleContainer.getBoost()
        # Needle
        self.boostNeedleAngle = self.MaxNeedleAngle * normalizedBoost
        self.boostNeedle_img.destroy()
        self.boostNeedle_img = OnscreenImage(image="models/dashb/meterNeedle.png", scale=self.boostScale, pos=(self.boostX, 0, self.boostY), hpr = (0,0,self.boostNeedleAngle))
        self.boostNeedle_img.setTransparency(TransparencyAttrib.MAlpha)
        # Meter Top
        self.boostTop.destroy()
        self.boostTop = OnscreenImage(image="models/dashb/meterTop.png", scale=self.boostScale, pos=(self.boostX, 0, self.boostY))
        self.boostTop.setTransparency(TransparencyAttrib.MAlpha)
        self.screenBtns.append(self.boostNeedle_img)
        self.screenBtns.append(self.boostTop)
        return task.cont

    def updateTimer(self, task):
        self.time_elapsed = datetime.datetime.now() - self.start_time
        game_time = "0.00.000"
        if(self.countdown_time <= self.time_elapsed):
            # print "Time must over here"
            self.isGameTimeOver = True
        else:
            game_time = str(self.countdown_time - self.time_elapsed)[2:11]

        # print "datetime.datetime.now(): ", datetime.datetime.now()
        # print "self.start_time:", self.start_time
        # print datetime.datetime.now(), " - ", self.start_time, " =", self.time_elapsed, "self.time_elapsed"
        # print "self.countdown_time", self.countdown_time
        # print "self.time_elapsed: ", self.time_elapsed
        # print self.countdown_time, " - ", self.time_elapsed, " ="
        # print "game_time: ", game_time
        # print "--------------------------------------------------------"

        self.display_timer.destroy()
        self.display_timer = OnscreenText(text=game_time, style=3, fg=(1, 1, 1, 1), pos=(0, .9), scale=.15,
                                          font=self.font_digital)
        self.screenBtns.append(self.display_timer)

        # updateTimer task will stop when the countdown time hits to zero
        if(self.isGameTimeOver):
            self.gameEngine.gameEnd()
            print "Time Over"
            # self.gameResult()
            return task.done
        else:
            return task.cont


    def setupSpeedImages(self):
        self.display_speed = OnscreenText(text="0", style=1, fg=(1, 1, 1, 1),
                                          pos=(1.3, -0.95), align=TextNode.ARight, scale=.07, font=self.font_digital)

        # Display Gear
        self.display_gear = OnscreenText(text="N", style=3, fg=(1, 1, 1, 1),
                                          pos=(0.917, -0.80), align=TextNode.ARight, scale=.10, font=self.font_digital)

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

        self.screenBtns.append(self.display_speed)
        self.screenBtns.append(self.display_gear)
        self.screenBtns.append(self.speed_img)
        self.screenBtns.append(self.speedNeedle_img)
        self.screenBtns.append(self.speedTop)



    def setupBoostImages(self):
        self.boostX = 1.30 # - self.offset
        self.boostY = -0.75
        self.boostScale = 0.19
        # Health meter
        self.boost_img = OnscreenImage(image="models/dashb/boostMeterBG.png", scale=self.boostScale, pos=(self.boostX, 0, self.boostY))
        self.boost_img.setTransparency(TransparencyAttrib.MAlpha)
        # Needle
        self.MaxNeedleAngle = 260
        self.boostNeedleAngle = 0
        self.boostNeedle_img = OnscreenImage(image="models/dashb/meterNeedle.png", scale=self.boostScale, pos=(self.boostX, 0, self.boostY), hpr = (0,0,self.boostNeedleAngle))
        self.boostNeedle_img.setTransparency(TransparencyAttrib.MAlpha)
        # Meter Top
        self.boostTop = OnscreenImage(image="models/dashb/meterTop.png", scale=self.boostScale, pos=(self.boostX, 0, self.boostY))
        self.boostTop.setTransparency(TransparencyAttrib.MAlpha)

        self.screenBtns.append(self.boost_img)
        self.screenBtns.append(self.boostNeedle_img)
        self.screenBtns.append(self.boostTop)



    def setupStatusBars(self):
        # Health-Bar
        # self.healthBarBG = OnscreenImage(image="models/dashb/seekBarBG.png", scale=(0.15, 1.0, 0.08), pos=(-1.125, 0, -.85))
        # self.healthBarBG.setTransparency(TransparencyAttrib.MAlpha)
        # self.healthBar = OnscreenImage(image="models/dashb/seekBar.png", scale=(0.15, 1.0, 0.08), pos=(-1.125, 0, -.85))
        # self.healthBar.setTransparency(TransparencyAttrib.MAlpha)
        self.bars = self.gameEngine.vehicleContainer.props.getBarDetails()


        # Health Bar      

        self.Health_bar = DirectWaitBar(text = "", range = self.bars["health"], pos = (0.647,0,0.558), barColor= (1,0,0,1), frameSize = (0,.475,0.29,0.34),barTexture =("models/dashb/barHealth.png"))

        self.EHealth_bar = DirectWaitBar(text = "", range = self.bars["additionalHealth"], pos = (1.133,0,0.558), barColor= (0,1,0,1), frameSize = (0,.15,0.29,0.34),barTexture =("models/dashb/barExtraHealth.png"))

        self.Armour_bar = DirectWaitBar(text = "",range = self.bars["armor"], pos = (0.74,0,0.418), barColor= (159,0,255,1), frameSize = (0,0.54,0.29,0.34),barTexture =("models/dashb/barArmor.png"))


        # Health Bar Frame
        self.frame = OnscreenImage(image = "models/dashb/frame.png", pos=(0.9, 0, 0.8), scale = (0.40, 0.15, 0.15) )
        self.frame.setTransparency(TransparencyAttrib.MAlpha)
        self.screenBtns.append(self.Health_bar)
        self.screenBtns.append(self.EHealth_bar)
        self.screenBtns.append(self.Armour_bar)
        self.screenBtns.append(self.frame)

    def show_map(self, task):

        main_char=self.gameEngine.vehicleContainer
        if main_char != None:
            x=main_char.chassisNP.getX()
            y=main_char.chassisNP.getY()
            h=main_char.chassisNP.getH()
            #temporary value
            size=200
            bound=80
            # connected player
            for i in  self.gameEngine.vehiclelist:
                car= self.gameEngine.vehiclelist[i]
                if car != None:
                    i_x=car.chassisNP.getX()
                    i_y=car.chassisNP.getY()
                    i_h=car.chassisNP.getH()
                    if(i_x<bound and i_y<bound and i_y>(bound*-1) and i_x>(bound*-1) ):
                        self.otherchar.destroy()


                        self.otherchar = OnscreenImage(image='models/power_ups/pow1.png', scale=.07, parent=self.mini_map ,
                                                   pos=(i_x/size, 0, i_y/size),color=(1,1,0,1))

                        self.otherchar.setR(-i_h)
                        self.screenBtns.append(self.otherchar)
            #powerup
            if(x<bound and y<bound and x>(bound*-1) and x>(bound*-1)):
                self.char.destroy()
                self.char = OnscreenImage(image='models/triangle.png', scale=.1, parent=self.mini_map ,pos=(x/size, 0, y/size))
                self.char.setR(-h)
                self.screenBtns.append(self.char)

        return task.cont


    # being called by ResponseRankings
    def update_ranking(self, leaders):
        self.players = leaders
        if(len(leaders)>= 3):
            self.lead1 = leaders[1]
            self.lead2 = leaders[2]
            self.lead3 = leaders[3]
        elif(len(leaders)==2):
            self.lead1 = leaders[1]
            self.lead2 = leaders[2]
        elif(len(leaders)==1):
            self.lead1 = leaders[1]


    def update_rank(self, task):
        self.display_rank.destroy()
        self.gameEngine.doRanking()
        # Your Rank
        self.rank = "Rank holder"
        for x in range(1, len(self.players)+1):
            if(self.players[x]== self.gameEngine.login):
                self.rank = str(x) + "/" + str(len(self.players))
                break

        self.display_rank = OnscreenText(text=self.rank, style=1, fg=(1, 1, 1, 1),
                                         pos=(-.8, .85), align=TextNode.ALeft,
                                         scale=.15, font=self.font_digital)

        # Leader board
        self.leader1.destroy()
        self.leader2.destroy()
        self.leader3.destroy()
        lead1 = "1:" + self.lead1
        lead2 = "2:" + self.lead2
        lead3 = "3:" + self.lead3

        self.leader1 = OnscreenText(text=lead1, style=1, fg=(1, 1, 1, 1),
                                    pos=(-1.88, .5), align=TextNode.ALeft,
                                    scale=.07, font=self.font_digital)
        self.leader2 = OnscreenText(text=lead2, style=1, fg=(1, 1, 1, 1),
                                    pos=(-1.88, .45), align=TextNode.ALeft,
                                    scale=.07, font=self.font_digital)
        self.leader3 = OnscreenText(text=lead3, style=1, fg=(1, 1, 1, 1),
                                    pos=(-1.88, .4), align=TextNode.ALeft,
                                    scale=.07, font=self.font_digital)

        self.screenBtns.append(self.display_rank)
        self.screenBtns.append(self.leader1)
        self.screenBtns.append(self.leader2)
        self.screenBtns.append(self.leader3)
        return task.cont


    def getRank(self):
        return self.rank


    def gameResult(self, isDead=False):

        #print "REsult"
        
        if isDead:
            print "Inside if"
            self.rank = len(self.gameEngine.vehiclelist) - self.gameEngine.deadCounter -1
            message = "Winner. You Won the Game!"
        else:
            rank = self.getRank().split("/")
            if rank[0]=="1" :
                message = "Winner. You Won the Game!"
            else :
                message = "Game Over. You Loose"

        self.ResultFrame = DirectFrame(frameColor=(1,0,0,0.8),frameSize = (-0.75,.75,-.5,.5),pos=(0, 0.0, 0))

        self.ResultMessage = OnscreenText(text=message, style=1, fg=(1, 1, 1, 1),
            pos=(0,0.1), align=TextNode.ACenter, scale=.1)

        position = "Position : "+str(self.getRank())

        self.ResultPosition = OnscreenText(text=position, style=1, fg=(1, 1, 1, 1),
            pos=(0,-0.1), align=TextNode.ACenter, scale=.1)

        self.backToLobby = DirectButton(image = 'IMAGES/enter.png', pos = (0.3, 0, -0.4),  scale = (.17, 1, .03), relief = None, command = self.goLobby)


        self.screenBtns.append(self.ResultFrame)
        self.screenBtns.append(self.ResultMessage)
        self.screenBtns.append(self.ResultPosition)
        self.screenBtns.append(self.backToLobby)
        # self.screenBtns.append(self.Pname)
        # self.screenBtns.append(self.Pname)


    def unloadScreen(self):
        for item in self.screenBtns:
            item.destroy()

    def goLobby(self):

        taskMgr.remove("updateSpeed")
        taskMgr.remove("updateBoost")
        taskMgr.remove("updateTimer")
        taskMgr.remove("updateStatusBars")
        taskMgr.remove("updateminimap")
        taskMgr.remove("updateRank")
        
        self.unloadScreen()
        print "Game over"

        self.gameEngine.callLobby()
