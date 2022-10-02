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

import arxml.port.arxml_port as arxml_port
import gui.port.port_cgen as port_cgen


class PortGeneralStr:
    error_detect = None
    verion_api = None
    pin_dir_api = None
    pin_mode_api = None

    def __init__(self):
        self.error_detect = tk.StringVar()
        self.verion_api = tk.StringVar()
        self.pin_dir_api = tk.StringVar()
        self.pin_mode_api = tk.StringVar()

    def __del__(self):
        del self.error_detect
        del self.verion_api
        del self.pin_dir_api
        del self.pin_mode_api


class PortGeneralTab:
    gui = None
    config = None
    tab_struct = None
    gen_data = None

    def __init__(self, gui):
        self.gui = gui
        self.config = PortGeneralStr()
        self.gen_data = {}
        port_pins, port_cfg, port_gen = arxml_port.parse_arxml(gui.arxml_file)
        if port_pins == None or port_gen == None:
            self.gen_data["PortDevErrorDetect"]      = "FALSE"
            self.gen_data["PortVersionInfoApi"]      = "FALSE"
            self.gen_data["PortSetPinDirectionApi"]  = "FALSE"
            self.gen_data["PortSetPinModeApi"]       = "FALSE"
            return
        self.gen_data["PortDevErrorDetect"]      = port_gen["PortDevErrorDetect"]
        self.gen_data["PortVersionInfoApi"]      = port_gen["PortVersionInfoApi"]
        self.gen_data["PortSetPinDirectionApi"]  = port_gen["PortSetPinDirectionApi"]
        self.gen_data["PortSetPinModeApi"]       = port_gen["PortSetPinModeApi"]

    def __del__(self):
        del self.config


    def draw(self, tab):
        self.tab_struct = tab
        port_cmbsel = ("FALSE", "TRUE")
        
        # empty space
        label = tk.Label(tab.frame, text="")
        label.grid(row=1, column=0, sticky="e")

        # PortDevErrorDetect
        label = tk.Label(tab.frame, text="PortDevErrorDetect: ")
        label.grid(row=2, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.config.error_detect, state="readonly")
        cmbsel['values'] = port_cmbsel
        self.config.error_detect.set(self.gen_data["PortDevErrorDetect"])
        cmbsel.current()
        cmbsel.grid(row=2, column=1)

        # PortVersionInfoApi
        label = tk.Label(tab.frame, text="PortVersionInfoApi: ")
        label.grid(row=3, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.config.verion_api, state="readonly")
        cmbsel['values'] = port_cmbsel
        self.config.verion_api.set(self.gen_data["PortVersionInfoApi"])
        cmbsel.current()
        cmbsel.grid(row=3, column=1)

        # PortSetPinDirectionApi
        label = tk.Label(tab.frame, text="PortSetPinDirectionApi: ")
        label.grid(row=4, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.config.pin_dir_api, state="readonly")
        cmbsel['values'] = port_cmbsel
        self.config.pin_dir_api.set(self.gen_data["PortSetPinDirectionApi"])
        cmbsel.current()
        cmbsel.grid(row=4, column=1)

        # PortSetPinModeApi
        label = tk.Label(tab.frame, text="PortSetPinModeApi: ")
        label.grid(row=5, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.config.pin_mode_api, state="readonly")
        cmbsel['values'] = port_cmbsel
        self.config.pin_mode_api.set(self.gen_data["PortSetPinModeApi"])
        cmbsel.current()
        cmbsel.grid(row=5, column=1)

        # empty space
        label = tk.Label(tab.frame, text="")
        label.grid(row=6, column=0, sticky="e")

        # Save Button
        genm = tk.Button(tab.frame, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=7, column=1)

        self.backup_data()
        tab.frame.mainloop()



    def backup_data(self):
        self.gen_data["PortDevErrorDetect"]      = self.config.error_detect.get()
        self.gen_data["PortVersionInfoApi"]      = self.config.verion_api.get()
        self.gen_data["PortSetPinDirectionApi"]  = self.config.pin_dir_api.get()
        self.gen_data["PortSetPinModeApi"]       = self.config.pin_mode_api.get()

        
    def save_data(self):
        self.backup_data()
        self.tab_struct.save_cb(self.gui)
