import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf, GLib
from tool.MaskGenerator import MaskGenerator

class SettingsWindow(Gtk.Box):
    def __init__(self):
        super().__init__(Gtk.Orientation.HORIZONTAL)
        imageFrame = Gtk.Frame()
        self.image = Gtk.Image()

        self.maskGenerator = MaskGenerator(circleSize=2, sideSize=800)

        rightBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

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
        self.pack_start(imageFrame, True, True, 6)
        self.pack_end(rightBox, True, True, 6)

        self.sliderMoved(None)

        rightBox.show_all()

    def sliderMoved(self, source):
        qualitySteps = [64, 128, 256]
        quality = qualitySteps[self.qualityComboBox.get_active()]
        magnet = self.magnetScale.get_value()
        pitch = self.pitchScale.get_value()
        offset = self.offsetScale.get_value()
        self.maskGenerator.reset()
        self.maskGenerator.createCircular(quality, offset=4)
        self.maskGenerator.drawMagnet(magnet)
        self.maskGenerator.drawBar(offset, pitch)
        self.image.set_from_pixbuf(self.image2pixbuf(self.maskGenerator.get()))

    def image2pixbuf(self, image):

        data = image.tobytes()
        width, height = image.size
        data = GLib.Bytes.new(data)
        pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB,
                False, 8, width, height, width * 3)
        return pix

    def generateMask(resolution):
        pass
