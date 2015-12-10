from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest
from Character import Character

class RequestCreateCharacter(ServerRequest):


    def send(self, args = None):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_CREATE_CHARACTER)
            pkg.addUint16(args[0]) #TYPE
            pkg.addFloat32(args[1]) #x pos
            pkg.addFloat32(args[2]) #y pos
            pkg.addFloat32(args[3]) #z pos

#             print "RequestCreateCharacter - ", args[0], " x:", args[1], " y:", args[2]," z:", args[3]

            self.cWriter.send(pkg, self.connection)

            #self.log('Sent [' + str(Constants.RAND_STRING) + '] Int Request')
        except:
            self.log('Bad [' + str(Constants.RAND_STRING) + '] Int Request')
            print_exc()
