from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestRankings(ServerRequest):

    #print "RequestRankings"
    def send(self, args= []):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_RANKINGS)

            self.cWriter.send(pkg, self.connection)

        except:
            self.log('Bad [' + str(Constants.CMSG_RANKINGS) + '] Ranking Request')
