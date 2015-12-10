from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestReady(ServerRequest):

    def send(self, data):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_READY)

            self.cWriter.send(pkg, self.connection)

        except:
            self.log('Bad [' + str(Constants.CMSG_READY) + '] Ready Request')
