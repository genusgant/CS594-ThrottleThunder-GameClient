'''
Created on Nov 20, 2015

@author: saul
'''
# import CurveHelper
from CurveHelper import loadTrack, makeVec, angleTo, mPoint
from rrCheckpoint import Checkpoint
from common.Constants import Constants

class RaceMaster():
    '''
    
    Keep track of racers positions i.e. who is in 1st, 2nd, 3rd, ...
    each instance tracks checkpointlocs the mvc (my vehicleContainer) object
    rank data is kept self-contained so vehicle classes can be shared by rr and dd
    
    Race master also manages:
        Staring postions
        Powerup positions
    
    Concept:
        Highest lap number
        Most check points
        shortest distance to next check point
        
        Check points exported from track models
        loaded by raceHelper class
    
    todo:
        add to position request response? i think so
        Request to server:
            laps done
            checkpointlocs done (on current lap) or calculate laps by check points?
            distance to next checkpoint (calculate my distance on client, do the work on the server?)
            
        response from server:
            my rank (1st of course)
            
            
        
    '''
    tracks = ['FullTrack.curves', 'flattrack.curves']
    trackscale = [70, 2*.6]

    def __init__(self, mGame, mvc, track, nracers, startingPos):
        '''
        Constructor
        '''
        self.vehicleContainer = mvc
        #         if track < len(RaceMaster.tracks):
        self.checkpointlocs = loadTrack(RaceMaster.tracks[track - 1], RaceMaster.trackscale[track - 1])
        if track == 1:
            self.reverseTrack()  # flip check point order
        #         print self.checkpointlocs
        self.trackSections = startingPos
        self.racers = nracers

        # for tracking race positions
        self.laps = 0
        self.checkpointspassed = 0
        self.distanceToNextCP = 0
        self.lastcp = -1
        self.main = mGame
        self.setupCheckpoints(mGame)
        self.rank = startingPos
        self.setStartingPos(self.rank)
        self.main.nameBar.updateRange(self.racers)


    def playerEliminated(self, playersRemaining):
        self.racers = playersRemaining
        self.main.nameBar.updateRange(self.racers)

    def reverseTrack(self):
        temp = self.checkpointlocs
        l = len(temp)
        self.checkpointlocs = []
        for i in range(l):
            self.checkpointlocs.append(temp[l - i - 1])

    # check points are only counted if its id is > the lastcp. or else you might be going backwards.
    def hitCheckpoint(self, cp):
        if cp > self.lastcp:
            self.lastcp = cp
            self.checkpointspassed += 1

        elif cp == 0:
            if self.lastcp >= self.getCPperLap() - 3:
                # if self.checkpointspassed >= self.getCPperLap():
                self.laps += 1
                self.checkpointspassed = 0
                self.lastcp = -1  #
            # elif self.lastcp != 0:
            #     self.laps -= 1
            #     self.lastcp = 0

                # recalculate cp distance

                # returns number of laps compleated

    def getLaps(self):
        self.laps

    def getCPperLap(self):
        return len(self.checkpointlocs)

    def getRacePos(self):
        return self.rank

    # ____TASK___
    def updateCheckpoints(self, task):
        #self.rank = self.main.mRank
        for i in range(len(self.checkpointmarkers)):
            ghost = self.checkpointmarkers[i].cpnode.node()
            hits = ghost.getNumOverlappingNodes()

            if hits > 0:
                #print("checkpoint" +  str(i) + " " +  str(hits))
                for node in ghost.getOverlappingNodes():
                    if node == self.vehicleContainer.chassisNode:
                        # print("I Hit a checkpoint!!!")
                        self.hitCheckpoint(self.checkpointmarkers[i].cid)
                        # print("cp: " + str( i) + " last id: " + str(self.lastcp) + " cp passed: " + str(self.checkpointspassed))
        self.main.nameBar.setVal(self.rank)
        arg = [ self.laps, self.checkpointspassed ]
        self.main.cManager.sendRequest(Constants.CMSG_CHECKPOINTS, arg)
        self.main.cManager.sendRequest(Constants.CMSG_RANKINGS)

        return task.again

    def setupCheckpoints(self, mGame):
        self.checkpointmarkers = []
        cpl = self.checkpointlocs
        for i in range(len(cpl)-1):
            a = angleTo(cpl[i + 1], cpl[i])
            self.checkpointmarkers.append(Checkpoint(mGame, cpl[i], a))

        self.startingOffsets = [12, 15]
        #                             [[-50.4339, 60.4705, 3.80965, 117.910705566, 0, 0],
        #                             [-51.3537, 64.2902, 3.84785, 116.122093201, 0, 0],
        #                             [-41.7162, 69.1233, 4.14399, 117.631515503, 0, 0],
        #                             [-40.1138, 65.7385, 4.12263, 115.860038757, 0, 0],
        #                             [-30.2054, 70.476, 4.41469, 114.678634644, 0, 0],
        #                             [-32.0705, 74.0726, 4.44123, 115.580863953, 0, 0],
        #                             [-20.1875, 74.9774, 4.47768, 113.226844788, 0, 0],
        #                             [-21.5922, 79.0628, 4.5176, 115.136543274, 0, 0]]

        self.powupPos = self.checkpointlocs

    #                     [(63.0958, 86.3576, 4.49076),
    #                      (26.3338, -54.2244, 4.5037),
    #                      (47.3323, 48.0089, 4.49297),
    #                      (-136.685, 88.1453, 4.49636)]


    def applyOffset(self, start, to, x, y, m):
        return [start.x + x * m, start.y + y * m, start.z, angleTo(start, to), 0, 0]

    def getStartingPoints(self):
        sp = []
        xoff = self.startingOffsets[0]
        yoff = self.startingOffsets[1]
        for i in range(self.racers):
            sp.append(self.applyOffset(self.checkpointlocs[0], self.checkpointlocs[1],  xoff, yoff, i))
        return sp

    def getStartingPoint(self, i):
        xoff = self.startingOffsets[0]
        yoff = self.startingOffsets[1]
        return self.applyOffset(self.checkpointlocs[1], self.checkpointlocs[2], xoff, yoff, i)

    def setStartingPos(self, i):
        print "Setting start pos: ", i
        p = self.getStartingPoint(i)
        self.setPosHpr(p)

    def setPosHpr(self, ph):
        self.vehicleContainer.chassisNP.setPosHpr(ph[0], ph[1], ph[2], ph[3], ph[4], ph[5])

    def resetCar(self):
        l = self.lastcp
        if l == -1: l = 0
        if l > len(self.checkpointlocs) - 2:
            l = l - 2
        pos = self.checkpointlocs[self.lastcp]
        to = self.checkpointlocs[self.lastcp - 1]
        p = [pos.x, pos.y, pos.z, angleTo(pos, to), 0, 0]
        self.setPosHpr(p)

# def generateSections(self):
#         points = self.trackPoints
#         s = len(points)-1
#         sec = []
#         for i int range(s):
#             pass
