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




class SpiJobTab:
    n_spi_job = 0
    max_spi_job = 255
    n_spi_job_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SpiJobId", "SpiJobPriority", "SpiJobEndNotification", "SpiDeviceAssignment"]
    
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels


    def __init__(self, gui):
        self.gui = gui
        self.configs = []
        self.n_spi_job = 0
        self.n_spi_job_str = tk.StringVar()

        #spi_sequence = arxml_spi.parse_arxml(gui.arxml_file)
        spi_sequence = None
        if spi_sequence == None:
            return 


    def __del__(self):
        del self.n_spi_job_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        spi_seq = {}
        spi_seq["SpiJobId"] = str(self.n_spi_job-1)
        spi_seq["SpiJobPriority"] = "0"
        spi_seq["SpiJobEndNotification"] = "e.g: JobEndNotificationFunc"
        spi_seq["SpiDeviceAssignment"] = ""
        return spi_seq



    def draw_dappa_row(self, i):
        dappa.label(self, "Spi Job #", self.header_row+i, 0, "e")
        dappa.entry(self, "SpiJobId", i, self.header_row+i, 1, 10, "readonly")
        dappa.entry(self, "SpiJobPriority", i, self.header_row+i, 2, 15, "normal")
        dappa.entry(self, "SpiJobEndNotification", i, self.header_row+i, 3, 30, "normal")
        dappa.combo(self, "SpiDeviceAssignment", i, self.header_row+i, 4, 13, ("Dev1", "Dev1", "Dev2"))



    def update(self):
        # get dappas to be added or removed
        self.n_spi_job = int(self.n_spi_job_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if self.n_spi_job > n_dappa_rows:
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
        label = tk.Label(self.scrollw.mnf, text="No. of Spi Sequence:")
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
