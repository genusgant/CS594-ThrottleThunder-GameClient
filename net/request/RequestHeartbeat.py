from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest
from traceback import print_exc

class RequestHeartbeat(ServerRequest):


    def send(self, args = None):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.REQ_HEARTBEAT)

            pkg.addString("adrien")


            self.cWriter.send(pkg, self.connection)

        except:
            self.log('Bad [' + str(Constants.REQ_HEARTBEAT) + '] Heartbeat Request')
