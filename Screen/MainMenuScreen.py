from direct.showbase.DirectObject               import DirectObject      
from direct.gui.OnscreenText                    import OnscreenText 
from direct.gui.DirectGui                       import *
from panda3d.core                               import *
from pandac.PandaModules                        import * 
from Network.models.CharacterConnectionModel    import CharacterConnectionModel
import sys

class MainMenuScreen:
    def __init__(self,World,render,base,camera):
        self.characterConnection = CharacterConnectionModel(self)
        World.ServerConnection.setupConnectionModel(self.characterConnection)
        
        # ADD MATCHMAKING BUTTON
        boxloc = Vec3(0.0, 0.0, 0.0)
        p = boxloc + Vec3(0.0, 0, 0.0)
        self.MatchmakingButton = DirectButton( text = ("Matchmaking", "Matchmaking", "Matchmaking", "Matchmaking"), pos = p, scale = 0.1, command=self.doMatchMaking)
        
        # ADD SOCIALIZATION BUTTON
        boxloc = Vec3(0.0, 0.0, 0.0)
        p = boxloc + Vec3(-0.75, 0, 0.0)
        self.SocializeButton = DirectButton( text = ("Socialize", "Socialize", "Socialize", "Socialize"), pos = p, scale = 0.1)
        
        # ADD CUSTOMIZATION BUTTON
        boxloc = Vec3(0.0, 0.0, 0.0)
        p = boxloc + Vec3(0.75, 0, 0.0)
        self.CustomizeButton = DirectButton( text = ("Customize", "Customize", "Customize", "Customize"), pos = p, scale = 0.1)
        
        boxloc = Vec3(0.0, 1.0, 0.0)
        p = boxloc + Vec3(0.0, 0.0, -0.5)
        self.SelectionFrame = DirectFrame(frameColor=(0,0,0,0.4),frameSize=(-1,1,-0.1,0.2),pos=p)       

        p = boxloc + Vec3(0.0, 0.0, 0.0)                                 
        self.SelectionFrame.textObject = OnscreenText(parent=self.SelectionFrame, text = "Main Menu", pos = p, scale = 0.2,fg=(1, 1, 1, 1),align=TextNode.ACenter)
        
        # self.makePickable()
        self.picker= CollisionTraverser() 
        self.queue=CollisionHandlerQueue() 
        
        self.pickerNode=CollisionNode('mouseRay') 
        self.pickerNP=camera.attachNewNode(self.pickerNode) 
        
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask()) 
        
        self.pickerRay=CollisionRay() 
        
        self.pickerNode.addSolid(self.pickerRay) 
        
        self.picker.addCollider(self.pickerNP, self.queue)
        
        #this holds the object that has been picked 
        self.pickedObj=None 
        
        World.accept('mouse1', self.getSelectedObject)
        
        self.base = base
        self.render = render
        self.World = World
    
    # def makePickable(self):
    #     for model in self.availableModels:
    #         model.actor.setPythonTag('pickable','true')
    def doMatchMaking(self):
        self.MatchmakingButton.destroy()
        self.SocializeButton.destroy()
        self.CustomizeButton.destroy()
        self.SelectionFrame.destroy()
        self.World.doSelectionScreen()

    def getSelectedObject(self): 
        self.getObjectHit( self.base.mouseWatcherNode.getMouse())
        if self.pickedObj != None:
            Character = self.getSelectedCharacter()
            if Character == None:
                print "Something went wrong"
            else:
                self.World.setPlayerCharacter(Character)
                if not self.World.bypassServer:
                    self.characterConnection.sendCharacter(Character.node.getName())
                self.unloadScreen()
                self.World.doGameScreen()
        
    def getObjectHit(self, mpos): #mpos is the position of the mouse on the screen 
        self.pickedObj=None #be sure to reset this 
        self.pickerRay.setFromLens(self.base.camNode, mpos.getX(),mpos.getY()) 
        self.picker.traverse(self.render) 
        if self.queue.getNumEntries() > 0: 
            self.queue.sortEntries() 
            self.pickedObj=self.queue.getEntry(0).getIntoNodePath() 
            self.pickedObj = self.pickedObj.findNetPythonTag('pickable')
            if not self.pickedObj.isEmpty():
                return self.pickedObj
        return None  

    def getSelectedCharacter(self):
        Character = None
        for model in self.availableModels:
            if model.node.getName() == self.pickedObj.getParent().getName():
                Character = model
            else:
                model.actor.delete()
        return Character
    def unloadScreen(self):
        self.SelectionFrame.destroy()
        self.World.ignore('mouse1')
        
    def parseResponse(self,data):
        pos = data.split(',')
        if len(pos) >= 3:
            print "here1"
            self.World.Character.actor.setPos(float(pos[0]),float(pos[1]),float(pos[2]))
        elif len(pos) >= 4:
            print "here2"
            self.World.Character.actor.setH(float(pos[3]))