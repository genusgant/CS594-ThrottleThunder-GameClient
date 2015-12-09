__author__ = 'dthakurta'

from direct.task import Task
from common.Constants import Constants
from panda3d.core import Vec3
import time, threading
import math
import copy
from Audio import Audio


class PowerupTypes:
    def __init__(self):
        self.list = {1: {"name": "SHIELD", "rating": 20, "time": 5},
                     2: {"name": "BOOST", "rating": 20, "time": 5},
                     3: {"name": "INVINCIBLE", "rating": 0, "time": 5},
                     4: {"name": "HEALTH", "rating": 20, "time": 5}}


class PowerupPositions:
    def __init__(self):
        self.positions = {
                1: {"id": 1, "x": 0, "y": 0, "z": -1.5},
                2: {"id": 2, "x": -30, "y": 40, "z": -3},
                3: {"id": 3, "x": -10, "y": 40, "z": -3},
                4: {"id": 4, "x": -15, "y": -20, "z": -2},
                5: {"id": 5, "x": 60, "y": 10, "z": -3},
                6: {"id": 6, "x": 70, "y": 60, "z": -3},
                7: {"id": 7, "x": 70, "y": 25, "z": -3.5},
                8: {"id": 8, "x": 40, "y": 75, "z": -3.5}
            }

class PowerupIcon:
    def __init__(self, main, powerupInfo):
        self.main = main
        self.id = powerupInfo['id']
        self.posX = powerupInfo['x']
        self.posY = powerupInfo['y']
        self.posZ = powerupInfo['z']
        self.powerName = powerupInfo['item']['name']
        self.powerRating = powerupInfo['item']['rating']
        self.powerTime = powerupInfo['item']['time']
        self.player = None
        
        self.itemIcon = loader.loadModel("models/speedpowerup.egg")

        if self.powerName == "SHIELD":
            self.shield_tex = loader.loadTexture("models/power_ups/shieldtext.png")
            self.itemIcon.setTexture(self.shield_tex, 1)
            self.itemIcon.setScale(.6)
        elif self.powerName == "BOOST":
            self.boost_tex = loader.loadTexture("models/power_ups/speedtext.png")
            self.itemIcon.setTexture(self.boost_tex, 1)
            self.itemIcon.setScale(.6)
        elif self.powerName == "INVINCIBLE":
            self.invincible_tex = loader.loadTexture("models/power_ups/invinstext.png")
            self.itemIcon.setTexture(self.invincible_tex, 1)
            self.itemIcon.setScale(.6)
        elif self.powerName == "HEALTH":
            self.health_tex = loader.loadTexture("models/power_ups/healthtext.png")
            self.itemIcon.setTexture(self.health_tex, 1)
            self.itemIcon.setScale(.6)

        self.itemIcon.reparentTo(self.main.worldNP)
        self.itemIcon.setPos(self.posX, self.posY, self.posZ)
        
        self.rotate()

    def removeFromField(self):
        # move the powerup under the map
        self.itemIcon.setPos(self.posX, self.posY, self.posZ - 50)
    
    def returnToField(self):
        self.itemIcon.setPos(self.posX, self.posY, self.posZ)
        
    def rotate(self):
        self.spinPowerUp = self.itemIcon.hprInterval(1, Vec3(360, 0, 0))
        self.spinPowerUp.loop()

class PowerupManager:
    #Max number of each powerup
    MAX_COUNT = 2
    POWERUP_RESET_TIME = 60

    def __init__(self, main, actor):
        self.actor = actor
        self.powerupViews = {}
        self.takenPowers = []
        self.activePowers = []
        self.main = main
        self.cManager = main.cManager
        self.Audio = Audio(self)

        powerupTypes = PowerupTypes()
        self.powerupPositions = PowerupPositions().positions

        pwrKey = 1
        instanceCount = 0
        for posKey in self.powerupPositions.keys():
            if instanceCount >= PowerupManager.MAX_COUNT:
                instanceCount = 0
                pwrKey += 1
            posValue = self.powerupPositions[posKey]
            pwrVal = powerupTypes.list[pwrKey]
            posValue["item"] = pwrVal
            self.powerupPositions[posKey] = posValue
            powerUpView = PowerupIcon(self.main, posValue)
            self.powerupViews[posKey] = powerUpView
            if posKey not in self.activePowers:
                self.activePowers.append(posKey)
            instanceCount += 1
            #print "posValue", posValue

    def createPowerup(self, powerupInfo):
        if (powerupInfo['item']['name'] == "SHIELD"):
            return ShieldPowerup(self, powerupInfo)
        elif(powerupInfo['item']['name'] == "BOOST"):
            return BoostPowerup(self, powerupInfo)
        elif(powerupInfo['item']['name'] == "INVINCIBLE"):
            return InvinciblePowerup(self, powerupInfo)
        elif(powerupInfo['item']['name'] == "HEALTH"):
            return HealthPowerup(self, powerupInfo)
    
    def setActors(self, actors):
        self.actors = actors

    def checkPowerPickup(self, task):
        powerObtain = self.powerPickup(self.main.vehicleContainer, self.main.vehicleContainer.chassisNP.getPos(), 1)#actor.actorRadius)
        
        # if powerObtain != 0:
        #     self.handlePowerups(powerObtain)
        return task.cont

    def obtainPowerups(self, powerObtain):
        #print self.powerupPositions[powerObtain]['item']['name']
        if self.powerupPositions[powerObtain]['item']['name'] == "SHIELD":
            self.actor.props.armor += self.powerupPositions[powerObtain]['item']['rating']
            #print "New Armor: ", self.actor.props.armor
            if self.actor.props.armor > self.actor.props.constants.MAX_ARMOR[self.actor.props.type]:
                self.actor.props.armor = self.actor.props.constants.MAX_ARMOR[self.actor.props.type]
            self.main.cManager.sendRequest(Constants.CMSG_HEALTH, self.actor.props.getHitPoint())

        if self.powerupPositions[powerObtain]['item']['name'] == "HEALTH":
            self.actor.props.health += self.powerupPositions[powerObtain]['item']['rating']
            #print "New Health: ", self.actor.props.health
            if self.actor.props.health > self.actor.props.constants.MAX_HEALTH[self.actor.props.type]:
                self.actor.props.health = self.actor.props.constants.MAX_HEALTH[self.actor.props.type]
            self.main.cManager.sendRequest(Constants.CMSG_HEALTH, self.actor.props.getHitPoint())

        if self.powerupPositions[powerObtain]['item']['name'] == "BOOST":
            if self.actor.boostCount < 3:
                self.actor.boostCount += 1

        if self.powerupPositions[powerObtain]['item']['name'] == "INVINCIBLE":
            #print "INVINCIBLE"
            self.actor.props.isInvincible = True
            killInvinsibility = threading.Thread(target=self.resetInvinsibility, args=(powerObtain,))
            killInvinsibility.start()

    def powerPickup(self, actor, actorPos, actorRadius):
        powerObtained = 0
        for posKey in self.powerupPositions.keys():
            powerUp = self.powerupPositions[posKey]
            if (math.pow((actorPos.x - powerUp['x']), 2) + math.pow((actorPos.y - powerUp['y']), 2) + math.pow((actorPos.z - powerUp['z']), 2)
                    <= math.pow(actorRadius, 2)):
                powerObtained = powerUp['id']
                if powerObtained in self.activePowers:
                    self.activePowers.remove(powerObtained)
                    if powerObtained not in self.takenPowers:
                        self.takenPowers.append(powerObtained)
                    self.cManager.sendRequest(Constants.CMSG_POWER_UP, powerUp['id'])
                    self.Audio.play_powerup()
                    # print "powerObtained: ", powerObtained
                    self.resetPowerupsTask(powerObtained)
                break

        return powerObtained

    def resetPowerupsTask(self, powerupId, pickup=False):
        processThread = threading.Thread(target=self.resetPowerup, args=(powerupId,))
        #Remove powerup from available list and add to taken list
        if powerupId in self.activePowers:
            self.activePowers.remove(powerupId)
        if powerupId not in self.takenPowers:
            self.takenPowers.append(powerupId)
        powerView = self.powerupViews[powerupId]
        powerView.removeFromField()
        processThread.start()
        if pickup:
            self.obtainPowerups(powerupId)

    def resetPowerup(self, powerupId):
        time.sleep(PowerupManager.POWERUP_RESET_TIME)
        #print self.takenPowers.get(powerupId)
        if powerupId not in self.activePowers:
            self.activePowers.append(powerupId)
        if powerupId in self.takenPowers:
            self.takenPowers.remove(powerupId)
        powerView = self.powerupViews[powerupId]
        powerView.returnToField()
        #print self.activePowers
        #print self.takenPowers

    def resetInvinsibility(self, powerupId):
        time.sleep(self.powerupPositions[powerupId]['item']['time'])
        self.actor.props.isInvincible = False