from math import cos, pi, sin, floor
from PIL import Image, ImageDraw


class MaskGenerator():
    def __init__(self, circleSize=2, sideSize=400, ledCount=42):
        self.circleSize = circleSize
        self.ledCount = ledCount
        self.circleOffset = self.circleSize/2
        self.backgroundPath = ""
        self.setSideSize(sideSize)
        self.reset()

    def setSideSize(self, sideSize):
        self.sideSize = sideSize
        self.center = self.sideSize/2
        self.reset()
        self._reloadBackground()

    def createRaster(self, xMax, yMax):
        xStep = self.sideSize/(xMax-1)
        yStep = self.sideSize/(yMax-1)

        for i in range(0, xMax):
            for y in range(0, yMax):
                startX = floor(xStep*i)-self.circleOffset
                startY = floor(yStep*y)-self.circleOffset
                stopX = floor(xStep*i)+self.circleOffset
                stopY = floor(yStep*y)+self.circleOffset
                coordinates = (startX, startY, stopX, stopY)
                self.draw.ellipse(coordinates, fill=(255,255,255))

    def createCircular(self, phiSteps, rMax=-1, offset=0):
        if rMax == -1:
            rMax = round(self.ledCount/2)

        for r in range(offset, rMax):
            radius = (self.center/rMax)*r
            for p in range(0, phiSteps):
                phi = ((2.0*pi)/phiSteps)*p
                startX = self.center + (sin(phi)*radius) - self.circleOffset
                startY = self.center + (cos(phi)*radius) - self.circleOffset
                stopX = self.center + (sin(phi)*radius) + self.circleOffset
                stopY = self.center + (cos(phi)*radius) + self.circleOffset
                coordinates = (floor(startX), floor(startY), floor(stopX), floor(stopY))
                self.draw.ellipse(coordinates, fill=(255,255,255,0))

    def drawBar(self, pitch, offset):
        barThickness = self.sideSize*0.05
        barLength = self.sideSize*0.8
        ledDistance = self.sideSize/self.ledCount
        startX = self.center - (barLength/2) - offset*ledDistance
        startY = self.center - (barThickness/2) - pitch*ledDistance
        stopX = self.center + (barLength/2) - offset*ledDistance
        stopY = self.center + (barThickness/2) - pitch*ledDistance
        coordinates = (floor(startX), floor(startY), floor(stopX), floor(stopY))
        self.draw.rectangle(coordinates, fill=(32,32,32,200), outline=(200,200,200,200))

    def drawMagnet(self, clock):
        phi = pi-((2*pi)/12.0)*clock
        radius = self.center - self.center/10
        magnetSize = 10
        startX = self.center + (sin(phi)*radius) - magnetSize
        startY = self.center + (cos(phi)*radius) - magnetSize
        stopX = self.center + (sin(phi)*radius) + magnetSize
        stopY = self.center + (cos(phi)*radius) + magnetSize
        coordinates = (floor(startX), floor(startY), floor(stopX), floor(stopY))
        print(coordinates)
        self.draw.ellipse(coordinates, fill=(64,64,64,200), outline=(200,200,200,200))

    def drawOverlay(self, filePath):
        try:
            image = Image.open(filePath)
        except Exception as e:
            print(f"Could not open image file: {e}")
            return
        image.resize((self.sideSize, self.sideSize))

    def reset(self):
        self.image = Image.new(mode="RGBA", size=(self.sideSize, self.sideSize), color=(0,0,0,255))
        self.draw = ImageDraw.Draw(self.image)

    def _reloadBackground(self):
        self.background = Image.new("RGBA", (self.sideSize, self.sideSize), (255,0,0,255))
        if self.backgroundPath != "":
            self.background = Image.open(self.backgroundPath).resize((self.sideSize, self.sideSize)).convert("RGBA")

    def setBackground(self, imagePath=""):
        self.backgroundPath = imagePath
        if self.backgroundPath != "":
            self._reloadBackground()

    def get(self):
        return Image.alpha_composite(self.background, self.image).convert("RGB")
