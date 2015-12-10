from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestPrizes(ServerRequest):

    def send(self):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_PRIZES)

            self.cWriter.send(pkg, self.connection)

        except:
            self.log('Bad [' + str(Constants.CMSG_PRIZES) + '] Prizes Request')
