from direct.showbase.DirectObject           import DirectObject      
from direct.gui.OnscreenText                import OnscreenText 
from direct.gui.DirectGui                   import *
from direct.gui.DirectScrolledList          import DirectScrolledList
from panda3d.core                           import *

class NotificationScreen:
    def __init__(self,World):
        self.World = World;
        self.World.accept("tab",self.toggleScreen)
        self.NotifyMessage = None
        self.hidden= True
        
    def toggleScreen(self):
        if self.hidden:
            self.showScreen()
        else:
            self.hideScreen()
            
    def joinStatus(self, username):
        self.showScreen()
        self.NotifyMessage.setText("Now Online: " + username)
        
    def leftStatus(self, username):
        self.showScreen()
        self.NotifyMessage.setText("Now Offline: " + username)        
        
    def unloadScreen(self):
        if self.NotifyMessage != None:
            self.NotifyMessage.destroy()
            self.NotifyMessage = None;
    
    def taskHideScreen(self,task):
        self.hideScreen()
        return task.done
        
    def hideScreen(self):
        self.unloadScreen()
        self.hidden = True
        
    def showScreen(self):
        if self.NotifyMessage == None:
            boxloc = Vec3(0,0,0)
            p = boxloc
            self.NotifyMessage = OnscreenText(text = "", pos = p, scale = 0.07,fg=(1, 1, 1, 1),align=TextNode.ACenter)
        self.hidden = False
        taskMgr.doMethodLater(3,self.taskHideScreen,"autoHideNotify")
