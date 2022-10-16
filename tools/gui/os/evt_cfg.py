#
# Created on Sun Oct 02 2022 10:06:38 AM
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

from copy import copy

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box



class EventWindow:
    n_events = 0
    n_events_str = None
    max_events = 64

    n_header_objs = 2 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 1
    xsize = None
    ysize = None
    mnf = None

    non_header_objs = []
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["OsEvent"]
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False


    def __init__(self, events):
        self.n_events_str = tk.StringVar()
        self.configs = []
        if events:
            self.n_events = len(events)
        else:
            return

        # add resources to UI passed from ARXML file
        for event in events:
            event_dict = {}
            event_dict["OsEvent"] = event
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, event_dict))


    def __del__(self):
        del self.n_events_str
        del self.non_header_objs[:]
        del self.configs[:]
        # del self.events_str[:]



    def create_empty_configs(self):
        def_event = {}
        def_event["OsEvent"] = "EVT_"
        return def_event


    # Event Window doesn't support scrollable view due to an unusual UI behavior
    def draw_dappa_row(self, i):
        label = tk.Label(self.mnf, text="Event "+str(i)+": ")
        label.grid(row=self.header_row+i, column=0, sticky="w")
        dappa.insert_widget_to_nh_objs(self.header_row+i, 0, self, label)

        entry = tk.Entry(self.mnf, width=40, textvariable=self.configs[i].dispvar["OsEvent"])
        self.configs[i].dispvar["OsEvent"].set(self.configs[i].datavar["OsEvent"])
        entry.grid(row=self.header_row+i, column=1)
        dappa.insert_widget_to_nh_objs(self.header_row+i, 1, self, entry)



    # Event Window doesn't support scrollable view due to an unusual UI behavior
    def update(self):
        # get dappas to be added or removed
        self.n_events = int(self.n_events_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_events > n_dappa_rows:
            for i in range(self.n_events - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_events:
            for i in range(n_dappa_rows - self.n_events):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # No scrolling support for Event View, due to unusual behavior


    def draw(self, tab):
        self.mnf = tab
        
        #Number of Events - Label + Spinbox
        label = tk.Label(self.mnf, text="No. of Events:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.mnf, width=10, textvariable=self.n_events_str, command=self.update,
                    values=tuple(range(0,self.max_events)))
        self.n_events_str.set(self.n_events)
        spinb.grid(row=0, column=1, sticky="w")

        # No scrolling support for Event View, due to unusual behavior
        self.update()



    def backup_data(self):
        print("backup_data called in evt_cfg")