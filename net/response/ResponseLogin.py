from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseLogin(ServerResponse):

    def execute(self, data):

        try:
            flag = data.getInt32()

            print "ResponseLogin - ", flag


            if flag == 1:
                self.world.responseValue = 1

        except:
            self.log('Bad [' + str(Constants.SMSG_LOGIN) + '] Login Response')
            print_exc()
