from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestPowerPickUp(ServerRequest):

    def send(self, powerId):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_POWER_UP_PICK_UP)
            pkg.addInt32(powerId)

            self.cWriter.send(pkg, self.connection)

        except:
            self.log('Bad [' + str(Constants.CMSG_POWER_UP_PICK_UP) + '] Power Pick Up Request')
