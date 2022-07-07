from math import cos, pi, sin, floor
from PIL import Image, ImageDraw


class MaskGenerator():
    def __init__(self, circleSize=2, sideSize=400, ledCount=42):
        self.circleSize = circleSize
        self.sideSize = sideSize
        self.ledCount = ledCount

        self.circleOffset = self.circleSize/2
        self.center = self.sideSize/2

        self.image = Image.new(mode="RGB", size=(sideSize, sideSize))
        self.draw = ImageDraw.Draw(self.image)

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
                self.draw.ellipse(coordinates, fill=(255,255,255))

    def drawBar(self, pitch, offset):
        barThickness = self.sideSize*0.05
        barLength = self.sideSize*0.8
        ledDistance = self.sideSize/self.ledCount
        startX = self.center - (barLength/2) - offset*ledDistance
        startY = self.center - (barThickness/2) - pitch*ledDistance
        stopX = self.center + (barLength/2) - offset*ledDistance
        stopY = self.center + (barThickness/2) - pitch*ledDistance
        coordinates = (floor(startX), floor(startY), floor(stopX), floor(stopY))
        self.draw.rectangle(coordinates, fill=(32,32,32))

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
        self.draw.ellipse(coordinates, fill=(255,0,0))

    def reset(self):
        self.image.paste('black', (0,0,self.sideSize, self.sideSize))

    def get(self):
        return self.image
