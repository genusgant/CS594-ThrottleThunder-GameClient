from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest
from traceback import print_exc

class RequestCreateLobby(ServerRequest):


    def send(self, args = []):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_CREATE_LOBBY)

            pkg.addString(args[0]) #game room name
            pkg.addInt32(int(args[1])) #gamemode
            pkg.addInt32(int(args[2])) #status

            self.cWriter.send(pkg, self.connection)

        except:
            self.log('Bad [' + str(Constants.CMSG_CREATE_LOBBY) + '] Create Lobby Request')
