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
    cfgkeys = ["EthIfMaxTrcvsTotal", "EthIfDevErrorDetect", "EthIfEnableRxInterrupt",
               "EthIfEnableTxInterrupt", "EthIfVersionInfoApi", "EthIfVersionInfoApiMacro",
               "EthIfTrcvLinkStateChgMainReload", "EthIfMainFunctionPeriod", "EthIfPublicCddHeaderFile",
               "EthIfRxIndicationIterations", "EthIfGetAndResetMeasurementDataApi",
               "EthIfStartAutoNegotiation", "EthIfGetBaudRate", "EthIfGetCounterState",
               "EthIfGlobalTimeSupport", "EthIfWakeUpSupport", "EthIfGetTransceiverWakeupModeApi",
               "EthIfSwitchOffPortTimeDelay", "EthIfPortStartupActiveTime", "EthIfMainFunctionStatePeriod",
               "EthIfSetForwardingModeApi", "EthIfVerifyConfigApi", "EthIfSwitchManagementSupport",
               "EthIfGetCtrlIdxList", "EthIfGetVlanIdSupport", "EthIfEnableWEthApi",
               "EthIfEnableSignalQualityApi", "EthIfSignalQualityCheckPeriod", "EthIfEnableSecurityEventReporting",
               "EthIfSecurityEventRefs"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)
    active_dialog = None
    active_view = None


    def __init__(self, gui, ethif_cfg):
        self.gui = gui
        self.configs = []
        
        if ethif_cfg:
            gen_cfg = ethif_cfg[0]["EthIfGeneral"]
        else:
            return

        # Create config string for AUTOSAR configs on this tab
        if not gen_cfg:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, gen_cfg))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}
        
        gen_dict["EthIfMaxTrcvsTotal"]      = "1"
        gen_dict["EthIfDevErrorDetect"]     = "FALSE"
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

        gen_dict["EthIfSwitchOffPortTimeDelay"]     = "0.001"
        gen_dict["EthIfPortStartupActiveTime"]      = "0.001"
        gen_dict["EthIfMainFunctionStatePeriod"]    = "0.0"
        gen_dict["EthIfSetForwardingModeApi"]       = "FALSE"
        gen_dict["EthIfVerifyConfigApi"]            = "FALSE"
        gen_dict["EthIfSwitchManagementSupport"]    = "FALSE"
        gen_dict["EthIfGetCtrlIdxList"]         = "FALSE"
        gen_dict["EthIfGetVlanIdSupport"]       = "FALSE"
        gen_dict["EthIfEnableWEthApi"]          = "FALSE"
        gen_dict["EthIfEnableSignalQualityApi"] = "FALSE"
        gen_dict["EthIfSignalQualityCheckPeriod"]       = "0.01"
        gen_dict["EthIfEnableSecurityEventReporting"]   = "FALSE"
        gen_dict["EthIfSecurityEventRefs"]              = "..."
        
        return gen_dict



    def draw_dappas(self):
        bool_cmbsel = ("FALSE", "TRUE")
        ref_cmbsel = ("Ref1", "Ref2", "...")

        # insert column separator at 0
        dappa.colsep(self, 0)

        # column = 2; label at 1
        dappa.spinbg(self, "EthIfMaxTrcvsTotal",     0, 0, 2, 21, tuple(range(0,256)))
        dappa.combog(self, "EthIfDevErrorDetect",    0, 1, 2, 20, bool_cmbsel)
        dappa.combog(self, "EthIfEnableRxInterrupt", 0, 2, 2, 20, bool_cmbsel)
        dappa.combog(self, "EthIfEnableTxInterrupt", 0, 3, 2, 20, bool_cmbsel)
        dappa.combog(self, "EthIfVersionInfoApi",    0, 4, 2, 20, bool_cmbsel)
        dappa.combog(self, "EthIfVersionInfoApiMacro",        0, 5, 2, 20, bool_cmbsel)
        dappa.spinbg(self, "EthIfTrcvLinkStateChgMainReload", 0, 6, 2, 21, tuple(range(0,256)))
        dappa.entryg(self, "EthIfMainFunctionPeriod",     0, 7, 2, 23, "normal")
        dappa.buttong(self, "EthIfPublicCddHeaderFile",   0, 8, 2, 19, "CDD HeaderFiles", self.ethif_cddhdr_select)
        dappa.spinbg(self, "EthIfRxIndicationIterations", 0, 9, 2, 21, tuple(range(0,65536)))
        dappa.combog(self, "EthIfGetAndResetMeasurementDataApi", 0, 10, 2, 20, bool_cmbsel)
        dappa.combog(self, "EthIfStartAutoNegotiation",  0, 11, 2, 20, bool_cmbsel)
        dappa.combog(self, "EthIfGetBaudRate",           0, 12, 2, 20, bool_cmbsel)
        dappa.combog(self, "EthIfGetCounterState",       0, 13, 2, 20, bool_cmbsel)
        dappa.combog(self, "EthIfGlobalTimeSupport",     0, 14, 2, 20, bool_cmbsel)
        dappa.combog(self, "EthIfWakeUpSupport",         0, 15, 2, 20, bool_cmbsel)
        dappa.combog(self, "EthIfGetTransceiverWakeupModeApi", 0, 16, 2, 20, bool_cmbsel)

        # insert column separator at 3
        dappa.colsep(self, 3)

        # column = 5; label at 4
        dappa.entryg(self, "EthIfSwitchOffPortTimeDelay",  0, 0, 5, 23, "normal")
        dappa.entryg(self, "EthIfPortStartupActiveTime",   0, 1, 5, 23, "normal")
        dappa.entryg(self, "EthIfMainFunctionStatePeriod", 0, 2, 5, 23, "normal")
        dappa.combog(self, "EthIfSetForwardingModeApi",    0, 3, 5, 20, bool_cmbsel)
        dappa.combog(self, "EthIfVerifyConfigApi",         0, 4, 5, 20, bool_cmbsel)
        dappa.combog(self, "EthIfSwitchManagementSupport", 0, 5, 5, 20, bool_cmbsel)
        dappa.combog(self, "EthIfGetCtrlIdxList",   0, 6, 5, 20, bool_cmbsel)
        dappa.combog(self, "EthIfGetVlanIdSupport", 0, 7, 5, 20, bool_cmbsel)
        dappa.combog(self, "EthIfEnableWEthApi",    0, 8, 5, 20, bool_cmbsel)
        dappa.combog(self, "EthIfEnableSignalQualityApi",       0, 9, 5, 20, bool_cmbsel)
        dappa.entryg(self, "EthIfSignalQualityCheckPeriod",     0, 10, 5, 23, "normal")
        dappa.combog(self, "EthIfEnableSecurityEventReporting", 0, 11, 5, 20, bool_cmbsel)
        dappa.combog(self, "EthIfSecurityEventRefs", 0, 12, 5, 20, ref_cmbsel)

        # empty space
        label = tk.Label(self.scrollw.mnf, text="")
        label.grid(row=17, column=0, sticky="e")

        # Save Button
        saveb = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        saveb.grid(row=18, column=1)



    def draw(self, view):
        self.tab_struct = view
        self.scrollw = window.ScrollableWindow(view.frame, view.xsize, view.ysize)

        # # Table heading @0th row, 0th column
        # dappa.place_column_heading(self, row=0, col=0)
        dappa.place_no_heading(self)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()


    def save_data(self):
        self.tab_struct.save_cb(self.gui)


    def on_ethif_cddhdr_select_close(self, row):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["EthIfPublicCddHeaderFile"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["EthIfPublicCddHeaderFile"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog



    def ethif_cddhdr_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_ethif_cddhdr_select_close(0))
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
                                            self.configs[0].datavar["EthIfPublicCddHeaderFile"])
        gen_view.name = "EthIfPublicCddHeaderFile"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)
