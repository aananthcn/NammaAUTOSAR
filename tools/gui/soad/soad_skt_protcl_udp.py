#
# Created on Sun Feb 19 2023 10:34:15 PM
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
#                 + SoAdSocketUdp
#                     + SoAdSocketUdpListenOnly
#                     + SoAdSocketUdpAliveSupervisionTimeout
#                     + SoAdSocketnPduUdpTxBufferMin
#                     + SoAdSocketUdpTriggerTimeout
#                     + SoAdSocketUdpStrictHeaderLenCheckEnabled
#                     + SoAdSocketUdpChecksumEnabled


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



class SoAdSocketUdpView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SoAdSocketUdpListenOnly", "SoAdSocketUdpAliveSupervisionTimeout",
               "SoAdSocketnPduUdpTxBufferMin", "SoAdSocketUdpTriggerTimeout",
               "SoAdSocketUdpStrictHeaderLenCheckEnabled", "SoAdSocketUdpChecksumEnabled"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)
    active_dialog = None
    active_view = None


    def __init__(self, gui, udp_cfg):
        self.gui = gui
        self.configs = []

        # Create config string for AUTOSAR configs on this tab
        if not udp_cfg:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, udp_cfg))

    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}
        
        gen_dict["SoAdSocketUdpListenOnly"]                     = "FALSE"
        gen_dict["SoAdSocketUdpAliveSupervisionTimeout"]        = "0"
        gen_dict["SoAdSocketnPduUdpTxBufferMin"]                = "0"
        gen_dict["SoAdSocketUdpTriggerTimeout"]                 = "0"
        gen_dict["SoAdSocketUdpStrictHeaderLenCheckEnabled"]    = "FALSE"
        gen_dict["SoAdSocketUdpChecksumEnabled"]                = "TRUE"
        
        return gen_dict



    def draw_dappas(self):
        bool_cmbsel = ("FALSE", "TRUE")

        # column = 2; label at 1
        dappa.combog(self, "SoAdSocketUdpListenOnly", 0, 0, 2, 20, bool_cmbsel)
        dappa.entryg(self, "SoAdSocketUdpAliveSupervisionTimeout", 0, 1, 2, 23, "normal")
        dappa.entryg(self, "SoAdSocketnPduUdpTxBufferMin", 0, 2, 2, 23, "normal")
        dappa.entryg(self, "SoAdSocketUdpTriggerTimeout", 0, 3, 2, 23, "normal")
        dappa.combog(self, "SoAdSocketUdpStrictHeaderLenCheckEnabled",  0, 4, 2, 20, bool_cmbsel)
        dappa.combog(self, "SoAdSocketUdpChecksumEnabled",  0, 5, 2, 20, bool_cmbsel)



    def draw(self, view):
        self.tab_struct = view
        self.scrollw = window.ScrollableWindow(view.frame, view.xsize, view.ysize)

        dappa.place_no_heading(self)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()
