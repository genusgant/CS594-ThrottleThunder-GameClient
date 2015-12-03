from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import *
from panda3d.core import TransparencyAttrib
from direct.gui.DirectGui import *
from pandac.PandaModules import WindowProperties
from Network.models.QueueConnectionModel import QueueConnectionModel
from Network.models.FriendConnectionModel import FriendConnectionModel
from Network.models.PrivateChatConnectionModel import PrivateChatConnectionModel
from Network.models.ChatConnectionModel import ChatConnectionModel
from Main import WorldManager
from RRMain import RRWorldManager

class Menu(ShowBase):

    def __init__(self, World):
        #just comment out the two lines below
        #self.appRunner = None#added this to overide the login
        self.playerList = []
        self.World = World
        self.WhichScreen = "";
        self.lastSelectedFriend = None

        # variable to save game selected DD or RR
        self.selectedGame = None

        #self.taskMgr = World.taskMgr#added this to overide the login

        props = WindowProperties()
        props.setTitle( 'Main Menu' )
        props.setFixedSize(True)
        props.setSize(1400,740)
        props.setOrigin(-2,-2)
        base.win.requestProperties( props )

        self.selectedCar = 0
        self.screenBtns = []

        self.globalChat = []
        self.privateChat = {}
        self.chatOffset = 0
        self.car = None

        self.onReturnMatch = self.createMatchMaking


        self.createSocialization()


        self.World.queueConnection.setHandler(self.handleQueueNotification)
        self.World.globalChatConnection.setHandler(self.handleChatNotification)
        self.World.friendConnection.setHandlers(self.handleFriendNotification,self.handleFriendListNotification)

        #self.World.privateChatConnection.setHandler(self.handlePrivateChatNotification)
        self.navi()

        self.accept('enter', self.sendMessage)


    def navi(self):
        if self.WhichScreen =="Social":
            self.mainmenuCustom = DirectButton(image = 'IMAGES/c_btn.png', pos = (-.1, 0, .80), scale = (.3, 1, .04), command=self.createCustomization, relief = None)
            self.mainmenuSocial = DirectButton(image = 'IMAGES/s_btn_s.png', pos = (0.7, 0, .80), scale = (.3, 1, .04), command=self.createSocialization, relief = None)
            self.mainmenuMatch = DirectButton(image = 'IMAGES/mm_btn.png', pos = (1.5, 0, .80), scale = (.3, 1, .04), command=self.onReturnMatch, relief = None)
        elif self.WhichScreen =="Custom":
            self.mainmenuCustom = DirectButton(image = 'IMAGES/c_btn_s.png', pos = (-.1, 0, .80), scale = (.3, 1, .04), command=self.createCustomization, relief = None)
            self.mainmenuSocial = DirectButton(image = 'IMAGES/s_btn.png', pos = (0.7, 0, .80), scale = (.3, 1, .04), command=self.createSocialization, relief = None)
            self.mainmenuMatch = DirectButton(image = 'IMAGES/mm_btn.png', pos = (1.5, 0, .80), scale = (.3, 1, .04), command=self.onReturnMatch, relief = None)
        elif self.WhichScreen =="Match":
            self.mainmenuCustom = DirectButton(image = 'IMAGES/c_btn.png', pos = (-.1, 0, .80), scale = (.3, 1, .04), command=self.createCustomization, relief = None)
            self.mainmenuSocial = DirectButton(image = 'IMAGES/s_btn.png', pos = (0.7, 0, .80), scale = (.3, 1, .04), command=self.createSocialization, relief = None)
            self.mainmenuMatch = DirectButton(image = 'IMAGES/mm_btn_s.png', pos = (1.5, 0, .80), scale = (.3, 1, .04), command=self.onReturnMatch, relief = None)
        self.Pname = DirectLabel(text=self.World.username, pos = (1.7,-4.0,0.88), text_scale=0.10, text_align = TextNode.ARight)
        self.Pname['text_fg'] = (0.7,0.7,1.0,0.5)
        self.Pname['frameColor'] = (0,0,0,0.1)
        self.screenBtns.append(self.Pname)
        self.screenBtns.append(self.mainmenuCustom)
        self.screenBtns.append(self.mainmenuSocial)
        self.screenBtns.append(self.mainmenuMatch)


    def createSocialization(self):
        self.unloadScreen()
        self.WhichScreen = "Social"
        self.lastSelectedFriend = None
        self.myImage=OnscreenImage(image = 'IMAGES/socialization_w.png', pos = (0, 0, 0), scale = (2, 1, 1))
        self.navi()
        self.World.friendConnection.sendFriendListRequest()
        self.friends = DirectButton(image = 'IMAGES/friends_btn.png', pos = (-0.5, 0, -.87), scale = (.2, 1, .04), relief = None)
        self.ntwork = DirectButton(image = 'IMAGES/global_btn.png', pos = (0, 0, -.87), scale = (.2, 1, .04), relief = None)
        self.send = DirectButton(image = 'IMAGES/send_btn.png', pos = (1.5, 0, -.87), scale = (.2, 1, .04), relief = None, command = self.sendMessage)
        self.addFriend = DirectButton(image = 'IMAGES/plus_friends_btn.png', pos = (-0.965, 0, -.88),  scale = (.17, 1, .03), relief = None, command = self.addNewFriend)
        self.addFriendBox = DirectEntry(text = "" , width=12,frameSize=(0, 12, -0.2, 1),pos = (-1.745,0.0,-0.9), scale=.05, initialText="")


        self.isGlobalChat = True
        #chat messages
        self.ChatFrame = DirectFrame(frameColor=(0,0,0,0.4),frameSize=(0.0, 2.5, -0.45, 0.9),pos=(-0.70, 0.0, -0.3))
        self.messageBox = DirectEntry(text = "" , width=50,frameSize=(0, 50, -0.2, 1),pos = (-0.70,0.0,-0.81), scale=.05, initialText="")


        #this lists the friends who are currently logged in

        self.usersChatFrame = DirectScrolledList(
            decButton_pos= (0.80, 0.0, -0.42),
            decButton_text = "-",
            decButton_text_fg = (1,1,1,1),
            decButton_text_scale = 0.08,
            decButton_frameSize = (-0.035, 0.045, -0.03, 0.04),
            decButton_frameColor = (0.5, 0.5, 0.6, 0.5),
            decButton_borderWidth = (0.01, 0.01),

            incButton_pos= (0.80, 0.0, 0.95),
            incButton_text = "+",
            incButton_text_fg = (1,1,1,1),
            incButton_text_scale = 0.08,
            incButton_frameSize = (-0.035, 0.045, -0.03, 0.04),
            incButton_frameColor = (0.5, 0.5, 0.6, 0.5),
            incButton_borderWidth = (0.01, 0.01),

            frameColor=(0,0,0,0.4),frameSize=(0.0, .75, -0.45, 1.0),pos=(-1.75, 0.0, -0.4),
            #items = [b1, b2],
            numItemsVisible = 14,
            #forceHeight = itemHeight,
            itemFrame_frameSize = (-0., 0.6, -0.45, 0.11),
            itemFrame_pos = (0.35, 0, 0.4),
            itemFrame_frameColor = (0, 0, 1.0, 0),
            text_fg = (1,1,1,1),

            itemFrame_text_bg = (1,1,1,0),
            text_bg = (1,1,1,0),
            text_scale = 0.2
            )



        self.screenBtns.append(self.myImage)
        self.screenBtns.append(self.friends)
        self.screenBtns.append(self.ntwork)
        self.screenBtns.append(self.send)
        self.screenBtns.append(self.ChatFrame)
        self.screenBtns.append(self.messageBox)
        self.screenBtns.append(self.addFriend)
        self.screenBtns.append(self.usersChatFrame)
        self.screenBtns.append(self.addFriendBox)
        self.printChat()

    def showFriendUsers(self):
        if (self.usersChatFrame != None):
            self.usersChatFrame.destroy()

        self.usersChatFrame = DirectScrolledList(
            decButton_pos= (0.80, 0.0, -0.42),
            decButton_text = "-",
            decButton_text_fg = (1,1,1,1),
            decButton_text_scale = 0.08,
            decButton_frameSize = (-0.035, 0.045, -0.03, 0.04),
            decButton_frameColor = (0.5, 0.5, 0.6, 0.5),
            decButton_borderWidth = (0.01, 0.01),

            incButton_pos= (0.80, 0.0, 0.95),
            incButton_text = "+",
            incButton_text_fg = (1,1,1,1),
            incButton_text_scale = 0.08,
            incButton_frameSize = (-0.035, 0.045, -0.03, 0.04),
            incButton_frameColor = (0.5, 0.5, 0.6, 0.5),
            incButton_borderWidth = (0.01, 0.01),

            frameColor=(0,0,0,0.4),frameSize=(0.0, .75, -0.45, 1.0),pos=(-1.75, 0.0, -0.4),
            #items = [b1, b2],
            numItemsVisible = 14,
            #forceHeight = itemHeight,
            itemFrame_frameSize = (-0.5, 0.6, -0.85, 1),
            itemFrame_pos = (0.35, 0, 0.9),
            itemFrame_frameColor = (0, 0, 1.0, 0),
            text_fg = (1,1,1,1),

            itemFrame_text_bg = (1,1,1,0),
            text_bg = (1,1,1,0),
            text_scale = 0.2
            )

        for friend in self.friends:
            l = DirectLabel(text = friend, text_scale=0.1,
            text_bg = (1,1,1,0), text_fg = (1,1,1,1),
            frameColor = (0,0,0,0))
            print 'Adding '+friend
            self.usersChatFrame.addItem(l)


    def addNewFriend(self):
        self.lastSelectedFriend = self.addFriendBox.get()
        self.World.friendConnection.sendRequestMessage(self.addFriendBox.get())
        pass

    def sendMessage(self):
        print "send", self.WhichScreen
        if self.WhichScreen == "Social":
            if self.isGlobalChat:
                self.World.globalChatConnection.sendChatMessage(self.messageBox.get())
            else:
                if (self.lastSelectedFriend != None):
                    self.World.privateChatConnection.sendChatMessage(self.lastSelectedFriend,self.messageBox.get())
            self.messageBox.enterText('')
            self.messageBox['focus'] = 1


    def printChat(self):
        if self.WhichScreen == "Social":
            if self.isGlobalChat:
                chat = self.globalChat[self.chatOffset:13+self.chatOffset]
            self.ChatFrame.destroy()
            self.ChatFrame = DirectFrame(frameColor=(0,0,0,0.4),frameSize=(0.0, 2.5, -0.45, 0.9),pos=(-0.70, 0.0, -0.3))
            self.screenBtns.append(self.ChatFrame)
            msgNum = 0
            for msg in chat:
                self.screenBtns.append(DirectLabel(text= (str(msg[0]) + ": "+str(msg[1])),
                                               parent = self.ChatFrame,
                                               pos = (0.05, -4.0,-0.4 + 0.1*msgNum), text_scale=0.05,
                                               text_bg = (0,0,0,0),
                                               text_fg = (1,1,1,1),
                                               text_align = TextNode.ALeft,
                                               frameColor = (0,0,0,0)))
                msgNum = msgNum+1



    def createMatchMaking(self):
        self.unloadScreen()
        self.WhichScreen = "Match"
        self.myImage=OnscreenImage(image = 'IMAGES/matchmaking_menu.png', pos = (0, 0, 0), scale = (2, 1, 1))
        self.navi()
        self.dd_btn = DirectButton(image = 'IMAGES/demolition_dirby.png', pos = (-.8, 0, -.2), command=self.ddMaps, scale = (.5, 1, .4), relief = None)
        self.dd_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.rr_btn = DirectButton(image = 'IMAGES/race_royale.png', pos = (0.8, 0, -.2), command=self.rrMaps, scale = (.5, 1, .4), relief = None)
        self.rr_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.screenBtns.append(self.myImage)
        self.screenBtns.append(self.dd_btn)
        self.screenBtns.append(self.rr_btn)



    def ddMaps(self):
        print "ddMaps"
        self.selectedGame = "DD";
        self.unloadScreen()
        self.myImage=OnscreenImage(image = 'IMAGES/matchmaking_menu_map.png', pos = (0, 0, 0), scale = (2, 1, 1))
        self.navi()
        self.map1_btn = DirectButton(image = 'IMAGES/map_1.png', pos = (-.8, 0, -.2), command=self.dd_ScreenMap1, scale = (.5, 1, .4), relief = None)
        self.map1_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.map2_btn = DirectButton(image = 'IMAGES/map_2.png', pos = (0.8, 0, -.2), command=self.dd_ScreenMap2, scale = (.5, 1, .4), relief = None)
        self.map2_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.onReturnMatch = self.ddMaps
        self.screenBtns.append(self.myImage)
        self.screenBtns.append(self.map1_btn)
        self.screenBtns.append(self.map2_btn)


    def rrMaps(self):
        print "rrMaps"
        self.selectedGame = "RR";
        self.unloadScreen()
        self.myImage=OnscreenImage(image = 'IMAGES/matchmaking_menu_map.png', pos = (0, 0, 0), scale = (2, 1, 1))
        self.navi()
        self.map1_btn = DirectButton(image = 'IMAGES/map_1.png', pos = (-.8, 0, -.2), command=self.rr_ScreenMap1, scale = (.5, 1, .4), relief = None)
        self.map1_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.map2_btn = DirectButton(image = 'IMAGES/map_2.png', pos = (0.8, 0, -.2), command=self.rr_ScreenMap2, scale = (.5, 1, .4), relief = None)
        self.map2_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.onReturnMatch = self.rrMaps
        self.screenBtns.append(self.myImage)
        self.screenBtns.append(self.map1_btn)
        self.screenBtns.append(self.map2_btn)

    def addCarButtons(self):
        self.bruiser_btn = DirectButton(image = 'IMAGES/bruiser_btn.png', pos = (-1.1, 0, .2), scale = (.17, 1, .04), relief = None, command=self.carBruiser)
        self.bruiser_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.swift_star_btn = DirectButton(image = 'IMAGES/swift_star_btn.png', pos = (-1.1, 0, .1), scale = (.17, 1, .04), relief = None, command=self.carSwiftStar)
        self.swift_star_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.stallion_btn = DirectButton(image = 'IMAGES/stallion_btn.png', pos = (-1.1, 0, .0), scale = (.17, 1, .04), relief = None, command=self.carStallion)
        self.stallion_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.mystery_car_btn = DirectButton(image = 'IMAGES/mystery_car_btn.png', pos = (-1.1, 0, -.1), scale = (.17, 1, .04), relief = None, command=self.carMystery)
        self.mystery_car_btn.setTransparency(TransparencyAttrib.MAlpha)

        # for DD team must be different command
        selectcommand = None
        if(self.selectedGame == "DD"):
            selectcommand = self.pressDDReady
        else:
            selectcommand = self.pressRRReady
        self.ready_btn = DirectButton(image = 'IMAGES/ready_btn.png', pos = (-1.1, 0, -.3), scale = (.2, 1, .04), relief = None, command=selectcommand)

        self.screenBtns.append(self.bruiser_btn)
        self.screenBtns.append(self.swift_star_btn)
        self.screenBtns.append(self.stallion_btn)
        self.screenBtns.append(self.mystery_car_btn)
        self.screenBtns.append(self.ready_btn)



    def rr_screen(self):
        self.unloadScreen()
        self.myImage=OnscreenImage(image = 'IMAGES/rr_screen.png', pos = (0, 0, 0), scale = (2, 1, 1))
        self.navi()
        self.addCarButtons()
        self.userCount = DirectLabel(text='', pos = (1.5,-4.0,0.475), text_scale=0.10);
        self.userCount['text_fg'] = (0.7,0.7,0.7,0.5);
        self.userMessage = DirectLabel(text='', pos = (1.4,-4.0,0.375), text_scale=0.10);
        self.userMessage['text_fg'] = (0.7,0.7,1.0,0.5);
        self.screenBtns.append(self.userCount)
        self.screenBtns.append(self.userMessage)

        self.screenBtns.append(self.myImage)

        self.onReturnMatch = self.rr_screen

    def dd_screen(self):
        self.unloadScreen()
        self.myImage=OnscreenImage(image = 'IMAGES/dd_screen.png', pos = (0, 0, 0), scale = (2, 1, 1))
        self.navi()
        # Problem: addCarButtons is calling the rrReady
        self.addCarButtons()
        self.userCount = DirectLabel(text='', pos = (1.5,-4.0,0.475), text_scale=0.10);
        self.userCount['text_fg'] = (0.7,0.7,0.7,0.5);
        self.userMessage = DirectLabel(text='', pos = (1.4,-4.0,0.375), text_scale=0.10);
        self.userMessage['text_fg'] = (0.7,0.7,1.0,0.5);
        self.screenBtns.append(self.userCount)
        self.screenBtns.append(self.userMessage)

        #added by genus
        self.screenBtns.append(self.myImage)

        self.onReturnMatch = self.dd_screen


#This code create the customiztion window
    def createCustomization(self):

        self.unloadScreen()
        self.WhichScreen = "Custom"
        self.myImage=OnscreenImage(parent=render2dp, image = 'IMAGES/customization_w2.png', pos = (0, 0, 0), scale = (1, 1, 1))
        base.cam2dp.node().getDisplayRegion(0).setSort(-1)
        self.navi()
        self.bruiser_btn = DirectButton(image = 'IMAGES/bruiser_btn.png', pos = (-1.5, 0, .32), scale = (.17, 1, .04), relief = None)
        self.bruiser_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.swift_star_btn = DirectButton(image = 'IMAGES/swift_star_btn.png', pos = (-1.5, 0, .22), scale = (.17, 1, .04), relief = None, command=self.loadSwiftStar)
        self.swift_star_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.stallion_btn = DirectButton(image = 'IMAGES/stallion_btn.png', pos = (-1.5, 0, .12), scale = (.17, 1, .04), relief = None)
        self.stallion_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.mystery_car_btn = DirectButton(image = 'IMAGES/mystery_car_btn.png', pos = (-1.5, 0, .02), scale = (.17, 1, .04), relief = None, command=self.loadMysteryCar)
        self.mystery_car_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.paint1_btn = DirectButton(image = 'IMAGES/paint1_btn.png', pos = (-1.5, 0, -.22), scale = (.17, 1, .04), relief = None)
        self.paint1_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.paint2_btn = DirectButton(image = 'IMAGES/paint2_btn.png', pos = (-1.5, 0, -.32), scale = (.17, 1, .04), relief = None)
        self.paint2_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.paint3_btn = DirectButton(image = 'IMAGES/paint3_btn.png', pos = (-1.5, 0, -.42), scale = (.17, 1, .04), relief = None)
        self.paint3_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.tire1_btn = DirectButton(image = 'IMAGES/tire1_btn.png', pos = (-1.5, 0, -.64), scale = (.17, 1, .04), relief = None)
        self.tire1_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.tire2_btn = DirectButton(image = 'IMAGES/tire2_btn.png', pos = (-1.5, 0, -.74), scale = (.17, 1, .04), relief = None)
        self.tire2_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.tire3_btn = DirectButton(image = 'IMAGES/tire3_btn.png', pos = (-1.5, 0, -.84), scale = (.17, 1, .04), relief = None)
        self.tire3_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.save_btn = DirectButton(image = 'IMAGES/save_btn.png', pos = (1.5, 0, -.9), scale = (.2, 1, .04), relief = None)

        self.upgrade_btn = DirectButton(image = 'IMAGES/upgrades_btn.png', pos = (1, 0, -.9), scale = (.2, 1, .04), relief = None)

        self.screenBtns.append(self.myImage)
        self.screenBtns.append(self.bruiser_btn)
        self.screenBtns.append(self.swift_star_btn)
        self.screenBtns.append(self.stallion_btn)
        self.screenBtns.append(self.mystery_car_btn)
        self.screenBtns.append(self.paint1_btn)
        self.screenBtns.append(self.paint2_btn)
        self.screenBtns.append(self.paint3_btn)
        self.screenBtns.append(self.tire1_btn)
        self.screenBtns.append(self.tire2_btn)
        self.screenBtns.append(self.tire3_btn)
        self.screenBtns.append(self.save_btn)
        self.screenBtns.append(self.upgrade_btn)
        base.disableMouse()
        base.camLens.setFov(40)
        plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 1))
        self.plnp = render.attachNewNode(plight)
        self.plnp.setPos(0, 5, 0)
        render.setLight(self.plnp)

    def loadSwiftStar(self):
        if self.car is not None:
            self.car.removeNode()
        self.car = loader.loadModel("models/swiftstar")
        self.car.reparentTo(render)
        self.car.setScale(.2)
        self.car.setPos(.6,8.5,-.9)
        self.car.setH(150)
        rotation_interval = self.car.hprInterval(10,Vec3(510,0,0))
        rotation_interval.loop()


    def loadMysteryCar(self):
        if self.car is not None:
            self.car.removeNode()
        self.car = loader.loadModel("models/batmobile-customized")
        self.car.setLightOff()
        self.car.setRenderModeWireframe()
        self.car.reparentTo(render)
        self.car.setScale(.3)
        self.car.setPos(.6,8.5,-.9)
        self.car.setH(150)
        rotation_interval = self.car.hprInterval(10,Vec3(510,0,0))
        rotation_interval.loop()

    def dd_ScreenMap1(self):
        self.World.queueConnection.sendQueueMessage(0) #0=map1
        print "Screen Map 1"
        self.dd_screen()

    def dd_ScreenMap2(self):
        self.World.queueConnection.sendQueueMessage(1) #1=map2
        print "Screen Map 2"
        self.dd_screen()

    def rr_ScreenMap1(self):
        self.World.queueConnection.sendQueueMessage(2) #2=map3
        print "Screen Map 3"
        self.rr_screen()

    def rr_ScreenMap2(self):
        self.World.queueConnection.sendQueueMessage(3) #3=map4
        print "Screen Map 4"
        self.rr_screen()

    def carBruiser(self):
        self.enableReady(1) #Bruiser

    def carSwiftStar(self):
        self.enableReady(2) #SwiftStar

    def carStallion(self):
        self.enableReady(3) #Stallion

    def carMystery(self):
        self.enableReady(4) #Mystery

    def handleQueueNotification(self, size, sizeNeeded, players):
        print "Received Handle Queue MAX_PLAYERS: ", sizeNeeded
        start = False
        if (len(players) >= sizeNeeded):
            self.userCount['text'] = str(len(players)) + ' / '+ str(size)
            self.userMessage['text'] = 'Ready to start'
            start = True
            print "Ready to go players list", players
            for val in players:
                print val
                if val != None and len(val) >= sizeNeeded and val[1] == 0:
                    start = False
                    break
        else:
            self.userCount['text'] = str(len(players)) + ' / '+ str(sizeNeeded)
            self.userMessage['text'] = 'More players needed'
        self.showUsers(players)
        if start:
            self.launchDDGame()
            #self.launchRRGame()

    def handleChatNotification(self, username, msg):
        self.globalChat.insert(0, [username, msg])
        print username, msg
        self.printChat()

    def handleFriendNotification(self, fromName, status):
        print "Recieved friend notification"

        self.friendRequestFrom = fromName
        self.acceptFriendDialog = YesNoDialog(text = "Do you want "+fromName+" to be your friend?", command=self.acceptFriend)
        pass

    def handleFriendListNotification(self, friends):
        print "Recieved friend list notification"

        self.friends = friends
        self.showFriendUsers()
        pass


    def acceptFriend(self, clickedYes):
        self.acceptFriendDialog.cleanup()
        if clickedYes:
            self.World.friendConnection.sendUpdateMessage(self.friendRequestFrom,0)
        else:
            self.World.friendConnection.sendUpdateMessage(self.friendRequestFrom,1)


    def handlePrivateChatNotification(self, username, msg):
        self.globalChat.insert(0, ['Private: '+username, msg])
        print 'private ', username, msg
        self.printChat()

    def enableReady(self, selectedCar):
        if (self.selectedCar == selectedCar):
            self.selectedCar = 0 #remove selection
        else:
            self.selectedCar = selectedCar

        if (self.selectedCar == 0):
            self.ready_btn['image'] = 'IMAGES/ready_btn.png'
            self.ready_btn['state'] = DGG.DISABLED
        else:
            self.ready_btn['image'] = 'IMAGES/ready_btn_inv.png'
            self.ready_btn['state'] = DGG.NORMAL

        self.bruiser_btn['image'] = 'IMAGES/bruiser_btn.png'
        self.swift_star_btn['image'] = 'IMAGES/swift_star_btn.png'
        self.stallion_btn['image'] = 'IMAGES/stallion_btn.png'
        self.mystery_car_btn['image'] = 'IMAGES/mystery_car_btn.png'

        if (self.selectedCar == 1):
            self.bruiser_btn['image'] = 'IMAGES/bruiser_btn_inv.png'
            #change image
        elif (self.selectedCar == 2):
            self.swift_star_btn['image'] = 'IMAGES/swift_star_btn_inv.png'
        elif (self.selectedCar == 3):
            self.stallion_btn['image'] = 'IMAGES/stallion_btn_inv.png'
        elif (self.selectedCar == 4):
            self.mystery_car_btn['image'] = 'IMAGES/mystery_car_btn_inv.png'

    def pressDDReady(self):
        if (self.selectedCar == 0):
            return
        print "Car selected: ", self.selectedCar
        self.World.queueConnection.sendReadyMessage(self.selectedCar)
        print "DD Ready pressed " , self.selectedCar
        # Call the DD World from here

    def launchDDGame(self):
        print "Launching DD GAME"
        self.World.ServerConnection.activeStatus = False
        self.unloadScreen()
        self.World.stopMusic()
        self.ddworld = WorldManager(self)
        #data might be require to send to DD world

    def pressRRReady(self):

        if (self.selectedCar == 0):
            return
        self.World.queueConnection.sendReadyMessage(self.selectedCar)
        print "RR Ready pressed ", self.selectedCar

    def launchRRGame(self):
        print "Launching RR GAME"
        self.World.ServerConnection.activeStatus = False
        self.unloadScreen()
        self.rrworld = RRWorldManager(self)
        # data might be require to send to DD world

    def showUsers(self, players):
        #print "showUsers"
        numItemsVisible = 8
        itemHeight = 0.11
        if (hasattr(self, "myScrolledList")) and (not self.myScrolledList is None):
            self.myScrolledList.destroy()
        self.myScrolledList = DirectScrolledList(
            decButton_pos= (0.35, 0.5, 0.5),
            decButton_text = "-",
            decButton_text_fg = (1,1,1,1),
            decButton_text_scale = 0.08,
            decButton_frameSize = (-0.035, 0.045, -0.03, 0.04),
            decButton_frameColor = (0.5, 0.5, 0.6, 0.5),
            decButton_borderWidth = (0.01, 0.01),

            incButton_pos= (0.35, 0.5, -0.5),
            incButton_text = "+",
            incButton_text_fg = (1,1,1,1),
            incButton_text_scale = 0.08,
            incButton_frameSize = (-0.035, 0.045, -0.03, 0.04),
            incButton_frameColor = (0.5, 0.5, 0.6, 0.5),
            incButton_borderWidth = (0.01, 0.01),

            frameSize = (0.7, 0.7, -.5, 1),
            frameColor = (0, 0, 1.0, 1),
            pos = (0.5, 0, -0.3),
            #items = [b1, b2],
            numItemsVisible = numItemsVisible,
            forceHeight = itemHeight,
            itemFrame_frameSize = (-0.5, 0.6, -0.85, 0.11),
            itemFrame_pos = (0.35, 0, 0.4),
            itemFrame_frameColor = (0, 0, 1.0, 0),
            text_fg = (1,1,1,1),

            itemFrame_text_bg = (1,1,1,0),
            text_bg = (1,1,1,0),
            text_scale = 0.2
            )

        for player in players:
            #print "PLAYERS GOT"
            l = DirectLabel(text = player[0], text_scale=0.1,
            text_bg = (1,1,1,0), text_fg = (1,1,1,1),
            frameColor = (0,0,0,0))
            if (player[1]): #player ready
                l['text'] = '         '+ l['text'] + ' (READY!)'
            if player[0] not in self.playerList:
                self.playerList.append(player[0])
            print 'Adding '+player[0]
            self.myScrolledList.addItem(l)
        self.screenBtns.append(self.myScrolledList)
            
    def unloadScreen(self):
        for btn in self.screenBtns:
            btn.destroy()
