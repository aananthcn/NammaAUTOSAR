#
# Created on Thu Aug 11 2022 10:35:41 PM
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
import arxml.main as arxml
import gui.autosar.mod_view as av


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

import gui.os.os_tab as gui_os_tab
import gui.os.am_tab as gui_am_tab
import gui.os.cnt_tab as gui_cr_tab
import gui.os.msg_tab as gui_ms_tab
import gui.os.res_tab as gui_rs_tab
import gui.os.tsk_tab as gui_tk_tab
import gui.os.alm_tab as gui_al_tab
import gui.os.isr_tab as gui_ir_tab


###############################################################################
# Globals
###############################################################################
# GUI stuffs
MenuBar = None
FileMenu = None
OsTab = AmTab = CtrTab = MsgTab = ResTab = TskTab = AlmTab = IsrTab = None

# I/O stuffs
OIL_FileName = None
ArXml_FileName = None
RecentFiles = os.getcwd()+"/.filelist"
ToolsPath = os.getcwd()+"/tools"


# UI Stuffs - View
class View:
    root = None
    xsize = None
    ysize = None
    window = None

    def __init__(self):
        self.root = tk.Tk()
        self.xsize = self.root.winfo_screenwidth()
        self.ysize = self.root.winfo_screenheight()

    def destroy_view(self):
        for widget in self.window.winfo_children():
	        widget.destroy()
        self.window.destroy()



# UI Stuffs - FreeAUTOSAR Configurator Tool
class FreeAutosarConfTool:
    view = View()
    title = "AUTOSAR Builder"


Gui = None



###############################################################################
# Functions
###############################################################################
def about():
    messagebox.showinfo(ToolName, "This tool is developed to replace the OSEK-Builder.xlsx and to set path for AUTOSAR development")



def show_os_tab_switch(event):
    global OsTab, AmTab, CtrTab, MsgTab, ResTab, TskTab, AlmTab, IsrTab 

    current_tab = None #this variable can be used for debugging!
    if Gui.view.window.tab(Gui.view.window.select(), "text").strip() == "OS Configs":
        TskTab.backup_data()
        OsTab.backup_data()  # take the lastest stack size updates from Task tab.
        OsTab.update()
        current_tab = OsTab
    if Gui.view.window.tab(Gui.view.window.select(), "text").strip() == "AppModes":
        current_tab = AmTab
    if Gui.view.window.tab(Gui.view.window.select(), "text").strip() == "Counters":
        current_tab = CtrTab
    if Gui.view.window.tab(Gui.view.window.select(), "text").strip() == "Messages":
        current_tab = MsgTab
    if Gui.view.window.tab(Gui.view.window.select(), "text").strip() == "Resources":
        current_tab = ResTab
    if Gui.view.window.tab(Gui.view.window.select(), "text").strip() == "Tasks":
        current_tab = TskTab
    if Gui.view.window.tab(Gui.view.window.select(), "text").strip() == "Alarms":
        AlmTab.update()
        current_tab = AlmTab
    if Gui.view.window.tab(Gui.view.window.select(), "text").strip() == "ISRs":
        current_tab = IsrTab


    
def show_os_config(view):
    global OsTab, AmTab, CtrTab, MsgTab, ResTab, TskTab, AlmTab, IsrTab

    if Gui.view.window != None:
        Gui.view.destroy_view()
    Gui.view.window = ttk.Notebook(view)
    
    os_tab = ttk.Frame(Gui.view.window)
    am_tab = ttk.Frame(Gui.view.window)
    cr_tab = ttk.Frame(Gui.view.window)
    ms_tab = ttk.Frame(Gui.view.window)
    rs_tab = ttk.Frame(Gui.view.window)
    tk_tab = ttk.Frame(Gui.view.window)
    al_tab = ttk.Frame(Gui.view.window)
    ir_tab = ttk.Frame(Gui.view.window)
    
    Gui.view.window.add(os_tab, text ='OS Configs')
    Gui.view.window.add(am_tab, text =' AppModes ')
    Gui.view.window.add(cr_tab, text =' Counters ')
    Gui.view.window.add(ms_tab, text =' Messages ')
    Gui.view.window.add(rs_tab, text =' Resources ')
    Gui.view.window.add(tk_tab, text ='   Tasks   ')
    Gui.view.window.add(al_tab, text ='  Alarms  ')
    Gui.view.window.add(ir_tab, text ='   ISRs   ')
    Gui.view.window.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    del OsTab
    del AmTab
    del CtrTab
    del MsgTab
    del ResTab
    del TskTab
    del AlmTab
    del IsrTab

    # create new GUI objects
    OsTab = gui_os_tab.OsTab(sg.OS_Cfgs, sg.Tasks)
    OsTab.draw(os_tab)

    AmTab = gui_am_tab.AmTab(sg.AppModes)
    AmTab.draw(am_tab)
    
    CtrTab = gui_cr_tab.CounterTab(sg.Counters)
    CtrTab.draw(cr_tab)

    MsgTab = gui_ms_tab.MessageTab(sg.Tasks)
    MsgTab.draw(ms_tab)

    ResTab = gui_rs_tab.ResourceTab(sg.Tasks)
    ResTab.draw(rs_tab)

    TskTab = gui_tk_tab.TaskTab(sg.Tasks, AmTab, ResTab, MsgTab)
    TskTab.draw(tk_tab)
    
    AlmTab = gui_al_tab.AlarmTab(sg.Alarms, TskTab, AmTab, CtrTab)
    AlmTab.draw(al_tab)

    IsrTab = gui_ir_tab.IsrTab(sg.ISRs, ResTab, MsgTab)
    IsrTab.draw(ir_tab)

    Gui.view.window.bind("<<NotebookTabChanged>>", show_os_tab_switch)
    


def new_file():
    global Gui
    global OsTab, AmTab, CtrTab, MsgTab, ResTab, TskTab, AlmTab, IsrTab

    sg.sg_reset()
    show_os_config(Gui.view.root)
    FileMenu.entryconfig("Save", state="normal")



def open_oil_file(fpath):
    global Gui, OIL_FileName

    init_dir = os.getcwd()
    if os.path.exists(os.getcwd()+"/output/oil-files"):
        init_dir = os.getcwd()+"/output/oil-files"

    if fpath == None:
        filename = filedialog.askopenfilename(initialdir=init_dir)
        if type(filename) is not tuple and len(filename) > 5:
            OIL_FileName = filename
        else:
            print("Info: no or many OIL file is chosen, hence open_oil_file() returning without processing!")
            return
    else:
        OIL_FileName = fpath

    if Gui.view.root != None:
        Gui.view.root.title(Gui.title + " [" + str(OIL_FileName).split("/")[-1] +"]")

    # Make System Generator to parse, so that we can use the content in GUI.
    sg.sg_reset()
    sg.parse(OIL_FileName)
    show_os_config(Gui.view.root)
    FileMenu.entryconfig("Save", state="normal")


def backup_gui_before_save():
    # Do the stack memory calculation before save
    OsTab.update()

    # Backup GUI strings to System Generator global data
    OsTab.backup_data()
    AmTab.backup_data()
    CtrTab.backup_data()
    MsgTab.backup_data()
    ResTab.backup_data()
    TskTab.backup_data()
    AlmTab.backup_data()
    IsrTab.backup_data()



def save_project():
    global OsTab, AmTab, CtrTab, MsgTab, ResTab, TskTab, AlmTab, IsrTab
    global OIL_FileName, ArXml_FileName

    backup_gui_before_save()

    # Export if the input file OIL file.
    if OIL_FileName != None:
        file_exts = [('ARXML Files', '*.arxml')]
        saved_filename = filedialog.asksaveasfile(initialdir=os.getcwd()+"/output/arxml", filetypes = file_exts, defaultextension = file_exts)
        if saved_filename == None:
            messagebox.showinfo(ToolName, "File to save is not done correctly, saving aborted!")
            return
        ArXml_FileName = saved_filename.name
        print("Info: Exporting "+OIL_FileName+" to "+ArXml_FileName+" ...")
        OIL_FileName = None

    # Save if the input file is ARXML
    elif ArXml_FileName != None:
        print("Info: Saving configs to "+ArXml_FileName+" ...")
    
    # Warn if both file variables are not set
    else:
        messagebox.showinfo(ToolName, "Invalid input (project) file. Can't save project!")
        return


    # Export and File name clean up
    arxml.export_arxml(ArXml_FileName)
    Gui.view.root.title(Gui.title + " [" + ArXml_FileName.split("/")[-1] +"]")



def generate_code():
    srcpath = ToolsPath+"\os_builder\src"
    if 0 == sg.generate_code(srcpath):
        messagebox.showinfo(ToolName, "Code Generated Successfully!")
    else:
        messagebox.showinfo(ToolName, "Code Generation Failed!")



def save_as_arxml():
    file_exts = [('ARXML Files', '*.arxml')]
    saved_filename = filedialog.asksaveasfile(initialdir=os.getcwd()+"/output/arxml", filetypes = file_exts, defaultextension = file_exts)
    if saved_filename == None:
        messagebox.showinfo(ToolName, "File to save is not done correctly, saving aborted!")
        return

    Gui.view.root.title(Gui.title + " [" + str(saved_filename.name).split("/")[-1] +"]")
    backup_gui_before_save()
    arxml.export_arxml(saved_filename.name)



def open_arxml_file(fpath):
    global Gui, ArXml_FileName

    init_dir = os.getcwd()
    if os.path.exists(os.getcwd()+"/output/arxml"):
        init_dir = os.getcwd()+"/output/arxml"

    if fpath == None:
        filename = filedialog.askopenfilename(initialdir=init_dir)
        if type(filename) is not tuple and len(filename) > 5:
            ArXml_FileName = filename
        else:
            print("Info: no or many ARXML file is chosen, hence open_arxml_file() returning without processing!")
            return
    else:
        ArXml_FileName = fpath.strip()

    if Gui.view.root != None:
        Gui.view.root.title(Gui.title + " [" + str(ArXml_FileName).split("/")[-1] +"]")

    # Import/Parse ARXML file, so that we can use the content in GUI.
    sg.sg_reset()
    imp_status = arxml.import_arxml(ArXml_FileName)
    update_recent_files(ArXml_FileName)
    show_os_config(Gui.view.root)
    if imp_status != 0:
        messagebox.showinfo(ToolName, "Input file contains errors, hence opening as new file!")
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
            FileMenu.add_command(label=file_path, command=lambda: open_arxml_file(file_path))
        FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=rv.quit)
    MenuBar.add_cascade(label="File", menu=FileMenu)

    view = tk.Menu(MenuBar, tearoff=0)
    view.add_command(label="OS Config", command=lambda: show_os_config(rv))
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


def init_view_setup(fpath, ftype):
    if ftype == None or fpath == None:
        return
    elif ftype == "oil":
        open_oil_file(fpath)
    elif ftype == "arxml":
        open_arxml_file(fpath)
    else:
        print("Unsupported filetype argument provided!")




def update_recent_files(filepath):
    with open(RecentFiles) as rfile:
        raw_list = rfile.readlines()
        rfile.close()

    rfile = open(RecentFiles, 'a')
    if filepath not in raw_list:
        rfile.write("\n"+filepath)
    rfile.close()



def get_recent_files():
    file_list = []
    try:
        with open(RecentFiles) as rfile:
            raw_list = rfile.readlines()
            rfile.close()
    except:
        raw_list = []

    for item in raw_list:
        if item.strip() not in file_list:
            if len(item) > 4: # 4 for a dot and at least 3 letters.
                file_list.append(item.strip())

    with open(RecentFiles, 'w') as rfile:
        for line in file_list:
            rfile.write(f"{line}\n")
    rfile.close()

    return file_list



def main(fpath, ftype):
    global Gui
    
    # Create the main window
    ## Gui.view.root = tk.Tk()
    Gui = FreeAutosarConfTool()
    Gui.view.root.title(Gui.title + " [uninitialized]")
    flst = get_recent_files()
    add_menus(Gui.view.root, flst)
    Gui.view.root.state("zoomed")

    # setup init view
    init_view_setup(fpath, ftype)

    # Run forever!
    Gui.view.root.mainloop()


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
        srcpath = filepath.split("FreeOSEK")[0]+"FreeOSEK/tools/src"
        sg.set_source_file_path(srcpath)
    if "-t" in sys.argv:
        filetype = sys.argv[sys.argv.index("-t") + 1]
    
    # let us start the GUI
    main(fpath=filepath, ftype=filetype)