#
# Created on Sun Feb 05 2023 7:35:52 PM
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



# SoAdConfig container structure
# 
# SoAd
#     + SoAdBswModules (0..*)
#     + SoAdGeneral
#     + SoAdConfig
#         + SoAdPduRoute (0..*)
#             + SoAdTxPduId
#             + SoAdTxPduRef --> Pdu (0..*)
#             + SoAdTxUpperLayerType
#             + SoAdTxPduCollectionSemantics [SOAD_COLLECT_LAST_IS_BEST / SOAD_COLLECT_QUEUED]
#             + SoAdPduRouteDest (1..*)
#                 + SoAdTxPduHeaderId
#                 + SoAdTxSocketConnOrSocketConnBundleRef
#                 + SoAdTxRoutingGroupRef
#                 + SoAdTxUdpTriggerMode [TRIGGER_ALWAYS / TRIGGER_NEVER]
#                 + SoAdTxUdpTriggerTimeout

import gui.soad.soad_pdu_r_dest as soad_pdur_dest


class SoAdChildView:
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



class SoAdPduRouteView:
    n_soad_pdu_r = 0
    n_soad_pdu_r_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SoAdTxPduId", "SoAdTxPduRef", "SoAdTxUpperLayerType",
               "SoAdTxPduCollectionSemantics", "SoAdPduRouteDest"]
    
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False
    
    active_dialog = None
    active_view = None
    save_cb = None


    def __init__(self, gui, soad_cfgs):
        self.gui = gui
        self.configs = []
        self.n_soad_pdu_r = 0
        self.max_soad_pdu_r = 65536
        self.n_soad_pdu_r_str = tk.StringVar()

        # Create config string for AUTOSAR configs on this tab
        if soad_cfgs:
            for i, cfg in enumerate(soad_cfgs):
                self.configs.append(dappa.AsrCfgStr(self.cfgkeys, cfg))
            self.n_soad_pdu_r = len(self.configs)


    def __del__(self):
        del self.configs[:]
        del self.n_soad_pdu_r_str



    def create_empty_configs(self, index):
        gen_dict = {}

        gen_dict["SoAdTxPduId"]          = str(index)
        gen_dict["SoAdTxPduRef"]         = "..."
        gen_dict["SoAdTxUpperLayerType"] = "IF"
        gen_dict["SoAdTxPduCollectionSemantics"]  = "SOAD_COLLECT_LAST_IS_BEST"
        gen_dict["SoAdPduRouteDest"]     = []

        return gen_dict



    def draw_dappa_row(self, i):
        bool_cmbsel = ("FALSE", "TRUE")
        ref_cmbsel = ("Ref1", "Ref2", "...")
        tx_uplt_cmbsel = ("IF", "TP")
        pdu_col_semant = ("SOAD_COLLECT_LAST_IS_BEST", "SOAD_COLLECT_QUEUED")

        dappa.label(self, "PDU_R. #", self.header_row+i,        0, "e")
        dappa.entry(self, "SoAdTxPduId", i, self.header_row+i,  1, 13, "readonly")
        dappa.combo(self, "SoAdTxPduRef", i, self.header_row+i, 2, 12, ref_cmbsel)
        dappa.combo(self, "SoAdTxUpperLayerType", i, self.header_row+i,         3, 19, tx_uplt_cmbsel)
        dappa.combo(self, "SoAdTxPduCollectionSemantics", i, self.header_row+i, 4, 30, pdu_col_semant)
        
        key = "SoAdPduRouteDest [" + str(len(self.configs[i].datavar["SoAdPduRouteDest"])) + "]"
        dappa.button(self, "SoAdPduRouteDest", i, self.header_row+i, 5, 20, key, self.soad_pdur_dest_select)


    def update(self):
        # get dappas to be added or removed
        self.n_soad_pdu_r = int(self.n_soad_pdu_r_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_soad_pdu_r > n_dappa_rows:
            for i in range(self.n_soad_pdu_r - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs(n_dappa_rows+i)))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_soad_pdu_r:
            for i in range(n_dappa_rows - self.n_soad_pdu_r):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="PDU Routes:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=6, textvariable=self.n_soad_pdu_r_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_soad_pdu_r+1)))
        self.n_soad_pdu_r_str.set(self.n_soad_pdu_r)
        spinb.grid(row=0, column=1, sticky="w")

        # Save Button
        genm = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=0, column=2)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()



    def save_data(self):
        self.tab_struct.save_cb(self.gui, self.configs)



    def on_soad_pdur_dest_close(self, row):
        # backup data
        if self.active_view.view.configs:
            self.configs[row].datavar["SoAdPduRouteDest"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[row].datavar["SoAdPduRouteDest"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def soad_pdur_dest_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda i = row : self.on_soad_pdur_dest_close(i))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 1050
        height = 540
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/8, y/7))
        self.active_dialog.title("SoAdPduRouteDest")

        # create views and draw
        gen_view = SoAdChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = soad_pdur_dest.SoAdPduRouteDestView(self.gui,
                                            self.configs[row].datavar["SoAdPduRouteDest"])
        gen_view.name = "SoAdPduRouteDest"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)
