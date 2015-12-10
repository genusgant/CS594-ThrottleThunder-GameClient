from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestResults(ServerRequest):

    def send(self, gameId):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_RESULTS)
            pkg.addInt32(gameId) # GameId

            self.cWriter.send(pkg, self.connection)

        except:
            self.log('Bad [' + str(Constants.CMSG_RESULTS) + '] Results Request')
