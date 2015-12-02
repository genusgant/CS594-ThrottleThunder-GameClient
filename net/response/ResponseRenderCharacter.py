from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse
# from finalhw1 import Character
from Vehicle import Vehicle


class ResponseRenderCharacter(ServerResponse):

    def execute(self, data):

        try:
            self.username = data.getString()
            self.CarType = data.getInt32()
            self.CarPaint = data.getInt32()
            self.CarTires = data.getInt32()
            print"Is this bad?", self.username, self.CarType, self.CarPaint, self.CarTires
            self.worldMgr.addVehicleProps(self.username, self.CarType, self.CarPaint, self.CarTires, 0, 0, 0, 0, 0, 0)
            #if self.world.login == self.username:
                #print "In ResponseRenderCharacter this is me", self.username
            #else:
                #self.world.createOtherVehicles(self.username, self.CarType, self.CarPaint, self.CarTires)
            print "In ResponseRenderCharacter - ", self.username
                #self.world.responseValue = 1

        except:
            self.log('Bad [' + str(Constants.SMSG_RENDER_CHARACTER) + '] Render Character Response')
            print_exc()
