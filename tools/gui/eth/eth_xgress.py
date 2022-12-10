#
# Created on Sat Dec 10 2022 7:13:24 AM
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



class EthConfigXgressFifoChildView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["EthCtrlConfigEgressFifoBufLenByte", "EthCtrlConfigEgressFifoBufTotal",
               "EthCtrlConfigEgressFifoIdx", "EthCtrlConfigEgressFifoPriorityAssignment",
               "EthCtrlConfigIngressFifoBufLenByte", "EthCtrlConfigIngressFifoBufTotal",
               "EthCtrlConfigIngressFifoIdx", "EthCtrlConfigIngressFifoPriorityAssignment"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)


    def __init__(self, gui, index, ethxgress_cfg):
        self.gui = gui
        self.configs = []

        # Create config string for AUTOSAR configs on this tab
        if not ethxgress_cfg:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs(index)))
        else:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, ethxgress_cfg))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self, index):
        gen_dict = {}
        
        gen_dict["EthCtrlConfigEgressFifoBufLenByte"]          = "128"
        gen_dict["EthCtrlConfigEgressFifoBufTotal"]            = "100"
        gen_dict["EthCtrlConfigEgressFifoIdx"]                 = str(index)
        gen_dict["EthCtrlConfigEgressFifoPriorityAssignment"]  = "7"
        gen_dict["EthCtrlConfigIngressFifoBufLenByte"]         = "128"
        gen_dict["EthCtrlConfigIngressFifoBufTotal"]           = "100"
        gen_dict["EthCtrlConfigIngressFifoIdx"]                = str(index)
        gen_dict["EthCtrlConfigIngressFifoPriorityAssignment"] = "7"
        
        return gen_dict



    def draw_dappas(self):
        bool_cmbsel = ("FALSE", "TRUE")

        dappa.spinb(self, "EthCtrlConfigEgressFifoBufLenByte",  0, 0, 1, 20, tuple(range(0,65536)))
        dappa.spinb(self, "EthCtrlConfigEgressFifoBufTotal",    0, 1, 1, 20, tuple(range(0,65536)))
        dappa.entry(self, "EthCtrlConfigEgressFifoIdx",         0, 2, 1, 22, "readonly")
        dappa.spinb(self, "EthCtrlConfigEgressFifoPriorityAssignment", 0, 3, 1, 20, tuple(range(0,256)))
        dappa.spinb(self, "EthCtrlConfigIngressFifoBufLenByte", 0, 4, 1, 20, tuple(range(0,65536)))
        dappa.spinb(self, "EthCtrlConfigIngressFifoBufTotal",   0, 5, 1, 20, tuple(range(0,65536)))
        dappa.entry(self, "EthCtrlConfigIngressFifoIdx",        0, 6, 1, 22, "readonly")
        dappa.spinb(self, "EthCtrlConfigIngressFifoPriorityAssignment", 0, 7, 1, 20, tuple(range(0,256)))



    def draw(self, view):
        self.tab_struct = view
        self.scrollw = window.ScrollableWindow(view.frame, view.xsize, view.ysize)

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)
        self.draw_dappas()

        # Place save button
        space = tk.Label(self.scrollw.mnf)
        space.grid(row=10, column=1)
        saveb = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        saveb.grid(row=11, column=1)

        # Support scrollable view
        self.scrollw.scroll()



    def save_data(self):
        self.tab_struct.save_cb()
