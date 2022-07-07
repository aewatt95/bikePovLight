import os
import gi


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ProgramWindow(Gtk.Box):

    def __init__(self):
        super().__init__(Gtk.Orientation.HORIZONTAL)

        self.deviceList = self.getSerialDevices("USB")
        self.programming = False
        leftBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        rightBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        diagnoseFrame = Gtk.Frame()
        diagnoseTextBox = Gtk.TextView()
        self.diagnoseText = diagnoseTextBox.get_buffer()
        diagnoseTextBox.set_monospace(True)
        diagnoseTextBox.set_editable(False)
        self.progressBar = Gtk.ProgressBar()
        self.progressBar.set_pulse_step(1.0)

        deviceComboBox = Gtk.ComboBoxText()
        self.refreshDeviceList(deviceComboBox)
        diagnoseFrame.add(diagnoseTextBox)

        baudCombooBox = Gtk.ComboBoxText()
        for index, element in enumerate(["9600", "19200", "115200", "256000"]):
            baudCombooBox.append(str(index), element)
        baudCombooBox.set_active(0)

        programButton = Gtk.Button(label="Start Programming")
        programButton.connect("clicked", self.program)
        leftBox.pack_start(Gtk.Label(label="Log"), False, True, 6)
        leftBox.pack_start(diagnoseFrame, True, True, 6)
        leftBox.pack_end(self.progressBar, False, True, 6)

        rightBox.pack_start(Gtk.Label(label="Device"), False, False, 6)
        rightBox.pack_start(deviceComboBox, False, True, 6)
        rightBox.pack_start(Gtk.Label(label="Baudrate"), False, False, 6)
        rightBox.pack_start(baudCombooBox, False, True, 6)

        rightBox.pack_end(programButton, False, True, 6)
        self.pack_start(leftBox, True, True, 6)
        self.pack_end(rightBox, True, True, 6)

    def getSerialDevices(self, filter=""):
        devDir = "/dev"
        devList = os.listdir(devDir)
        devList = [f"{devDir}/{element}" for element in devList if "tty" in element and filter in element]
        return devList

    def refreshDeviceList(self, deviceComboBox):
        for index, element in enumerate(self.deviceList):
            deviceComboBox.append(str(index), element)
        if len(self.deviceList) == 0:
            deviceComboBox.append("0", "No devices found")
        deviceComboBox.set_active(0)

    def program(self, source: Gtk.Button):
        headerBar = self.get_parent().get_parent().get_titlebar()
        if not self.programming:
            self.diagnoseText.set_text("Programming started ...")
            source.set_label("Stop Programming")
            headerBar.set_sensitive(False)
            [element.set_sensitive(False) for element in source.get_parent().get_children() if element != source]
            self.progressBar.pulse()
            self.programming = True
        else:
            self.diagnoseText.set_text("Programming stopped...")
            source.set_label("Start Programming")
            headerBar.set_sensitive(True)
            [element.set_sensitive(True) for element in source.get_parent().get_children() if element != source]
            self.progressBar.set_fraction(0.0)
            self.programming = False
