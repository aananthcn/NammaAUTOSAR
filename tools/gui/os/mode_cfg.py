#
# Created on Sun Oct 02 2022 10:06:55 AM
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



class AmTab:
    n_app_modes = 1
    n_app_modes_str = None
    max_app_modes = 16

    header_row = 0
    n_header_objs = 2 #Objects / widgets that are part of the header and shouldn't be destroyed
    non_header_objs = []
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["OsAppMode"]
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False


    def __init__(self, appmodes):
        self.n_app_modes = len(appmodes)
        self.n_app_modes_str = tk.StringVar()
        self.configs = []

        # add tasks to UI passed from ARXML file
        for appmode in appmodes:
            am_dict = {}
            am_dict["OsAppMode"] = appmode
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, am_dict))


    def __del__(self):
        del self.n_app_modes_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        appmode = {}
        appmode["OsAppMode"] = "OSDEFAULTAPPMODE"
        return appmode



    def draw_dappa_row(self, i):
        dappa.label(self, "Mode "+str(i)+":", self.header_row+i, 0, "e")
        am = dappa.entry(self, "OsAppMode", i, self.header_row+i, 1, 30, "normal")
        am.bind("<FocusOut>", lambda evt, id = i : self.appmode_changed(evt, id))



    def update(self):
        # get dappas to be added or removed
        self.n_app_modes = int(self.n_app_modes_str.get())

        # tune memory allocation and draw or delete rows
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_app_modes > n_dappa_rows:
            for i in range(self.n_app_modes - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_app_modes:
            for i in range(n_dappa_rows - self.n_app_modes):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()




    def draw(self, tab, xsize, ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.scrollw = window.ScrollableWindow(tab, self.xsize, self.ysize)

        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="Number of Modes ")
        label.grid(row=1, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=28, command=self.update, textvariable=self.n_app_modes_str,
                           values=tuple(range(1,self.max_app_modes+1)))
        self.n_app_modes_str.set(self.n_app_modes)
        spinb.grid(row=1, column=1)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)
        self.update()



    def appmode_changed(self, event, row):
        # read from UI (backup last writes)
        # self.configs[row].datavar["ALARMTIME"] = self.configs[row].dispvar["ALARMTIME"].get()
        self.configs[row].get()



    def backup_data(self):
        print("backup_data called in mode_cfg")
