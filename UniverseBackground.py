from pandac.PandaModules import CompassEffect

class UniverseBackground():
    def __init__(self):
        self.universeBackground = loader.loadModel('models/sky')
        tex = loader.loadTexture('models/tex/space.jpg')
        self.universeBackground.setTexture(tex)
        self.universeBackground.setEffect(CompassEffect.make(render))
        self.universeBackground.setScale(500)
        self.universeBackground.setZ(-65)
        self.universeBackground.reparentTo(base.camera)
    def remove(self):
        self.universeBackground.remove()