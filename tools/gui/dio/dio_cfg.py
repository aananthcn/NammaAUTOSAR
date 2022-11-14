#
# Created on Sun Oct 02 2022 10:05:21 AM
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

    

class DioConfigTab:
    n_pins = 0
    max_pins = 65535
    n_pins_str = None

    # dio_ports = []  # copy of port info

    n_header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    init_view_done = False
    
    toplvl = None

    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["DioPortId", "DioChannelId"]
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels


    def __init__(self, gui):
        self.gui = gui
        self.configs = []
        self.toplvl = gui.main_view.child_window
        self.n_pins_str = tk.StringVar()

        dio_pins, dio_cfg, dio_grps, dio_gen = arxml_dio.parse_arxml(gui.arxml_file)
        if dio_pins == None:
            return

        for cfg in dio_cfg:
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, cfg))
            self.n_pins += 1
        self.n_pins_str.set(self.n_pins)
        

    def __del__(self):
        del self.n_pins_str
        del self.non_header_objs[:]
        del self.configs[:]


    def create_empty_configs(self):
        diopin = {}
        diopin["DioPortId"] = "65535"
        diopin["DioChannelId"] = "65535"
        return diopin


    def get_chan_id(self, port_id, dio_ports):
        chan_id = None
        for port in dio_ports:
            if port["DioChannelId"] == port_id:
                chan_id = port["DioChannelId"]
                break
        return chan_id



    def draw_dappa_row(self, i):
        dappa.label(self, "Pin #", self.header_row+i, 0, "e")

        # DioPortId
        dappa.entry(self, "DioPortId", i, self.header_row+i, 1, 10, "readonly")

        # DioChannelId
        dappa.entry(self, "DioChannelId", i, self.header_row+i, 2, 10, "normal")



    def update(self):
        # get dappas to be added or removed
        self.n_pins = int(self.n_pins_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_pins > n_dappa_rows:
            for i in range(self.n_pins - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_pins:
            for i in range(n_dappa_rows - self.n_pins):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()


    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)

        #Number of Dio pins
        label = tk.Label(self.scrollw.mnf, text="No. of Dio Pins:")
        label.grid(row=0, column=0, sticky="w")
        dio_entry = tk.Entry(self.scrollw.mnf, width=10, textvariable=self.n_pins_str, justify='center', state="readonly")
        self.n_pins_str.set(self.n_pins)
        dio_entry.grid(row=0, column=1, sticky="w")

        # Save Button
        genm = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=0, column=2)

        self.scrollw.update()
        
        if self.n_pins == 0:
            label = tk.Label(self.scrollw.mnf, text="No ports are configured as DIO in Port module. Please open "
                             "Port module and configure pins as DIO to see them here.""", justify="left")
            label.grid(row=2, column=3, sticky="w")
            return

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()



    def save_data(self):
        self.tab_struct.save_cb(self.gui)
        