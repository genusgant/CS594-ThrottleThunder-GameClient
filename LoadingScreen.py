__author__ = 'debasish'
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText,TextNode
from direct.task import Task

#countDownStart = 6

class LoadingScreen:
    def __init__(self, main):
        self.main = main
        self.imageObject = OnscreenImage(image = 'IMAGES/loading.jpg', pos = (0, 0, 0))
        self.imageObject.reparentTo(render2d)
        #base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

    def finish(self, countDownStart):
        self.countDownStart = int(countDownStart/1000)
        self.imageObject.destroy()
        self.countDownText = OnscreenText(text=str(countDownStart), style=1, fg=(1,1,1,1),
                pos=(0.01, 0.1), align = TextNode.ACenter, scale = .2, mayChange = 1)
        taskMgr.add(self.countDown,"countDownTask")

    def countDown(self,task):
        timeLeft = "%01d" % (self.countDownStart - task.time)
        if (self.countDownStart - task.time) > 1:
            self.countDownText.setText(timeLeft)
            return task.cont
        elif 1 > (self.countDownStart - task.time) > 0:
            self.countDownText.setText("GO!")
            return task.cont
        else:
            self.canMove = True
            if not self.main.isActive:
                print "Activate"
                self.main.isActive = True
                taskMgr.add(self.main.update, 'updateWorld')
                self.main.activateKeys()
            self.countDownText.destroy()
            return task.done