from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestCheckpoints(ServerRequest):

    def send(self, args = []):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_CHECKPOINTS)
            pkg.addInt32(args[0])
            pkg.addInt32(args[1])
            pkg.addFloat32(args[2])

            self.cWriter.send(pkg, self.connection)

        except:
            self.log('Bad [' + str(Constants.CMSG_CHECKPOINTS) + '] Checkpoints Request')