import gi
import os


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def main():
    
    builder = Gtk.Builder()
    builder.add_from_file(os.getcwd()+"/ui/res/ui-about.glade")
    #builder.connect_signals(MainViewHandler())

    window = builder.get_object("ASR_DIALOG_ABOUT")
    window.show_all()

    #Gtk.main()


if __name__ == '__main__':
    # start the GUI
    main(fpath=filepath, ftype=filetype)