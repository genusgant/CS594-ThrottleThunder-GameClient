from pandac.PandaModules import CompassEffect

class SkyDome(object):

    SCALE_MOD = 2

    def __init__(self):
        self.sky = loader.loadModel('models/env')
        tex = loader.loadTexture('models/tex/env_sky.jpg')
        self.sky.setTexture(tex)
        self.sky.setEffect(CompassEffect.make(render))
        self.sky.setScale(500)
        self.sky.setZ(-65)
        self.sky.reparentTo(base.camera)
        self.period_cloud = self.sky.hprInterval(400, (360, 0, 0))
        self.period_cloud.loop()

        self.ground = loader.loadModel("models/ground")
        self.ground_tex = loader.loadTexture("models/tex/grass.jpg")
        self.ground.setTexture(self.ground_tex)
        self.ground.setScale(250 * self.SCALE_MOD, 250 * self.SCALE_MOD, 1)
        self.ground.setPos(0, 0, 0)
        self.ground.reparentTo(render)

        self.hills = loader.loadModel("models/hills")
        self.hill_tex = loader.loadTexture("models/tex/mt.jpg")
        self.hills.setTexture(self.hill_tex,1)
        self.hills.setScale(.6 * self.SCALE_MOD, .6 * self.SCALE_MOD, 1 * self.SCALE_MOD)
        self.hills.setPos(0, 0, 0)
        self.hills.reparentTo(render)


        self.wall = loader.loadModel("models/trackwalls")
        self.wall_tex = loader.loadTexture("models/tex/wall.jpg")
        self.wall.setTexture(self.wall_tex,1)
        self.wall.setScale(.6 * self.SCALE_MOD, .6 * self.SCALE_MOD, 1 * self.SCALE_MOD)
        self.wall.setPos(0, 0, 0)
        self.wall.reparentTo(render)

        self.track = loader.loadModel("models/flatTrackSurface")
        self.track.reparentTo(render)
        self.track.setPos(0, 0, -2.8)
        self.track.setScale(.6 * self.SCALE_MOD, .6 * self.SCALE_MOD, 10 * self.SCALE_MOD)
        self.track_tex = loader.loadTexture("models/tex/road.jpg")
        self.track.setTexture(self.track_tex,1)

        self.tree = loader.loadModel("models/trees")
        self.tree.reparentTo(render)
        self.tree.setPos(0, 0, 0)
        self.tree.setScale(.5 * self.SCALE_MOD, .5 * self.SCALE_MOD, .5 * self.SCALE_MOD)
        self.tree_tex = loader.loadTexture("models/tex/tree.jpg")
        self.tree.setTexture(self.tree_tex, 1)