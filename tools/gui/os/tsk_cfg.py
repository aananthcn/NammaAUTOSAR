#
# Created on Sun Oct 02 2022 10:07:39 AM
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
import tkinter as tk
from tkinter import ttk

from .evt_cfg import EventWindow

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box



class TaskTab:
    n_tasks = 1
    n_tasks_str = None
    max_tasks = 1024
    events = []
    
    n_header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    xsize = None
    ysize = None

    active_dialog = None
    active_widget = None

    non_header_objs = []
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["Task Name", "PRIORITY", "SCHEDULE", "ACTIVATION", "AUTOSTART_APPMODE", "EVENT", "RESOURCE", "STACK_SIZE"]
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False

    amtab = None
    rstab = None
    mstab = None


    # def __init__(self, tasks, amtab, rstab, mstab):
    def __init__(self, tasks, amtab, rstab):
        self.n_tasks = len(tasks)
        self.n_tasks_str = tk.StringVar()
        self.configs = []

        # add tasks to UI passed from ARXML file
        for task in tasks:
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, task))

        # collect all info from other tabs
        self.amtab = amtab
        self.rstab = rstab


    def __del__(self):
        del self.n_tasks_str
        del self.non_header_objs[:]
        del self.configs[:]


    def create_empty_configs(self):
        task = {}
        
        # Use the last task's name and numbers to ease the edits made by user 
        task["Task Name"] = "Task_"
        task["PRIORITY"] = "0"
        task["SCHEDULE"] = "NON" # Pre-emption (NON / FULL)
        task["ACTIVATION"] = "1"
        task["AUTOSTART"] = "FALSE"
        task["AUTOSTART_APPMODE"] = []
        task["RESOURCE"] = []
        task["EVENT"] = []
        task["STACK_SIZE"] = "512"

        return task



    def draw_dappa_row(self, i):
        n_appmod = n_events = n_resources = 0
        dappa.label(self, "Task ", self.header_row+i, 0, "e")
        
        # Task Name
        dappa.entry(self, "Task Name", i, self.header_row+i, 1, 30, "normal")

        # PRIORITY
        dappa.entry(self, "PRIORITY", i, self.header_row+i, 2, 10, "normal")

        # SCHEDULE
        dappa.combo(self, "SCHEDULE", i, self.header_row+i, 3, 8, ("NON", "FULL"))

        # ACTIVATION
        dappa.entry(self, "ACTIVATION", i, self.header_row+i, 4, 11, "normal")

        # AUTOSTART[]
        text = "AppModes["+str(dappa.button_selections(self, i, "AUTOSTART_APPMODE"))+"]"
        cb = lambda id = i: self.select_autostart_modes(id)
        dappa.button(self, "AUTOSTART_APPMODE", i, self.header_row+i, 5, 13, text, cb)

        # EVENT[]
        text = "Events["+str(dappa.button_selections(self, i, "EVENT"))+"]"
        cb = lambda id = i: self.select_events(id)
        dappa.button(self, "EVENT", i, self.header_row+i, 6, 13, "Events["+str(n_events)+"]", cb)

        # RESOURCE[]
        text = "Resources["+str(dappa.button_selections(self, i, "RESOURCE"))+"]"
        cb = lambda id = i: self.select_resources(id)
        dappa.button(self, "RESOURCE", i, self.header_row+i, 7, 13, text, cb)

        # # MESSAGE[]
        dappa.entry(self, "STACK_SIZE", i, self.header_row+i, 8, 11, "normal")



    def update(self):
        # get dappas to be added or removed
        self.n_tasks = int(self.n_tasks_str.get())
        
        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_tasks > n_dappa_rows:
            for i in range(self.n_tasks - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_tasks:
            for i in range(n_dappa_rows - self.n_tasks):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab, xsize, ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.scrollw = window.ScrollableWindow(tab, self.xsize, self.ysize)

        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Tasks:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_tasks_str, command=self.update,
                    values=tuple(range(1,self.max_tasks+1)))
        self.n_tasks_str.set(self.n_tasks)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()




    def backup_data(self):
        print("backup_data called in tsk_cfg")



    def on_autostart_dialog_close(self, task_id):
        # remove old selections
        if "AUTOSTART_APPMODE" in self.configs[task_id].datavar:
            # del self.sg_tasks[task_id].datavar["AUTOSTART_APPMODE"][:]
            if self.configs[task_id].datavar["AUTOSTART_APPMODE"]:
                del self.configs[task_id].datavar["AUTOSTART_APPMODE"][:]
    
        # update new selections
        if len(self.active_widget.curselection()) == 0:
            self.configs[task_id].datavar["AUTOSTART"] = "FALSE"
        else:
            self.configs[task_id].datavar["AUTOSTART"] = "TRUE"
            for i in self.active_widget.curselection():
                self.configs[task_id].datavar["AUTOSTART_APPMODE"].append(self.active_widget.get(i))
        
        # dialog elements are no longer needed, destroy them. Else, new dialogs will not open!
        self.active_widget.destroy()
        del self.active_widget
        self.active_dialog.destroy()
        del self.active_dialog

        # refresh screen
        self.update()


    def select_autostart_modes(self, id):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_autostart_dialog_close(id))
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        self.active_dialog.geometry("+%d+%d" % (0 + x/3, y/16))

        # show all app modes
        self.active_widget = tk.Listbox(self.active_dialog, selectmode=tk.MULTIPLE, width=40, height=15)
        for i, obj in enumerate(self.amtab.AM_StrVar):
            appmode = obj.get()
            self.active_widget.insert(i, appmode)
            if id < len(self.configs) and self.configs[id].datavar["AUTOSTART_APPMODE"]:
                    if appmode in self.configs[id].datavar["AUTOSTART_APPMODE"]:
                        self.active_widget.selection_set(i)
        self.active_widget.pack()


    def on_event_dialog_close(self, task_id):
        # remove old selections
        if self.configs[task_id].datavar["EVENT"]:
            del self.configs[task_id].datavar["EVENT"][:]

        # update new selections from last window session
        for strvar in self.active_widget.events_str:
            self.configs[task_id].datavar["EVENT"].append(strvar.get())
        
        # dialog elements are no longer needed, destroy them. Else, new dialogs will not open!
        del self.active_widget
        self.active_dialog.destroy()
        del self.active_dialog

        # refresh screen
        self.update()


    def select_events(self, id):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_event_dialog_close(id))
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        self.active_dialog.geometry("+%d+%d" % (0 + x/3, y/12))

        # show all events specific to task[id]
        self.active_widget = EventWindow(self.configs[id].get())
        self.active_widget.draw(self.active_dialog)


    def on_resource_dialog_close(self, task_id):
        # remove old selections
        if self.configs[task_id].datavar["RESOURCE"]:
            del self.configs[task_id].datavar["RESOURCE"][:]

        # update new selections
        if len(self.active_widget.curselection()):
            for i in self.active_widget.curselection():
                self.configs[task_id].datavar["RESOURCE"].append(self.active_widget.get(i))
        
        # dialog elements are no longer needed, destroy them. Else, new dialogs will not open!
        self.active_widget.destroy()
        del self.active_widget
        self.active_dialog.destroy()
        del self.active_dialog

        # refresh screen
        self.update()


    def select_resources(self, id):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_resource_dialog_close(id))
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        self.active_dialog.geometry("+%d+%d" % (0 + x/2, y/16))

        # show all app modes
        self.active_widget = tk.Listbox(self.active_dialog, selectmode=tk.MULTIPLE, width=40, height=15)
        for i, obj in enumerate(self.rstab.ress_str):
            res = obj.get()
            self.active_widget.insert(i, res)
            if id < len(self.configs) and self.configs[id].datavar["RESOURCE"]:
                if res in self.configs[id].datavar["RESOURCE"]:
                    self.active_widget.selection_set(i)
        self.active_widget.pack()
