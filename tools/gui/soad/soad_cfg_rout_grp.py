#
# Created on Wed Feb 08 2023 8:31:07 AM
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
#         + SoAdRoutingGroup (0..*)
#             + SoAdRoutingGroupId
#             + SoAdRoutingGroupIsEnabledAtInit
#             + SoAdRoutingGroupTxTriggerable

import gui.soad.soad_cfg_pdu_r_dest as soad_pdur_dest


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



class SoAdRoutingGroupView:
    n_soad_pdu_r = 0
    n_soad_pdu_r_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SoAdRoutingGroupId", "SoAdRoutingGroupIsEnabledAtInit",
               "SoAdRoutingGroupTxTriggerable"]
    
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

        gen_dict["SoAdRoutingGroupId"]              = str(index)
        gen_dict["SoAdRoutingGroupIsEnabledAtInit"] = "FALSE"
        gen_dict["SoAdRoutingGroupTxTriggerable"]   = "FALSE"

        return gen_dict



    def draw_dappa_row(self, i):
        bool_cmbsel = ("FALSE", "TRUE")

        dappa.label(self, "R. Group #", self.header_row+i,              0, "e")
        dappa.entry(self, "SoAdRoutingGroupId", i, self.header_row+i,   1, 20, "readonly")
        dappa.combo(self, "SoAdRoutingGroupIsEnabledAtInit", i, self.header_row+i, 2, 29, bool_cmbsel)
        dappa.combo(self, "SoAdRoutingGroupTxTriggerable", i, self.header_row+i,   3, 28, bool_cmbsel)



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

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()
