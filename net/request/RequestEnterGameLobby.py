from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestEnterGameLobby(ServerRequest):


    def send(self, args ):

        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_ENTER_GAME_LOBBY)
            #pkg.addString(args[0]) #username
            #pkg.addUint16(args[1]) #gameId
            #pkg.addUint16(args[2]) #lobbyId
            pkg.addUInt16(args) #room id
            self.cWriter.send(pkg, self.connection)

            print "RequestEnterGameLobby sent"

        except:
            self.log('Bad [' + str(Constants.CMSG_ENTER_GAME_LOBBY) + '] Login Request')
            print_exc()
