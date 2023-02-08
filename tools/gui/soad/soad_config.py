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

import gui.soad.soad_cfg_pdu_route as soad_pdur
import gui.soad.soad_cfg_rout_grp as soad_rout_grp


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
    n_soad_bswm_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SoAdPduRoute", "SoAdRoutingGroup",
               "SoAdSocketConnectionGroup", "SoAdSocketRoute"]
    
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

        if soad_cfgs:
            soadcfg = soad_cfgs["SoAdConfig"]
        else:
            soadcfg = None

        # Create config string for AUTOSAR configs on this tab
        if not soadcfg:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, soadcfg))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}
        
        gen_dict["SoAdPduRoute"]     = []
        gen_dict["SoAdRoutingGroup"] = []
        gen_dict["SoAdSocketConnectionGroup"]  = []
        gen_dict["SoAdSocketRoute"]  = []
        
        return gen_dict



    def draw_dappas(self):
        # insert column separator at 0
        dappa.colsep(self, 0)

        # column = 2; label at 1
        key = "SoAdPduRoute [" + str(len(self.configs[0].datavar["SoAdPduRoute"])) + "]"
        dappa.buttong(self, "SoAdPduRoute", 0, 0, 2, 40, key, self.soad_pduroute_select)

        key = "SoAdRoutingGroup [" + str(len(self.configs[0].datavar["SoAdRoutingGroup"])) + "]"
        dappa.buttong(self, "SoAdRoutingGroup", 0, 1, 2, 40, key, self.soad_routing_grp_select)

        key = "SoAdSocketConnectionGroup [" + str(len(self.configs[0].datavar["SoAdSocketConnectionGroup"])) + "]"
        dappa.buttong(self, "SoAdSocketConnectionGroup", 0, 2, 2, 40, key, self.soad_pduroute_select)

        key = "SoAdSocketRoute [" + str(len(self.configs[0].datavar["SoAdSocketRoute"])) + "]"
        dappa.buttong(self, "SoAdSocketRoute", 0, 3, 2, 40, key, self.soad_pduroute_select)

        # insert column separator at 3
        dappa.colsep(self, 3)

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


    def on_soad_pduroute_close(self):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["SoAdPduRoute"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["SoAdPduRoute"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappas(self)
        self.draw_dappas()


    def soad_pduroute_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_soad_pduroute_close())
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 820
        height = 540
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/4, y/5))
        self.active_dialog.title("SoAdPduRoute")

        # create views and draw
        gen_view = SoAdChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = soad_pdur.SoAdPduRouteView(self.gui,
                                            self.configs[0].datavar["SoAdPduRoute"])
        gen_view.name = "SoAdPduRoute"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)


    def on_soad_routing_grp_close(self):
        # backup data
        if self.active_view.view.configs:
            self.configs[0].datavar["SoAdRoutingGroup"] = []  # ignore old data
            for cfg in self.active_view.view.configs:
                self.configs[0].datavar["SoAdRoutingGroup"].append(cfg.get())

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappas(self)
        self.draw_dappas()


    def soad_routing_grp_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_soad_routing_grp_close())
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 630
        height = 540
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/4, y/5))
        self.active_dialog.title("SoAdRoutingGroup")

        # create views and draw
        gen_view = SoAdChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = soad_rout_grp.SoAdRoutingGroupView(self.gui,
                                            self.configs[0].datavar["SoAdRoutingGroup"])
        gen_view.name = "SoAdRoutingGroup"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)
