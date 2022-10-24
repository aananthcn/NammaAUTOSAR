#
# Created on Wed Oct 20 2022 9:51:55 PM
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

import gui.spi.spi_chan_list as spi_chlist
import gui.spi.spi_view as spi_view




class SpiJobTab:
    n_spi_job = 0
    max_spi_job = 255
    n_spi_job_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SpiJobId", "SpiJobPriority", "SpiJobEndNotification", "SpiDeviceAssignment", "SpiChannelList"]
    
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False

    active_dialog = None
    active_widget = None


    def __init__(self, gui, spidrvtab, spidevtab, spichtab, ar_cfg):
        self.gui = gui
        self.configs = []
        self.n_spi_job = 0
        self.n_spi_job_str = tk.StringVar()
        self.spidrvtab = spidrvtab
        self.spichtab = spichtab
        self.spidev_lst = []

        if ar_cfg["SpiJob"] == None:
            return
        for job in ar_cfg["SpiJob"]:
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, job))
            self.n_spi_job += 1
        self.n_spi_job_str.set(self.n_spi_job)


    def __del__(self):
        del self.n_spi_job_str
        del self.non_header_objs[:]
        del self.configs[:]
        del self.spidev_lst[:]



    def create_empty_configs(self):
        spi_seq = {}
        spi_seq["SpiJobId"] = str(self.n_spi_job-1)
        spi_seq["SpiJobPriority"] = "0"
        spi_seq["SpiJobEndNotification"] = "e.g: JobEndNotificationFunc"
        spi_seq["SpiDeviceAssignment"] = ""
        spi_seq["SpiChannelList"] = []
        return spi_seq



    def draw_dappa_row(self, i):
        dappa.label(self, "Spi Job #", self.header_row+i, 0, "e")
        dappa.entry(self, "SpiJobId", i, self.header_row+i, 1, 10, "readonly")
        dappa.entry(self, "SpiJobPriority", i, self.header_row+i, 2, 15, "normal")
        dappa.entry(self, "SpiJobEndNotification", i, self.header_row+i, 3, 30, "normal")
        dappa.combo(self, "SpiDeviceAssignment", i, self.header_row+i, 4, 13, self.spidev_lst)
        cb = lambda id = i : self.channel_list_select(id)
        text = "SpiChannelList["+str(len(self.configs[i].datavar["SpiChannelList"]))+"]"
        dappa.button(self, "SpiChannelList", i, self.header_row+i, 5, 20, text, cb)
        # Channel list changed hence ask SpiDriver to redraw
        self.spidrvtab.tab.spi_job_list_changed(self.configs)


    def update(self):
        # get dappas to be added or removed
        self.n_spi_job = int(self.n_spi_job_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_spi_job > n_dappa_rows:
            for i in range(self.n_spi_job - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_spi_job:
            for i in range(n_dappa_rows - self.n_spi_job):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Spi Jobs:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_spi_job_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_spi_job+1)))
        self.n_spi_job_str.set(self.n_spi_job)
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
        self.tab_struct.save_cb(self.gui)



    def spi_extdrv_list_changed(self, exd_configs):
        del self.spidev_lst[:]
        for cfg in exd_configs:
            self.spidev_lst.append(cfg.datavar["SpiHwUnit"])
            
        if not self.init_view_done:
            return

        # channel list changed, hence re-draw this view completely
        for obj in self.non_header_objs:
            obj.destroy()
            del obj

        # redraw all dappas
        n_dappa_rows = len(self.configs)
        for i in range(n_dappa_rows):
            self.draw_dappa_row(i)



    def channel_list_select_close(self, row):
        # remove old selections
        if self.configs[row].datavar["SpiChannelList"]:
            del self.configs[row].datavar["SpiChannelList"][:]


        # update new selections from last window session
        for chlist_cfg in self.active_widget.configs:
            chlist_cfg.get() # pull from UI
            ch_dict = {}
            ch_dict['SpiChannelIndex'] = chlist_cfg.datavar['SpiChannelIndex']
            ch_dict['SpiChannelAssignment'] = chlist_cfg.datavar['SpiChannelAssignment']
            self.configs[row].datavar["SpiChannelList"].append(ch_dict)
        
        # dialog elements are no longer needed, destroy them. Else, new dialogs will not open!
        del self.active_widget
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)



    def channel_list_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        xsize = 400
        ysize = 400
        self.active_dialog = tk.Toplevel(width=xsize, height=ysize) # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.channel_list_select_close(row))
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        self.active_dialog.geometry("+%d+%d" % (0 + x/3, y/12))
        
        # prepare channel list and device list
        spi_chids = []
        for cfg in self.spichtab.tab.configs:
            spi_chids.append(cfg.datavar["SpiChannelId"])

        # show channel list dialog box to select channels
        spichnlsttab = spi_view.SpiTab(self.active_dialog, xsize, ysize)
        chan_list = self.configs[row].datavar["SpiChannelList"]
        for chan in chan_list:
            chan["SpiChannelAssignment"] = row
        self.active_widget = spi_chlist.SpiChannelListTab(self.gui, spi_chids, chan_list)
        spichnlsttab.tab = self.active_widget
        spichnlsttab.name = "SpiChannelList"
        spichnlsttab.tab.draw(spichnlsttab, row)

