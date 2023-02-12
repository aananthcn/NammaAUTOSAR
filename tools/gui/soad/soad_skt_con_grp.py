#
# Created on Sat Feb 11 2023 6:46:17 AM
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
#         + SoAdSocketConnectionGroup (1..*)
#             + SoAdPduHeaderEnable
#             + SoAdSocketPathMTUEnable
#             + SoAdSocketAutomaticSoConSetup
#             + SoAdSocketIpAddrAssignmentChgNotification
#             + SoAdSocketLocalAddressRef --> TcpIpLocalAddr <>-- TcpIpAddrId
#             + SoAdSocketLocalPort
#             + SoAdSocketSoConModeChgBswMNotification
#             + SoAdSocketSoConModeChgNotification
#             + SoAdSocketProtocol [SoAdSocketTcp / SoAdSocketUdp]
#             + SoAdSocketTpRxBufferMin
#             + SoAdSocketFramePriority
#             + SoAdSocketMsgAcceptanceFilterEnabled
#             + SoAdSocketSoConModeChgNotifUpperLayerRef --> SoAdBswModules 
#             + SoAdSocketFlowLabel
#             + SoAdSocketDifferentiatedServicesField
#             + SoAdSocketConnection

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



class SoAdSocketConnectionGrpView:
    n_soad_sktcn = 0
    n_soad_sktcn_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SoAdPduHeaderEnable", "SoAdSocketPathMTUEnable", "SoAdSocketAutomaticSoConSetup",
               "SoAdSocketIpAddrAssignmentChgNotification", "SoAdSocketLocalAddressRef",
               "SoAdSocketLocalPort", "SoAdSocketSoConModeChgBswMNotification",
               "SoAdSocketSoConModeChgNotification", "SoAdSocketProtocol",
               "SoAdSocketTpRxBufferMin", "SoAdSocketFramePriority",
               "SoAdSocketMsgAcceptanceFilterEnabled", "SoAdSocketSoConModeChgNotifUpperLayerRef",
               "SoAdSocketFlowLabel", "SoAdSocketDifferentiatedServicesField", "SoAdSocketConnection"]
    
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
        self.n_soad_sktcn = len(soad_cfgs)
        self.max_soad_sktcn = 65536
        self.n_soad_sktcn_str = tk.StringVar()

        # Create config string for AUTOSAR configs on this tab
        if soad_cfgs:
            for i, cfg in enumerate(soad_cfgs):
                self.configs.append(dappa.AsrCfgStr(self.cfgkeys, cfg))
            self.n_soad_sktcn = len(self.configs)


    def __del__(self):
        del self.configs[:]
        del self.n_soad_sktcn_str



    def create_empty_configs(self, index):
        gen_dict = {}

        gen_dict["SoAdPduHeaderEnable"]     = "FALSE"
        gen_dict["SoAdSocketPathMTUEnable"] = "FALSE"
        gen_dict["SoAdSocketAutomaticSoConSetup"]   = "FALSE"
        gen_dict["SoAdSocketIpAddrAssignmentChgNotification"]   = "FALSE"
        gen_dict["SoAdSocketLocalAddressRef"]   = "..."
        gen_dict["SoAdSocketLocalPort"]   = "0"                     # 0 - 65535 (16 bit)
        gen_dict["SoAdSocketSoConModeChgBswMNotification"]   = "FALSE"
        gen_dict["SoAdSocketSoConModeChgNotification"]   = "FALSE"
        gen_dict["SoAdSocketProtocol"]   = "FALSE"
        gen_dict["SoAdSocketTpRxBufferMin"]   = "0"                 # 0 - 65535
        gen_dict["SoAdSocketFramePriority"]   = "0"                 # 0 - 7 (3 bit)
        gen_dict["SoAdSocketMsgAcceptanceFilterEnabled"]   = "FALSE"
        gen_dict["SoAdSocketSoConModeChgNotifUpperLayerRef"]   = "..."
        gen_dict["SoAdSocketFlowLabel"]   = "0"                     # 0 - 1048575 (20 bit)
        gen_dict["SoAdSocketDifferentiatedServicesField"]   = "0"   # 0 - 63
        gen_dict["SoAdSocketConnection"]   = "FALSE"

        return gen_dict



    def draw_dappa_row(self, i):
        # add a new tab
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.insert("end", tab_frame, text ='SoAdGeneral')
        self.notebook.pack(expand = 1, fill ="both")
        self.tab_frames.append(tab_frame)
        self.header_orientation = None

        bool_cmbsel = ("FALSE", "TRUE")
        ref_cmbsel = ("Ref1", "Ref2", "...")

        # dappa.labelf(tab_frame, self, "R. Group #", 0,                          0, "e")
        dappa.combogf(tab_frame, self, "SoAdPduHeaderEnable", i,                    0, 0, 32, bool_cmbsel)
        dappa.combogf(tab_frame, self, "SoAdSocketPathMTUEnable", i,                1, 0, 32, bool_cmbsel)
        dappa.combogf(tab_frame, self, "SoAdSocketAutomaticSoConSetup", i,          2, 0, 32, bool_cmbsel)
        dappa.combogf(tab_frame, self, "SoAdSocketIpAddrAssignmentChgNotification", i, 3, 0, 32, bool_cmbsel)
        dappa.combogf(tab_frame, self, "SoAdSocketLocalAddressRef", i,              4, 0, 32, ref_cmbsel)
        dappa.entrygf(tab_frame, self, "SoAdSocketLocalPort", i,                    5, 0, 35, "normal")
        dappa.combogf(tab_frame, self, "SoAdSocketSoConModeChgBswMNotification", i, 6, 0, 32, bool_cmbsel)
        dappa.combogf(tab_frame, self, "SoAdSocketSoConModeChgNotification", i,     7, 0, 32, bool_cmbsel)
        dappa.combogf(tab_frame, self, "SoAdSocketProtocol", i,                       0, 3, 32, bool_cmbsel)
        dappa.entrygf(tab_frame, self, "SoAdSocketTpRxBufferMin", i,                  1, 3, 35, "normal")
        dappa.entrygf(tab_frame, self, "SoAdSocketFramePriority", i,                  2, 3, 35, "normal")
        dappa.combogf(tab_frame, self, "SoAdSocketMsgAcceptanceFilterEnabled", i,     3, 3, 32, bool_cmbsel)
        dappa.combogf(tab_frame, self, "SoAdSocketSoConModeChgNotifUpperLayerRef", i, 4, 3, 32, ref_cmbsel)
        dappa.entrygf(tab_frame, self, "SoAdSocketFlowLabel", i,                      5, 3, 35, "normal")
        dappa.entrygf(tab_frame, self, "SoAdSocketDifferentiatedServicesField", i,    6, 3, 35, "normal")
        dappa.combogf(tab_frame, self, "SoAdSocketConnection", i,                     7, 3, 32, bool_cmbsel)


    def delete_tab(self, i):
        # self.notebook.forget(self.notebook.select())
        self.notebook.forget(i)
        del self.tab_frames[i]



    def update(self):
        # get dappas to be added or removed
        self.n_soad_sktcn = int(self.n_soad_sktcn_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_soad_sktcn > n_dappa_rows:
            for i in range(self.n_soad_sktcn - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs(n_dappa_rows+i)))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_soad_sktcn:
            for i in range(n_dappa_rows - self.n_soad_sktcn):
                # dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                self.delete_tab((n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)

        # create a top frame for common widgets
        top_frame = ttk.Frame(self.scrollw.mnf)
        top_frame.grid(row=0, column=0, sticky="w")
        
        #Number of modes - Label + Spinbox
        label = tk.Label(top_frame, text="Sock Conns:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(top_frame, width=6, textvariable=self.n_soad_sktcn_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_soad_sktcn+1)))
        self.n_soad_sktcn_str.set(self.n_soad_sktcn)
        spinb.grid(row=0, column=1, sticky="w")

        # Save Button
        genm = tk.Button(top_frame, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=0, column=2)


        # draw tabbed view
        noteb_frame = ttk.Frame(self.scrollw.mnf)
        noteb_frame.grid(row=1, column=0, sticky="w")
        self.notebook = ttk.Notebook(noteb_frame)
        self.tab_frames = []
    
        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()


        self.update()



    def save_data(self):
        self.tab_struct.save_cb(self.gui, self.configs)
