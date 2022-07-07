import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf

from common import Common

class FileWindow(Gtk.Box):
    def __init__(self):
        super().__init__(Gtk.Orientation.HORIZONTAL)

        imageFrame = Gtk.Frame()
        self.image = Gtk.Image()
        addButton = Gtk.Button.new_with_label("Add")
        rightBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        imageFrame.add(self.image)
        self.imageList = Gtk.ListBox()
        self.imageList.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.imageList.connect('row-activated', self.imageClicked)

        addButton.connect("clicked", self.buttonHandler)

        rightBox.pack_start(self.imageList, True, True, 0)
        rightBox.pack_end(addButton, False, True, 6)

        self.pack_start(imageFrame, True, True, 6)
        self.pack_end(rightBox, True, True, 6)

    def imageClicked(self, listBox: Gtk.ListBox, row: Gtk.ListBoxRow):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename=Common.fileList[row.get_index()])
        pixbuf = pixbuf.scale_simple(400,400,GdkPixbuf.InterpType.BILINEAR)
        self.image.set_from_pixbuf(pixbuf=pixbuf)

    def sortUp(self, element: Gtk.Button):
        rowIndex = element.get_parent().get_parent().get_index()
        Common.fileList.insert(rowIndex-1, Common.fileList.pop(rowIndex))
        self.recreateImageList()

    def sortDown(self, element: Gtk.Button):
        rowIndex = element.get_parent().get_parent().get_index()
        Common.fileList.insert(rowIndex+1, Common.fileList.pop(rowIndex))
        self.recreateImageList()

    def deleteFile(self, element: Gtk.Button):
        rowIndex = element.get_parent().get_parent().get_index()
        Common.fileList.pop(rowIndex)
        self.recreateImageList()
        if len(Common.fileList) == 0:
            self.image.clear()
        else:
            nextSelect = rowIndex
            if nextSelect == len(self.imageList):
                nextSelect = len(self.imageList)-1
            self.imageList.select_row(self.imageList.get_row_at_index(nextSelect))
            self.imageClicked(None, self.imageList.get_selected_row())

    def buttonHandler(self, widget):
        fileDialog = Gtk.FileChooserDialog(action=Gtk.FileChooserAction.OPEN)
        fileDialog.set_title("Please choose an image file")
        fileDialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        if len(Common.fileList) != 0:
            print("Setting folder to " + str(("".join(Common.fileList[-1][:Common.fileList[-1].rindex("/")]))))
            fileDialog.set_current_folder("".join(Common.fileList[-1][:Common.fileList[-1].rindex("/")]))

        imageFiler = Gtk.FileFilter()
        imageFiler.set_name("Image files")
        imageFiler.add_mime_type("image/jpg")
        imageFiler.add_mime_type("image/jpeg")
        imageFiler.add_mime_type ("image/png")


        fileDialog.add_filter(imageFiler)

        response = fileDialog.run()

        if response == Gtk.ResponseType.OK:
            Common.fileList.append(fileDialog.get_filename())
            self.recreateImageList()

        fileDialog.destroy()

    def recreateImageList(self):
        for row in self.imageList:
            print(row.get_index())
            self.imageList.remove(row)

        for index, element in enumerate(Common.fileList):
            rowLabel = Gtk.Label(label=element.split("/")[-1])
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            Gtk.StyleContext.add_class(hbox.get_style_context(), "linked")
            row = Gtk.ListBoxRow()

            upButton = Gtk.Button.new_from_icon_name("pan-up-symbolic", Gtk.IconSize.BUTTON)
            upButton.connect("clicked", self.sortUp)
            downButton =  Gtk.Button.new_from_icon_name("pan-down-symbolic", Gtk.IconSize.BUTTON)
            downButton.connect("clicked", self.sortDown)
            deleteButton = Gtk.Button.new_from_icon_name("edit-delete-symbolic", Gtk.IconSize.BUTTON)
            deleteButton.connect("clicked", self.deleteFile)

            if index == 0:
                upButton.set_sensitive(False)
            if index == len(Common.fileList)-1:
                downButton.set_sensitive(False)

            hbox.pack_start(rowLabel, True, True, 6)
            hbox.pack_end(deleteButton, False, False, 0)
            hbox.pack_end(downButton, False, False, 0)
            hbox.pack_end(upButton, False, False, 0)

            row.add(hbox)
            self.imageList.add(row)
        self.imageList.show_all()
