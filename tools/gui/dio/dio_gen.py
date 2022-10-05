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

import arxml.port.arxml_port as arxml_port
import arxml.dio.arxml_dio as arxml_dio

import gui.port.port_cgen as port_cgen


class DioGeneralStr:
    error_detect = None
    verion_api = None
    flip_chan_api = None
    masked_write_port_api = None

    def __init__(self):
        self.error_detect = tk.StringVar()
        self.verion_api = tk.StringVar()
        self.flip_chan_api = tk.StringVar()
        self.masked_write_port_api = tk.StringVar()

    def __del__(self):
        del self.error_detect
        del self.verion_api
        del self.flip_chan_api
        del self.masked_write_port_api


class DioGeneralTab:
    gui = None
    tab_struct = None # passed from *_view.py file
    gen_str = None
    gen_dict = None

    def __init__(self, gui):
        self.gui = gui
        self.gen_str = DioGeneralStr()
        self.gen_dict = {}
        dio_pins, dio_cfg, dio_gen = arxml_dio.parse_arxml(gui.arxml_file)
        if dio_pins == None:
            self.gen_dict["DioDevErrorDetect"]      = "FALSE"
            self.gen_dict["DioVersionInfoApi"]      = "FALSE"
            self.gen_dict["DioFlipChannelApi"]      = "FALSE"
            self.gen_dict["DioMaskedWritePortApi"]  = "FALSE"
            return
        self.gen_dict["DioDevErrorDetect"]      = dio_gen["DioDevErrorDetect"]
        self.gen_dict["DioVersionInfoApi"]      = dio_gen["DioVersionInfoApi"]
        self.gen_dict["DioFlipChannelApi"]      = dio_gen["DioFlipChannelApi"]
        self.gen_dict["DioMaskedWritePortApi"]  = dio_gen["DioMaskedWritePortApi"]

    def __del__(self):
        del self.gen_str


    def draw(self, tab):
        self.tab_struct = tab
        dio_cmbsel = ("FALSE", "TRUE")
        
        # empty space
        label = tk.Label(tab.frame, text="")
        label.grid(row=1, column=0, sticky="e")

        # DioDevErrorDetect
        label = tk.Label(tab.frame, text="DioDevErrorDetect: ")
        label.grid(row=2, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.gen_str.error_detect, state="readonly")
        cmbsel['values'] = dio_cmbsel
        self.gen_str.error_detect.set(self.gen_dict["DioDevErrorDetect"])
        cmbsel.current()
        cmbsel.grid(row=2, column=1)

        # DioVersionInfoApi
        label = tk.Label(tab.frame, text="DioVersionInfoApi: ")
        label.grid(row=3, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.gen_str.verion_api, state="readonly")
        cmbsel['values'] = dio_cmbsel
        self.gen_str.verion_api.set(self.gen_dict["DioVersionInfoApi"])
        cmbsel.current()
        cmbsel.grid(row=3, column=1)

        # DioFlipChannelApi
        label = tk.Label(tab.frame, text="DioFlipChannelApi: ")
        label.grid(row=4, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.gen_str.flip_chan_api, state="readonly")
        cmbsel['values'] = dio_cmbsel
        self.gen_str.flip_chan_api.set(self.gen_dict["DioFlipChannelApi"])
        cmbsel.current()
        cmbsel.grid(row=4, column=1)

        # DioMaskedWritePortApi
        label = tk.Label(tab.frame, text="DioMaskedWritePortApi: ")
        label.grid(row=5, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.gen_str.masked_write_port_api, state="readonly")
        cmbsel['values'] = dio_cmbsel
        self.gen_str.masked_write_port_api.set(self.gen_dict["DioMaskedWritePortApi"])
        cmbsel.current()
        cmbsel.grid(row=5, column=1)

        # empty space
        label = tk.Label(tab.frame, text="")
        label.grid(row=6, column=0, sticky="e")

        # Save Button
        genm = tk.Button(tab.frame, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=7, column=1)

        self.backup_data()
        # tab.frame.mainloop()



    def backup_data(self):
        self.gen_dict["DioDevErrorDetect"]      = self.gen_str.error_detect.get()
        self.gen_dict["DioVersionInfoApi"]      = self.gen_str.verion_api.get()
        self.gen_dict["DioFlipChannelApi"]      = self.gen_str.flip_chan_api.get()
        self.gen_dict["DioMaskedWritePortApi"]  = self.gen_str.masked_write_port_api.get()

        
    def save_data(self):
        self.backup_data()
        self.tab_struct.save_cb(self.gui)
