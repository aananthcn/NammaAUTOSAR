#
# Created on Wed Oct 05 2022 8:04:30 PM
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



class SpiGeneralStr:
    cancel_api = None
    ch_buf_allowed = None
    dev_err_detect = None
    hw_status_api = None
    intr_seq_allowed = None
    level_delivered = None
    main_per_func = None
    sup_con_sync_tx = None
    version_api = None

    def __init__(self):
        self.cancel_api = tk.StringVar()
        self.ch_buf_allowed = tk.StringVar()
        self.dev_err_detect = tk.StringVar()
        self.hw_status_api = tk.StringVar()
        self.intr_seq_allowed = tk.StringVar()
        self.level_delivered = tk.StringVar()
        self.main_per_func = tk.StringVar()
        self.sup_con_sync_tx = tk.StringVar()
        self.version_api = tk.StringVar()

    def __del__(self):
        del self.cancel_api
        del self.ch_buf_allowed
        del self.dev_err_detect
        del self.hw_status_api
        del self.intr_seq_allowed
        del self.level_delivered
        del self.main_per_func
        del self.sup_con_sync_tx
        del self.version_api



class SpiGeneralTab:
    gui = None
    tab_struct = None # passed from *_view.py file
    gen_str = None
    gen_dict = None

    def __init__(self, gui):
        self.gui = gui
        self.gen_str = SpiGeneralStr()
        # self.gen_dict = arxml_spi.parse_arxml(gui.arxml_file)
        self.gen_dict = None
        if self.gen_dict == None:
            self.gen_dict = {}
            self.gen_dict["SpiLevelDelivered"]                  = "1"
            self.gen_dict["SpiChannelBuffersAllowed"]           = "IB"
            self.gen_dict["SpiInterruptibleSeqAllowed"]         = "FALSE"
            self.gen_dict["SpiHwStatusApi"]                     = "FALSE"
            self.gen_dict["SpiCancelApi"]                       = "FALSE"
            self.gen_dict["SpiVersionInfoApi"]                  = "FALSE"
            self.gen_dict["SpiDevErrorDetect"]                  = "FALSE"
            self.gen_dict["SpiSupportConcurrentSyncTransmit"]   = "FALSE"
            self.gen_dict["SpiMainFunctionPeriod"]              = "0.01" # secs = 100 ms

    def __del__(self):
        del self.gen_str


    def draw(self, tab):
        self.tab_struct = tab
        spi_cmbsel = ("FALSE", "TRUE")
        
        # empty space
        label = tk.Label(tab.frame, text="")
        label.grid(row=1, column=0, sticky="e")

        # SpiLevelDelivered
        label = tk.Label(tab.frame, text="SpiLevelDelivered: ")
        label.grid(row=2, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=20, textvariable=self.gen_str.level_delivered, state="readonly")
        cmbsel['values'] = ('0', '1', '2')
        self.gen_str.level_delivered.set(self.gen_dict["SpiLevelDelivered"])
        cmbsel.current()
        cmbsel.grid(row=2, column=1)

        # SpiChannelBuffersAllowed
        label = tk.Label(tab.frame, text="SpiChannelBuffersAllowed: ")
        label.grid(row=3, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=20, textvariable=self.gen_str.ch_buf_allowed, state="readonly")
        cmbsel['values'] = ('IB (Internal Buffer)', 'EB (External Buffer)', 'IB / EB')
        self.gen_str.ch_buf_allowed.set(self.gen_dict["SpiChannelBuffersAllowed"])
        cmbsel.current()
        cmbsel.grid(row=3, column=1)

        # SpiInterruptibleSeqAllowed
        label = tk.Label(tab.frame, text="SpiInterruptibleSeqAllowed: ")
        label.grid(row=4, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=20, textvariable=self.gen_str.intr_seq_allowed, state="readonly")
        cmbsel['values'] = spi_cmbsel
        self.gen_str.intr_seq_allowed.set(self.gen_dict["SpiInterruptibleSeqAllowed"])
        cmbsel.current()
        cmbsel.grid(row=4, column=1)

        # SpiHwStatusApi
        label = tk.Label(tab.frame, text="SpiHwStatusApi: ")
        label.grid(row=5, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=20, textvariable=self.gen_str.hw_status_api, state="readonly")
        cmbsel['values'] = spi_cmbsel
        self.gen_str.hw_status_api.set(self.gen_dict["SpiHwStatusApi"])
        cmbsel.current()
        cmbsel.grid(row=5, column=1)

        # SpiCancelApi
        label = tk.Label(tab.frame, text="SpiCancelApi: ")
        label.grid(row=6, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=20, textvariable=self.gen_str.cancel_api, state="readonly")
        cmbsel['values'] = spi_cmbsel
        self.gen_str.cancel_api.set(self.gen_dict["SpiCancelApi"])
        cmbsel.current()
        cmbsel.grid(row=6, column=1)

        # SpiVersionInfoApi
        label = tk.Label(tab.frame, text="SpiVersionInfoApi: ")
        label.grid(row=7, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=20, textvariable=self.gen_str.version_api, state="readonly")
        cmbsel['values'] = spi_cmbsel
        self.gen_str.version_api.set(self.gen_dict["SpiVersionInfoApi"])
        cmbsel.current()
        cmbsel.grid(row=7, column=1)

        # SpiDevErrorDetect
        label = tk.Label(tab.frame, text="SpiDevErrorDetect: ")
        label.grid(row=8, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=20, textvariable=self.gen_str.dev_err_detect, state="readonly")
        cmbsel['values'] = spi_cmbsel
        self.gen_str.dev_err_detect.set(self.gen_dict["SpiDevErrorDetect"])
        cmbsel.current()
        cmbsel.grid(row=8, column=1)

        # SpiSupportConcurrentSyncTransmit
        label = tk.Label(tab.frame, text="SpiSupportConcurrentSyncTransmit: ")
        label.grid(row=9, column=0, sticky="e")
        
        cmbsel = ttk.Combobox(tab.frame, width=20, textvariable=self.gen_str.sup_con_sync_tx, state="readonly")
        cmbsel['values'] = spi_cmbsel
        self.gen_str.sup_con_sync_tx.set(self.gen_dict["SpiSupportConcurrentSyncTransmit"])
        cmbsel.current()
        cmbsel.grid(row=9, column=1)

        # SpiMainFunctionPeriod
        label = tk.Label(tab.frame, text="SpiMainFunctionPeriod (sec): ")
        label.grid(row=10, column=0, sticky="e")
        
        entry = tk.Entry(tab.frame, width=23, textvariable=self.gen_str.main_per_func)
        self.gen_str.main_per_func.set(self.gen_dict["SpiMainFunctionPeriod"])
        entry.grid(row=10, column=1)

        # empty space
        label = tk.Label(tab.frame, text="")
        label.grid(row=11, column=0, sticky="e")

        # Save Button
        genm = tk.Button(tab.frame, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=12, column=1)

        self.backup_data()
        #tab.frame.mainloop()



    def backup_data(self):
        self.gen_dict["SpiDevErrorDetect"]      = self.gen_str.cancel_api.get()
        self.gen_dict["SpiVersionInfoApi"]      = self.gen_str.ch_buf_allowed.get()
        self.gen_dict["SpiFlipChannelApi"]      = self.gen_str.dev_err_detect.get()
        self.gen_dict["SpiMaskedWritePortApi"]  = self.gen_str.hw_status_api.get()

        
    def save_data(self):
        self.backup_data()
        self.tab_struct.save_cb(self.gui)
