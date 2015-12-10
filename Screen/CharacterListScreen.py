from direct.showbase.DirectObject           import DirectObject      
from direct.gui.OnscreenText                import OnscreenText 
from direct.gui.DirectGui                   import *
from direct.gui.DirectScrolledList          import DirectScrolledList
from panda3d.core                           import *

class CharacterListScreen:
    def __init__(self,World):
        self.World = World;
        self.items = []
        
        #boxloc = Vec3(0.65, 0.0, 0.7)
        boxloc = Vec3(-0.35,0.0,0.0)
        frameSize = Vec4(-0.35, 0.35, -0.05, 0.59)
        p = boxloc
        self.CharListFrame = DirectFrame(frameColor=(0,0,0,0.4),frameSize=frameSize,pos=p)       

        #size = frameSize + Vec4(0.0,0.0,-0.5,0.0)
        size = frameSize
        self.CharListFrame.scrolledList = DirectScrolledList(
            parent=self.CharListFrame,
            
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
        
    def toggleScreen(self):
        if self.hidden:
            self.showScreen()
        else:
            self.hideScreen()
            
    def addPlayer(self, username):
        l = DirectLabel(text = username, frameSize=(-0.35, 0.35, -0.05, 0.06),text_scale=0.05,frameColor=(0,0,0,0),text_fg=(1,1,1,1))
        self.items.append(l)
        self.CharListFrame.scrolledList.addItem(l)
                
    def removePlayer(self, username):
        for item in self.items:
            if item["text"] == username:
                self.CharListFrame.scrolledList.removeItem(item)
        
    def unloadScreen(self):
        self.CharListFrame.destroy()
        
    def hideScreen(self):
        self.CharListFrame.hide()
        self.hidden = True
        
    def showScreen(self):
        self.CharListFrame.show()        
        self.hidden = False          