#
# Created on Sun Feb 19 2023 10:34:26 PM
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
#     + SoAdConfig
#         + SoAdSocketConnectionGroup (1..*)
#             + SoAdSocketProtocol [SoAdSocketTcp / SoAdSocketUdp]
#                 + SoAdSocketTcp
#                     + SoAdSocketTcpRetransmissionTimeout
#                     + SoAdSocketTcpAutoConnectTimeout
#                     + SoAdSocketTcpInitiate
#                     + SoAdSocketTcpNoDelay
#                     + SoAdSocketTcpImmediateTpTxConfirmation
#                     + SoAdSocketTcpTxQuota
#                     + SoAdSocketTcpKeepAlive
#                     + SoAdSocketTcpKeepAliveProbesMax
#                     + SoAdSocketTcpKeepAliveInterval
#                     + SoAdSocketTcpKeepAliveTime
#                     + SoAdSocketTCPOptionFilterRef --> TcpIpTcpConfigOptionFilter
#                     + SoAdSocketTcpTlsConnectionRef --> TcpIpTlsConnection


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



class SoAdSocketTcpView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SoAdSocketTcpRetransmissionTimeout", "SoAdSocketTcpAutoConnectTimeout",
               "SoAdSocketTcpInitiate", "SoAdSocketTcpNoDelay",
               "SoAdSocketTcpImmediateTpTxConfirmation", "SoAdSocketTcpTxQuota",
               "SoAdSocketTcpKeepAlive", "SoAdSocketTcpKeepAliveProbesMax",
               "SoAdSocketTcpKeepAliveInterval", "SoAdSocketTcpKeepAliveTime",
               "SoAdSocketTCPOptionFilterRef", "SoAdSocketTcpTlsConnectionRef"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)
    active_dialog = None
    active_view = None


    def __init__(self, gui, tcp_cfgs):
        self.gui = gui
        self.configs = []

        # Create config string for AUTOSAR configs on this tab
        if not tcp_cfgs:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            for cfg in tcp_cfgs:
                self.configs.append(dappa.AsrCfgStr(self.cfgkeys, cfg))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}
        
        gen_dict["SoAdSocketTcpRetransmissionTimeout"] = "0.001"
        gen_dict["SoAdSocketTcpAutoConnectTimeout"]    = "0"
        gen_dict["SoAdSocketTcpInitiate"]              = "FALSE"
        gen_dict["SoAdSocketTcpNoDelay"]               = "FALSE"
        gen_dict["SoAdSocketTcpImmediateTpTxConfirmation"]  = "FALSE"
        gen_dict["SoAdSocketTcpTxQuota"]               = "0"
        gen_dict["SoAdSocketTcpKeepAlive"]             = "FALSE"
        gen_dict["SoAdSocketTcpKeepAliveProbesMax"]    = "0"
        gen_dict["SoAdSocketTcpKeepAliveInterval"]     = "0"
        gen_dict["SoAdSocketTcpKeepAliveTime"]         = "7200"
        gen_dict["SoAdSocketTCPOptionFilterRef"]       = "..."
        gen_dict["SoAdSocketTcpTlsConnectionRef"]      = "..."
        
        return gen_dict



    def draw_dappas(self):
        bool_cmbsel = ("FALSE", "TRUE")
        ref_cmbsel = ("Ref1", "Ref2", "...")

        # column = 2; label at 1
        dappa.entryg(self, "SoAdSocketTcpRetransmissionTimeout", 0, 0, 2, 23, "normal")
        dappa.entryg(self, "SoAdSocketTcpAutoConnectTimeout", 0, 1, 2, 23, "normal")
        dappa.combog(self, "SoAdSocketTcpInitiate",     0, 2, 2, 20, bool_cmbsel)
        dappa.combog(self, "SoAdSocketTcpNoDelay",     0, 3, 2, 20, bool_cmbsel)
        dappa.combog(self, "SoAdSocketTcpImmediateTpTxConfirmation", 0, 4, 2, 20, bool_cmbsel)
        dappa.entryg(self, "SoAdSocketTcpTxQuota", 0, 5, 2, 23, "normal")
        dappa.combog(self, "SoAdSocketTcpKeepAlive", 0, 6, 2, 20, bool_cmbsel)
        dappa.entryg(self, "SoAdSocketTcpKeepAliveProbesMax", 0, 7, 2, 23, "normal")
        dappa.entryg(self, "SoAdSocketTcpKeepAliveInterval", 0, 8, 2, 23, "normal")
        dappa.entryg(self, "SoAdSocketTcpKeepAliveTime", 0, 9, 2, 23, "normal")
        dappa.combog(self, "SoAdSocketTCPOptionFilterRef",  0, 10, 2, 20, ref_cmbsel)
        dappa.combog(self, "SoAdSocketTcpTlsConnectionRef",  0, 11, 2, 20, ref_cmbsel)

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
