from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse


class ResponseChatOne(ServerResponse):
    def execute(self, data):

        try:
            self.sender_id = data.getInt32()
            self.receiver_id = data.getInt32()
            self.msg = data.getString()

            print "ResponseChatOne - ", self.sender_id, self.receiver_id, self.msg

            # if self.receiver_id == self.world.character.playerId:
            #    print self.msg
            self.temp = "/" + str(self.sender_id) + ": " + self.msg
            # if self.otherId == self.world.character.playerId or self.otherId == 0:
            self.world.chatbox.chat_memory[self.sender_id].append(self.temp)

            # refresh chatbox
            self.world.chatbox.updateChat(self.sender_id)

            # self.log('Received [' + str(Constants.CMSG_CHAT_ALL) + '] String Response')

        except:
            self.log('Bad [' + str(Constants.CMSG_CHAT_ONE) + '] String Response')
            print_exc()
