from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseResults(ServerResponse):

    def execute(self, data):

        try:
            self.playerCount = data.getInt32()
            self.results = {data.getString() : data.getInt32()}

            # for x in range(0, self.playerCount)
            #     self.results[data.getString()] = data.getInt32()

            print "ResponseMove - ",self.playerCount

            #self.log('Received [' + str(Constants.RAND_STRING) + '] String Response')

        except:
            self.log('Bad [' + str(Constants.SMSG_RESULTS) + '] Results Response')
            print_exc()
