#
# Created on Sun Oct 02 2022 10:05:32 AM
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

import arxml.port.arxml_port as arxml_port
import arxml.dio.arxml_dio_parse as arxml_dio

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box



class DioChannelGroupTab:
    n_chgrps = 0
    max_chgrps = 65535
    n_chgrps_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["DioPortId", "DioChannelGroupIdentification", "DioPortOffset", "DioPortMask"]

    port_pin_ids = []
    n_header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False


    def __init__(self, gui):
        self.gui = gui
        self.configs = []
        self.n_chgrps = 0
        self.n_chgrps_str = tk.StringVar()

        pins, ports, general = arxml_port.parse_arxml(gui.arxml_file)
        if pins == None or ports == None:
            return
        for port in ports:
            if port['PortPinMode'] == "PORT_PIN_MODE_DIO":
                self.port_pin_ids.append(port["PortPinId"])

        dio_pins, dio_cfgs, dio_grps, dio_gen = arxml_dio.parse_arxml(gui.arxml_file)
        for grp in dio_grps:
            if "DioChannelGroupIdentification" in grp:
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, grp))
                self.n_chgrps += 1
        self.n_chgrps_str.set(self.n_chgrps)


    def __del__(self):
        del self.n_chgrps_str
        del self.non_header_objs[:]
        del self.port_pin_ids[:]
        del self.configs[:]




    def create_empty_configs(self):
        chgrp = {}
        chgrp["DioPortId"] = "65535"
        chgrp["DioChannelGroupIdentification"] = "ChGrp_"
        chgrp["DioPortOffset"] = "e.g., 0x4"
        chgrp["DioPortMask"] = "e.g., 0xF0F"
        return chgrp



    def draw_dappa_row(self, i):
        dappa.label(self, "Channel Group #", self.header_row+i, 0, "e")

        # DioPortId
        dappa.combo(self, "DioPortId", i, self.header_row+i, 1, 14, self.port_pin_ids)

        # DioChannelGroupIdentification
        dappa.entry(self, "DioChannelGroupIdentification", i, self.header_row+i, 2, 30, "normal")

        # Channel Group - DioPortOffset
        dappa.entry(self, "DioPortOffset", i, self.header_row+i, 3, 15, "normal")

        # Channel Group - DioPortMask
        dappa.entry(self, "DioPortMask", i, self.header_row+i, 4, 15, "normal")



    def update(self):
        # get dappas to be added or removed
        self.n_chgrps = int(self.n_chgrps_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_chgrps > n_dappa_rows:
            for i in range(self.n_chgrps - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_chgrps:
            for i in range(n_dappa_rows - self.n_chgrps):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Chan. Groups:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_chgrps_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_chgrps+1)))
        self.n_chgrps_str.set(self.n_chgrps)
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
        self.tab_struct.save_cb(self.gui)
