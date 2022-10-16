#
# Created on Sun Oct 02 2022 10:07:31 AM
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
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER n_ressLIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import tkinter as tk
from tkinter import ttk

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box



class ResourceTab:
    n_resources = 1
    n_resources_str = None
    max_resources = 1024

    n_header_objs = 2 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 1
    xsize = None
    ysize = None

    non_header_objs = []
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["OsResource"]
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False


    def __init__(self, tasks):
        resources = self.extract_resources(tasks)
        self.n_resources = len(resources)
        self.n_resources_str = tk.StringVar()
        self.configs = []

        # add resources to UI passed from ARXML file
        for res in resources:
            res_dict = {}
            res_dict["OsResource"] = res
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, res_dict))


    def __del__(self):
        del self.n_resources_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        def_res = {}
        def_res["OsResource"] = "RES_"
        return def_res



    def draw_dappa_row(self, i):
        dappa.label(self, "Res "+str(i)+":", self.header_row+i, 0, "e")
        am = dappa.entry(self, "OsResource", i, self.header_row+i, 1, 40, "normal")
        am.bind("<FocusOut>", lambda evt, id = i : self.resource_changed(evt, id))



    def update(self):
        # get dappas to be added or removed
        self.n_resources = int(self.n_resources_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_resources > n_dappa_rows:
            for i in range(self.n_resources - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_resources:
            for i in range(n_dappa_rows - self.n_resources):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab, xsize, ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.scrollw = window.ScrollableWindow(tab, self.xsize, self.ysize)

        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Resources:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_resources_str, command=self.update,
                    values=tuple(range(1,self.max_resources+1)))
        self.n_resources_str.set(self.n_resources)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        self.update()




    def resource_changed(self, event, row):
        # read from UI (backup last writes)
        self.configs[row].get()



    def backup_data(self):
        print("backup_data called in mode_cfg")



    def extract_resources(self, tasks):
        # OSEK spec mandates having RES_SCHEDULER as the default/1st resource.
        resources = ["RES_SCHEDULER"]

        # extract resources from tasks
        for task in tasks:
            if "RESOURCE" in task:
                for res in task["RESOURCE"]:
                    if res not in resources:
                        resources.append(res)

        return resources