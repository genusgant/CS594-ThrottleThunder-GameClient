from Models3D.Characters.PandaCharacter     import PandaCharacter
from Models3D.Characters.RalphCharacter     import RalphCharacter
from Models3D.Characters.VehicleCharacter   import VehicleCharacter

class CharacterManager:
    characters = []
    
    def __init__(self, World, render, base,loader):
        self.World = World
        self.render = render
        self.base = base
        self.loader = loader
    
    def createCharacter(self,username="", modelName="", pos=(0.0,0.0,0.0), hpr=(0.0,0.0,0.0)):
        model = self.getModel(username)
        if modelName == "panda1":
            model = PandaCharacter(World=self.World,render=self.render,base=self.base,loader=self.loader)
        elif modelName == "ralph1":
            model = RalphCharacter(World=self.World,render=self.render,base=self.base,loader=self.loader)
        elif modelName == "vehicle1":
            model = VehicleCharacter(World=self.World,render=self.render,base=self.base,loader=self.loader)
        else:
            model = RalphCharacter(World=self.World,render=self.render,base=self.base,loader=self.loader)
        model.placeAt((float(pos[0]),float(pos[1]),float(pos[2])))
        model.actor.setHpr(float(hpr[0]),float(hpr[1]),float(hpr[2]))
        model.username = username
        
        self.characters.append(model)
        self.World.NotificationScreen.joinStatus(model.username)
        self.World.CharacterListScreen.addPlayer(model.username)
        return model
    
    def removeCharacter(self,username=""):
        model = self.getModel(username)
        if model != None:
            self.World.NotificationScreen.leftStatus(model.username)
            self.World.CharacterListScreen.removePlayer(model.username)
            model.actor.delete()
            self.characters.remove(model)
            
    
    def moveCharacter(self, username, time, pos):
        list = pos.split(',')
        model = self.getModel(username)
        if model == None:
            #model = self.createCharacter(username,"",pos)
            return False
        pos = (list[0],list[1],list[2])
        if len(list) == 3:
            model.moveCharacterTo(pos)
        else:
            model.moveCharacterTo(pos,list[3])        
    
    def getModel(self,username):
        for model in self.characters:
            if(model.username == username):
                return model
        return None
            
    def getCharacters(self):
        list = []
        for model in self.characters:
            list.append(model)
            
        return list