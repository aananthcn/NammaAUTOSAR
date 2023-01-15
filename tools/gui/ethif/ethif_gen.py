#
# Created on Sat Jan 14 2023 10:42:05 PM
#
# The MIT License (MIT)
# Copyright (c) 2023 Aananth C N
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

import gui.ethif.ethif_cddhdr as ethif_cddhdr



class EthChildView:
    view = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h, cb):
        self.save_cb = cb
        self.frame = f
        self.xsize = w
        self.ysize = h



class EthIfGeneralView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["EthifMaxTrcvsTotal", "EthifDevErrorDetect", "EthIfEnableRxInterrupt",
               "EthIfEnableTxInterrupt", "EthIfVersionInfoApi", "EthIfVersionInfoApiMacro",
               "EthIfTrcvLinkStateChgMainReload", "EthIfMainFunctionPeriod", "EthIfPublicCddHeaderFile",
               "EthIfRxIndicationIterations", "EthIfGetAndResetMeasurementDataApi",
               "EthIfStartAutoNegotiation", "EthIfGetBaudRate", "EthIfGetCounterState",
               "EthIfGlobalTimeSupport", "EthIfWakeUpSupport", "EthIfGetTransceiverWakeupModeApi"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)
    active_dialog = None
    active_view = None


    def __init__(self, gui, gen_cfg):
        self.gui = gui
        self.configs = []

        # Create config string for AUTOSAR configs on this tab
        if not gen_cfg:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, gen_cfg))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}
        
        gen_dict["EthifMaxTrcvsTotal"]      = "1"
        gen_dict["EthifDevErrorDetect"]     = "FALSE"
        gen_dict["EthIfEnableRxInterrupt"]  = "FALSE"
        gen_dict["EthIfEnableTxInterrupt"]  = "FALSE"
        gen_dict["EthIfVersionInfoApi"]     = "FALSE"
        gen_dict["EthIfVersionInfoApiMacro"]        = "FALSE"
        gen_dict["EthIfTrcvLinkStateChgMainReload"] = "1"
        gen_dict["EthIfMainFunctionPeriod"]     = "0.01" # time in seconds
        gen_dict["EthIfPublicCddHeaderFile"]    = []
        gen_dict["EthIfRxIndicationIterations"] = "0"
        gen_dict["EthIfStartAutoNegotiation"]   = "FALSE"
        gen_dict["EthIfGetBaudRate"]            = "FALSE"
        gen_dict["EthIfGetCounterState"]        = "FALSE"
        gen_dict["EthIfGlobalTimeSupport"]      = "FALSE"
        gen_dict["EthIfWakeUpSupport"]          = "FALSE"
        gen_dict["EthIfGetAndResetMeasurementDataApi"]  = "FALSE"
        gen_dict["EthIfGetTransceiverWakeupModeApi"]    = "FALSE"
        
        return gen_dict



    def draw_dappas(self):
        bool_cmbsel = ("FALSE", "TRUE")

        dappa.spinb(self, "EthifMaxTrcvsTotal",     0, 0, 1, 21, tuple(range(0,256)))
        dappa.combo(self, "EthifDevErrorDetect",    0, 1, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthIfEnableRxInterrupt", 0, 2, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthIfEnableTxInterrupt", 0, 3, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthIfVersionInfoApi",    0, 4, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthIfVersionInfoApiMacro",        0, 5, 1, 20, bool_cmbsel)
        dappa.spinb(self, "EthIfTrcvLinkStateChgMainReload", 0, 6, 1, 21, tuple(range(0,256)))
        dappa.entry(self, "EthIfMainFunctionPeriod",     0, 7, 1, 23, "normal")
        dappa.button(self, "EthIfPublicCddHeaderFile",   0, 8, 1, 19, "CDD HeaderFiles", self.ethif_cddhdr_select)
        dappa.spinb(self, "EthIfRxIndicationIterations", 0, 9, 1, 21, tuple(range(0,65536)))
        dappa.combo(self, "EthIfGetAndResetMeasurementDataApi", 0, 10, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthIfStartAutoNegotiation",  0, 11, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthIfGetBaudRate",           0, 12, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthIfGetCounterState",       0, 13, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthIfGlobalTimeSupport",     0, 14, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthIfWakeUpSupport",         0, 15, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthIfGetTransceiverWakeupModeApi", 0, 16, 1, 20, bool_cmbsel)

        # empty space
        label = tk.Label(self.scrollw.mnf, text="")
        label.grid(row=17, column=0, sticky="e")

        # Save Button
        saveb = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        saveb.grid(row=18, column=1)



    def draw(self, view):
        self.tab_struct = view
        self.scrollw = window.ScrollableWindow(view.frame, view.xsize, view.ysize)

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()


    def save_data(self):
        print("save_data called!")


    def on_ethif_cddhdr_select_close(self, row):
        # backup data
        self.configs[row].datavar["EthIfPublicCddHeaderFile"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # # re-draw all boxes (dappas) of this row
        # dappa.delete_dappa_row(self, row)
        # self.draw_dappas(row)


    def ethif_cddhdr_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_ethif_cddhdr_select_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 450
        height = 240
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/10, y/5))

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = ethif_cddhdr.EthIfPublicHeaderFilesView(self.gui,
                                            self.configs[row].datavar["EthIfPublicCddHeaderFile"])
        gen_view.name = "EthIfPublicCddHeaderFile"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)
