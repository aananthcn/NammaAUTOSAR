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
    config = None
    tabstr = None
    gen_data = None

    def __init__(self, gui):
        self.gui = gui
        self.config = DioGeneralStr()
        self.gen_data = {}
        dio_pins, dio_cfg, dio_gen = arxml_dio.parse_arxml(gui.arxml_file)
        if dio_pins == None:
            self.gen_data["DioDevErrorDetect"]      = "FALSE"
            self.gen_data["DioVersionInfoApi"]      = "FALSE"
            self.gen_data["DioFlipChannelApi"]      = "FALSE"
            self.gen_data["DioMaskedWritePortApi"]  = "FALSE"
            return
        self.gen_data["DioDevErrorDetect"]      = dio_gen["DioDevErrorDetect"]
        self.gen_data["DioVersionInfoApi"]      = dio_gen["DioVersionInfoApi"]
        self.gen_data["DioFlipChannelApi"]      = dio_gen["DioFlipChannelApi"]
        self.gen_data["DioMaskedWritePortApi"]  = dio_gen["DioMaskedWritePortApi"]

    def __del__(self):
        del self.config


    def draw(self, tab):
        self.tabstr = tab
        dio_cmbsel = ("FALSE", "TRUE")
        
        # empty space
        label = tk.Label(tab.frame, text="")
        label.grid(row=1, column=0, sticky="e")

        # DioDevErrorDetect
        label = tk.Label(tab.frame, text="DioDevErrorDetect: ")
        label.grid(row=2, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.config.error_detect, state="readonly")
        cmbsel['values'] = dio_cmbsel
        self.config.error_detect.set(self.gen_data["DioDevErrorDetect"])
        cmbsel.current()
        cmbsel.grid(row=2, column=1)

        # DioVersionInfoApi
        label = tk.Label(tab.frame, text="DioVersionInfoApi: ")
        label.grid(row=3, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.config.verion_api, state="readonly")
        cmbsel['values'] = dio_cmbsel
        self.config.verion_api.set(self.gen_data["DioVersionInfoApi"])
        cmbsel.current()
        cmbsel.grid(row=3, column=1)

        # DioFlipChannelApi
        label = tk.Label(tab.frame, text="DioFlipChannelApi: ")
        label.grid(row=4, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.config.flip_chan_api, state="readonly")
        cmbsel['values'] = dio_cmbsel
        self.config.flip_chan_api.set(self.gen_data["DioFlipChannelApi"])
        cmbsel.current()
        cmbsel.grid(row=4, column=1)

        # DioMaskedWritePortApi
        label = tk.Label(tab.frame, text="DioMaskedWritePortApi: ")
        label.grid(row=5, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.config.masked_write_port_api, state="readonly")
        cmbsel['values'] = dio_cmbsel
        self.config.masked_write_port_api.set(self.gen_data["DioMaskedWritePortApi"])
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
        self.gen_data["DioDevErrorDetect"]      = self.config.error_detect.get()
        self.gen_data["DioVersionInfoApi"]      = self.config.verion_api.get()
        self.gen_data["DioFlipChannelApi"]      = self.config.flip_chan_api.get()
        self.gen_data["DioMaskedWritePortApi"]  = self.config.masked_write_port_api.get()

        
    def save_data(self):
        self.backup_data()
        self.tabstr.save_cb(self.gui)
