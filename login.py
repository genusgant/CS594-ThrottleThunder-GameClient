from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import *
from panda3d.core import TransparencyAttrib
from direct.gui.DirectGui import *
from pandac.PandaModules import WindowProperties
from Network.models.AuthConnectionModel import AuthConnectionModel
from Network.models.NullConnectionModel import NullConnectionModel
from Network.models.HeartbeatConnectionModel import HeartbeatConnectionModel
from Network.ServerConnection import ServerConnection


from direct.task.TaskManagerGlobal import taskMgr

import random, sys, os, math, json

def doPass():
    pass

class Login(ShowBase):

    def __init__(self, World):
        self.appRunner = None
        self.World = World

        self.taskMgr = World.taskMgr
        self.createLoginWindow()

        self.hasClickedRegister = False

    def createLoginWindow(self):

        self.myImage = OnscreenImage(image='IMAGES/game_login.png', pos=(0, 0, 0), scale=(2, 1, 1))

        self.enter_btn = DirectButton(image='IMAGES/enter.png', pos=(-1.4, 0, -.5), scale=(.15, 1, .04),
                                      command=self.auth, relief=None)

        self.register_btn = DirectButton(image='IMAGES/register.png', pos=(-1, 0, -.5), command=self.clickedRegister, scale=(.15, 1, .04), relief=None)


        self.userTextbox = DirectEntry(text="" , scale=.05, pos=(-1.4, 0, 0.1), command=self.setUserText, initialText="", numLines=1, focus=1, focusInCommand=doPass, focusOutCommand=self.getUserText)

        self.passTextbox = DirectEntry(text="" , scale=.05, pos=(-1.4, 0, -.2), command=self.setPassText, initialText="", numLines=1, focus=0, focusInCommand=doPass, obscured=1, focusOutCommand=self.getPassText)

        self.enter_btn['state'] = DGG.NORMAL

        self.ignore('tab')
        self.ignore('enter')

        self.accept('tab', self.cycleLoginBox)
        self.accept('enter', self.auth)


        self.status = OnscreenText(text="", pos=(-0.5, -0.7, 0), scale=0.075, fg=(1, 1, 0, 1), align=TextNode.ACenter)

    def createRegisterWindow(self):


        self.myImage = OnscreenImage(image='IMAGES/game_register.png', pos=(0, 0, 0), scale=(2, 1, 1))

        self.cancel_btn = DirectButton(image='IMAGES/cancel.png', pos=(-1, 0, -.5), command=self.clickedRegCancel, scale=(.15, 1, .04), relief=None)

        self.register_btn = DirectButton(image='IMAGES/register.png', pos=(-1.4, 0, -.5), command=self.reg, scale=(.15, 1, .04), relief=None)

        self.regInputUser = DirectEntry(text="" , scale=.05, pos=(-1.4, 0, 0.1), command=self.setUserText, initialText="", numLines=1, focus=1, focusInCommand=doPass, focusOutCommand=self.getRegUserText)

        self.regInputPass = DirectEntry(text="" , scale=.05, pos=(-1.4, 0, -0.1), command=self.setPassText, initialText="", numLines=1, focus=0, focusInCommand=doPass, obscured=1, focusOutCommand=self.getRegPassText)

        self.regInputCPass = DirectEntry(text="" , scale=.05, pos=(-1.4, 0, -.3), command=self.setPassText, initialText="", numLines=1, focus=0, focusInCommand=doPass, obscured=1, focusOutCommand=self.testRegPassText)

        self.hasClickedRegister = True

        self.ignore('tab')
        self.ignore('enter')

        self.accept('tab', self.cycleRegisterBox)
        self.accept('enter', self.reg)

        self.status = OnscreenText(text=self.status['text'], pos=(-0.5, -0.7, 0), scale=0.075, fg=(1, 1, 0, 1), align=TextNode.ACenter)

    def setUserText(self, textEntered):
        print "username: ", textEntered
        self.usernameInput = textEntered

    def setPassText(self, textEntered):
        print "password: ", textEntered
        self.passwordInput = textEntered

    def clearPassText(self):
        self.passTextbox.enterText('')

    def clearUserText(self):
        self.userTextbox.enterText('')

    def getUserText(self):
        self.usernameInput = self.userTextbox.get()
        return self.usernameInput

    def getPassText(self):
        self.passwordInput = self.passTextbox.get()
        return self.passwordInput


    def getRegUserText(self):
        self.RegUsername = self.regInputUser.get()
        return self.RegUsername

    def getRegPassText(self):
        self.RegPassword = self.regInputPass.get()
        return self.RegPassword

    def testRegPassText(self):

        return self.getRegPassText() == self.regInputCPass.get()

    def unloadScreen(self):
        self.ignoreAll()
        self.destroyLoginWindow()
        self.status.destroy()
        if self.hasClickedRegister:
            self.destroyRegisterWindow()

    def auth(self):
        self.getPassText()
        self.getUserText()
        if(self.usernameInput == ""):
            if(self.passwordInput == ""):
                self.setStatusText("ERROR: You must enter a username and password before logging in.")
            else:
                self.setStatusText("ERROR: You must specify a username")
            self.passTextbox['focus'] = 0
            self.userTextbox['focus'] = 1

        elif(self.passwordInput == ""):
            self.setStatusText("ERROR: You must enter a password")
            self.userTextbox['focus'] = 0
            self.passTextbox['focus'] = 1


        else:
            self.setStatusText("Attempting to log in...")
            self.enter_btn['state'] = DGG.DISABLED
            self.register_btn['state'] = DGG.DISABLED
            self.World.username = self.usernameInput
            self.World.authConnection.sendLoginRequest(self.usernameInput, self.passwordInput)

    def reg(self):
        if(self.getRegUserText() == ""):
            if(self.getRegPassText() == ""):
                self.setStatusText("ERROR: You must enter a username and password before logging in.")
            else:
                self.setStatusText("ERROR: You must specify a username")
            self.regInputPass['focus'] = 0
            self.regInputCPass['focus'] = 0
            self.regInputUser['focus'] = 1

        elif(self.getRegPassText() == ""):
            self.setStatusText("ERROR: You must enter a password")
            self.regInputUser['focus'] = 0
            self.regInputCPass['focus'] = 0
            self.regInputPass['focus'] = 1

        elif(not self.testRegPassText()):
            self.setStatusText("ERROR: Your passwords must match")
            self.regInputPass.enterText("")
            self.regInputCPass.enterText("")
            self.regInputUser['focus'] = 0
            self.regInputCPass['focus'] = 0
            self.regInputPass['focus'] = 1
        else:
            self.setStatusText("Attempting to sign up...")
            self.cancel_btn['state'] = DGG.DISABLED
            self.register_btn['state'] = DGG.DISABLED
            self.World.username = self.getRegUserText()
            self.World.authConnection.sendRegisterRequest(self.getRegUserText(), self.getRegPassText())

    def cycleLoginBox(self):
        # function is triggered by the tab key so you can cycle between
        # the two input fields like on most login screens

        # IMPORTANT: When you change the focus to one of the text boxes,
        # you have to unset the focus on the other textbox.  If you do not
        # do this Panda seems to get confused.

        if(self.passTextbox['focus'] == 1):
            self.passTextbox['focus'] = 0
            self.userTextbox['focus'] = 1
        elif(self.userTextbox['focus'] == 1):
            self.userTextbox['focus'] = 0
            self.passTextbox['focus'] = 1

    def cycleRegisterBox(self):
        if(self.regInputUser['focus'] == 1):
            self.regInputUser['focus'] = 0
            self.regInputCPass['focus'] = 0
            self.regInputPass['focus'] = 1
        elif(self.regInputPass['focus'] == 1):
            self.regInputUser['focus'] = 0
            self.regInputPass['focus'] = 0
            self.regInputCPass['focus'] = 1
        elif(self.regInputCPass['focus'] == 1):
            self.regInputPass['focus'] = 0
            self.regInputCPass['focus'] = 0
            self.regInputUser['focus'] = 1

    def clickedCancel(self):
        exit()

    def clickedRegister(self):
        self.destroyLoginWindow()
        self.createRegisterWindow()

    def clickedRegCancel(self):
        self.destroyRegisterWindow()
        self.createLoginWindow()

    def destroyLoginWindow(self):
        self.userTextbox.destroy()
        self.passTextbox.destroy()
        self.enter_btn.destroy()
        self.register_btn.destroy()
        self.myImage.destroy()

    def destroyRegisterWindow(self):
        self.regInputUser.destroy()
        self.regInputPass.destroy()
        self.regInputCPass.destroy()
        self.cancel_btn.destroy()
        self.register_btn.destroy()
        self.myImage.destroy()



    def parseAuthResponse(self, data):
        if data == 1:
            print("unloading")
            self.unloadScreen()
            self.World.doMenu()
        else:
            if data == 2:
                self.status["text"] = ("Already logged in")
            else:
                self.setStatusText("Invalid username/password")

        self.enter_btn['state'] = DGG.NORMAL
        self.register_btn['state'] = DGG.NORMAL


    def setStatusText(self, s):
        self.status["text"] = s

    def parseRegResponse(self, data):
        if data == 1:
            print("unloading")
            self.unloadScreen()
            self.World.doMenu()
        else:
            self.setStatusText("User already exists")

        self.cancel_btn['state'] = DGG.NORMAL
        self.register_btn['state'] = DGG.NORMAL
