#
# Created on Sun Oct 02 2022 10:06:30 AM
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

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box

import os_builder.scripts.System_Generator as sg

class CounterTab:
    n_counters = 1
    n_counters_str = None
    max_counters = 16

    n_header_objs = None #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 2
    non_header_objs = []
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["Counter Name", "MINCYCLE", "MAXALLOWEDVALUE", "TICKSPERBASE", "OsCounterType"]
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False


    def __init__(self, cntrs):
        self.n_counters = len(cntrs)
        self.n_counters_str = tk.StringVar()
        self.configs = []

        # add tasks to UI passed from ARXML file
        for counter in cntrs:
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, counter))


    def __del__(self):
        del self.n_counters_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        counter = {}

        # Use the last counter's name and numbers to ease the edits made by user 
        counter["Counter Name"] = "COUNTER_"
        counter["MINCYCLE"] = "1"
        counter["MAXALLOWEDVALUE"] = "0xFFFFFFFF"
        counter["TICKSPERBASE"] = "1"
        counter["OsCounterType"] = "HARDWARE"

        return counter



    def draw_dappa_row(self, i):
        dappa.label(self, "Counter #", self.header_row+i, 0, "e")
        dappa.entry(self, "Counter Name", i, self.header_row+i, 1, 30, "normal")
        dappa.entry(self, "MINCYCLE", i, self.header_row+i, 2, 15, "normal")
        dappa.entry(self, "MAXALLOWEDVALUE", i, self.header_row+i, 3, 20, "normal")
        dappa.entry(self, "TICKSPERBASE", i, self.header_row+i, 4, 15, "normal")
        dappa.combo(self, "OsCounterType", i, self.header_row+i, 5, 20, ("HARDWARE", "SOFTWARE"))



    def update(self):
        # get dappas to be added or removed
        self.n_counters = int(self.n_counters_str.get())

        # tune memory allocation based on number of dappas
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif int(self.n_counters) > n_dappa_rows:
            for i in range(int(self.n_counters) - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > int(self.n_counters):
            for i in range(n_dappa_rows - int(self.n_counters)):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab, xsize, ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.scrollw = window.ScrollableWindow(tab, self.xsize, self.ysize)

        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="Number of Counters ")
        label.grid(row=1, column=1, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_counters_str, command=self.update, 
                           values=tuple(range(1, self.max_counters+1)))
        self.n_counters_str.set(self.n_counters)
        spinb.grid(row=1, column=2, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()



    def backup_data(self):
        if sg.Counters:
            del sg.Counters[:]
        for cfg in self.configs:
            cfg_dict = cfg.get()
            sg.Counters.append(cfg_dict)
