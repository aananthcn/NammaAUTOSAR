#
# Created on Wed Oct 05 2022 9:51:55 PM
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




class SpiSequenceTab:
    n_spi_seqs = 0
    max_spi_seqs = 255
    n_spi_seqs_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SpiSequenceId", "SpiInterruptibleSequence", "SpiSeqEndNotification", "SpiJobAssignment"]
    
    n_header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels


    def __init__(self, gui):
        self.gui = gui
        self.configs = []
        self.n_spi_seqs = 0
        self.n_spi_seqs_str = tk.StringVar()

        #spi_sequence = arxml_spi.parse_arxml(gui.arxml_file)
        spi_sequence = None
        if spi_sequence == None:
            return 


    def __del__(self):
        del self.n_spi_seqs_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        spi_seq = {}
        spi_seq["SpiSequenceId"] = str(self.n_spi_seqs-1)
        spi_seq["SpiInterruptibleSequence"] = "FALSE"
        spi_seq["SpiSeqEndNotification"] = "e.g: SeqEndNotificationFunc"
        spi_seq["SpiJobAssignment"] = "SELECT"
        return spi_seq



    def draw_dappa_row(self, i):
        dappa.label(self, "Spi Sequence #", self.header_row+i, 0, "e")

        # SpiSequenceId
        dappa.entry(self, "SpiSequenceId", i, self.header_row+i, 1, 10, "readonly")

        # Spi Sequence - SpiInterruptibleSequence
        dappa.combo(self, "SpiInterruptibleSequence", i, self.header_row+i, 2, 15, ("FALSE", "TRUE"))
        
        # Spi Sequence - SpiSeqEndNotification
        dappa.entry(self, "SpiSeqEndNotification", i, self.header_row+i, 3, 30, "normal")
        
        # Spi Sequence - SpiJobAssignment
        dappa.button(self, "SpiJobAssignment", i, self.header_row+i, 4, 13, "Job [#]", self.select_spi_jobs)



    def update(self):
        # get dappas to be added or removed
        self.n_spi_seqs = int(self.n_spi_seqs_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if self.n_spi_seqs > n_dappa_rows:
            for i in range(self.n_spi_seqs - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_spi_seqs:
            for i in range(n_dappa_rows - self.n_spi_seqs):
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
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_spi_seqs_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_spi_seqs+1)))
        self.n_spi_seqs_str.set(self.n_spi_seqs)
        spinb.grid(row=0, column=1, sticky="w")

        # Save Button
        genm = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=0, column=2)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()


    def select_spi_jobs(self, id):
        print("select_spi_jobs() called with ",id, " as argument!")


    def save_data(self):
        self.tab_struct.save_cb(self.gui)
