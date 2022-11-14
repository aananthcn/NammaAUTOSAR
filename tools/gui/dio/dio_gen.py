#
# Created on Sun Oct 02 2022 10:05:07 AM
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
import arxml.dio.arxml_dio_parse as arxml_dio

import gui.port.port_cgen as port_cgen


class DioGeneralTab:
    gui = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["DioDevErrorDetect", "DioVersionInfoApi", "DioFlipChannelApi", "DioMaskedWritePortApi"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)

    def __init__(self, gui):
        self.gui = gui
        self.configs = []
        dio_pins, dio_cfg, dio_grp, dio_gen = arxml_dio.parse_arxml(gui.arxml_file)
        if dio_gen == None:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, dio_gen))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self):
        dio_gen = {}
        dio_gen["DioDevErrorDetect"]      = "FALSE"
        dio_gen["DioVersionInfoApi"]      = "FALSE"
        dio_gen["DioFlipChannelApi"]      = "FALSE"
        dio_gen["DioMaskedWritePortApi"]  = "FALSE"
        return dio_gen
        


    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        dio_cmbsel = ("FALSE", "TRUE")
        
        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)

        # DioDevErrorDetect
        dappa.combo(self, "DioDevErrorDetect", 0, 0, 1, 14, dio_cmbsel)

        # DioVersionInfoApi
        dappa.combo(self, "DioVersionInfoApi", 0, 1, 1, 14, dio_cmbsel)

        # DioFlipChannelApi
        dappa.combo(self, "DioFlipChannelApi", 0, 2, 1, 14, dio_cmbsel)

        # DioMaskedWritePortApi
        dappa.combo(self, "DioMaskedWritePortApi", 0, 3, 1, 14, dio_cmbsel)

        # empty space
        label = tk.Label(self.scrollw.mnf, text="")
        label.grid(row=6, column=0, sticky="e")

        # Save Button
        saveb = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        saveb.grid(row=7, column=1)

        # Support scrollable view
        self.scrollw.scroll()



    def save_data(self):
        self.tab_struct.save_cb(self.gui)
