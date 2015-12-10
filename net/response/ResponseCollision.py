from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseCollision(ServerResponse):

    def execute(self, data):

        try:
            validate = data.getInt32()

            # if validate == 1:
                # Change Characters Health
                # break

            # I think we are going to have 1 returned to the user, after the Server
            # Registers that they took damage.

            # print "ResponseCollision - ", validate

        except:
            self.log('Bad [' + str(Constants.SMSG_COLLISION) + '] Collision Response')
            print_exc()
