import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf, GLib
from tool.MaskGenerator import MaskGenerator

from common import Common
class SettingsWindow(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        leftBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        rightBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.lastSize = 0
        self.currentPreviewIndex = 0
        self.maskGenerator = MaskGenerator(circleSize=4, sideSize=400)

        self.connect("size_allocate", self.resizeHandler)

        imageFrame = Gtk.Frame.new(label="Preview")
        self.image = Gtk.Image()

        previewSettingsBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        backButton = Gtk.Button.new_from_icon_name("pan-start-symbolic", Gtk.IconSize.BUTTON)
        backButton.connect("clicked", self.imageChange, -1)
        nextButton = Gtk.Button.new_from_icon_name("pan-end-symbolic", Gtk.IconSize.BUTTON)
        nextButton.connect("clicked", self.imageChange, 1)
        self.deviceCheckBox = Gtk.CheckButton.new_with_label(label="Show device")
        self.deviceCheckBox.connect("toggled", self.sliderMoved)
        self.magnetCheckBox = Gtk.CheckButton.new_with_label(label="Show magnet")
        self.magnetCheckBox.connect("toggled", self.sliderMoved)
        previewSettingsBox.pack_start(backButton, True, True, 6)
        previewSettingsBox.pack_start(self.deviceCheckBox, False, False, 6)
        previewSettingsBox.pack_start(self.magnetCheckBox, False, False, 6)
        previewSettingsBox.pack_end(nextButton, True, True, 6)

        qualityList = ["Low", "Normal", "High"]

        qualityLabel = Gtk.Label(label="Quality")
        self.qualityComboBox = Gtk.ComboBoxText()
        for element in qualityList:
            self.qualityComboBox.append_text(element)
        self.qualityComboBox.set_entry_text_column(0)
        self.qualityComboBox.set_active(1)
        self.qualityComboBox.connect("changed", self.sliderMoved)

        pitchLabel = Gtk.Label(label="Pitch")
        self.pitchScale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        self.pitchScale.set_range(-20,20)
        self.pitchScale.set_digits(0)
        self.pitchScale.connect("value-changed", self.sliderMoved)

        offsetLabel = Gtk.Label(label="Offset")
        self.offsetScale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        self.offsetScale.set_range(-20,20)
        self.offsetScale.set_digits(0)
        self.offsetScale.connect("value-changed", self.sliderMoved)

        magnetLabel = Gtk.Label(label="Magent position")
        self.magnetScale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        self.magnetScale.set_range(0,12)
        self.magnetScale.set_digits(1)
        self.magnetScale.connect("value-changed", self.sliderMoved)

        rightBox.pack_start(qualityLabel, False, False, 6)
        rightBox.pack_start(self.qualityComboBox, False, True,6)
        rightBox.pack_start(pitchLabel, False, False, 6)
        rightBox.pack_start(self.pitchScale, False, True, 6)
        rightBox.pack_start(offsetLabel, False, False, 6)
        rightBox.pack_start(self.offsetScale, False, True, 6)
        rightBox.pack_start(magnetLabel, False, False, 6)
        rightBox.pack_start(self.magnetScale, False, True, 6)

        imageFrame.add(self.image)

        leftBox.pack_start(imageFrame, True, True, 6)
        leftBox.pack_end(previewSettingsBox, False, False, 6)
        self.pack_start(leftBox, True, True, 6)
        self.pack_end(rightBox, True, True, 6)

        self.sliderMoved(None)

        rightBox.show_all()

    def imageChange(self, source, skipCount=0):
        self.currentPreviewIndex += skipCount
        if self.currentPreviewIndex > len(Common.fileList) - 1:
            self.currentPreviewIndex = len(Common.fileList) - 1
        if self.currentPreviewIndex < 0:
            self.currentPreviewIndex = 0
        print(f"imageChanged: {self.currentPreviewIndex} | {len(Common.fileList)}")
        if len(Common.fileList) == 0:
            self.maskGenerator.setBackground()
        else:
            self.maskGenerator.setBackground(imagePath=Common.fileList[self.currentPreviewIndex])
        self.sliderMoved(None)

    def sliderMoved(self, source):
        qualitySteps = [64, 128, 256]
        quality = qualitySteps[self.qualityComboBox.get_active()]
        magnet = self.magnetScale.get_value()
        pitch = self.pitchScale.get_value()
        offset = self.offsetScale.get_value()
        self.maskGenerator.reset()
        self.maskGenerator.createCircular(quality, offset=4)
        if self.magnetCheckBox.get_active():
            self.maskGenerator.drawMagnet(magnet)
        if self.deviceCheckBox.get_active():
            self.maskGenerator.drawBar(offset, pitch)
        image = self.maskGenerator.get()
        self.image.set_from_pixbuf(self.image2pixbuf(image))

    def image2pixbuf(self, image):
        data = image.tobytes()
        width, height = image.size
        data = GLib.Bytes.new(data)
        pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB,
                False, 8, width, height, width * 3)
        return pix

    def resizeHandler(self, source: Gtk.Box, whatever):
        if self.lastSize == (source.get_allocated_height(), source.get_allocated_width()):
            return

        self.lastSize = (source.get_allocated_height(), source.get_allocated_width())
        heightDiff = int(source.get_allocated_height()*0.8)
        widthDiff = int(source.get_allocated_width()*0.8)

        newImageSize = heightDiff
        if heightDiff > widthDiff:
            newImageSize = widthDiff

        self.maskGenerator.setSideSize(newImageSize)
        self.sliderMoved(None)