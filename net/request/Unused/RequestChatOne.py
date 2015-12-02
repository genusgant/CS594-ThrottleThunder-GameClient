from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest


class RequestChatOne(ServerRequest):
    def send(self, args=[]):

        try:
            # print "sender's id:", args[0]
            # print "receiver's id:", args[1]
            pkg = PyDatagram()
            pkg.addUint16(Constants.CMSG_CHAT_ONE)
            pkg.addInt32(args[0])  # sender's id
            pkg.addInt32(args[1])  # receiver's id
            pkg.addString(args[2])  # message

            self.cWriter.send(pkg, self.connection)


            # self.log('Sent [' + str(Constants.CMSG_CHAT_ONE) + '] Chat Request')
        except:
            self.log('Bad [' + str(Constants.CMSG_CHAT_ONE) + '] Chat Request')
            print_exc()
