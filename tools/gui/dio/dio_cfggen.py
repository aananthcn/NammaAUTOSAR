import tkinter as tk
from tkinter import ttk

import arxml.port.arxml_port as arxml_port
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

    def __init__(self, gui):
        self.gui = gui
        self.config = DioGeneralStr()

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
        self.config.error_detect.set("FALSE")
        cmbsel.current()
        cmbsel.grid(row=2, column=1)

        # DioVersionInfoApi
        label = tk.Label(tab.frame, text="DioVersionInfoApi: ")
        label.grid(row=3, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.config.verion_api, state="readonly")
        cmbsel['values'] = dio_cmbsel
        self.config.verion_api.set("FALSE")
        cmbsel.current()
        cmbsel.grid(row=3, column=1)

        # DioFlipChannelApi
        label = tk.Label(tab.frame, text="DioFlipChannelApi: ")
        label.grid(row=4, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.config.flip_chan_api, state="readonly")
        cmbsel['values'] = dio_cmbsel
        self.config.flip_chan_api.set("FALSE")
        cmbsel.current()
        cmbsel.grid(row=4, column=1)

        # DioMaskedWritePortApi
        label = tk.Label(tab.frame, text="DioMaskedWritePortApi: ")
        label.grid(row=5, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=14, textvariable=self.config.masked_write_port_api, state="readonly")
        cmbsel['values'] = dio_cmbsel
        self.config.masked_write_port_api.set("FALSE")
        cmbsel.current()
        cmbsel.grid(row=5, column=1)

        # empty space
        label = tk.Label(tab.frame, text="")
        label.grid(row=6, column=0, sticky="e")

        # Save Button
        genm = tk.Button(tab.frame, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=7, column=1)

        tab.frame.mainloop()



    def save_data(self):
        self.tabstr.save_cb()
        return
        arxml_port.update_arxml(self.gui.arxml_file, self)
        port_cgen.generate_code(self.gui)

