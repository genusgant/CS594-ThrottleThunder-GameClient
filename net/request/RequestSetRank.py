from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestSetRank(ServerRequest):

    def send(self, rank):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_SET_RANK)
            pkg.addInt32(rank)

            self.cWriter.send(pkg, self.connection)

        except:
            self.log('Bad [' + str(Constants.CMSG_SET_RANK) + '] Set Rank Request')
