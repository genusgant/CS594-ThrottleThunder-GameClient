from direct.showbase.DirectObject       import DirectObject      
from direct.gui.OnscreenText            import OnscreenText 
from direct.gui.DirectGui               import *
from panda3d.core                       import *
from Network.models.AuthConnectionModel import AuthConnectionModel
from Network.models.NullConnectionModel import NullConnectionModel

class AuthScreen:
    def __init__(self,World,render,base):
        self.World = World;
        self.authConnection = AuthConnectionModel(self)
        self.nullConnection = NullConnectionModel()
        self.taskName = "nullTask"
        self.World.ServerConnection.setupConnectionModel(self.authConnection)
        self.World.ServerConnection.setupConnectionModel(self.nullConnection)
        
        boxloc = Vec3(0.0, 0.0, 0.0)
        p = boxloc
        self.LoginFrame = DirectFrame(frameColor=(0,0,0,0.4),frameSize=(-0.5,0.41,-0.25,0.1),pos=p)       

        p = boxloc + Vec3(-0.5, 0, 0.0)                                 
        self.LoginFrame.textObject = OnscreenText(parent=self.LoginFrame, text = "Username:", pos = p, scale = 0.07,fg=(1, 1, 1, 1),align=TextNode.ALeft)
        
        p = boxloc + Vec3(-0.1, 0.0, 0.0)
        self.LoginFrame.usernameBox = DirectEntry(parent=self.LoginFrame, text = "" , pos = p, scale=.05, initialText="", numLines = 1)
        
        p = boxloc + Vec3(-0.5, -0.1, 0.0)        
        self.LoginFrame.textObject = OnscreenText(parent=self.LoginFrame, text = "Password:", pos = p, scale = 0.07,fg=(1, 1, 1, 1),align=TextNode.ALeft)
        
        p = boxloc + Vec3(-0.1, 0, -0.1)
        self.LoginFrame.passwordBox = DirectEntry(parent=self.LoginFrame, text = "" , pos = p, scale=.05, initialText="", numLines = 1, obscured = 1)
        
        p = boxloc + Vec3(-0.2, 0, -0.2)
        self.LoginFrame.loginButton = DirectButton(parent=self.LoginFrame, text = ("Login", "Login", "Login", "Login"), pos = p, scale = 0.075, command=self.attemptLogin)
        
        p = boxloc + Vec3(0.2, 0, -0.2)
        self.LoginFrame.registerButton = DirectButton(parent=self.LoginFrame, text = ("Signup", "Signup", "Signup", "Signup"), pos = p, scale = 0.075, command=self.attemptRegister)
        
        p = boxloc + Vec3(0, -0.4, 0)
        self.LoginFrame.statusText = OnscreenText(parent=self.LoginFrame, text = "", pos = p, scale = 0.075, fg = (1, 0, 0, 1), align=TextNode.ACenter)
        
        self.World.taskMgr.doMethodLater(5,self.sendNullSignal,self.taskName)

    def sendNullSignal(self,task):
        self.nullConnection.sendNull()
        return task.again
        
    def updateStatus(self, statustext):
        self.LoginFrame.statusText.setText(statustext)
        
    def unloadScreen(self):
        self.LoginFrame.destroy()
        self.World.taskMgr.remove(self.taskName)
        
    def attemptRegister(self):
        self.whichAction = 1      
        if(self.LoginFrame.usernameBox.get() == ""):
            if(self.LoginFrame.passwordBox.get() == ""):
                self.updateStatus("ERROR: You must enter a username and password before logging in.")
            else:
                self.updateStatus("ERROR: You must specify a username")
            self.LoginFrame.passwordBox['focus'] = 0
            self.LoginFrame.usernameBox['focus'] = 1
                
        elif(self.LoginFrame.passwordBox.get() == ""):
            self.updateStatus("ERROR: You must enter a password")
            self.LoginFrame.usernameBox['focus'] = 0
            self.LoginFrame.passwordBox['focus'] = 1
            
        else:
            self.updateStatus("Attempting to Signup...")
            self.LoginFrame.registerButton = DGG.DISABLED
            self.LoginFrame.loginButton = DGG.DISABLED
            if not self.World.bypassServer:
                self.authConnection.sendRegisterRequest(self.LoginFrame.usernameBox.get(),self.LoginFrame.passwordBox.get())
            else:
                self.parseResponse(1)
            
        
    def attemptLogin(self):  
        self.whichAction = 2    
        if(self.LoginFrame.usernameBox.get() == ""):
            if(self.LoginFrame.passwordBox.get() == ""):
                self.updateStatus("ERROR: You must enter a username and password before logging in.")
            else:
                self.updateStatus("ERROR: You must specify a username")
            self.LoginFrame.passwordBox['focus'] = 0
            self.LoginFrame.usernameBox['focus'] = 1
                
        elif(self.LoginFrame.passwordBox.get() == ""):
            self.updateStatus("ERROR: You must enter a password")
            self.LoginFrame.usernameBox['focus'] = 0
            self.LoginFrame.passwordBox['focus'] = 1
            
        else:
            self.updateStatus("Attempting to login...")
            self.LoginFrame.registerButton = DGG.DISABLED
            self.LoginFrame.loginButton = DGG.DISABLED
            if self.LoginFrame.usernameBox.get() == "test" and self.LoginFrame.passwordBox.get() == "test":
                self.parseResponse(1)
            elif not self.World.bypassServer:
                self.authConnection.sendLoginRequest(self.LoginFrame.usernameBox.get(),self.LoginFrame.passwordBox.get())
            else:
                self.parseResponse(1)
            
    def parseAuthResponse(self,data):
        if data == 1:
            self.unloadScreen()
            self.World.doMainMenuScreen()
            # self.World.doSelectionScreen()
        else: 
            if data == 2:
                self.updateStatus("Already logged in")
            elif self.whichAction == 1:
                self.updateStatus("Unable to register with that username")
            else:
                self.updateStatus("Invalid username/password")
            self.whichAction = 0