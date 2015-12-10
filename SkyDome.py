from pandac.PandaModules import CompassEffect

class SkyDome(object):
    def __init__(self):
        self.sky = loader.loadModel('models/env_test')
        tex = loader.loadTexture('models/tex/env_sky_edit_test.jpg')
        self.sky.setTexture(tex)
        self.sky.setEffect(CompassEffect.make(render))
        self.sky.setScale(700)
        self.sky.setZ(-65)
        self.sky.reparentTo(base.camera)
    