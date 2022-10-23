#
# Created on Wed Oct 19 2022 10:48:15 PM
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

import gui.spi.spi_chan as spi_chan

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box




class SpiChannelListTab:
    n_spi_chan_list = 0
    max_spi_chan_list = 255
    n_spi_chan_list_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SpiChannelIndex", "SpiChannelAssignment"]
    
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels


    def __init__(self, gui, chids):
        self.gui = gui
        self.configs = []
        self.n_spi_chan_list = 0
        self.n_spi_chan_list_str = tk.StringVar()
        self.chids = chids

        #spi_chan_lists = arxml_spi.parse_arxml(gui.arxml_file)
        spi_chan_lists = None
        if spi_chan_lists == None:
            return 


    def __del__(self):
        del self.n_spi_chan_list_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        spi_seq = {}
        spi_seq["SpiChannelIndex"] = "0"
        spi_seq["SpiChannelAssignment"] = "0"
        return spi_seq



    def draw_dappa_row(self, i):
        dappa.label(self, "Spi Chan List #", self.header_row+i, 0, "e")
        dappa.combo(self, "SpiChannelIndex", i, self.header_row+i, 1, 15, self.chids)

        self.configs[i].datavar["SpiChannelAssignment"] = "Job no: "+str(self.jobid)
        dappa.entry(self, "SpiChannelAssignment", i, self.header_row+i, 2, 15, "readonly")
        


    def update(self):
        # get dappas to be added or removed
        self.n_spi_chan_list = int(self.n_spi_chan_list_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if self.n_spi_chan_list > n_dappa_rows:
            for i in range(self.n_spi_chan_list - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_spi_chan_list:
            for i in range(n_dappa_rows - self.n_spi_chan_list):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab, jobid):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        self.jobid = jobid
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Spi Chan List:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_spi_chan_list_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_spi_chan_list+1)))
        self.n_spi_chan_list_str.set(self.n_spi_chan_list)
        spinb.grid(row=0, column=1, sticky="w")

        # # Save Button
        # genm = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        # genm.grid(row=0, column=2)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()



    def select_spi_jobs(self, id):
        print("select_spi_jobs() called with ",id, " as argument!")



    # def save_data(self):
    #     self.tab_struct.save_cb(self.gui)
