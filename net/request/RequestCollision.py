from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestCollision(ServerRequest):

    def send(self, args = []):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_COLLISION)
            pkg.addString(args[0]) # Username
            pkg.addInt32(args[1]) # Damage Dealt

            self.cWriter.send(pkg, self.connection)

        except:
            self.log('Bad [' + str(Constants.CMSG_COLLISION) + '] Collision Request')
