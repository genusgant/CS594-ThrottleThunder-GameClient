from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseRankings(ServerResponse):

    def execute(self, data):

        try:
            self.world.dashboard.total_players = data.getInt32()
            rankings={}
            # rankings = {data.getString() : data.getInt32()}

            #print "self.world.dashboard.total_players: ",self.world.dashboard.total_players
            for x in range(0, self.world.dashboard.total_players):
                name = data.getString()
                rank = data.getInt32()
                rankings[rank] = name
            self.world.dashboard.update_ranking(rankings)

            #self.log('Received [' + str(Constants.RAND_STRING) + '] String Response')

        except:
            self.log('Bad [' + str(Constants.SMSG_RANKINGS) + '] Rankings Response')
            print_exc()
