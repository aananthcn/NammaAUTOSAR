#
# Created on Sun Oct 02 2022 10:04:54 AM
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

import arxml.port.arxml_port as arxml_port
import gui.port.port_cgen as port_cgen



class PortGeneralTab:
    gui = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["PortDevErrorDetect", "PortVersionInfoApi", "PortSetPinDirectionApi", "PortSetPinModeApi"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)


    def __init__(self, gui):
        self.gui = gui
        self.configs = []
        port_pins, port_cfg, port_gen = arxml_port.parse_arxml(gui.arxml_file)
        if port_gen == None:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, port_gen))


    def __del__(self):
        del self.configs[:]


    def create_empty_configs(self):
        port_gen = {}
        port_gen["PortDevErrorDetect"]      = "FALSE"
        port_gen["PortVersionInfoApi"]      = "FALSE"
        port_gen["PortSetPinDirectionApi"]  = "FALSE"
        port_gen["PortSetPinModeApi"]       = "FALSE"
        return port_gen



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        port_cmbsel = ("FALSE", "TRUE")

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)

        # PortDevErrorDetect
        dappa.combo(self, "PortDevErrorDetect", 0, 0, 1, 14, port_cmbsel)

        # PortVersionInfoApi
        dappa.combo(self, "PortVersionInfoApi", 0, 1, 1, 14, port_cmbsel)

        # PortSetPinDirectionApi
        dappa.combo(self, "PortSetPinDirectionApi", 0, 2, 1, 14, port_cmbsel)

        # PortSetPinModeApi
        dappa.combo(self, "PortSetPinModeApi", 0, 3, 1, 14, port_cmbsel)

        # empty space
        label = tk.Label(self.scrollw.mnf, text="")
        label.grid(row=6, column=0, sticky="e")

        # Save Button
        genm = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=7, column=1)

        self.scrollw.scroll()



    def save_data(self):
        # self.backup_data()
        self.tab_struct.save_cb(self.gui)
