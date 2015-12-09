from traceback import print_exc
from common.Constants import Constants
from net.response.ServerResponse import ServerResponse


class ResponseDead(ServerResponse):
    def execute(self, data):

        try:
            self.username = data.getString()
            print "server sent dead guy:", self.username

            if self.worldMgr.isDDGame:
                if self.username in self.world.vehiclelist.keys():
                    vehicle = self.world.vehiclelist[self.username]
                    vehicle.props.health = vehicle.props.armor = 0
                    vehicle.isDead = True
                    vehicle.remove()
<<<<<<< HEAD
                    self.world.deadCounter += 1
                    # del self.world.vehiclelist[self.username]
                    if self.world.deadCounter == len(self.world.vehiclelist) - 1:
                        print "Last Man Standing"
                    self.world.gameEnd()
            else:  # for RR game
                print "I am:", self.world.login
                if self.world.login == self.username:
                    print "you are dead"
                    self.world.vehicleContainer.chassisNP.remove()

                if self.username in self.world.vehiclelist.keys():
                    vehicle = self.world.vehiclelist[self.username]
                    vehicle.remove()
                    del self.world.vehiclelist[self.username]
                    self.world.deadCounter += 1

                    print "deadCounter/vehiclelist :", self.world.deadCounter, "/", len(self.world.vehiclelist)

                    if self.world.deadCounter == len(self.world.vehiclelist) - 1:
                        print "Last Man Standing"
                        self.world.gameEnd()

                        # vehicle.chassisNP.removeNode()

            print "ResponseDead - ", self.username
            # self.log('Received [' + str(Constants.RAND_STRING) + '] String Response')
=======
                    self.world.deadCounter +=1
                    #del self.world.vehiclelist[self.username]
                    if self.world.deadCounter == len(self.world.vehiclelist)-1:
                        print "Last Man Standing"
                    self.world.gameEnd()
                else:  # for RR game
                    print "RR code here"
                    #vehicle.remove()

            print "ResponseDead - ",self.username
>>>>>>> d5accc3f7cc83e9bbf0afdc242696b051aeb8ee1

        except:
            self.log('Bad [' + str(Constants.SMSG_DEAD) + '] Dead Response')
            print_exc()
