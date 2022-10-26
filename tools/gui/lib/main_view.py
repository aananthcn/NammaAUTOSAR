#
# Created on Fri Aug 19 2022 12:39:35 PM
#
# The MIT License (MIT)
# Copyright (c) 2022 Aananth C N
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import os
import sys


# Let us use the System Generator functions to parse OIL and Generate code
sys.path.insert(0, os.getcwd()+"/tools/os_builder")
sys.path.insert(0, os.getcwd()+"/tools/arxml")

import os_builder.scripts.System_Generator as sg
import os_builder.scripts.oil as oil
import arxml.core.main as arxml


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

import gui.os.os_view as os_view
import gui.mcu.uc_view as uc_view
import gui.lib.asr_view as av

import arxml.core.lib as lib

#
#   CLASSES
#
class MainView:
    tk = None
    xsize = None
    ysize = None
    child_window = None
    
    def __init__(self):
        self.tk = tk.Tk()
        self.xsize = self.tk.winfo_screenwidth()
        self.ysize = self.tk.winfo_screenheight()

    def destroy_childwindow(self):
        if self.child_window == None:
            return
        for widget in self.child_window.winfo_children():
	        widget.destroy()
        self.child_window.destroy()



# UI Stuffs - FreeAUTOSAR Configurator Tool
class FreeAutosarConfTool:
    # Target System Attributes
    uc_info = uc_view.Uc_Info()
    
    # General Attributes
    arxml_file = None
    
    # Graphical Attributes
    title = "NammaAUTOSAR Builder"
    main_view = None        # the GUI root frame
    micro_block = None      # the Microcontroller block widget
    recentfiles = None
    asr_blocks = {}

    # Methods
    def __init__(self):
        global Gui
        Gui = self
        self.main_view = MainView()
        self.main_view.tk.title(self.title + " [uninitialized]")
        recentfiles = get_recent_files()
        add_menus(self.main_view.tk, recentfiles)
        # self.main_view.tk.state("zoomed")
        self.main_view.tk.wm_state("normal")

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
    


###############################################################################
# Globals
###############################################################################
# GUI stuffs
MenuBar = None
FileMenu = None

# I/O stuffs
OIL_FileName = None
RecentFiles = os.getcwd()+"/.filelist"
ToolsPath = os.getcwd()+"/tools"


# UI Stuffs - View
Gui = None



###############################################################################
# Functions
###############################################################################
def about():
    messagebox.showinfo(Gui.title, "This tool is developed to replace the OSEK-Builder.xlsx and to set path for AUTOSAR development")



def new_file():
    global Gui

    sg.sg_reset()
    av.show_autosar_modules_view(Gui)
    FileMenu.entryconfig("Save", state="normal")



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

    if Gui.main_view.tk != None:
        Gui.main_view.tk.title(Gui.title + " [" + str(OIL_FileName).split("/")[-1] +"]")

    # Make System Generator to parse, so that we can use the content in GUI.
    sg.sg_reset()
    sg.parse(OIL_FileName)
    av.show_autosar_modules_view(Gui)
    FileMenu.entryconfig("Save", state="normal")



def save_project():
    global OIL_FileName, Gui

    os_view.backup_os_gui_before_save()

    # Export if the input file OIL file.
    if OIL_FileName != None:
        file_exts = [('ARXML Files', '*.arxml')]
        saved_filename = filedialog.asksaveasfile(initialdir=os.getcwd()+"/output/arxml", filetypes = file_exts, defaultextension = file_exts)
        if saved_filename == None:
            messagebox.showinfo(Gui.title, "File to save is not done correctly, saving aborted!")
            return
        Gui.set_arxml_filepath(saved_filename.name)
        print("Info: Exporting "+OIL_FileName+" to "+Gui.arxml_file+" ...")
        OIL_FileName = None

    # Save if the input file is ARXML
    elif Gui.arxml_file != None:
        print("Info: Saving configs to "+Gui.arxml_file+" ...")
    
    # Warn if both file variables are not set
    else:
        messagebox.showinfo(Gui.title, "Invalid input (project) file. Can't save project!")
        return


    # Export and File name clean up
    arxml.export_arxml(Gui.arxml_file, Gui)
    Gui.main_view.tk.title(Gui.title + " [" + Gui.arxml_file.split("/")[-1] +"]")



def generate_code():
    srcpath = ToolsPath+"\os_builder\src"
    if 0 == sg.generate_code(srcpath):
        messagebox.showinfo(Gui.title, "Code Generated Successfully!")
    else:
        messagebox.showinfo(Gui.title, "Code Generation Failed!")



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
    arxml.export_arxml(saved_filename.name, Gui)



def open_arxml_file(fpath):
    global Gui

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

    if Gui.main_view.tk != None:
        Gui.main_view.tk.title(Gui.title + " [" + str(Gui.arxml_file).split("/")[-1] +"]")

    # Import/Parse ARXML file, so that we can use the content in GUI.
    sg.sg_reset()
    imp_status = arxml.import_arxml(Gui.arxml_file)
    update_recent_files(Gui.arxml_file)
    av.show_autosar_modules_view(Gui)
    if imp_status != 0:
        messagebox.showinfo(Gui.title, "Input file contains errors, hence opening as new file!")
        new_file()
    else:
        FileMenu.entryconfig("Save", state="normal")



###############################################################################
# Fuction: add_menus
# args: rv - root view
#    
def add_menus(rv, flst):
    global MenuBar, FileMenu
    MenuBar = tk.Menu(rv, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
    FileMenu = tk.Menu(MenuBar, tearoff=0)
    FileMenu.add_command(label="New", command=new_file)
    FileMenu.add_command(label="Import OIL File", command=lambda: open_oil_file(None))
    FileMenu.add_command(label="Import ARXML File", command=lambda: open_arxml_file(None))
    FileMenu.add_separator()
    FileMenu.add_command(label="Save", command=save_project, state="disabled")
    FileMenu.add_command(label="Save As", command=save_as_arxml)
    FileMenu.add_separator()
    if len(flst) > 0:
        for file_path in flst:
            FileMenu.add_command(label=file_path, command=lambda fp = file_path: open_arxml_file(fp))
        FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=rv.quit)
    MenuBar.add_cascade(label="File", menu=FileMenu)

    view = tk.Menu(MenuBar, tearoff=0)
    view.add_command(label="OS Config", command=lambda: os_view.show_os_config(Gui))
    view.add_command(label="AUTOSAR Module View", command=lambda: av.show_autosar_modules_view(Gui))
    MenuBar.add_cascade(label="View", menu=view)

    gen = tk.Menu(MenuBar, tearoff=0)
    gen.add_command(label="Generate Source", command=generate_code)
    MenuBar.add_cascade(label="Generate", menu=gen)

    help = tk.Menu(MenuBar, tearoff=0)
    help.add_command(label="About", command=about)
    MenuBar.add_cascade(label="Help", menu=help)
    
    rv.config(menu=MenuBar)



def textBox():
    print(textb.get())






def update_recent_files(filepath):
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

