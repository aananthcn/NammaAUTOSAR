#
# Created on Mon Nov 28 2022 10:04:37 PM
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



class EthGeneralTab:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["EthIndex", "EthDevErrorDetect", "EthGetCounterValuesApi", "EthGetRxStatsApi",
               "EthGetTxErrorCounterValuesApi", "EthGetTxStatsApi", "EthGlobalTimeSupport", 
               "EthMainFunctionPeriod", "EthMaxCtrlsSupported", "EthVersionInfoApi",
               "EthCtrlOffloading", 
               "EthCtrlConfigSwBufferHandling", "EthCtrlEnableMii", "EthCtrlEnableRxInterrupt"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)
    active_dialog = None
    ctrlr_idx = 0
    header_row = 0
    dappas_per_row = 0


    def __init__(self, gui, ar_cfg, idx):
        self.gui = gui
        self.configs = []
        self.ctrlr_idx = idx

        # Create config string for AUTOSAR configs on this tab
        self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs(idx)))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self, index):
        gen_dict = {}
        gen_dict["EthIndex"]                        = str(index)
        gen_dict["EthDevErrorDetect"]               = "FALSE"
        gen_dict["EthMainFunctionPeriod"]           = "FALSE"
        gen_dict["EthGetCounterValuesApi"]          = "IB"
        gen_dict["EthGetRxStatsApi"]                = "FALSE"
        gen_dict["EthGetTxErrorCounterValuesApi"]   = "FALSE"
        gen_dict["EthGetTxStatsApi"]                = "FALSE"
        gen_dict["EthGlobalTimeSupport"]            = "FALSE"
        gen_dict["EthMaxCtrlsSupported"]            = str(index)
        gen_dict["EthVersionInfoApi"]               = "FALSE"
        
        # Checksum OffLoad
        gen_dict["EthCtrlOffloading"]               = {}
        gen_dict["EthCtrlOffloading"]["IPv4"]       = tk.StringVar()
        gen_dict["EthCtrlOffloading"]["ICMP"]       = tk.StringVar()
        gen_dict["EthCtrlOffloading"]["TCP"]        = tk.StringVar()
        gen_dict["EthCtrlOffloading"]["UDP"]        = tk.StringVar()
        
        return gen_dict



    def draw_dappas(self, i):
        bool_cmbsel = ("FALSE", "TRUE")

        group = dappa.group(self, "EthGeneral", row=0, col=0)

        # Table heading @0th row, 0th column
        # dappa.place_column_heading_f(group, self, row=1, col=0)

        # EthGeneral group
        dappa.entryg(group, self, "EthIndex",               i, 1, 1, 23, "readonly")
        dappa.entryg(group, self, "EthMainFunctionPeriod",  i, 2, 1, 23, "normal")
        dappa.combog(group, self, "EthDevErrorDetect",      i, 3, 1, 20, bool_cmbsel)
        dappa.combog(group, self, "EthGetCounterValuesApi", i, 4, 1, 20, bool_cmbsel)
        dappa.combog(group, self, "EthGetRxStatsApi",       i, 5, 1, 20, bool_cmbsel)
        dappa.combog(group, self, "EthGetTxErrorCounterValuesApi", i, 6, 1, 20, bool_cmbsel)
        dappa.combog(group, self, "EthGetTxStatsApi",       i, 7, 1, 20, bool_cmbsel)
        dappa.combog(group, self, "EthGlobalTimeSupport",   i, 8, 1, 20, bool_cmbsel)
        dappa.entryg(group, self, "EthMaxCtrlsSupported",   i, 9, 1, 23, "readonly")
        dappa.combog(group, self, "EthVersionInfoApi",      i, 10, 1, 20, bool_cmbsel)
        cb = lambda id = self.ctrlr_idx : self.eth_offloading_select(id)
        dappa.buttong(group, self, "EthCtrlOffloading",     i, 11, 1, 19, "SELECT", cb)

        # EthCtrlConfig group
        group = dappa.group(self, "EthCtrlConfig", row=0, col=1)
        dappa.combog(group, self, "EthCtrlConfigSwBufferHandling",  i, 1, 2, 20, bool_cmbsel)
        dappa.combog(group, self, "EthCtrlEnableMii",               i, 2, 2, 20, bool_cmbsel)
        dappa.combog(group, self, "EthCtrlEnableRxInterrupt",       i, 3, 2, 20, bool_cmbsel)


    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)

        self.draw_dappas(0)

        # Support scrollable view
        self.scrollw.scroll()



    def save_data(self):
        self.tab_struct.save_cb(self.gui)


    # idx: Controller Index
    # max_ctrlr: Total controllers configured
    def update_ethernet_config(self, idx, max_ctrlr):
        self.configs[idx].dispvar["EthMaxCtrlsSupported"].set(max_ctrlr)


    def eth_offloading_close(self):
        # # remove old selections
        # if self.configs[0].datavar["SpiChannelList"]:
        #     del self.configs[0].datavar["SpiChannelList"][:]


        # # update new selections from last window session
        # for chlist_cfg in self.active_widget.configs:
        #     chlist_cfg.get() # pull from UI
        #     ch_dict = {}
        #     ch_dict['SpiChannelIndex'] = chlist_cfg.datavar['SpiChannelIndex']
        #     ch_dict['SpiChannelAssignment'] = chlist_cfg.datavar['SpiChannelAssignment']
        #     self.configs[0].datavar["SpiChannelList"].append(ch_dict)
        
        # dialog elements are no longer needed, destroy them. Else, new dialogs will not open!
        # del self.active_widget
        self.active_dialog.destroy()
        del self.active_dialog

        # # re-draw all boxes (dappas) of this row
        # dappa.delete_dappa_row(self, 0)
        # self.draw_dappa_row(0)



    def eth_offloading_select(self, ctrlr_idx):
        print("clicked eth_offloading_select")
        if self.active_dialog != None:
            return

        # function to create dialog window
        xsize = 350
        ysize = 100
        self.active_dialog = tk.Toplevel(width=xsize, height=ysize) # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.eth_offloading_close())
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        self.active_dialog.geometry("%dx%d+%d+%d" % (xsize, ysize, x/4, 4*y/10))

        cmbsel_bool = ("FALSE", "TRUE")
        
        # row 1
        label = tk.Label(self.active_dialog, text="EthCtrlEnableOffloadChecksumIPv4")
        label.grid(row=0, column=0, sticky="e")
        cmbsel = ttk.Combobox(self.active_dialog, width=20, 
                    textvariable=self.configs[ctrlr_idx].datavar["EthCtrlOffloading"]["IPv4"])
        cmbsel['values'] = cmbsel_bool
        cmbsel.current()
        cmbsel.grid(row=0, column=1)

        # row 2
        label = tk.Label(self.active_dialog, text="EthCtrlEnableOffloadChecksumICMP")
        label.grid(row=1, column=0, sticky="e")
        cmbsel = ttk.Combobox(self.active_dialog, width=20, 
                    textvariable=self.configs[ctrlr_idx].datavar["EthCtrlOffloading"]["ICMP"])
        cmbsel['values'] = cmbsel_bool
        cmbsel.current()
        cmbsel.grid(row=1, column=1)

        # row 3
        label = tk.Label(self.active_dialog, text="EthCtrlEnableOffloadChecksumTCP")
        label.grid(row=2, column=0, sticky="e")
        cmbsel = ttk.Combobox(self.active_dialog, width=20, 
                    textvariable=self.configs[ctrlr_idx].datavar["EthCtrlOffloading"]["TCP"])
        cmbsel['values'] = cmbsel_bool
        cmbsel.current()
        cmbsel.grid(row=2, column=1)

        # row 4
        label = tk.Label(self.active_dialog, text="EthCtrlEnableOffloadChecksumUDP")
        label.grid(row=3, column=0, sticky="e")
        cmbsel = ttk.Combobox(self.active_dialog, width=20, 
                    textvariable=self.configs[ctrlr_idx].datavar["EthCtrlOffloading"]["UDP"])
        cmbsel['values'] = cmbsel_bool
        cmbsel.current()
        cmbsel.grid(row=3, column=1)