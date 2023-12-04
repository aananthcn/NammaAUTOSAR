import gi
import os
import sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import ui_about as about

from tkinter import filedialog


# Include local paths
sys.path.insert(0, os.getcwd()+"/tools/os_builder")
sys.path.insert(0, os.getcwd()+"/tools/arxml")
sys.path.insert(0, os.getcwd()+"/tools/gui")
sys.path.insert(0, os.getcwd()+"/tools")

import os_builder.scripts.System_Generator as sg
import os_builder.scripts.oil as oil

import arxml.core.main_os as arxml
import arxml.core.lib as lib

import gui.os.os_view as os_view
import gui.mcu.uc_view as uc_view



###############################################################################
# Globals
###############################################################################
# I/O stuffs
OIL_FileName = None
RecentFiles = os.getcwd()+"/.filelist"
ToolsPath = os.getcwd()+"/tools"


# UI Stuffs - View
Gui = None
AppNameStr = "Namma AUTOSAR Builder"




###############################################################################
# Project and File related
###############################################################################
def new_file():
    sg.sg_reset()
    #av.show_autosar_modules_view(Gui)
    print("av.show_autosar_modules_view(Gui)")
    #FileMenu.entryconfig("Save", state="normal")
    print("FileMenu.entryconfig(\"Save\", state=\"normal\")")



def open_oil_file(fpath):
    global Gui, OIL_FileName

    init_dir = os.getcwd()
    if os.path.exists(os.getcwd()+"/cfg/oil-files"):
        init_dir = os.getcwd()+"/cfg/oil-files"

    if fpath == None:
        filename = filedialog.askopenfilename(initialdir=init_dir)
        if type(filename) is not tuple and len(filename) > 5:
            OIL_FileName = filename
        else:
            print("Info: no or many OIL file is chosen, hence open_oil_file() returning without processing!")
            return
    else:
        OIL_FileName = fpath

    window = Gui.builder.get_object("ASR_MAIN_WINDOW")
    window.set_title(AppNameStr+" ["+filename+"]")
    

    # Make System Generator to parse, so that we can use the content in GUI.
    sg.sg_reset()
    sg.parse(OIL_FileName)
    print("av.show_autosar_modules_view(Gui)")
    #FileMenu.entryconfig("Save", state="normal")



def open_arxml_file(fpath):
    global Gui
    
    print("open file ="+fpath)

    init_dir = os.getcwd()
    if os.path.exists(os.getcwd()+"/cfg/arxml"):
        init_dir = os.getcwd()+"/cfg/arxml"

    if fpath == None:
        filename = filedialog.askopenfilename(initialdir=init_dir)
        if type(filename) is not tuple and len(filename) > 5:
            Gui.set_arxml_filepath(filename)
        else:
            print("Info: no or many ARXML file is chosen, hence open_arxml_file() returning without processing!")
            return
    else:
        Gui.set_arxml_filepath(fpath.strip())
        filename = fpath

    window = Gui.builder.get_object("ASR_MAIN_WINDOW")
    window.set_title(AppNameStr+" ["+filename+"]")

    # Import/Parse ARXML file, so that we can use the content in GUI.
    sg.sg_reset()
    imp_status = arxml.import_arxml(Gui.arxml_file)
    update_recent_files(Gui.arxml_file)
    print("av.show_autosar_modules_view(Gui)")
    if imp_status != 0:
        messagebox.showinfo(Gui.title, "Input file contains errors, hence opening as new file!")
        new_file()
    else:
        print("correct the menu state handling!")
        #FileMenu.entryconfig("Save", state="normal")



###############################################################################
# Save and Save As Handling
###############################################################################
def save_as_arxml():
    global Gui
    
    file_exts = [('ARXML Files', '*.arxml')]
    saved_filename = filedialog.asksaveasfile(initialdir=os.getcwd()+"/output/arxml", filetypes = file_exts, defaultextension = file_exts)
    if saved_filename == None:
        messagebox.showinfo(Gui.title, "File to save is not done correctly, saving aborted!")
        return

    Gui.set_arxml_filepath(saved_filename.name)
    Gui.main_view.tk.title(Gui.title + " [" + str(saved_filename.name).split("/")[-1] +"]")
    os_view.backup_os_gui_before_save()
    arxml.export_os_cfgs_2_arxml(saved_filename.name, Gui)



###############################################################################
# Recent Files related
###############################################################################
def recent_file_menu_click(self):
        label = self.get_label()
        print("menu item selected: " + label)
        open_arxml_file(label)


def add_submenus(builder, obj_str, menulst_str):
        root_menu = builder.get_object(obj_str)
        submenu = Gtk.Menu()
        root_menu.set_submenu(submenu)

        for mitem in menulst_str:
                ch_m_item = Gtk.MenuItem(label=mitem)
                ch_m_item.connect("activate", recent_file_menu_click)
                submenu.append(ch_m_item)

def update_recent_files(filepath):
        if not os.path.exists(RecentFiles):
                # create empty file
                wfile = open(RecentFiles, 'w')
                wfile.close()

        with open(RecentFiles) as rfile:
                raw_list = rfile.readlines()
                rfile.close()

        wlist = []
        wlist.append(filepath)
        for file in raw_list:
                if file.strip() not in wlist and ".arxml" in file:
                        if len(wlist) < 10:
                                wlist.append(file.strip())

        wfile = open(RecentFiles, 'w')
        for item in wlist:
                wfile.write(item+"\n")
        wfile.close()


def get_recent_files():
        file_list = []
        try:
                with open(RecentFiles) as rfile:
                        raw_list = rfile.readlines()
                        rfile.close()
        except:
                raw_list = []

        for item in raw_list:
                if item.strip() not in file_list and ".arxml" in item:
                        file_list.append(item.strip())

        return file_list



###############################################################################
# Main View Class and stuffs
###############################################################################
class MainViewHandler:
        def on_MainWindow_destroy(self, *args):
                Gtk.main_quit()
            
        def on_ASR_MENU_NEW_activate(self, args):
                new_file()

        def on_ASR_MENU_OPEN_activate(self, args):
                open_arxml_file(None)

        def on_ASR_MENU_IMP_ARXML_FILE_activate(self, args):
                open_arxml_file(None)

        def on_ASR_MENU_IMP_OIL_FILE_activate(self, args):
                open_oil_file(None)

        def on_ASR_MENU_ABOUT_activate(self, args):
                about.main()


# UI Stuffs - FreeAUTOSAR Configurator Tool
class MainView:
        # Target System Attributes
        uc_info = uc_view.Uc_Info()
        
        # General Attributes
        arxml_file = None

        # Glade stuffs
        builder = None
        
        # Graphical Attributes
        main_view = None        # the GUI root frame
        micro_block = None      # the Microcontroller block widget
        recentfiles = None
        asr_blocks = {}

        # Methods
        def __init__(self, builder):
                self.builder = builder
                self.main_view = self
                # self.main_view.tk.title(self.title + " [uninitialized]")
                recentfiles = get_recent_files()
                add_submenus(self.builder, "ASR_MENU_RECENT_FILES", recentfiles)
                #if os.name == 'nt':
                #self.main_view.tk.state("zoomed")
                #else:
                #self.main_view.tk.wm_state("normal")

        def init_view_setup(self, fpath, ftype):
                if ftype == None or fpath == None:
                        return
                elif ftype == "oil":
                        open_oil_file(fpath)
                elif ftype == "arxml":
                        open_arxml_file(fpath)
                else:
                        print("Unsupported filetype argument provided!")

        def show_os_config(self):
                os_view.show_os_config(self)

        def show_uc_view(self):
                uc_view.show_microcontroller_block(self)
                
        def set_arxml_filepath(self, filepath):
                self.arxml_file = filepath
                lib.setget_ecuc_arpkg_name(filepath)



def main(fpath, ftype):
        global Gui
        
        builder = Gtk.Builder()
        builder.add_from_file(os.getcwd()+"/ui/res/ui-main-view.glade")
        builder.connect_signals(MainViewHandler())

        Gui = MainView(builder)

        window = builder.get_object("ASR_MAIN_WINDOW")
        window.show_all()

        Gtk.main()



#
# Arguments to osek-builder-gui.py if invoked from command-line
#
# -f: "file name with path to open"
# -t: filetype ["oil", "arxml"]
#
if __name__ == '__main__':
    filepath = None
    filetype = None

    # collect the arguments if it is passed as arguments
    if "-f" in sys.argv:
        filepath = sys.argv[sys.argv.index("-f") + 1]
        filepath = os.path.abspath(filepath)
        filepath = filepath.replace(os.sep, '/')
        # set source code generation path
        srcpath = filepath.split("NammaAUTOSAR")[0]+"NammaAUTOSAR/tools/src"
        sg.set_source_file_path(srcpath)
    if "-t" in sys.argv:
        filetype = sys.argv[sys.argv.index("-t") + 1]
    
    # let us start the GUI
    main(fpath=filepath, ftype=filetype)