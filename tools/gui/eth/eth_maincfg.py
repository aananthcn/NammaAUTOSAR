#
# Created on Fri Dec 09 2022 5:55:53 AM
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

import gui.eth.eth_gen as eth_gen
import gui.eth.eth_offload as eth_offload
import gui.eth.eth_ctrlcfg as eth_ctrlcfg
import gui.eth.eth_xgress as eth_xgress
import gui.eth.eth_sch as eth_sch
import gui.eth.eth_shaper as eth_shaper
import gui.eth.eth_spicfg as eth_spicfg

import arxml.spi.arxml_spi_parse as arxml_spi_r


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



class EthernetConfigMainView:
    n_eth_dev = 0
    max_eth_dev = 255
    n_eth_dev_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["EthIndex", "EthGeneral", "EthCtrlOffloading", "EthCtrlConfig",
               "EthCtrlConfigXgressFifo", "EthCtrlConfigScheduler",
               "EthCtrlConfigShaper", "EthCtrlConfigSpiConfiguration"]
    
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False
    
    active_dialog = None
    active_view = None
    save_cb = None
    


    def __init__(self, gui, eth_cfgs, save_cb):
        self.gui = gui
        self.configs = []
        self.n_eth_dev = 0
        self.n_eth_dev_str = tk.StringVar()
        self.save_cb = save_cb

        # read configs from ARXML
        self.n_eth_dev = len(eth_cfgs)
        self.n_eth_dev_str.set(len(eth_cfgs))

        # initialize configurations from ARXML file
        for i, cfg in enumerate(eth_cfgs):
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, cfg))
            self.configs[i].datavar["EthGeneral"] = cfg["EthGeneral"]
            self.configs[i].datavar["EthCtrlConfig"] = cfg["EthCtrlConfig"]
            self.configs[i].datavar["EthCtrlConfigXgressFifo"] = cfg["EthCtrlConfigXgressFifo"]
            self.configs[i].datavar["EthCtrlConfigScheduler"] = cfg["EthCtrlConfigScheduler"]
            self.configs[i].datavar["EthCtrlConfigShaper"] = cfg["EthCtrlConfigShaper"]
            self.configs[i].datavar["EthCtrlConfigSpiConfiguration"] = cfg["EthCtrlConfigSpiConfiguration"]


    def __del__(self):
        del self.n_eth_dev_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self, index):
        eth_dev = {}

        # child view configs
        eth_dev["EthIndex"] = str(self.n_eth_dev-1)
        eth_dev["EthGeneral"] = eth_gen.EthGeneralChildView(self.gui, 0, None).create_empty_configs(index)
        eth_dev["EthCtrlOffloading"] = eth_offload.EthChecksumOffloadChildView(self.gui, 0, None).create_empty_configs()
        eth_dev["EthCtrlConfig"] = eth_ctrlcfg.EthCtrlConfigChildView(self.gui, 0, None).create_empty_configs(index)
        eth_dev["EthCtrlConfigXgressFifo"] = eth_xgress.EthConfigXgressFifoChildView(self.gui, 0, None).create_empty_configs(index)
        eth_dev["EthCtrlConfigScheduler"] = eth_sch.EthConfigSchedulerChildView(self.gui, 0, None).create_empty_configs()
        eth_dev["EthCtrlConfigShaper"] = eth_shaper.EthConfigShaperChildView(self.gui, 0, None).create_empty_configs()
        eth_dev["EthCtrlConfigSpiConfiguration"] = eth_spicfg.EthConfigSpiConfigChildView(self.gui, 0, None, None).create_empty_configs()

        return eth_dev



    def draw_dappa_row(self, i):
        dappa.label(self, "Eth Dev. #", self.header_row+i, 0, "e")
        dappa.entry(self, "EthIndex", i, self.header_row+i, 1, 8, "readonly")
        
        text = "General["+str(i)+"]"
        cb = lambda id = i : self.eth_general_select(id)
        dappa.button(self, "EthGeneral", i, self.header_row+i, 2, 10, text, cb)

        text = "EthCtrlOffloading["+str(i)+"]"
        cb = lambda id = i : self.eth_ctrl_offloading_select(id)
        dappa.button(self, "EthCtrlOffloading", i, self.header_row+i, 3, 18, text, cb)

        text = "EthCtrlConfig["+str(i)+"]"
        cb = lambda id = i : self.eth_ctrl_config_select(id)
        dappa.button(self, "EthCtrlConfig", i, self.header_row+i, 4, 15, text, cb)

        text = "EthCtrlConfigXgressFifo["+str(i)+"]"
        cb = lambda id = i : self.eth_config_xgress_fifo_select(id)
        dappa.button(self, "EthCtrlConfigXgressFifo", i, self.header_row+i, 5, 22, text, cb)

        text = "EthCtrlConfigScheduler["+str(i)+"]"
        cb = lambda id = i : self.eth_config_scheduler_select(id)
        dappa.button(self, "EthCtrlConfigScheduler", i, self.header_row+i, 6, 22, text, cb)

        text = "EthCtrlConfigShaper["+str(i)+"]"
        cb = lambda id = i : self.eth_config_shaper_select(id)
        dappa.button(self, "EthCtrlConfigShaper", i, self.header_row+i, 7, 20, text, cb)

        # Spi configuration is valid only if EthCtrlConfig->EthCtrlEnableSpiInterface is TRUE
        ecc_cfg = self.configs[i].datavar["EthCtrlConfig"]
        if ecc_cfg and "TRUE" in ecc_cfg["EthCtrlEnableSpiInterface"]:
            text = "EthCtrlConfigSpiConfiguration["+str(i)+"]"
            cb = lambda id = i : self.eth_config_spicfg_select(id)
        else:
            text = "SPI disabled in EthCtrlConfig"
            cb = lambda id = i : self.do_nothing(id)
        dappa.button(self, "EthCtrlConfigSpiConfiguration", i, self.header_row+i, 8, 27, text, cb)



    def update(self):
        # get dappas to be added or removed
        self.n_eth_dev = int(self.n_eth_dev_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_eth_dev > n_dappa_rows:
            for i in range(self.n_eth_dev - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs(n_dappa_rows+i)))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_eth_dev:
            for i in range(n_dappa_rows - self.n_eth_dev):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Update EthMaxCtrlsSupported for EthGeneral
        for config in self.configs:
            config.datavar["EthGeneral"]["EthMaxCtrlsSupported"] = str(self.n_eth_dev)

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="Eth Controllers:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=6, textvariable=self.n_eth_dev_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_eth_dev+1)))
        self.n_eth_dev_str.set(self.n_eth_dev)
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



    def on_eth_general_select_close(self, row):
        # backup data
        self.configs[row].datavar["EthGeneral"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def eth_general_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_eth_general_select_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 350
        height = 240
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/10, y/5))
        self.active_dialog.title("EthGeneral")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = eth_gen.EthGeneralChildView(self.gui, row, self.configs[row].datavar["EthGeneral"] )
        gen_view.name = "EthGeneral"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)


    def do_nothing(self, row):
        return


    def on_eth_ctrl_offloading_select_close(self, row):
        # backup data
        self.configs[row].datavar["EthCtrlOffloading"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def eth_ctrl_offloading_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_eth_ctrl_offloading_select_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 370
        height = 110
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/8, y/5))
        self.active_dialog.title("EthCtrlOffloading")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = eth_offload.EthChecksumOffloadChildView(self.gui, row, self.configs[row].datavar["EthCtrlOffloading"] )
        gen_view.name = "EthCtrlOffloading"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)



    def on_eth_ctrl_config_select_close(self, row):
        # backup data
        self.configs[row].datavar["EthCtrlConfig"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def eth_ctrl_config_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_eth_ctrl_config_select_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 400
        height = 260
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/4, y/5))
        self.active_dialog.title("EthCtrlConfig")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = eth_ctrlcfg.EthCtrlConfigChildView(self.gui, row, self.configs[row].datavar["EthCtrlConfig"] )
        gen_view.name = "EthCtrlConfig"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)



    def on_eth_config_xgress_fifo_select_close(self, row):
        # backup data
        self.configs[row].datavar["EthCtrlConfigXgressFifo"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def eth_config_xgress_fifo_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_eth_config_xgress_fifo_select_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 400
        height = 190
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/4, y/5))
        self.active_dialog.title("EthCtrlConfigXgressFifo")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = eth_xgress.EthConfigXgressFifoChildView(self.gui, row, self.configs[row].datavar["EthCtrlConfigXgressFifo"] )
        gen_view.name = "EthCtrlConfigXgressFifo"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)



    def on_eth_config_scheduler_close(self, row):
        # backup data
        self.configs[row].datavar["EthCtrlConfigScheduler"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def eth_config_scheduler_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_eth_config_scheduler_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 370
        height = 40
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, 2*x/5, y/5))
        self.active_dialog.title("EthCtrlConfigScheduler")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = eth_sch.EthConfigSchedulerChildView(self.gui, row, self.configs[row].datavar["EthCtrlConfigScheduler"] )
        gen_view.name = "EthCtrlConfigScheduler"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)



    def on_eth_config_shaper_close(self, row):
        # backup data
        self.configs[row].datavar["EthCtrlConfigShaper"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def eth_config_shaper_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_eth_config_shaper_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 330
        height = 80
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/2, y/5))
        self.active_dialog.title("EthCtrlConfigShaper")

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = eth_shaper.EthConfigShaperChildView(self.gui, row, self.configs[row].datavar["EthCtrlConfigShaper"] )
        gen_view.name = "EthCtrlConfigShaper"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)



    def on_eth_config_spicfg_close(self, row):
        # backup data
        self.configs[row].datavar["EthCtrlConfigSpiConfiguration"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def eth_config_spicfg_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_eth_config_spicfg_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 490
        height = 315
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/2, y/5))
        self.active_dialog.title("EthCtrlConfigSpiConfiguration")

        # parse ARXML for SPI sequence
        spi_configs = arxml_spi_r.parse_arxml(self.gui.arxml_file)

        # create views and draw
        gen_view = EthChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = eth_spicfg.EthConfigSpiConfigChildView(self.gui, row, spi_configs["SpiSequence"],
                            self.configs[row].datavar["EthCtrlConfigSpiConfiguration"] )
        gen_view.name = "EthCtrlConfigSpiConfiguration"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)
