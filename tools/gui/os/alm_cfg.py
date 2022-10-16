#
# Created on Sun Oct 02 2022 10:06:23 AM
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
from copy import copy

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box



class AlarmTab:
    n_alarms = None
    max_alarms = 1024
    n_alarms_str = None
    alarms_str = []
    # sg_alarms = None
    
    non_header_objs = []
    n_header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3

    xsize = None
    ysize = None

    active_dialog = None
    active_widget = None

    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["Alarm Name", "COUNTER", "Action-Type", "arg1", "arg2", "IsAutostart", "ALARMTIME", "CYCLETIME", "APPMODE"]
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False

    amtab = None
    crtab = None
    tktab = None
    counter_names = []
    task_names = []
    task_events = []


    def __init__(self, alarms, tktab, amtab, crtab):
        self.n_alarms = len(alarms)
        self.n_alarms_str = tk.StringVar()
        self.configs = []

        # add alarms to UI configs which is passed from ARXML file 
        for alarm in alarms:
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, alarm))

        # collect all info from other tabs
        self.amtab = amtab
        self.crtab = crtab
        self.tktab = tktab


    def __del__(self):
        del self.n_alarms_str
        del self.non_header_objs[:]
        del self.configs[:]


    def create_empty_configs(self):
        alarm = {}
        # Use the last alarm's name and numbers to ease the edits made by user 
        alarm["Alarm Name"] = "ALARM_"
        alarm["COUNTER"] = "" # self.sg_alarms[-1]["COUNTER"]
        alarm["Action-Type"] = "ACTIVATETASK"
        alarm["arg1"] = ""
        alarm["arg2"] = "FALSE"
        alarm["IsAutostart"] = "FALSE"
        alarm["ALARMTIME"] = "0"
        alarm["CYCLETIME"] = "0"
        alarm["APPMODE"] = []

        return alarm


 
    def draw_dappa_row(self, i):
        dappa.label(self, "Alarm "+str(i)+": ", self.header_row+i, 0, "e")
        
        # Alarm Name
        dappa.entry(self, "Alarm Name", i, self.header_row+i, 1, 30, "normal")

        # COUNTER
        dappa.combo(self, "COUNTER", i, self.header_row+i, 2, 17, self.extract_counter_names())

        # Action-Type
        values = ("ACTIVATETASK", "SETEVENT", "ALARMCALLBACK")
        atcb = dappa.combo(self, "Action-Type", i, self.header_row+i, 3, 17, values)
        atcb.bind("<<ComboboxSelected>>", lambda evt, id=i : self.action_type_selected(evt, id))

        # arg1
        if self.configs[i].datavar["Action-Type"] == "ALARMCALLBACK":
            # Draw Entry box for ALARMCALLBACK
            dappa.entry(self, "arg1", i, self.header_row+i, 4, 30, "normal")
        else: 
            # Draw Combobox for Task select
            arg1 = dappa.combo(self, "arg1", i, self.header_row+i, 4, 30-3, self.extract_task_names())
            arg1.bind("<<ComboboxSelected>>", lambda evt, id = i : self.arg1_task_selected(evt, id))

        # arg2
        if self.configs[i].datavar["Action-Type"] == "SETEVENT":
            # Draw Combobox for Event select
            event_list = self.extract_task_events(i)
            if not self.configs[i].datavar["arg2"]:
                self.configs[i].datavar["arg2"] = ""
            dappa.combo(self, "arg2", i, self.header_row+i, 5, 25-3, event_list)
        else:
            dappa.label(self, "", self.header_row+i, 5, "e")


        # IsAutoStart
        isas = dappa.combo(self, "IsAutostart", i, self.header_row+i, 6, 8, ("TRUE", "FALSE"))
        isas.bind("<<ComboboxSelected>>", lambda evt, id = i : self.isautostart_changed(evt, id))

        # ALARMTIME, CYCLETIME AND APPMODE are not required if IsAutostart is False
        if self.configs[i].datavar["IsAutostart"] == "FALSE":
            dappa.label(self, "", self.header_row+i, 7, "e")
            dappa.label(self, "", self.header_row+i, 8, "e")
            dappa.label(self, "", self.header_row+i, 9, "e")
            return

        # ALARMTIME
        at = dappa.entry(self, "ALARMTIME", i, self.header_row+i, 7, 11, "normal")
        at.bind("<FocusOut>", lambda evt, id = i : self.alarm_cycle_time_changed(evt, id))

        # CYCLETIME
        ct = dappa.entry(self, "CYCLETIME", i, self.header_row+i, 8, 11, "normal")
        ct.bind("<FocusOut>", lambda evt, id = i : self.alarm_cycle_time_changed(evt, id))

        # APPMODE[]
        n_appmode = 0
        if self.configs[i].datavar["APPMODE"]:
            n_appmode = len(self.configs[i].datavar["APPMODE"])
        cb = lambda id = i: self.select_autostart_modes(id)
        dappa.button(self, "APPMODE", i, self.header_row+i, 9, 10, "SELECT["+str(n_appmode)+"]", cb)



    def update(self):
        # get dappas to be added or removed
        self.n_alarms = int(self.n_alarms_str.get())
        
        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_alarms > n_dappa_rows:
            for i in range(self.n_alarms - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_alarms:
            for i in range(n_dappa_rows - self.n_alarms):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()


    def draw(self, tab, xsize, ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.scrollw = window.ScrollableWindow(tab, self.xsize, self.ysize)

        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Alarms:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_alarms_str, command=lambda : self.update(),
                    values=tuple(range(1,self.max_alarms+1)))
        self.n_alarms_str.set(self.n_alarms)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle sg_alarms to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()


    def extract_task_names(self):
        del self.task_names[:]
        for tsk in self.tktab.configs:
            tsk_data = tsk.get()
            self.task_names.append(tsk_data["Task Name"])
        return self.task_names


    def extract_task_events(self, aid):
        events = []
        alarm_id = int(aid)

        # For action type == ALARMCALLBACK, there are no events associated!
        if self.configs[alarm_id].datavar["Action-Type"] == "ALARMCALLBACK":
            return events

        # get events from tasks configured in Alarm[alarm_id]
        task_name = self.configs[alarm_id].datavar["arg1"]
        for task in self.tktab.configs:
            if task_name == task.get()["Task Name"]:
                if "EVENT" in task.get():
                    events = copy(task.get()["EVENT"])
                    break

        return events



    def extract_counter_names(self):
        del self.counter_names[:]
        # for cntr in self.crtab.Ctr_StrVar:
        #     self.counter_names.append(cntr.name.get())
        for counter in self.crtab.configs:
            self.counter_names.append(counter.datavar["Counter Name"])
        return self.counter_names



    def backup_data(self):
        print("alm_cfg.backup_data() called!")



    def action_type_selected(self, event, row):
        self.configs[row].get() # read from UI (backup last selection)
        self.configs[row].datavar["arg1"] = self.configs[row].datavar["arg2"] = ""
        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def arg1_task_selected(self, event, row):
        self.configs[row].get() # read from UI (backup last selection)
        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def isautostart_changed(self, event, row):
        self.configs[row].get() # read from UI (backup last selection)
        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def alarm_cycle_time_changed(self, event, row):
        # read from UI (backup last writes)
        self.configs[row].datavar["ALARMTIME"] = self.configs[row].dispvar["ALARMTIME"].get()
        self.configs[row].datavar["CYCLETIME"] = self.configs[row].dispvar["CYCLETIME"].get()



    def select_autostart_modes(self, row):
        self.configs[row].get() # read from UI (backup last selection)
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_autostart_dialog_close(row))

        # show all app modes
        self.active_widget = tk.Listbox(self.active_dialog, selectmode=tk.MULTIPLE, width=40, height=15)
        for i, am_cfg in enumerate(self.amtab.configs):
            appmode = am_cfg.datavar["OsAppMode"]
            self.active_widget.insert(i, appmode)
            if self.configs[row].datavar["APPMODE"]:
                if appmode in self.configs[row].datavar["APPMODE"]:
                    self.active_widget.selection_set(i)
        self.active_widget.pack()


    def on_autostart_dialog_close(self, row):
        self.configs[row].get() # read from UI (backup last selection)
        
        # remove old selections
        if self.configs[row].datavar["APPMODE"]:
            del self.configs[row].datavar["APPMODE"][:]

        # update new selections
        if len(self.active_widget.curselection()):
            for i in self.active_widget.curselection():
                if not self.configs[row].datavar["APPMODE"]:
                    self.configs[row].datavar["APPMODE"] = []
                self.configs[row].datavar["APPMODE"].append(self.active_widget.get(i))
        
        # dialog elements are no longer needed, destroy them. Else, new dialogs will not open!
        self.active_widget.destroy()
        del self.active_widget
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)
