from pandac.PandaModules import CompassEffect

class SkyDome(object):
    def __init__(self):
        self.sky = loader.loadModel('models/sky')
        tex = loader.loadTexture('models/tex/space.jpg')
        self.sky.setTexture(tex)
        self.sky.setEffect(CompassEffect.make(render))
        self.sky.setScale(500)
        self.sky.setZ(-65)
        self.sky.reparentTo(base.camera)
    