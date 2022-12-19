#
# Created on Mon Dec 19 2022 7:21:01 AM
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

import gui.lin.lin_gen as lin_gen
import gui.lin.lin_chancfg as lin_chancfg

# import arxml.spi.arxml_spi_parse as arxml_spi_r


class LinChildView:
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



class LinConfigMainView:
    n_lin_dev = 0
    max_lin_dev = 255
    n_lin_dev_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["LinIndex", "LinGeneral", "LinGlobalConfig"]
    
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False
    
    active_dialog = None
    active_view = None
    save_cb = None
    


    def __init__(self, gui, lin_cfgs, save_cb):
        self.gui = gui
        self.configs = []
        self.n_lin_dev = 0
        self.n_lin_dev_str = tk.StringVar()
        self.save_cb = save_cb

        # read configs from ARXML
        if not lin_cfgs:
            return
        self.n_lin_dev = len(lin_cfgs)
        self.n_lin_dev_str.set(len(lin_cfgs))

        # initialize configurations from ARXML file
        for i, cfg in enumerate(lin_cfgs):
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, cfg))
            self.configs[i].datavar["LinGeneral"] = cfg["LinGeneral"]
            self.configs[i].datavar["LinChannel"] = cfg["LinChannel"]


    def __del__(self):
        del self.n_lin_dev_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        lin_dev = {}

        # child view configs
        lin_dev["LinIndex"] = str(self.n_lin_dev-1)
        lin_dev["LinGeneral"] = []
        lin_dev["LinGlobalConfig"] = []

        return lin_dev



    def draw_dappa_row(self, i):
        dappa.label(self, "Lin Dev. #", self.header_row+i, 0, "e")
        dappa.entry(self, "LinIndex", i, self.header_row+i, 1, 8, "readonly")
        
        text = "LinGeneral["+str(i)+"]"
        cb = lambda id = i : self.lin_general_select(id)
        dappa.button(self, "LinGeneral", i, self.header_row+i, 2, 15, text, cb)

        text = "LinGlobalConfig["+str(i)+"]"
        cb = lambda id = i : self.lin_chan_config_select(id)
        dappa.button(self, "LinGlobalConfig", i, self.header_row+i, 3, 20, text, cb)



    def update(self):
        # get dappas to be added or removed
        self.n_lin_dev = int(self.n_lin_dev_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_lin_dev > n_dappa_rows:
            for i in range(self.n_lin_dev - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_lin_dev:
            for i in range(n_dappa_rows - self.n_lin_dev):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="Lin Controllers:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=6, textvariable=self.n_lin_dev_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_lin_dev+1)))
        self.n_lin_dev_str.set(self.n_lin_dev)
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



    def on_lin_general_select_close(self, row):
        # backup data
        self.configs[row].datavar["LinGeneral"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def lin_general_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_lin_general_select_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 280
        height = 110
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/3, y/5))

        # create views and draw
        gen_view = LinChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = lin_gen.LinGeneralChildView(self.gui, row, self.configs[row].datavar["LinGeneral"] )
        gen_view.name = "LinGeneral"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)



    def on_lin_chan_config_select_close(self, row):
        # backup data
        self.configs[row].datavar["LinGlobalConfig"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def lin_chan_config_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_lin_chan_config_select_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 400
        height = 145
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/2, y/5))

        # create views and draw
        gen_view = LinChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = lin_chancfg.LinChannelConfigChildView(self.gui, row, self.configs[row].datavar["LinGlobalConfig"] )
        gen_view.name = "LinGlobalConfig"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)
