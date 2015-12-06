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
from Network.models.GroupConnectionModel import GroupConnectionModel

class Menu(ShowBase):

    def __init__(self, World):
        #just comment out the two lines below
        #self.appRunner = None#added this to overide the login

        self.World = World
        self.ServerConnection = self.World.ServerConnection
        self.WhichScreen = "";
        self.lastSelectedFriend = None

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
        self.privateChatSeen = {}
        self.chatOffset = 0
        self.car = None
        self.groupMembers = []

        self.onReturnMatch = self.createMatchMaking



        self.privateChatConnection = PrivateChatConnectionModel()
        self.privateChatConnection.setHandler(self.handlePrivateChatNotification)
        self.ServerConnection.setupConnectionModel(self.privateChatConnection)

        self.globalChatConnection = ChatConnectionModel(self)
        self.globalChatConnection.setHandler(self.handleChatNotification)
        self.ServerConnection.setupConnectionModel(self.globalChatConnection)

        self.queueConnection = QueueConnectionModel(self)
        self.queueConnection.setHandler(self.handleQueueNotification)
        self.ServerConnection.setupConnectionModel(self.queueConnection)

        self.groupConnection = GroupConnectionModel(self)
        self.groupConnection.setHandler(self.receiveInvite, self.updateGroup)
        self.ServerConnection.setupConnectionModel(self.groupConnection)


        self.friendConnection = FriendConnectionModel(self)
        self.friendConnection.setHandlers(self.handleFriendNotification,self.handleFriendListNotification)
        self.ServerConnection.setupConnectionModel(self.friendConnection)

        self.createSocialization()
        self.navi()


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
        self.friendConnection.sendFriendListRequest()
        self.friends_btn = DirectButton(image = 'IMAGES/friends_btn.png', pos = (-0.5, 0, -.87), scale = (.2, 1, .04), relief = None, command = self.setFriend)
        self.ntwork = DirectButton(image = 'IMAGES/global_btn_s.png', pos = (0, 0, -.87), scale = (.2, 1, .04), relief = None, command = self.setGlobal)
        self.send = DirectButton(image = 'IMAGES/send_btn.png', pos = (1.5, 0, -.87), scale = (.2, 1, .04), relief = None, command = self.sendMessage)
        self.addFriend = DirectButton(image = 'IMAGES/plus_friends_btn.png', pos = (-0.965, 0, -.88),  scale = (.17, 1, .03), relief = None, command = self.addNewFriend)
        self.addFriendBox = DirectEntry(text = "" , width=12,frameSize=(0, 12, -0.2, 1),pos = (-1.745,0.0,-0.9), scale=.05, initialText="")

        self.isGlobalChat = True
        #chat messages
        self.ChatFrame = DirectFrame(frameColor=(0,0,0,0.4),frameSize=(0.0, 2.5, -0.45, 0.9),pos=(-0.70, 0.0, -0.3))
        self.messageBox = DirectEntry(text = "" , width=50,frameSize=(0, 50, -0.2, 1),pos = (-0.70,0.0,-0.81), scale=.05, initialText="", command = self.sendMessage)

        #this lists the friends who are currently logged in

        self.usersFriendFrame = DirectScrolledList(
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
        self.screenBtns.append(self.friends_btn)
        self.screenBtns.append(self.ntwork)
        self.screenBtns.append(self.send)
        self.screenBtns.append(self.ChatFrame)
        self.screenBtns.append(self.messageBox)
        self.screenBtns.append(self.addFriend)
        self.screenBtns.append(self.addFriendBox)
        self.screenBtns.append(self.usersFriendFrame)
        self.printChat()

    def setFriend(self):
        self.friends_btn['image'] = 'IMAGES/friends_btn_s.png'
        self.ntwork['image'] = 'IMAGES/global_btn.png'
        self.isGlobalChat = False

        self.printChat()

    def setGlobal(self):
        self.friends_btn['image'] = 'IMAGES/friends_btn.png'
        self.ntwork['image'] = 'IMAGES/global_btn_s.png'
        self.isGlobalChat = True
        self.printChat()

    def showFriendUsers(self):
        if self.WhichScreen != "Social":
            return
        if (self.usersFriendFrame != None):
            self.usersFriendFrame.destroy()

        self.usersFriendFrame = DirectScrolledList(
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
            forceHeight = 0.15,
            itemFrame_frameSize = (-0.5, 0.6, -0.85, 1),
            itemFrame_pos = (0.35, 0, 0.9),
            itemFrame_frameColor = (0, 0, 1.0, 0),
            text_fg = (1,1,1,1),

            itemFrame_text_bg = (1,1,1,0),
            text_bg = (1,1,1,0),
            text_scale = 0.2
            )

        for friend in self.friends:
            f = DirectFrame(frameColor=(0, 0, 0, 0),
                      frameSize=(-1, 1, -1, 1))
            l = DirectButton(text = friend, text_scale=0.1,
            text_bg = (0.5,0.5,0,0.6) if friend == self.lastSelectedFriend else
            ((1,1,1,0) if self.privateChatSeen.setdefault(friend, True) else (0.3, 0.8, 0.7, 0.4)), text_fg = (1,1,1,1),
            frameColor = (0,0,0,0), parent = f, pos=(-0.1,0,0),command = self.selectFriend, extraArgs = [friend])
            g = DirectButton(image="IMAGES/plus_btn.png",frameColor = (0,0,0,0),
            parent = f, pos=(0.34,0,0), scale = (0.05,0.05,0.05), command = self.inviteToGroup, extraArgs = [friend])
            if friend in self.groupMembers and self.privateChatSeen.setdefault(friend, True) and not friend == self.lastSelectedFriend:
                l["text_bg"] = (0.6,0.8,0.8,0.2)
            if friend == self.lastSelectedFriend: self.lastSelectedButton = l
            l["extraArgs"].append(l)
            print 'Adding '+friend
            self.usersFriendFrame.addItem(f)

        self.screenBtns.append(self.usersFriendFrame)

    def selectFriend(self, friend, button):
        self.lastSelectedFriend = friend
        if(hasattr(self, "lastSelectedButton") and not self.lastSelectedButton is None):
            self.lastSelectedButton['text_bg'] = (1,1,1,0)
        button['text_bg'] = (0.5,0.5,0,0.6)
        self.lastSelectedButton = button
        if not self.isGlobalChat:
            self.printChat()

    def addNewFriend(self):
        self.friendConnection.sendRequestMessage(self.addFriendBox.get())
        pass

    def inviteToGroup(self, friend):
        self.groupConnection.sendInviteMessage(friend)

    def sendMessage(self, message = []):
        print "send", self.WhichScreen
        if message == []: message = self.messageBox.get()
        if self.WhichScreen == "Social":
            if self.isGlobalChat:
                self.globalChatConnection.sendChatMessage(message)
            else:
                if (self.lastSelectedFriend != None):
                    self.privateChatConnection.sendChatMessage(self.lastSelectedFriend,message)
            self.messageBox.enterText('')
            self.messageBox['focus'] = 1


    def printChat(self):
        if self.WhichScreen == "Social":
            if self.isGlobalChat:
                chat = self.globalChat[self.chatOffset:13+self.chatOffset]
            else:
                chat = self.privateChat.setdefault(self.lastSelectedFriend,[])[self.chatOffset:13+self.chatOffset]
                self.privateChatSeen[self.lastSelectedFriend] = True
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

        self.ready_btn = DirectButton(image = 'IMAGES/ready_btn.png', pos = (-1.1, 0, -.3), scale = (.2, 1, .04), relief = None, command=self.pressRRReady)

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

        self.onReturnMatch = self.rr_screen

    def dd_screen(self):
        self.unloadScreen()
        self.myImage=OnscreenImage(image = 'IMAGES/dd_screen.png', pos = (0, 0, 0), scale = (2, 1, 1))
        self.navi()
        self.addCarButtons()
        self.userCount = DirectLabel(text='', pos = (1.5,-4.0,0.475), text_scale=0.10);
        self.userCount['text_fg'] = (0.7,0.7,0.7,0.5);
        self.userMessage = DirectLabel(text='', pos = (1.4,-4.0,0.375), text_scale=0.10);
        self.userMessage['text_fg'] = (0.7,0.7,1.0,0.5);
        self.screenBtns.append(self.userCount)
        self.screenBtns.append(self.userMessage)

        self.onReturnMatch = self.dd_screen


#This code create the customiztion window
    def createCustomization(self):

        self.unloadScreen()
        self.WhichScreen = "Custom"
        self.myImage = OnscreenImage(parent=render2dp,
                                     image = 'IMAGES/customization_w.png',
                                     pos = (0, 0, 0),
                                     scale = (1, 1, 1))
        base.cam2dp.node().getDisplayRegion(0).setSort(-1)
        self.navi()
        self.bruiser_btn = DirectButton(image = 'IMAGES/bruiser_btn.png',
                                        pos = (-1.5, 0, .32),
                                        scale = (.17, 1, .04),
                                        relief = None,
                                        command=self.loadBruiser)
        self.bruiser_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.swift_star_btn = DirectButton(image = 'IMAGES/swift_star_btn.png',
                                           pos = (-1.5, 0, .22),
                                           scale = (.17, 1, .04),
                                           relief = None,
                                           command=self.loadSwiftStar)
        self.swift_star_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.stallion_btn = DirectButton(image = 'IMAGES/stallion_btn.png',
                                         pos = (-1.5, 0, .12),
                                         scale = (.17, 1, .04),
                                         relief = None,
                                         command=self.loadStallion)
        self.stallion_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.mystery_car_btn = DirectButton(image = 'IMAGES/mystery_car_btn.png',
                                            pos = (-1.5, 0, .02),
                                            scale = (.17, 1, .04),
                                            relief = None,
                                            command=self.loadMysteryCar)
        self.mystery_car_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.paint1_btn = DirectButton(image = 'IMAGES/paint1_btn.png',
                                       pos = (-1.5, 0, -.22),
                                       scale = (.17, 1, .04),
                                       relief = None)
        self.paint1_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.paint2_btn = DirectButton(image = 'IMAGES/paint2_btn.png',
                                       pos = (-1.5, 0, -.32),
                                       scale = (.17, 1, .04),
                                       relief = None)
        self.paint2_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.paint3_btn = DirectButton(image = 'IMAGES/paint3_btn.png',
                                       pos = (-1.5, 0, -.42),
                                       scale = (.17, 1, .04),
                                       relief = None)
        self.paint3_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.tire1_btn = DirectButton(image = 'IMAGES/tire1_btn.png',
                                      pos = (-1.5, 0, -.64),
                                      scale = (.17, 1, .04),
                                      relief = None)
        self.tire1_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.tire2_btn = DirectButton(image = 'IMAGES/tire2_btn.png',
                                      pos = (-1.5, 0, -.74),
                                      scale = (.17, 1, .04),
                                      relief = None)
        self.tire2_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.tire3_btn = DirectButton(image = 'IMAGES/tire3_btn.png',
                                      pos = (-1.5, 0, -.84),
                                      scale = (.17, 1, .04),
                                      relief = None)
        self.tire3_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.save_btn = DirectButton(image = 'IMAGES/save_btn.png',
                                     pos = (1.5, 0, -.9),
                                     scale = (.2, 1, .04),
                                     relief = None)

        self.upgrade_btn = DirectButton(image = 'IMAGES/upgrades_btn.png',
                                        pos = (1, 0, -.9),
                                        scale = (.2, 1, .04),
                                        relief = None)
                                        
#This is the current level of the upgrades. This variable should correspond to what ever is in the 
#database. 
		current_level = 0
        self.power_btn = DirectButton(image = 'IMAGES/power.png',
                                      pos = (-.9, 0, -.75),
                                      scale = (.1, 1, .1),
                                      relief = None,
                                      command=self.power_function(current_level))
        self.power_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.handling_btn = DirectButton(image = 'IMAGES/handling.png',
                                         pos = (-.6, 0, -.75),
                                         scale = (.1, 1, .1),
                                         relief = None,
                                         command=self.handling_function(current_level))
        self.handling_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.armor_btn = DirectButton(image = 'IMAGES/armor.png',
                                      pos = (-.3, 0, -.75),
                                      scale = (.1, 1, .1),
                                      relief = None,
                                      command=self.armor_function(current_level))
        self.armor_btn.setTransparency(TransparencyAttrib.MAlpha)

        self.speed_btn = DirectButton(image = 'IMAGES/speed.png',
                                      pos = (0, 0, -.75),
                                      scale = (.1, 1, .1),
                                      relief = None,
                                      command=self.speed_function(current_level))
        self.speed_btn.setTransparency(TransparencyAttrib.MAlpha)
        


        self.screenBtns.append(self.power_btn)
        self.screenBtns.append(self.handling_btn)
        self.screenBtns.append(self.armor_btn)
        self.screenBtns.append(self.speed_btn)
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
        self.plnp.setPos(1.4, 8, 1)
        render.setLight(self.plnp)
#Below are the functions for the upgrades. When a button is clicked it should displayMeter function further
#below with its corresponding level of the meter and the cost of the level to upgrade.


	def armor_function(self, level):
		if level == 0:
			self.displayMeter(level)
			self.displayCost(level)
		
		elif level == 1:
			self.displayMeter(level)
			self.displayCost(level)	

		elif level == 2:
			self.displayMeter(level)
			self.displayCost(level)		
	
		elif level == 3:
			self.displayMeter(level)
			self.displayCost(level)	
	
		elif level == 4:
			self.displayMeter(level)
			self.displayCost(level)	

		elif level == 5:	
			self.displayMeter(level)
			self.displayCost(level)
	
		elif level == 6:
			self.displayMeter(level)
			self.displayCost(level)	
	
		else:
			self.displayMeter(7)
			self.displayCost(7)	
	
	def power_function(self, level):

		if level == 0:
			self.displayMeter(level)
			self.displayCost(level)
		
		elif level == 1:
			self.displayMeter(level)
			self.displayCost(level)	

		elif level == 2:
			self.displayMeter(level)
			self.displayCost(level)		
	
		elif level == 3:
			self.displayMeter(level)
			self.displayCost(level)	
	
		elif level == 4:
			self.displayMeter(level)
			self.displayCost(level)	

		elif level == 5:	
			self.displayMeter(level)
			self.displayCost(level)
	
		elif level == 6:
			self.displayMeter(level)
			self.displayCost(level)	
	
		else:
			self.displayMeter(7)
			self.displayCost(7)
			
	def handling_function(self, level):

		if level == 0:
			self.displayMeter(level)
			self.displayCost(level)
		
		elif level == 1:
			self.displayMeter(level)
			self.displayCost(level)	

		elif level == 2:
			self.displayMeter(level)
			self.displayCost(level)		
	
		elif level == 3:
			self.displayMeter(level)
			self.displayCost(level)	
	
		elif level == 4:
			self.displayMeter(level)
			self.displayCost(level)	

		elif level == 5:	
			self.displayMeter(level)
			self.displayCost(level)
	
		elif level == 6:
			self.displayMeter(level)
			self.displayCost(level)	
	
		else:
			self.displayMeter(7)
			self.displayCost(7)	

					
	def speed_function(self, level):
		
		if level == 0:
			self.displayMeter(level)
			self.displayCost(level)
		
		elif level == 1:
			self.displayMeter(level)
			self.displayCost(level)	

		elif level == 2:
			self.displayMeter(level)
			self.displayCost(level)		
	
		elif level == 3:
			self.displayMeter(level)
			self.displayCost(level)	
	
		elif level == 4:
			self.displayMeter(level)
			self.displayCost(level)	

		elif level == 5:	
			self.displayMeter(level)
			self.displayCost(level)
	
		elif level == 6:
			self.displayMeter(level)
			self.displayCost(level)	
	
		else:
			self.displayMeter(7)
			self.displayCost(7)	

					
    def displayMeter(self, level):
		
        self.power_btn = DirectButton(image = 'IMAGES/meters/'+str(level)+'.png',
                                      pos = (-.6, 0, 0),
                                      scale = (.35, 1, .5),
                                      relief = None)
        self.power_btn.setTransparency(TransparencyAttrib.MAlpha)
#This is the cost for each upgrade.
	def displayCost(self, level):
		cost = 0
		if level == 0:
			cost =100
			textObject = OnscreenText(text = str(cost), pos = (0.18, -.567), scale = 0.07, fg= (1,1,1,1))
		
		elif level == 1:
			cost =200	
			textObject = OnscreenText(text = str(cost), pos = (0.18, -.567), scale = 0.07, fg= (1,1,1,1))
		elif level == 2:
			cost =300		
			textObject = OnscreenText(text = str(cost), pos = (0.18, -.567), scale = 0.07, fg= (1,1,1,1))	
		elif level == 3:
			cost =500	
			textObject = OnscreenText(text = str(cost), pos = (0.18, -.567), scale = 0.07, fg= (1,1,1,1))	
		elif level == 4:
			cost =800	
			textObject = OnscreenText(text = str(cost), pos = (0.18, -.567), scale = 0.07, fg= (1,1,1,1))
		elif level == 5:
			cost =1300	
			textObject = OnscreenText(text = str(cost), pos = (0.18, -.567), scale = 0.07, fg= (1,1,1,1))	
		elif level == 6:
			cost =2100	
			textObject = OnscreenText(text = str(cost), pos = (0.18, -.567), scale = 0.07, fg= (1,1,1,1))	
		else:
			textObject = OnscreenText(text = "Max out", pos = (0.18, -.567), scale = 0.07, fg= (1,1,1,1))				
		
    def loadBruiser(self, texture = None):
        if self.car is not None:
            self.car.removeNode()
        self.car = loader.loadModel("models/bruiser")
        self.car.reparentTo(render)
        self.car.setScale(.4)
        self.car.setPos(2,11.5,-.6)
        self.car.setH(150)
        rotation_interval = self.car.hprInterval(10,Vec3(510,0,0))
        rotation_interval.loop()

    def loadStallion(self, texture = None):
        if self.car is not None:
            self.car.removeNode()
        self.car = loader.loadModel("models/stallion")
        self.car.reparentTo(render)
        self.car.setScale(.2)
        self.car.setPos(2,11.5,-.6)
        self.car.setH(150)
        rotation_interval = self.car.hprInterval(10,Vec3(510,0,0))
        rotation_interval.loop()

    def loadSwiftStar(self, texture = None):
        if self.car is not None:
            self.car.removeNode()
        self.car = loader.loadModel("models/swiftstar")
        self.wheels = loader.loadModel("models/swiftstar-wheels")
        tex = loader.loadTexture("models/tex/swiftstar_tire2.jpg")
        self.wheels.setTexture(tex, 1)
        self.car.reparentTo(render)
        self.car.setScale(.25)
        self.car.setPos(2,11.5,-.6)
        self.car.setH(150)
        rotation_interval = self.car.hprInterval(10,Vec3(510,0,0))
        rotation_interval.loop()
        self.wheels.reparentTo(render)
        self.wheels.setScale(.25)
        self.wheels.setPos(2,11.5,-.6)
        self.wheels.setH(150)
        rotation_interval2 = self.wheels.hprInterval(10,Vec3(510,0,0))
        rotation_interval2.loop()

    def loadMysteryCar(self):
        if self.car is not None:
            self.car.removeNode()
        self.car = loader.loadModel("models/batmobile-customized")
        self.car.setLightOff()
        self.car.setRenderModeWireframe()
        self.car.reparentTo(render)
        self.car.setScale(.4)
        self.car.setPos(2,11.5,-.6)
        self.car.setH(150)
        rotation_interval = self.car.hprInterval(10,Vec3(510,0,0))
        rotation_interval.loop()

    def dd_ScreenMap1(self):
        self.queueConnection.sendQueueMessage(0) #0=map1
        print "Screen Map 1"
        self.dd_screen()

    def dd_ScreenMap2(self):
        self.queueConnection.sendQueueMessage(1) #1=map2
        print "Screen Map 2"
        self.dd_screen()

    def rr_ScreenMap1(self):
        self.queueConnection.sendQueueMessage(2) #2=map3
        print "Screen Map 3"
        self.rr_screen()

    def rr_ScreenMap2(self):
        self.queueConnection.sendQueueMessage(3) #3=map4
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
        print "Received Handle Queue"
        if (len(players) >= sizeNeeded):
            self.userCount['text'] = str(len(players)) + ' / '+ str(size)
            self.userMessage['text'] = 'Ready to start'
        else:
            self.userCount['text'] = str(len(players)) + ' / '+ str(sizeNeeded)
            self.userMessage['text'] = 'More players needed'
        self.showUsersInLobby(players)

    def handleChatNotification(self, username, msg):
        self.globalChat.insert(0, [username, msg])

        print username, msg
        self.printChat()

    def handleFriendNotification(self, fromName, status):
        print "Recieved friend notification"

        self.friendRequestFrom = fromName
        self.acceptFriendDialog = YesNoDialog(text = "Do you want "+fromName+" to be your friend?", command=self.acceptFriend)


    def receiveInvite(self, fromName):
        print "Recieved friend notification"

        self.groupRequestFrom = fromName
        self.acceptGroupDialog = YesNoDialog(text = "Do you want to join "+fromName+"'s group?", command=self.acceptGroup)

    def acceptGroup(self, clickedYes):
        self.acceptGroupDialog.cleanup()
        self.acceptFriendDialog.cleanup()
        if clickedYes:
            self.groupConnection.sendResponseMessage(self.friendRequestFrom,0)
        else:
            self.groupConnection.sendResponseMessage(self.friendRequestFrom,1)

    def updateGroup(self, members):
        self.groupMembers = members

    def handleFriendListNotification(self, friends):
        print "Recieved friend list notification"

        self.friends = friends
        self.showFriendUsers()
        pass


    def acceptFriend(self, clickedYes):
        self.acceptFriendDialog.cleanup()
        if clickedYes:
            self.friendConnection.sendUpdateMessage(self.friendRequestFrom,0)
        else:
            self.friendConnection.sendUpdateMessage(self.friendRequestFrom,1)


    def handlePrivateChatNotification(self, username, msg, isSelf):
        self.privateChat.setdefault(username, []).insert(0, [username if isSelf else self.World.username, msg])
        self.privateChatSeen[username] = False
        print 'private ', username, msg
        self.printChat()
        self.showFriendUsers()

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
        self.queueConnection.sendReadyMessage(self.selectedCar)
        print "DD Ready pressed " , self.selectedCar

    def pressRRReady(self):

        if (self.selectedCar == 0):
            return
        self.queueConnection.sendReadyMessage(self.selectedCar)
        print "RR Ready pressed " , self.selectedCar

    def showUsersInLobby(self, playersInLobby):
        print "showUsersInLobby"
        numItemsVisible = 8
        itemHeight = 0.11
        if (hasattr(self, "usersInLobbyList")) and (not self.usersInLobbyList is None):
            self.usersInLobbyList.destroy()
        self.usersInLobbyList = DirectScrolledList(
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

        for player in playersInLobby:
            l = DirectLabel(text = player[0], text_scale=0.1,
            text_bg = (1,1,1,0), text_fg = (1,1,1,1),
            frameColor = (0,0,0,0))
            if (player[1]): #player ready
                l['text'] = '         '+ l['text'] + ' (READY!)'
            print 'Adding '+player[0]
            self.usersInLobbyList.addItem(l)
        self.screenBtns.append(self.usersInLobbyList)

    def unloadScreen(self):
        for btn in self.screenBtns:
            btn.destroy()
