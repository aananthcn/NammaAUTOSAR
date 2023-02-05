#
# Created on Sat Feb 04 2023 6:35:52 PM
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
#         + SoAdRoutingGroup (0..*)
#             + SoAdRoutingGroupId
#             + SoAdRoutingGroupIsEnabledAtInit
#             + SoAdRoutingGroupTxTriggerable
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
#                 + SoAdSocketUdp
#                     + SoAdSocketUdpListenOnly
#                     + SoAdSocketUdpAliveSupervisionTimeout
#                     + SoAdSocketnPduUdpTxBufferMin
#                     + SoAdSocketUdpTriggerTimeout
#                     + SoAdSocketUdpStrictHeaderLenCheckEnabled
#                     + SoAdSocketUdpChecksumEnabled
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
#             + SoAdSocketTpRxBufferMin
#             + SoAdSocketFramePriority
#             + SoAdSocketMsgAcceptanceFilterEnabled
#             + SoAdSocketSoConModeChgNotifUpperLayerRef --> SoAdBswModules 
#             + SoAdSocketFlowLabel
#             + SoAdSocketDifferentiatedServicesField
#             + SoAdSocketConnection
#                 + SoAdSocketId
#                 + SoAdSocketRemoteAddress
#                     + SoAdSocketRemoteIpAddress
#                     + SoAdSocketRemotePort
#         + SoAdSocketRoute (0..*)
#             + SoAdRxPduHeaderId
#             + SoAdRxSocketConnOrSocketConnBundleRef --> [SoAdSocketConnection, SoAdSocketConnectionGroup]
#             + SoAdSocketRouteDest
#                 + SoAdRxPduRef --> Pdu
#                 + SoAdRxUpperLayerType [IF / TP]
#                 + SoAdRxPduId
#                 + SoAdRxRoutingGroupRef --> SoAdRoutingGroup




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



class SoAdConfigView:
    n_soad_bswm = 0
    max_soad_bswm = 255
    n_soad_bswm_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SoAdIf", "SoAdIfTriggerTransmit", "SoAdIfTxConfirmation",
               "SoAdLocalIpAddrAssigmentChg", "SoAdSoConModeChg", "SoAdTp",
               "SoAdUseCallerInfix", "SoAdUseTypeInfix", "SoAdBswModuleRef"]
    
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
        self.n_soad_bswm = 0
        self.n_soad_bswm_str = tk.StringVar()
        # self.save_cb = save_cb

        if soad_cfgs:
            soad_bswm = soad_cfgs["SoAdBswModules"]
        else:
            return

        # read configs from ARXML
        self.n_soad_bswm = len(soad_bswm)
        self.n_soad_bswm_str.set(len(soad_bswm))

        # initialize configurations from ARXML file
        for i, cfg in enumerate(soad_bswm):
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, cfg))


    def __del__(self):
        del self.n_soad_bswm_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        soad_dict = {}

        # child view configs
        soad_dict["SoAdIf"]                  = "FALSE"
        soad_dict["SoAdIfTriggerTransmit"]   = "FALSE"
        soad_dict["SoAdIfTxConfirmation"]    = "FALSE"
        soad_dict["SoAdLocalIpAddrAssigmentChg"] = "FALSE"
        soad_dict["SoAdSoConModeChg"]        = "FALSE"
        soad_dict["SoAdTp"]                  = "FALSE"
        soad_dict["SoAdUseCallerInfix"]      = "FALSE"
        soad_dict["SoAdUseTypeInfix"]        = "FALSE"
        soad_dict["SoAdBswModuleRef"]        = "..."

        return soad_dict



    def draw_dappa_row(self, i):
        bool_cmbsel = ("FALSE", "TRUE")
        ref_cmbsel = ("Ref1", "Ref2", "...")

        dappa.label(self, "Mod. #", self.header_row+i,                      0, "e")
        dappa.combo(self, "SoAdIf", i, self.header_row+i,                   1, 6, bool_cmbsel)
        dappa.combo(self, "SoAdIfTriggerTransmit", i, self.header_row+i,    2, 18, bool_cmbsel)
        dappa.combo(self, "SoAdIfTxConfirmation", i, self.header_row+i,     3, 18, bool_cmbsel)
        dappa.combo(self, "SoAdLocalIpAddrAssigmentChg", i, self.header_row+i, 4, 27, bool_cmbsel)
        dappa.combo(self, "SoAdSoConModeChg", i, self.header_row+i,         5, 18, bool_cmbsel)
        dappa.combo(self, "SoAdTp", i, self.header_row+i,                   6, 6, bool_cmbsel)
        dappa.combo(self, "SoAdUseCallerInfix", i, self.header_row+i,       7, 15, bool_cmbsel)
        dappa.combo(self, "SoAdUseTypeInfix", i, self.header_row+i,         8, 15, bool_cmbsel)
        dappa.combo(self, "SoAdBswModuleRef", i, self.header_row+i,         9, 15, ref_cmbsel)


    def update(self):
        # get dappas to be added or removed
        self.n_soad_bswm = int(self.n_soad_bswm_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_soad_bswm > n_dappa_rows:
            for i in range(self.n_soad_bswm - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_soad_bswm:
            for i in range(n_dappa_rows - self.n_soad_bswm):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="BSW Modules:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=6, textvariable=self.n_soad_bswm_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_soad_bswm+1)))
        self.n_soad_bswm_str.set(self.n_soad_bswm)
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
