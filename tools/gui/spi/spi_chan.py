#
# Created on Thu Oct 06 2022 6:53:58 AM
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



class SpiChannelTab:
    n_spi_chans = 0
    max_spi_chans = 255
    n_spi_chans_str = None

    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SpiChannelId", "SpiChannelType", "SpiDataWidth", "SpiDefaultData", "SpiEbMaxLength",
               "SpiIbNBuffers", "SpiTransferStart"]

    n_header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False


    def __init__(self, gui, spidrvtab, ar_cfg):
        self.gui = gui
        self.configs = []
        self.n_spi_chans = 0
        self.n_spi_chans_str = tk.StringVar()
        self.spidrvtab = spidrvtab

        if ar_cfg["SpiChannel"] == None:
            return
        for chan in ar_cfg["SpiChannel"]:
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, chan))
            self.n_spi_chans += 1
        self.n_spi_chans_str.set(self.n_spi_chans)


    def __del__(self):
        del self.n_spi_chans_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        spi_chan = {}
        spi_chan["SpiChannelId"] = str(self.n_spi_chans-1)
        spi_chan["SpiChannelType"] = "IB"
        spi_chan["SpiDataWidth"] = "4" # bytes
        spi_chan["SpiDefaultData"] = "0xAA551234"
        spi_chan["SpiEbMaxLength"] = "65535"
        spi_chan["SpiIbNBuffers"] = "65535"
        spi_chan["SpiTransferStart"] = "MSB"
        return spi_chan



    def draw_dappa_row(self, i):
        dappa.label(self, "Spi Channel #", self.header_row+i, 0, "e")

        # SpiChannelId
        dappa.entry(self, "SpiChannelId", i, self.header_row+i, 1, 10, "readonly")

        # SpiChannelType
        values = ("IB (Internal Buffer)", "EB (External Buffer)")
        chtype = dappa.combo(self, "SpiChannelType", i, self.header_row+i, 2, 17, values)
        chtype.bind("<<ComboboxSelected>>", lambda evt, id = i : self.chan_type_selected(evt, id))

        # SpiDataWidth
        dappa.spinb(self, "SpiDataWidth", i,self.header_row+i, 3, 13, tuple(range(1,33)))

        # SpiDefaultData
        dappa.entry(self, "SpiDefaultData", i, self.header_row+i, 4, 30, "normal")

        # SpiEbMaxLength
        if "EB" in self.configs[i].dispvar["SpiChannelType"].get():
            dappa.spinb(self, "SpiEbMaxLength", i, self.header_row+i, 5, 13, tuple(range(0,65536)))
        else:
            dappa.label(self, "", self.header_row+i, 5, "e")
            self.configs[i].datavar["SpiEbMaxLength"] = 0

        # SpiIbNBuffers
        if "IB" in self.configs[i].dispvar["SpiChannelType"].get():
            dappa.spinb(self, "SpiIbNBuffers", i, self.header_row+i, 6, 13, tuple(range(0,65536)))
        else:
            dappa.label(self, "", self.header_row+i, 6, "e")
            self.configs[i].datavar["SpiIbNBuffers"] = 0

        # SpiTransferStart
        values = ("MSB", "LSB")
        dappa.combo(self, "SpiTransferStart", i, self.header_row+i, 7, 10, values)
        
        # Channel list changed hence ask SpiDriver to redraw
        self.spidrvtab.tab.spi_chan_list_changed(self.configs)



    def update(self):
        # get dappas to be added or removed
        self.n_spi_chans = int(self.n_spi_chans_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_spi_chans > n_dappa_rows:
            for i in range(self.n_spi_chans - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_spi_chans:
            for i in range(n_dappa_rows - self.n_spi_chans):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Support scrollable view
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Channels:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_spi_chans_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_spi_chans+1)))
        self.n_spi_chans_str.set(self.n_spi_chans)
        spinb.grid(row=0, column=1, sticky="w")

        # Save Button
        genm = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=0, column=2)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)
        
        self.update()



    def save_data(self):
        # self.backup_data()
        self.tab_struct.save_cb(self.gui)



    def chan_type_selected(self, event, row):
        self.configs[row].get() # read from UI (backup last selection)
        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)
