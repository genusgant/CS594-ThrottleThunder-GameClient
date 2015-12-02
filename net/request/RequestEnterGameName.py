from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestEnterGameName(ServerRequest):


    def send(self, args ):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_ENTER_GAME_NAME)
            pkg.addString(args) #room name
            self.cWriter.send(pkg, self.connection)

            print "RequestEnterGameLobby sent"

        except:
            self.log('Bad [' + str(Constants.CMSG_ENTER_GAME_NAME) + '] Login Request')
            print_exc()
