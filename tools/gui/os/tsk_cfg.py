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


class TaskStr:
    id = 0
    name = None
    prio = None
    schedule = None
    activation = None
    stack_sz = None
    n_appmod = 0
    n_events = 0
    n_resources = 0
    n_messages = 0

    def __init__(self, id):
        self.id = id
        self.name = tk.StringVar()
        self.prio = tk.StringVar()
        self.schedule = tk.StringVar()
        self.activation = tk.StringVar()
        self.stack_sz = tk.StringVar()
        self.n_appmod = 0  # start with zero appmodes
        self.n_events = 0  # start with zero events
        self.n_resources = 0 # start with zero resources
        self.n_messages = 0 # start with zero messages

    def __del__(self):
        del self.name
        del self.prio
        del self.schedule
        del self.activation
        del self.stack_sz


class TaskTab:
    n_tasks = 1
    max_tasks = 1024
    n_tasks_str = None
    tasks_str = []
    events = []
    sg_tasks = None
    HeaderObjs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    HeaderSize = 3
    # prf = None  # Parent Frame
    # cvf = None  # Canvas Frame
    # cv  = None  # Canvas
    # sb  = None  # Scrollbar
    # mnf = None  # Main Frame - where the widgets are scrolled
    scrollw = None
    xsize = None
    ysize = None

    active_dialog = None
    active_widget = None

    amtab = None
    rstab = None
    mstab = None


    def __init__(self, tasks, amtab, rstab, mstab):
        self.sg_tasks = tasks
        if not self.sg_tasks:
            ntask = self.create_empty_task()
            self.sg_tasks.append(ntask)
        self.n_tasks = len(self.sg_tasks)
        self.n_tasks_str = tk.StringVar()
        for i in range(self.n_tasks):
            self.tasks_str.insert(i, TaskStr(i))
        
        # collect all info from other tabs
        self.amtab = amtab
        self.rstab = rstab
        self.mstab = mstab


    def __del__(self):
        del self.n_tasks_str
        del self.tasks_str[:]


    def create_empty_task(self):
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
        task["MESSAGE"] = []
        task["STACK_SIZE"] = "512"

        return task


    def draw(self, tab, xsize, ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.scrollw = window.ScrollableWindow(tab, self.xsize, self.ysize)

        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Tasks:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_tasks_str, command=lambda : self.update(),
                    values=tuple(range(1,self.max_tasks+1)))
        self.n_tasks_str.set(self.n_tasks)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading
        label = tk.Label(self.scrollw.mnf, text=" ")
        label.grid(row=2, column=0, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="Task Name")
        label.grid(row=2, column=1, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="PRIORITY")
        label.grid(row=2, column=2, sticky="we")
        label = tk.Label(self.scrollw.mnf, text="PREMPTION")
        label.grid(row=2, column=3, sticky="we")
        label = tk.Label(self.scrollw.mnf, text="ACTIVATION")
        label.grid(row=2, column=4, sticky="we")
        label = tk.Label(self.scrollw.mnf, text="AUTOSTART[]")
        label.grid(row=2, column=5, sticky="we")
        label = tk.Label(self.scrollw.mnf, text="EVENT[]")
        label.grid(row=2, column=6, sticky="we")
        label = tk.Label(self.scrollw.mnf, text="RESOURCE[]")
        label.grid(row=2, column=7, sticky="we")
        label = tk.Label(self.scrollw.mnf, text="MESSAGE[]")
        label.grid(row=2, column=8, sticky="we")
        label = tk.Label(self.scrollw.mnf, text="Stack Size")
        label.grid(row=2, column=9, sticky="we")

        self.update()


    def update(self):
        # Backup current task entries from GUI
        self.backup_data()

        # destroy most old gui widgets
        self.n_tasks = int(self.n_tasks_str.get())
        for i, item in enumerate(self.scrollw.mnf.winfo_children()):
            if i >= self.HeaderObjs:
                item.destroy()

        # Tune memory allocations based on number of rows or boxes
        n_tasks_str = len(self.tasks_str)
        if self.n_tasks > n_tasks_str:
            for i in range(self.n_tasks - n_tasks_str):
                self.tasks_str.insert(len(self.tasks_str), TaskStr(n_tasks_str+i))
                self.sg_tasks.insert(len(self.sg_tasks), self.create_empty_task())
        elif n_tasks_str > self.n_tasks:
            for i in range(n_tasks_str - self.n_tasks):
                del self.tasks_str[-1]
                del self.sg_tasks[-1]

        #print("n_tasks_str = "+ str(n_tasks_str) + ", n_tasks = " + str(self.n_tasks))
        # Draw new objects
        for i in range(0, self.n_tasks):
            label = tk.Label(self.scrollw.mnf, text="Task "+str(i)+": ")
            label.grid(row=self.HeaderSize+i, column=0, sticky="e")
            
            # Task Name
            entry = tk.Entry(self.scrollw.mnf, width=30, textvariable=self.tasks_str[i].name)
            self.tasks_str[i].name.set(self.sg_tasks[i]["Task Name"])
            entry.grid(row=self.HeaderSize+i, column=1)

            # PRIORITY
            entry = tk.Entry(self.scrollw.mnf, width=10, textvariable=self.tasks_str[i].prio, justify='center')
            self.tasks_str[i].prio.set(self.sg_tasks[i]["PRIORITY"])
            entry.grid(row=self.HeaderSize+i, column=2)

            # SCHEDULE
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=8, textvariable=self.tasks_str[i].schedule, state="readonly")
            cmbsel['values'] = ("NON", "FULL")
            self.tasks_str[i].schedule.set(self.sg_tasks[i]["SCHEDULE"])
            cmbsel.current()
            cmbsel.grid(row=self.HeaderSize+i, column=3)

            # ACTIVATION
            entry = tk.Entry(self.scrollw.mnf, width=11, textvariable=self.tasks_str[i].activation, justify='center')
            self.tasks_str[i].activation.set(self.sg_tasks[i]["ACTIVATION"])
            entry.grid(row=self.HeaderSize+i, column=4)

            # AUTOSTART[]
            if "AUTOSTART_APPMODE" in self.sg_tasks[i]:
                self.tasks_str[i].n_appmod = len(self.sg_tasks[i]["AUTOSTART_APPMODE"])
            text = "AppModes["+str(self.tasks_str[i].n_appmod)+"]"
            select = tk.Button(self.scrollw.mnf, width=13, text=text, command=lambda id = i: self.select_autostart_modes(id))
            select.grid(row=self.HeaderSize+i, column=5)

            # EVENT[]
            if "EVENT" in self.sg_tasks[i]:
                self.tasks_str[i].n_events = len(self.sg_tasks[i]["EVENT"])
            text = "Events["+str(self.tasks_str[i].n_events)+"]"
            select = tk.Button(self.scrollw.mnf, width=13, text=text, command=lambda id = i: self.select_events(id))
            select.grid(row=self.HeaderSize+i, column=6)

            # RESOURCE[]
            if "RESOURCE" in self.sg_tasks[i]:
                self.tasks_str[i].n_resources = len(self.sg_tasks[i]["RESOURCE"])
            text = "Resources["+str(self.tasks_str[i].n_resources)+"]"
            select = tk.Button(self.scrollw.mnf, width=13, text=text, command=lambda id = i: self.select_resources(id))
            select.grid(row=self.HeaderSize+i, column=7)

            # MESSAGE[]
            if "MESSAGE" in self.sg_tasks[i]:
                self.tasks_str[i].n_messages = len(self.sg_tasks[i]["MESSAGE"])
            text = "Messages["+str(self.tasks_str[i].n_messages)+"]"
            select = tk.Button(self.scrollw.mnf, width=13, text=text, command=lambda id = i: self.select_messages(id))
            select.grid(row=self.HeaderSize+i, column=8)
            
            # STACK_SIZE
            entry = tk.Entry(self.scrollw.mnf, width=11, textvariable=self.tasks_str[i].stack_sz, justify='center')
            self.tasks_str[i].stack_sz.set(self.sg_tasks[i]["STACK_SIZE"])
            entry.grid(row=self.HeaderSize+i, column=9)

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def backup_data(self):
        n_tasks_str = len(self.tasks_str)
        # print("tsk_cfg.py: backup_data called! || n_tasks_str = "+ str(n_tasks_str))
        for i in range(n_tasks_str):
            if len(self.tasks_str[i].name.get()):
                self.sg_tasks[i]["Task Name"] = self.tasks_str[i].name.get()
            if len(self.tasks_str[i].prio.get()):
                self.sg_tasks[i]["PRIORITY"] = self.tasks_str[i].prio.get()
            if len(self.tasks_str[i].schedule.get()):
                self.sg_tasks[i]["SCHEDULE"] = self.tasks_str[i].schedule.get()
            if len(self.tasks_str[i].activation.get()):
                self.sg_tasks[i]["ACTIVATION"] = self.tasks_str[i].activation.get()
            if "AUTOSTART_APPMODE" in self.sg_tasks[i]:
                if len(self.sg_tasks[i]["AUTOSTART_APPMODE"]):
                    self.sg_tasks[i]["AUTOSTART"] = "TRUE"
                else:
                    self.sg_tasks[i]["AUTOSTART"] = "FALSE"
            else:
                self.sg_tasks[i]["AUTOSTART"] = "FALSE"
            if len(self.tasks_str[i].stack_sz.get()):
                self.sg_tasks[i]["STACK_SIZE"] = self.tasks_str[i].stack_sz.get()
                # print(self.sg_tasks[i]["STACK_SIZE"])


    def on_autostart_dialog_close(self, task_id):
        # remove old selections
        if "AUTOSTART_APPMODE" in self.sg_tasks[task_id]:
            del self.sg_tasks[task_id]["AUTOSTART_APPMODE"][:]
        else:
            self.sg_tasks[task_id]["AUTOSTART_APPMODE"] = []

        # update new selections
        if len(self.active_widget.curselection()) == 0:
            self.sg_tasks[task_id]["AUTOSTART"] = "FALSE"
        else:
            self.sg_tasks[task_id]["AUTOSTART"] = "TRUE"
            for i in self.active_widget.curselection():
                self.sg_tasks[task_id]["AUTOSTART_APPMODE"].append(self.active_widget.get(i))
        
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

        # show all app modes
        self.active_widget = tk.Listbox(self.active_dialog, selectmode=tk.MULTIPLE, width=40, height=15)
        for i, obj in enumerate(self.amtab.AM_StrVar):
            appmode = obj.get()
            self.active_widget.insert(i, appmode)
            if "AUTOSTART_APPMODE" in self.sg_tasks[id]:
                if appmode in self.sg_tasks[id]["AUTOSTART_APPMODE"]:
                    self.active_widget.selection_set(i)
        self.active_widget.pack()


    def on_event_dialog_close(self, task_id):
        # remove old selections
        if "EVENT" in self.sg_tasks[task_id]:
            del self.sg_tasks[task_id]["EVENT"][:]
        else:
            self.sg_tasks[task_id]["EVENT"] = []

        # update new selections from last window session
        for strvar in self.active_widget.events_str:
            self.sg_tasks[task_id]["EVENT"].append(strvar.get())
        
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
        self.active_dialog.geometry("+%d+%d" % (0 + x/2, y/16))

        # show all events
        self.active_widget = EventWindow(self.sg_tasks[id])
        self.active_widget.draw(self.active_dialog)


    def on_resource_dialog_close(self, task_id):
        # remove old selections
        if "RESOURCE" in self.sg_tasks[task_id]:
            del self.sg_tasks[task_id]["RESOURCE"][:]
        else:
            self.sg_tasks[task_id]["RESOURCE"] = []

        # update new selections
        if len(self.active_widget.curselection()):
            for i in self.active_widget.curselection():
                self.sg_tasks[task_id]["RESOURCE"].append(self.active_widget.get(i))
        
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

        # show all app modes
        self.active_widget = tk.Listbox(self.active_dialog, selectmode=tk.MULTIPLE, width=40, height=15)
        for i, obj in enumerate(self.rstab.ress_str):
            res = obj.get()
            self.active_widget.insert(i, res)
            if "RESOURCE" in self.sg_tasks[id]:
                if res in self.sg_tasks[id]["RESOURCE"]:
                    self.active_widget.selection_set(i)
        self.active_widget.pack()


    def on_message_dialog_close(self, task_id):
        # remove old selections
        if "MESSAGE" in self.sg_tasks[task_id]:
            del self.sg_tasks[task_id]["MESSAGE"][:]
        else:
            self.sg_tasks[task_id]["MESSAGE"] = []

        # update new selections
        if len(self.active_widget.curselection()):
            for i in self.active_widget.curselection():
                self.sg_tasks[task_id]["MESSAGE"].append(self.active_widget.get(i))
        
        # dialog elements are no longer needed, destroy them. Else, new dialogs will not open!
        self.active_widget.destroy()
        del self.active_widget
        self.active_dialog.destroy()
        del self.active_dialog

        # refresh screen
        self.update()


    def select_messages(self, id):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_message_dialog_close(id))

        # show all app modes
        self.active_widget = tk.Listbox(self.active_dialog, selectmode=tk.MULTIPLE, width=40, height=15)
        for i, obj in enumerate(self.mstab.msgs_str):
            msg = obj.get()
            self.active_widget.insert(i, msg)
            if "MESSAGE" in self.sg_tasks[id]:
                if msg in self.sg_tasks[id]["MESSAGE"]:
                    self.active_widget.selection_set(i)
        self.active_widget.pack()


