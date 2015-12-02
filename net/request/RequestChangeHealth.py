from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestChangeHealth(ServerRequest):

    def send(self, health):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_HEALTH)
            pkg.addInt32(health) # Health Change

            self.cWriter.send(pkg, self.connection)
            
        except:
            self.log('Bad [' + str(Constants.CMSG_HEALTH) + '] Health Request')
