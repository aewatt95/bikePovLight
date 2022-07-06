from fastapi import File
import gi

from ui.FileWindow import FileWindow
from ui.SettingsWindow import SettingsWindow
from ui.ProgramWindow import ProgramWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="bSpokeLight Editor")
        self.fileList = []


        stack = self.createMainWindow()
        self.add(stack)
        self.set_titlebar(self.createHeaderBar(stack))



    def createHeaderBar(self, stack):
        headerBar = Gtk.HeaderBar(show_close_button=True)
        backButton = Gtk.Button()

        backButton.add(Gtk.Arrow(arrow_type=Gtk.ArrowType.LEFT, shadow_type=Gtk.ShadowType.NONE))

        headerBar.pack_start(backButton)
        headerBar.pack_start(self.createStackSwitcher(stack))

        return headerBar

    def createStackSwitcher(self, stack):
        stackSwitcher = Gtk.StackSwitcher()
        stackSwitcher.set_stack(stack)
        return stackSwitcher

    def createMainWindow(self):

        self.set_border_width(10)
        self.set_default_size(800, 500)


        stack = Gtk.Stack()
        stack.set_transition_duration(500)
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.add_titled(FileWindow(), "file", "Images")
        stack.add_titled(SettingsWindow(), "settings", "Configuration")
        stack.add_titled(ProgramWindow(), "program", "Programming")

        return stack


if __name__ == "__main__":
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()