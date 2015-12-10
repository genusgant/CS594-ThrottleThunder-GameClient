from direct.showbase.DirectObject import DirectObject
from direct.showbase import Audio3DManager
from direct.interval.IntervalGlobal import Sequence, SoundInterval
from panda3d.core import *
from direct.gui.DirectGui import *
from time import sleep


class Audio(DirectObject):
    def __init__(self, main):
        
        self.main = main
        

    def play_music_rr(self):
        # load background music
        music1 = loader.loadSfx("audio/bkgd/m1.ogg")
        music2 = loader.loadSfx("audio/bkgd/m2.ogg")
        music3 = loader.loadSfx("audio/bkgd/m3.ogg")
        music4 = loader.loadSfx("audio/bkgd/m4.ogg")
        music5 = loader.loadSfx("audio/bkgd/m5.ogg")
        music6 = loader.loadSfx("audio/bkgd/m6.ogg")
#        music1 = loader.loadSfx("audio/bkgd/Sandstorm.ogg")
#        music2 = loader.loadSfx("audio/bkgd/LevelsNoVocals.ogg")
#        music3 = loader.loadSfx("audio/bkgd/RaceMusic.ogg")

        music_seq = Sequence(SoundInterval(music1), SoundInterval(music2), SoundInterval(music3), SoundInterval(music4), SoundInterval(music5), SoundInterval(music6),
                             name="Music Sequence")
        music_seq.loop(0.0, -1.0, 1.0)

    def play_music_dd(self):
        # load background music
        self.dd_bg = loader.loadSfx("audio/bg music/DD music/ThrottleThunderSong2.mp3")
        self.dd_bg.setVolume(0.6)       

        # self.music_seq = Sequence(SoundInterval(music1),name="Music Sequence")
        # self.music_seq.loop(0.0, -1.0, 1.0)
        self.dd_bg.setLoop(True)
        self.dd_bg.play()


    def stop_music_dd(self):
        # self.music_seq.stop()
        self.dd_bg.setLoop(False)
        self.dd_bg.stop()


    def play_collision(self):
        crash = loader.loadSfx("audio/Sounds effects/crashing/crashing4.mp3")
        crash.setVolume(0.7) 
        crash.play()


    def play_powerup(self):
        music = loader.loadSfx("audio/Sounds effects/powerups/powerup1.mp3")
        music.setVolume(0.8) 
        music.play()


    def play_brake(self):
        brake = loader.loadSfx("audio/Sounds effects/braking/braking3.mp3")
        brake.setVolume(0.7) 
        brake.play()

    def play_victory(self):
        music = loader.loadSfx("audio/victory music/victory1.ogg")
        music.setVolume(0.8) 
        sleep(2)
        music.play()

    def play_loser(self):
        music = loader.loadSfx("audio/lose music/Losing Horn.mp3")
        music.setVolume(0.8) 
        sleep(2)
        music.play()

    def play_brake(self):
        crash = loader.loadSfx("audio/Sounds effects/braking/braking3.mp3")
        crash.setVolume(0.8) 
        crash.play()

        

    def startAudioManager(self):

        # Create an audio manager. This is attached to the camera for
        # player 1, so sounds close to other players might not be very
        # loud
        self.audioManager = Audio3DManager.Audio3DManager(base.sfxManagerList[0],base.camera)

        # Distance should be in m, not feet
        self.audioManager.setDistanceFactor(3.28084)


    def StopAudioManager(self):

        self.engineSound.stop()
        




    def initialiseSound(self,vehicleContainer):

        """Start the engine sound and set collision sounds"""

        # Set sounds to play for collisions
        # self.collisionSound = CollisionSound(
        #     nodePath=self.np,
        #     sounds=["data/sounds/09.wav"],
        #     thresholdForce=600.0,
        #     maxForce=800000.0)

        # np - nodePath

        self.engineSound = self.audioManager.loadSfx("audio/sound/engine.wav")
        self.audioManager.attachSoundToObject(self.engineSound, vehicleContainer.chassisNP)
        self.engineSound.setLoop(True)
        self.engineSound.setPlayRate(0.6)
        self.engineSound.setVolume(0.4)
        self.engineSound.play()

        self.gearSpacing = (vehicleContainer.specs['maxSpeed'] / 4)

        self.reversing = False
            


    def updateSound(self,vehicleContainer):
        """Use vehicle speed to update sound pitch"""

        speed, normalizedSpeed = vehicleContainer.getSpeed()
            
        wheelRate = 0.75 * speed

        # Calculate which gear we're in, and what the normalised revs are
        if self.reversing:
            numberOfGears = 1
        else:
            numberOfGears = 4

        gear = min(int(wheelRate/ self.gearSpacing),
                numberOfGears - 1)            

        if max(int(wheelRate/ self.gearSpacing),numberOfGears - 1) < 4 :
            
            posInGear = (wheelRate - gear * self.gearSpacing) / self.gearSpacing

            targetPlayRate = 0.6 + posInGear * (1.5 - 0.6)

            currentRate = self.engineSound.getPlayRate()
            self.engineSound.setPlayRate(0.8 * currentRate + 0.2 * targetPlayRate)
