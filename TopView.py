from direct.directbase.DirectStart import *
from pandac.PandaModules import *
from Vehicle import Vehicle

class TopView(object):
    def __init__(self, vehicle):
        view = base.win.makeDisplayRegion(.65, .95, .65, .95)
        #view.setClearColor(VBase4(1, 1, 1, .5))
        #view.setClearColorActive(True)
        view.setClearDepthActive(True)
        
        self.vehicle = vehicle
        
        self.cam = render.attachNewNode(Camera('cam2'))
        view.setCamera(self.cam)
        
        self.cam.setPos(self.vehicle.chassisNP.getPos())
        #self.cam.setPos(self.vehicle.chassisNP, (0, 0, 150))
        self.cam.setZ(150)
        self.cam.setP(-90)
        
    def update(self, task):
        self.cam.setPos(self.vehicle.chassisNP.getPos())
        #self.cam.setPos(self.vehicle.chassisNP, (0, 0, 150))
        self.cam.setH(self.vehicle.chassisNP.getH())
        self.cam.setZ(250)
        self.cam.setP(-90)
        
        return task.again
    
        