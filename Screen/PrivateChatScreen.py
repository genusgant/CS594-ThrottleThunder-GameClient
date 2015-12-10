from direct.showbase.DirectObject                   import DirectObject      
from direct.gui.OnscreenText                        import OnscreenText 
from direct.gui.DirectGui                           import *
from direct.gui.DirectScrolledList                  import DirectScrolledList
from panda3d.core                                   import *
from Network.models.PrivateChatConnectionModel      import PrivateChatConnectionModel

class PrivateChatScreen:
    def __init__(self,World,render,base):
        self.World = World;
        self.World.accept("p",self.toggleScreen)
        self.chatConnection = PrivateChatConnectionModel(self)
        self.World.ServerConnection.setupConnectionModel(self.chatConnection)
        
        boxloc = Vec3(0.65, 0.0, -0.7)
        frameSize = Vec4(0.0, 0.7, -0.05, 0.59)
        p = boxloc
        self.boxloc = boxloc
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
        self.ChatFrame.toButton = DirectButton(parent=self.ChatFrame, text = ("Mesg", "Mesg", "Mesg", "Mesg"), pos = p, scale = 0.075, command=self.showMessage)
        
        p = boxloc + Vec3(-0.75,0.0,0.7)
        self.ChatFrame.toBoxLabel = OnscreenText(parent=self.ChatFrame, text = "To: " , pos = p, scale=.05,align=TextNode.ALeft)
        
        p = boxloc + Vec3(-0.64,0.0,0.7)
        self.ChatFrame.toBox = DirectEntry(parent=self.ChatFrame, pos = p, scale=.05, initialText="")
        
        self.ChatFrame.sendButton = None
        self.ChatFrame.messageBox = None
        
    def showMessage(self):
        self.ChatFrame.toBoxLabel.hide()
        self.ChatFrame.toButton.hide()
        self.ChatFrame.toBox.hide()
        
        boxloc = self.boxloc
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
        self.ChatFrame.toBoxLabel.show()
        self.ChatFrame.toButton.show()
        self.ChatFrame.toBox.show()        
        
        if self.ChatFrame.sendButton != None:
            self.ChatFrame.sendButton.hide()
            self.ChatFrame.messageBox.hide()
            
        self.ChatFrame.hide()        
        self.hidden = True
        self.World.ignore("escape")
        self.World.ignore("enter")
        self.World.accept("t",self.World.chatScreen.toggleScreen)
        self.World.accept("p",self.toggleScreen)
        self.World.Character.setControls()
        
        
        
    def showScreen(self):
        self.ChatFrame.show()        
        self.hidden = False
        self.World.Character.blockControls()
        self.World.ignore("p")
        self.World.ignore("t")
        self.ChatFrame.toBox.setFocus()
        self.World.accept("escape", self.hideScreen)
        #self.World.accept("enter", self.sendMessage) 
        
    def sendMessage(self):  
        self.parseResponse("To " + self.ChatFrame.toBox.get(),self.ChatFrame.messageBox.get())
        if not self.World.bypassServer:
            self.chatConnection.sendChatMessage(self.ChatFrame.toBox.get(), self.ChatFrame.messageBox.get())
        self.ChatFrame.messageBox.set("")
        
        self.ChatFrame.toBoxLabel.show()
        self.ChatFrame.toButton.show()
        self.ChatFrame.toBox.show()
        
        self.ChatFrame.sendButton.hide()
        self.ChatFrame.messageBox.hide()
            
    def parseResponse(self,username,message):
        l = DirectLabel(text = username+": "+message, frameSize=(-0.35, 0.35, -0.05, 0.06),text_scale=0.05,frameColor=(0,0,0,0),text_fg=(1,1,1,1))
        self.ChatFrame.scrolledList.addItem(l)          