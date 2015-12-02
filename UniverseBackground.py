from pandac.PandaModules import CompassEffect

class UniverseBackground():
    def __init__(self):
        universeBackground = loader.loadModel('models/sky')
        tex = loader.loadTexture('models/tex/space.jpg')
        universeBackground.setTexture(tex)
        universeBackground.setEffect(CompassEffect.make(render))
        universeBackground.setScale(500)
        universeBackground.setZ(-65)
        universeBackground.reparentTo(base.camera)
