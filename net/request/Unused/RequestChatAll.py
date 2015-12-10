from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest


class RequestChatAll(ServerRequest):
    def send(self, args=[]):

        try:

            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_CHAT_ALL)
            pkg.addInt32(args[0]) #sender id
            pkg.addString(args[1]) #msg

            self.cWriter.send(pkg, self.connection)
            # print "id:", self.world.mainCharRef.playerId

            #elf.log('Sent [' + str(Constants.CMSG_CHAT_ALL) + '] Chat Request')
        except:
            self.log('Bad [' + str(Constants.CMSG_CHAT_ALL) + '] Chat Request')
            print_exc()
