from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestMove(ServerRequest):

  #args stores the x y z h and keys components of the moving
    def send(self, forces):

        try:
            #print "Req Move: ", forces[3], forces[4], forces[5], forces[6], forces[7], forces[8]
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_MOVE)
            pkg.addFloat32(forces[0])
            pkg.addFloat32(forces[1])
            pkg.addFloat32(forces[2])
            pkg.addFloat32(forces[3])
            pkg.addFloat32(forces[4])
            pkg.addFloat32(forces[5])
            pkg.addFloat32(forces[6])
            pkg.addFloat32(forces[7])
            pkg.addFloat32(forces[8])

            self.cWriter.send(pkg, self.connection)

        except:
            self.log('Bad [' + str(Constants.CMSG_MOVE) + '] Move Request')
