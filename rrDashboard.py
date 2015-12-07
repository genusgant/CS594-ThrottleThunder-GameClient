from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
import datetime
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib


class Dashboard(DirectObject):
    def __init__(self, world, taskMgr, raceMst):
        # def __init__(self, world, taskMgr):
        self.world = world

        self.font_digital = loader.loadFont('models/font/SFDigitalReadout-Heavy.ttf')
        self.total_players = 30
        self.rank = 21
        self.main_char = world.vehicleContainer
        self.rm = raceMst
        self.speed = "0.0 km/h"
        self.lead1 = ""
        self.lead2 = ""
        self.lead3 = ""
        self.start_time = datetime.datetime.now()
        self.time_elapsed = datetime.timedelta(milliseconds=0)
        self.countdown_time = datetime.timedelta(minutes=8)
        # insert total time
        self.game_time = self.countdown_time - self.time_elapsed
        # print self.game_time

        # Timer
        self.display_timer = OnscreenText(text=str(self.game_time), style=1, fg=(1, 1, 1, 1), pos=(0, .9), scale=.1,
                                          font=self.font_digital)

        # Mini-Map
        # self.mini_map = OnscreenImage(image="models/dashb/minimap.png", scale=.15, pos=(-1.15, 0, .8))
        # self.mini_map.setTransparency(TransparencyAttrib.MAlpha)


        # Speedometer
        self.speed_img = OnscreenImage(image="models/dashb/speedometer.png", scale=.5, pos=(1.1, 0, -.95))
        self.speed_img.setTransparency(TransparencyAttrib.MAlpha)
        OnscreenText(text="km\n/h", style=1, fg=(1, 1, 1, 1),
                     font=self.font_digital, scale=.07, pos=(1.25, -.92))

        # Your Rank
        OnscreenText(text="Rank", style=1, fg=(1, 1, 1, 1), pos=(-.9, .89), align=TextNode.ALeft,
                     font=self.font_digital, scale=.06)
        rank = str(self.rm.rank) + "/" + str(self.rm.racers)
        self.display_rank = OnscreenText(text=rank, style=1, fg=(1, 1, 1, 1),
                                         pos=(-.8, .85), align=TextNode.ALeft,
                                         scale=.15, font=self.font_digital)
        OnscreenText(text="Players\nLeft", style=1, fg=(1, 1, 1, 1), pos=(-.5, .89), align=TextNode.ALeft,
                     font=self.font_digital, scale=.06)

        laps = str(self.rm.laps) + " Laps"
        self.display_lap = OnscreenText(text=laps, style=1, fg=(1, 1, 1, 1), pos=(1.0, .89), align=TextNode.ALeft,
                                        font=self.font_digital, scale=.06)

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

        # Power-ups
        # OnscreenText(text="1", style=1, fg=(1, 1, 1, 1),
        #              pos=(-1.25, -.95),
        #              scale=.07)
        # OnscreenText(text="2", style=1, fg=(1, 1, 1, 1),
        #              pos=(-1.15, -.95),
        #              scale=.07)
        # OnscreenText(text="3", style=1, fg=(1, 1, 1, 1),
        #              pos=(-1.05, -.95),
        #              scale=.07)
        # self.power1 = OnscreenImage(image='models/power_ups/pow1.png', pos=(-1.25, 0, -0.85), scale=.05)
        # self.power2 = OnscreenImage(image='models/power_ups/pow2.png', pos=(-1.15, 0, -0.85), scale=.05)
        # self.power3 = OnscreenImage(image='models/power_ups/pow3.png', pos=(-1.05, 0, -0.85), scale=.05)

        # Display Speed
        self.display_speed = OnscreenText(text=self.speed, style=1, fg=(1, 1, 1, 1),
                                          pos=(1.3, -0.95), align=TextNode.ARight, scale=.07, font=self.font_digital)

        taskMgr.doMethodLater(.1, self.show_speed, 'updateSpeed')
        taskMgr.doMethodLater(.1, self.show_timer, 'updateTimer')
        taskMgr.doMethodLater(.1, self.update_rank, 'updateRank')

    def show_speed(self, task):
        self.speed = str(format(self.main_char.vehicle.getCurrentSpeedKmHour(), '0.2f'))
        # print self.speed

        # Update Speed Display
        self.display_speed.destroy()
        self.display_speed = OnscreenText(text=self.speed, style=3, fg=(1, 1, 1, 1),
                                          pos=(1.2, -0.95), align=TextNode.ARight, scale=.15, font=self.font_digital)
        return task.cont

    def show_timer(self, task):
        self.time_elapsed = datetime.datetime.now() - self.start_time
        game_time = str(self.countdown_time - self.time_elapsed)[2:11]
        self.display_timer.destroy()
        self.display_timer = OnscreenText(text=game_time, style=3, fg=(1, 1, 1, 1), pos=(0, .9), scale=.15,
                                          font=self.font_digital)
        return task.cont

    # server updates client time in ms
    # def force_timer(self, server_time):
    #     self.start_time = datetime.datetime.now()
    #     self.countdown_time = datetime.timedelta(milliseconds=server_time)

    def update_ranking(self, leaders):
            for i in range(len(leaders)):
                if leaders.get(i) == self.world.login:
                    self.rm.rank = i
                    print("My rank: " + str(i))
                    break

            # get usernames from list
            # self.lead1 = leaders.get(1)
            # self.lead2 = leaders.get(2)
            # self.lead3 = leaders.get(3)

    def update_rank(self, task):
        self.display_rank.destroy()
        self.display_lap.destroy()

        # Your Rank
        rank = str(self.rm.rank) + "/" + str(self.rm.racers)
        self.display_rank = OnscreenText(text=rank, style=1, fg=(1, 1, 1, 1),
                                         pos=(-.8, .85), align=TextNode.ALeft,
                                         scale=.15, font=self.font_digital)

        laps = str(self.rm.laps) + " Laps - " + str(self.rm.checkpointspassed)
        self.display_lap = OnscreenText(text=laps, style=1, fg=(1, 1, 1, 1), pos=(1.0, .89), align=TextNode.ALeft,
                                        font=self.font_digital, scale=.06)

        # Leader board
        self.leader1.destroy()
        self.leader2.destroy()
        self.leader3.destroy()
        lead1 = "1:" + self.lead1
        lead2 = "2:" + self.lead2
        lead3 = "3:" + self.lead3
        self.leader1 = OnscreenText(text=lead1, style=1, fg=(1, 1, 1, 1),
                                    pos=(-1.3, .5), align=TextNode.ALeft,
                                    scale=.07, font=self.font_digital)
        self.leader2 = OnscreenText(text=lead2, style=1, fg=(1, 1, 1, 1),
                                    pos=(-1.3, .45), align=TextNode.ALeft,
                                    scale=.07, font=self.font_digital)
        self.leader3 = OnscreenText(text=lead3, style=1, fg=(1, 1, 1, 1),
                                    pos=(-1.3, .4), align=TextNode.ALeft,
                                    scale=.07, font=self.font_digital)

        return task.cont

    def gameResult(self, isDead=False):

        # print "REsult"

        if isDead:
            print "Inside if"
            self.rank = len(self.gameEngine.vehiclelist) - self.gameEngine.deadCounter - 1
            message = "Winner. You Won the Game!"
        else:
            rank = self.getRank().split("/")
            if rank[0] == "1":
                message = "Winner. You Won the Game!"
            else:
                message = "Game Over. You Loose"

        self.ResultFrame = DirectFrame(frameColor=(1, 0, 0, 0.8), frameSize=(-0.75, .75, -.5, .5), pos=(0, 0.0, 0))

        self.ResultMessage = OnscreenText(text=message, style=1, fg=(1, 1, 1, 1),
                                          pos=(0, 0.1), align=TextNode.ACenter, scale=.1)

        position = "Position : " + str(self.getRank())

        self.ResultPosition = OnscreenText(text=position, style=1, fg=(1, 1, 1, 1),
                                           pos=(0, -0.1), align=TextNode.ACenter, scale=.1)

        self.backToLobby = DirectButton(image='IMAGES/enter.png', pos=(0.3, 0, -0.4), scale=(.17, 1, .03), relief=None,
                                        command=self.goLobby)

        self.screenBtns.append(self.ResultFrame)
        self.screenBtns.append(self.ResultMessage)
        self.screenBtns.append(self.ResultPosition)
        self.screenBtns.append(self.backToLobby)

    def unloadScreen(self):
        for item in self.screenBtns:
            item.destroy()

    def goLobby(self):
        taskMgr.remove("updateSpeed")
        taskMgr.remove("updateTimer")
        taskMgr.remove("updateRank")

        self.unloadScreen()
        print "Game over"

        self.gameEngine.callLobby()
