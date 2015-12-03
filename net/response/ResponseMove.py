from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseMove(ServerResponse):

    def execute(self, data):

        try:
            username = data.getString()
            #print "MOVE: ", username
            if username != self.world.login:
                steering = data.getFloat32()
                wheelforce = data.getFloat32()
                brakeforce = data.getFloat32()
                x = data.getFloat32()
                y = data.getFloat32()
                z = data.getFloat32()
                h = data.getFloat32()
                p = data.getFloat32()
                r = data.getFloat32()
                #print "Response Move for: ", username,steering, wheelforce, brakeforce, x, y, z, h, p, r
                if username in self.world.vehiclelist.keys():
                    vehicle = self.world.vehiclelist[username]
                    vehicle.move(steering, wheelforce, brakeforce, x, y, z, h, p, r)

        except:
            self.log('Bad [' + str(Constants.SMSG_MOVE) + '] Move Response')
            print_exc()
