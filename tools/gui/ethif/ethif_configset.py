#
# Created on Sun Jan 15 2023 1:00:15 PM
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

import gui.ethif.ethif_frameowner as ethif_fo
import gui.ethif.ethif_rx_ind as ethif_rxi
import gui.ethif.ethif_tx_cnfrm as ethif_txc
import gui.ethif.ethif_lnk_state_chg as ethif_lsc
import gui.ethif.ethif_phys_ctrlr as ethif_pctrl
import gui.ethif.ethif_ctrlr as ethif_ctrl
import gui.ethif.ethif_trcv as ethif_trcv
import gui.ethif.ethif_switch as ethif_swt
import gui.ethif.ethif_swt_prt_grp as ethif_spg



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



class EthIfConfigSetView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["EthIfFrameOwnerConfig", "EthIfRxIndicationConfig", "EthIfTxConfirmationConfig",
               "EthIfTrcvLinkStateChgConfig", "EthIfPhysController", "EthIfController",
               "EthIfTransceiver", "EthIfSwitch", "EthIfSwitchPortGroup"]

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
        
        gen_dict["EthIfFrameOwnerConfig"]       = []
        gen_dict["EthIfRxIndicationConfig"]     = []
        gen_dict["EthIfTxConfirmationConfig"]   = []
        gen_dict["EthIfTrcvLinkStateChgConfig"] = []
        gen_dict["EthIfPhysController"]         = []
        gen_dict["EthIfController"]             = []
        gen_dict["EthIfTransceiver"]            = []
        gen_dict["EthIfSwitch"]                 = []
        gen_dict["EthIfSwitchPortGroup"]        = []
        
        return gen_dict



    def draw_dappas(self):
        bool_cmbsel = ("FALSE", "TRUE")

        dappa.button(self, "EthIfFrameOwnerConfig",      0, 0, 1, 30, "EthIfFrameOwnerConfig", self.ethif_frameowner_select)
        dappa.button(self, "EthIfRxIndicationConfig",    0, 1, 1, 30, "EthIfRxIndicationConfig", self.ethif_rx_indic_select)
        dappa.button(self, "EthIfTxConfirmationConfig",  0, 2, 1, 30, "EthIfTxConfirmationConfig", self.ethif_tx_cnfrm_select)
        dappa.button(self, "EthIfTrcvLinkStateChgConfig",0, 3, 1, 30, "EthIfTrcvLinkStateChgConfig", self.ethif_lnk_state_chg_select)
        dappa.button(self, "EthIfPhysController",  0, 4, 1, 30, "EthIfPhysController", self.ethif_phys_ctrlr_select)
        dappa.button(self, "EthIfController",      0, 5, 1, 30, "EthIfController", self.ethif_ctrlr_select)
        dappa.button(self, "EthIfTransceiver",     0, 6, 1, 30, "EthIfTransceiver", self.ethif_trcv_select)
        dappa.button(self, "EthIfSwitch",          0, 7, 1, 30, "EthIfSwitch", self.ethif_switch_select)
        dappa.button(self, "EthIfSwitchPortGroup", 0, 8, 1, 30, "EthIfSwitchPortGroup", self.ethif_swt_prt_grp_select)

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
        self.tab_struct.save_cb(self.gui)


    def on_ethif_frameowner_close(self):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["EthIfFrameOwnerConfig"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["EthIfFrameOwnerConfig"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog


    def ethif_frameowner_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_ethif_frameowner_close())
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 450
        height = 540
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/4, y/5))
        self.active_dialog.title("EthIfFrameOwnerConfig")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = ethif_fo.EthIfFrameOwnerConfigView(self.gui,
                                            self.configs[0].datavar["EthIfFrameOwnerConfig"])
        gen_view.name = "EthIfFrameOwnerConfig"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)


    def on_ethif_rx_indic_close(self):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["EthIfRxIndicationConfig"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["EthIfRxIndicationConfig"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog


    def ethif_rx_indic_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_ethif_rx_indic_close())
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 450
        height = 540
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/4, y/5))
        self.active_dialog.title("EthIfRxIndicationConfig")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = ethif_rxi.EthIfRxIndicationConfigView(self.gui,
                                            self.configs[0].datavar["EthIfRxIndicationConfig"])
        gen_view.name = "EthIfRxIndicationConfig"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)


    def on_ethif_tx_cnfrm_close(self):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["EthIfTxConfirmationConfig"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["EthIfTxConfirmationConfig"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog


    def ethif_tx_cnfrm_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_ethif_tx_cnfrm_close())
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 450
        height = 540
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/4, y/5))
        self.active_dialog.title("EthIfTxConfirmationConfig")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = ethif_txc.EthIfTxConfirmConfigView(self.gui,
                                            self.configs[0].datavar["EthIfTxConfirmationConfig"])
        gen_view.name = "EthIfTxConfirmationConfig"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)



    def on_ethif_lnk_state_chg_close(self):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["EthIfTrcvLinkStateChgConfig"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["EthIfTrcvLinkStateChgConfig"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog


    def ethif_lnk_state_chg_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_ethif_lnk_state_chg_close())
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 450
        height = 540
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/4, y/5))
        self.active_dialog.title("EthIfTrcvLinkStateChgConfig")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = ethif_lsc.EthIfLinkStateChangeCfgView(self.gui,
                                            self.configs[0].datavar["EthIfTrcvLinkStateChgConfig"])
        gen_view.name = "EthIfTrcvLinkStateChgConfig"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)



    def on_ethif_phys_ctrlr_close(self):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["EthIfPhysController"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["EthIfPhysController"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog


    def ethif_phys_ctrlr_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_ethif_phys_ctrlr_close())
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 1050
        height = 240
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/6, y/5))
        self.active_dialog.title("EthIfPhysController")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = ethif_pctrl.EthIfPhysControllerView(self.gui,
                                            self.configs[0].datavar["EthIfPhysController"])
        gen_view.name = "EthIfPhysController"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)




    def on_ethif_ctrlr_close(self):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["EthIfController"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["EthIfController"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog


    def ethif_ctrlr_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_ethif_ctrlr_close())
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 1050
        height = 440
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/5, y/5))
        self.active_dialog.title("EthIfController")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = ethif_ctrl.EthIfControllerView(self.gui,
                                            self.configs[0].datavar["EthIfController"])
        gen_view.name = "EthIfController"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)



    def on_ethif_trcv_close(self):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["EthIfTransceiver"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["EthIfTransceiver"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog


    def ethif_trcv_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_ethif_trcv_close())
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 650
        height = 240
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/5, y/5))
        self.active_dialog.title("EthIfTransceiver")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = ethif_trcv.EthIfTransceiverView(self.gui,
                                            self.configs[0].datavar["EthIfTransceiver"])
        gen_view.name = "EthIfTransceiver"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)



    def on_ethif_switch_close(self):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["EthIfSwitch"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["EthIfSwitch"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog


    def ethif_switch_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_ethif_switch_close())
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 370
        height = 240
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/5, y/5))
        self.active_dialog.title("EthIfSwitch")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = ethif_swt.EthIfSwitchView(self.gui,
                                            self.configs[0].datavar["EthIfSwitch"])
        gen_view.name = "EthIfSwitch"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)



    def on_ethif_swt_prt_grp_close(self):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["EthIfSwitchPortGroup"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["EthIfSwitchPortGroup"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog


    def ethif_swt_prt_grp_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_ethif_swt_prt_grp_close())
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 950
        height = 440
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/5, y/5))
        self.active_dialog.title("EthIfSwitchPortGroup")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = ethif_spg.EthIfSwtPortGrpView(self.gui,
                                            self.configs[0].datavar["EthIfSwitchPortGroup"])
        gen_view.name = "EthIfSwitchPortGroup"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)
