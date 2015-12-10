
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import *
from panda3d.core import TransparencyAttrib
from direct.gui.DirectGui import *
from pandac.PandaModules import WindowProperties
from Network.models.AuthConnectionModel import AuthConnectionModel
from Network.models.NullConnectionModel import NullConnectionModel
from Network.models.HeartbeatConnectionModel import HeartbeatConnectionModel
from Network.models.QueueConnectionModel import QueueConnectionModel
from Network.models.ChatConnectionModel import ChatConnectionModel
from Network.models.FriendConnectionModel import FriendConnectionModel

from Network.ServerConnection import ServerConnection
from Main import WorldManager
from RRMain import RRWorldManager
from login import Login
from menu import Menu
loadPrcFileData('', 'bullet-enable-contact-events true')

from direct.task.TaskManagerGlobal import taskMgr

import random, sys, os, math, json

class World(DirectObject):
    #client side making it easier and not having to log in everytime for debuging just follow the comments
    def __init__(self):
        print("began")
        self.taskMgr = taskMgr
        with open('config.json') as data_file:
            self.conf = json.load(data_file)
        self.ServerConnection = ServerConnection()#uncomment when going live
        self.ServerConnection.connect(self.conf['host'],self.conf['port'])#uncomment when going live
        props = WindowProperties( )
        props.setTitle( 'Log In' )
        props.setFixedSize(True)
        props.setSize(1280,740)
        props.setOrigin(-2,-2)
        base.win.requestProperties( props )
        self.base = ShowBase
        self.main_theme = base.loader.loadSfx("audio/bg music/Lobby music/drive_fast.ogg")
        # Song = Three Chain Links - Drive Fast: https://soundcloud.com/beardmont/three-chain-links-the-5
        self.main_theme.play()

        self.username = ""
        self.balance = "900000"

        self.authConnection = AuthConnectionModel(self)#uncomment when going live
        self.authConnection.setHandler(self.parseAuthResponse, self.parseRegResponse)
        self.ServerConnection.setupConnectionModel(self.authConnection)#uncomment when going live


        self.heartbeatConnection = HeartbeatConnectionModel()#uncomment when going live

        self.ServerConnection.setupConnectionModel(self.heartbeatConnection)#uncomment when going live

        #self.globalChatConnection = ChatConnectionModel(self)
        #self.ServerConnection.setupConnectionModel(self.globalChatConnection)

        #self.queueConnection = QueueConnectionModel(self)
        #self.ServerConnection.setupConnectionModel(self.authConnection)#uncomment when going live

        #self.friendConnection = FriendConnectionModel(self)
        #self.ServerConnection.setupConnectionModel(self.friendConnection)


        self.taskMgr.doMethodLater(self.conf['heartbeatRate'], self.doHeartbeat, "heartbeat")#uncomment when going live
        self.taskMgr.doMethodLater(self.conf['heartbeatRate'], self.doHeartbeat, "heartbeat")#uncomment when going live

        self.screen = Login(self)#uncomment when going live
        #self.screen = Menu(self)#comment this one when you are trying to log into it like normal

        #self.ServerConnection.setupConnectionModel(self.queueConnection)
        self.taskMgr.doMethodLater(self.conf['heartbeatRate'], self.doHeartbeat, "heartbeat")

        self.taskMgr.doMethodLater(1, self.doSong, "song")

        self.screenType = "login"
        self.screen.run()

    def doHeartbeat(self,task):
        self.heartbeatConnection.sendHeartbeat()
        return task.again

    def doSong(self,task):
        if self.main_theme.status() == self.main_theme.READY:
            self.main_theme.play()
        return task.again

    def startMusic(self):
        self.taskMgr.doMethodLater(1, self.doSong, "song")


    def stopMusic(self):
        self.main_theme.stop()
        self.taskMgr.remove("song")
        print "stopMusic"

    def doMenu(self):
        print("doing menu")
        if self.screenType == "login" :
            self.screen.unloadScreen()

        self.screenType = "menu"
        self.ServerConnection.activeStatus = True
        self.screen = Menu(self)

    def launchDDGame(self):
        print "Launching DD GAME"
        self.ServerConnection.activeStatus = False
        self.screen.unloadScreen()
        self.stopMusic()
        self.screen = WorldManager(self.screen)

    def launchRRGame(self):
        print "Launching RR GAME"
        self.ServerConnection.activeStatus = False
        self.screen.unloadScreen()
        self.stopMusic()
        self.screen = RRWorldManager(self.screen)
        # data might be require to send to DD world

    def parseAuthResponse(self,data):
        if data == 1:
            print("unloading")
            self.doMenu()
        else:
            if data == 2:
                self.screen.setStatusText("Already logged in")
            else:
                self.screen.setStatusText("Invalid username/password")
            self.screen.enter_btn['state'] = DGG.NORMAL
            self.screen.register_btn['state'] = DGG.NORMAL

    def parseRegResponse(self,data):
        if data == 1:
            print("unloading")
            self.doMenu()
        else:
            self.screen.setStatusText("User already exists")
            self.screen.cancel_btn['state'] = DGG.NORMAL
            self.screen.register_btn['state'] = DGG.NORMAL
app = World();
