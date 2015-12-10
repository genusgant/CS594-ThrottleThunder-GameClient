from direct.showbase.DirectObject import DirectObject
from direct.showbase import Audio3DManager
from direct.interval.IntervalGlobal import Sequence, SoundInterval


class Audio(DirectObject):
    def __init__(self, base, world):
        self.world = world
        self.base = base

        # Create an audio manager. This is attached to the camera for
        # player 1, so sounds close to other players might not be very loud
        # self.audioManager = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.camera)
        self.startAudioManager()

        # play background music
        self.play_music_rr()
        # engine sound
        self.engineSound = self.audioManager.loadSfx("audio/accelerating/accelerating1.ogg")
        # self.engineSound.setLoop(True)
        self.engineSound.setPlayRate(1.0)
        # self.engineSound.play()

        self.audioManager.attachSoundToObject(self.engineSound, self.world.vehicleContainer.chassisNP)
        self.brakeSound = self.audioManager.loadSfx("audio/braking/braking2.ogg")
        # self.brakeSound.setLoop(True)
        self.brakeSound.setPlayRate(1.0)
        self.audioManager.attachSoundToObject(self.brakeSound, self.world.vehicleContainer.chassisNP)

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

    def play_collision(self):
        collide = loader.loadSfx("audio/crashing/crashing4.ogg")
        collide.setVolume(1.0)
        collide.play()

    def process_input(self, inputState):
        if inputState.isSet('forward') and (
                        self.engineSound.status() != self.engineSound.PLAYING or self.engineSound.getVolume() < .5):
            self.play_acceleration()
            # print "accel"
        elif not inputState.isSet('forward') and self.engineSound.status() == self.engineSound.PLAYING:
            self.stop_acceleration()

        if inputState.isSet('brake') and (
                        self.brakeSound.status() != self.brakeSound.PLAYING or self.brakeSound.getVolume() < .5) and self.world.vehicleContainer.vehicle.getCurrentSpeedKmHour() > 2.0:
            self.play_brake()
        elif not inputState.isSet('brake') and (
                    self.brakeSound.status() == self.brakeSound.PLAYING) or self.world.vehicleContainer.vehicle.getCurrentSpeedKmHour() < 1.0:
            self.stop_brake()

    def stop_brake(self):
        # print self.brakeSound.getVolume()
        # self.brakeSound.setVolume(self.brakeSound.getVolume)
        # fades the brake sound
        if self.brakeSound.getVolume() < .5:
            self.brakeSound.stop()
        self.brakeSound.setVolume(self.brakeSound.getVolume() - .02)
        self.brakeSound.stop()

    def play_brake(self):
        # self.audioManager.attachSoundToObject(self.brakeSound, self.world.mainCharRef.chassisNP)
        if self.engineSound.status() == self.engineSound.PLAYING:
            self.engineSound.stop()
        self.brakeSound.setVolume(1.0)
        self.brakeSound.play()

    def stop_acceleration(self):
        # fades the sound out then stops when volume is too low
        if self.engineSound.getVolume() < .3:
            self.engineSound.stop()
        self.engineSound.setVolume(self.engineSound.getVolume() - .02)
        # print self.engineSound.getVolume()

    def play_acceleration(self):
        # self.audioManager.attachSoundToObject(self.engineSound, self.world.mainCharRef.chassisNP)
        #        self.engineSound.setLoop(True)
        #       self.engineSound.setPlayRate(0.6)
        # reset volume
        # if self.engineSound.getVolume() < 0.0:
        self.engineSound.setVolume(1.0)
        self.engineSound.play()

    def startAudioManager(self):

        # Create an audio manager. This is attached to the camera for
        # player 1, so sounds close to other players might not be very
        # loud
        self.audioManager = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.camera)

        # Distance should be in m, not feet
        self.audioManager.setDistanceFactor(3.28084)

        # self.initialiseSound(self.audioManager)

        # def initialiseSound(self, vehicleContainer):
        #     """Start the engine sound and set collision sounds"""
        #
        #     # Set sounds to play for collisions
        #     # self.collisionSound = CollisionSound(
        #     #     nodePath=self.np,
        #     #     sounds=["data/sounds/09.ogg"],
        #     #     thresholdForce=600.0,
        #     #     maxForce=800000.0)
        #
        #     # np - nodePath
        #
        #     self.engineSound = self.audioManager.loadSfx("audio/accelerating/accelerating1.ogg")
        #     self.audioManager.attachSoundToObject(self.engineSound, self.world.mainCharRef.chassisNP)
        #     self.engineSound.setLoop(True)
        #     self.engineSound.setPlayRate(0.6)
        #     self.engineSound.play()
        #
        #     self.display_gear = OnscreenText(text="N", style=3, fg=(1, 1, 1, 1),
        #                                      pos=(0.917, -0.80), align=TextNode.ARight, scale=.10, font=self.font_digital)
        #
        #     # self.gearSpacing = (self.specs["sound"]["maxExpectedRotationRate"] /
        #     #     self.specs["sound"]["numberOfGears"])
        #
        #
        #
        #     self.gearSpacing = (self.mainCharRef.specs['maxSpeed'] / 4)
        #
        #     self.reversing = False
        #
        # def updateSound(self, vehicleContainer):
        #     """Use vehicle speed to update sound pitch"""
        #
        #     # soundSpecs = self.specs["sound"]
        #     # Use rear wheel rotation speed as some measure of engine revs
        #     # wheels = (self.vehicle.getWheel(idx) for idx in (2, 3))
        #     # wheelRate is in degrees per second
        #     # wheelRate = 0.5 * abs(sum(w.getDeltaRotation() / dt for w in wheels))
        #     # self.speed = char.getSpeed()
        #     speed = vehicleContainer.getSpeed()
        #     # print speed
        #     # print vehicleContainer.specs['maxSpeed']
        #
        #     wheelRate = 0.75 * speed
        #
        #     # Calculate which gear we're in, and what the normalised revs are
        #     if self.reversing:
        #         numberOfGears = 1
        #     else:
        #         numberOfGears = 4
        #     # gear = min(int(wheelRate / self.gearSpacing),
        #     #         numberOfGears - 1)
        #
        #     gear = min(int(wheelRate / self.gearSpacing),
        #                numberOfGears - 1)
        #
        #     # print gear
        #     self.display_gear.destroy()
        #     self.display_gear = OnscreenText(text=str(gear + 1), style=3, fg=(1, 1, 1, 1),
        #                                      pos=(0.917, -0.80), align=TextNode.ARight, scale=.10, font=self.font_digital)
        #
        #     if max(int(wheelRate / self.gearSpacing), numberOfGears - 1) < 4:
        #         # posInGear = (wheelRate - gear * self.gearSpacing) / self.gearSpacing
        #         posInGear = (wheelRate - gear * self.gearSpacing) / self.gearSpacing
        #
        #         # print posInGear
        #
        #         targetPlayRate = 0.6 + posInGear * (1.5 - 0.6)
        #
        #         # print targetPlayRate
        #
        #         currentRate = self.engineSound.getPlayRate()
        #         self.engineSound.setPlayRate(0.8 * currentRate + 0.2 * targetPlayRate)
