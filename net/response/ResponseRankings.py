from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseRankings(ServerResponse):

    def execute(self, data):

        try:
            if self.worldMgr.isDDGame:
                self.world.dashboard.total_players = data.getInt32()
                rankings = {}
                # rankings = {data.getString() : data.getInt32()}

                #print "self.world.dashboard.total_players: ",self.world.dashboard.total_players
                for x in range(0, self.world.dashboard.total_players):
                    name = data.getString()
                    rank = data.getInt32()
                    rankings[rank] = name
                self.world.dashboard.update_ranking(rankings)
            else:
                if self.world.dash_ready: # if dashboard is ready
                    self.world.dashboard.total_players = data.getInt32()
                    rankings = {}
                    # rankings = {data.getString() : data.getInt32()}

                    #print "self.world.dashboard.total_players: ",self.world.dashboard.total_players
                    for x in range(0, self.world.dashboard.total_players):
                        name = data.getString()
                        rank = data.getInt32()
                        rankings[rank] = name
                        #print(name +  " Rank: " + str(rank))
                    self.world.dashboard.update_ranking(rankings)

        except:
            self.log('Bad [' + str(Constants.SMSG_RANKINGS) + '] Rankings Response')
            print_exc()
