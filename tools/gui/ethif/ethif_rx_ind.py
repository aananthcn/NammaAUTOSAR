#
# Created on Sun Jan 15 2023 5:33:00 PM
#
# The MIT License (MIT)
# Copyright (c) 2023 Aananth C N
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




class EthIfRxIndicationConfigView:
    n_ethif_rxi_fns = 0
    max_ethif_rxi_fns = 255
    n_ethif_rxi_fns_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["Idx", "EthIfRxIndicationFunction"]
    
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False

    active_dialog = None
    active_widget = None


    def __init__(self, gui, rxi_cfg):
        self.gui = gui
        self.configs = []
        self.n_ethif_rxi_fns = 0
        self.n_ethif_rxi_fns_str = tk.StringVar()

        for cfg in rxi_cfg:
            if not cfg:
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
            else:
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, cfg))
            self.n_ethif_rxi_fns += 1
        self.n_ethif_rxi_fns_str.set(self.n_ethif_rxi_fns)



    def __del__(self):
        del self.n_ethif_rxi_fns_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        ethif_hfile = {}

        ethif_hfile["Idx"] = str(self.n_ethif_rxi_fns-1)
        ethif_hfile["EthIfRxIndicationFunction"] = ""

        return ethif_hfile



    def draw_dappa_row(self, i):
        dappa.label(self, "Config #", self.header_row+i, 0, "e")

        dappa.entry(self, "Idx", i, self.header_row+i, 1, 10, "readonly")
        dappa.entry(self, "EthIfRxIndicationFunction", i, self.header_row+i, 2, 40, "normal")



    def update(self):
        # get dappas to be added or removed
        self.n_ethif_rxi_fns = int(self.n_ethif_rxi_fns_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_ethif_rxi_fns > n_dappa_rows:
            for i in range(self.n_ethif_rxi_fns - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_ethif_rxi_fns:
            for i in range(n_dappa_rows - self.n_ethif_rxi_fns):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="Rx Ind. Fns:")
        label.grid(row=0, column=0, sticky="w")
        ethifnb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_ethif_rxi_fns_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_ethif_rxi_fns+1)))
        self.n_ethif_rxi_fns_str.set(self.n_ethif_rxi_fns)
        ethifnb.grid(row=0, column=1, sticky="w")

        # Save Button
        genm = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=0, column=2)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()



    def save_data(self):
        self.tab_struct.save_cb(self.gui)
