import sys
from panda3d.core import PandaNode,NodePath,Camera,TextNode

class BaseModel3D:
    def __init__(self, World, render, base,loader):
        self.World = World
        self.render = render
        self.base = base
        self.loader = loader
    
    def setActor(self, _Actor):
        self.actor = _Actor
        
    def getActor(self):
        return self.actor