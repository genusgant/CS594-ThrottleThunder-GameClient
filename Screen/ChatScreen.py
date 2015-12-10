from direct.showbase.DirectObject           import DirectObject      
from direct.gui.OnscreenText                import OnscreenText 
from direct.gui.DirectGui                   import *
from direct.gui.DirectScrolledList          import DirectScrolledList
from panda3d.core                           import *
from Network.models.ChatConnectionModel     import ChatConnectionModel

class ChatScreen:
    def __init__(self,World,render,base):
        self.World = World;
        self.World.accept("t",self.toggleScreen)
        self.chatConnection = ChatConnectionModel(self)
        self.World.ServerConnection.setupConnectionModel(self.chatConnection)
        
        boxloc = Vec3(0.65, 0.0, -0.7)
        frameSize = Vec4(0.0, 0.7, -0.05, 0.59)
        p = boxloc
        self.ChatFrame = DirectFrame(frameColor=(0,0,0,0.4),frameSize=frameSize,pos=p)       

        #size = frameSize + Vec4(0.0,0.0,-0.5,0.0)
        size = frameSize
        self.ChatFrame.scrolledList = DirectScrolledList(
            parent=self.ChatFrame,
            
            decButton_pos= (0.2, 0, 0.53),
            decButton_text = "Up",
            decButton_text_scale = 0.04,
            decButton_borderWidth = (0.1, 0.005),
         
            incButton_pos= (0.5, 0, 0.53),
            incButton_text = "Down",
            incButton_text_scale = 0.04,
            incButton_borderWidth = (0.1, 0.005),
            
            frameSize=size,
            frameColor = (0,0,0,0.0),
            #pos=p,
            numItemsVisible = 4,
            #forceHeight = 0.11,
            itemFrame_frameSize = (-0.35, 0.35, -0.37, 0.11),
            itemFrame_pos = (0.35, 0, 0.4),
            itemFrame_frameColor=(0,0,0,0) 
        )
            
        p = boxloc + Vec3(-0.05,0.0,0.695)
        self.ChatFrame.sendButton = DirectButton(parent=self.ChatFrame, text = ("Send", "Send", "Send", "Send"), pos = p, scale = 0.075, command=self.sendMessage)
        
        p = boxloc + Vec3(-0.64,0.0,0.7)
        self.ChatFrame.messageBox = DirectEntry(parent=self.ChatFrame, text = "" , pos = p, scale=.05, initialText="")
        
    def toggleScreen(self):
        if self.hidden:
            self.showScreen()
            
    def updateStatus(self, statustext):
        self.ChatFrame.statusText.setText(statustext)
        
    def unloadScreen(self):
        self.ChatFrame.destroy()
        
    def hideScreen(self):
        self.ChatFrame.hide()
        self.hidden = True
        self.World.ignore("escape")
        self.World.ignore("enter")
        self.World.Character.setControls()
        self.World.accept("t",self.toggleScreen)
        self.World.accept("p",self.World.pChatScreen.toggleScreen)
        
    def showScreen(self):
        self.ChatFrame.show()        
        self.hidden = False
        self.World.Character.blockControls()
        self.World.ignore("p")
        self.World.ignore("t")
        self.ChatFrame.messageBox.setFocus()
        self.World.accept("escape", self.hideScreen)
        self.World.accept("enter", self.sendMessage) 
        
    def sendMessage(self):  
        self.parseResponse("You", self.ChatFrame.messageBox.get())
        if not self.World.bypassServer:
            self.chatConnection.sendChatMessage(self.ChatFrame.messageBox.get())
        self.ChatFrame.messageBox.set("")
            
    def parseResponse(self,username,message):
        l = DirectLabel(text = username+": "+message, frameSize=(-0.35, 0.35, -0.05, 0.06),text_scale=0.05,frameColor=(0,0,0,0),text_fg=(1,1,1,1))
        self.ChatFrame.scrolledList.addItem(l)          