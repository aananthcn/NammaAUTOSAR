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
    cfgkeys = ["SpiSequenceId", "SpiSequenceName","SpiInterruptibleSequence", "SpiSeqEndNotification", "SpiJobAssignment"]
    
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False

    active_dialog = None
    active_widget = None


    def __init__(self, gui, spidrvtab, spijobtab, ar_cfg):
        self.gui = gui
        self.configs = []
        self.n_spi_seqs = 0
        self.n_spi_seqs_str = tk.StringVar()
        self.spidrvtab = spidrvtab
        self.spijobtab = spijobtab

        if ar_cfg["SpiSequence"] == None:
            return
        for seq in ar_cfg["SpiSequence"]:
            # let us do some correction between how UI and ARXML stores job assignment
            job_list = seq["SpiJobAssignment"]
            seq["SpiJobAssignment"] = []
            for job in job_list:
                seq["SpiJobAssignment"].append(job['SpiJob'])
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, seq))
            self.n_spi_seqs += 1
        self.n_spi_seqs_str.set(self.n_spi_seqs)



    def __del__(self):
        del self.n_spi_seqs_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        spi_seq = {}
        spi_seq["SpiSequenceId"] = str(self.n_spi_seqs-1)
        spi_seq["SpiSequenceName"] = "SEQ_NAME_"+str(self.n_spi_seqs-1)
        spi_seq["SpiInterruptibleSequence"] = "FALSE"
        spi_seq["SpiSeqEndNotification"] = "e.g: SeqEndNotificationFunc"
        spi_seq["SpiJobAssignment"] = []
        return spi_seq



    def draw_dappa_row(self, i):
        dappa.label(self, "Spi Sequence #", self.header_row+i, 0, "e")

        # SpiSequenceId
        dappa.entry(self, "SpiSequenceId", i, self.header_row+i, 1, 10, "readonly")
        dappa.entry(self, "SpiSequenceName", i, self.header_row+i, 2, 30, "normal")

        # Spi Sequence - SpiInterruptibleSequence
        dappa.combo(self, "SpiInterruptibleSequence", i, self.header_row+i, 3, 15, ("FALSE", "TRUE"))
        
        # Spi Sequence - SpiSeqEndNotification
        dappa.entry(self, "SpiSeqEndNotification", i, self.header_row+i, 4, 30, "normal")
        
        # Spi Sequence - SpiJobAssignment
        cb = lambda id = i : self.select_spi_jobs(id)
        text = "SpiJobAssignment["+str(len(self.configs[i].datavar["SpiJobAssignment"]))+"]"
        dappa.button(self, "SpiJobAssignment", i, self.header_row+i, 5, 20, text, cb)



    def update(self):
        # get dappas to be added or removed
        self.n_spi_seqs = int(self.n_spi_seqs_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_spi_seqs > n_dappa_rows:
            for i in range(self.n_spi_seqs - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_spi_seqs:
            for i in range(n_dappa_rows - self.n_spi_seqs):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Sequence list changed hence ask SpiDriver to redraw
        self.spidrvtab.tab.spi_seq_list_changed(self.configs)

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



    def on_select_spi_jobs_close(self, row):
        # remove old selections
        if self.configs[row].datavar["SpiJobAssignment"]:
            del self.configs[row].datavar["SpiJobAssignment"][:]

        # update new selections
        if len(self.active_widget.curselection()):
            for i in self.active_widget.curselection():
                if not self.configs[row].datavar["SpiJobAssignment"]:
                    self.configs[row].datavar["SpiJobAssignment"] = []
                self.configs[row].datavar["SpiJobAssignment"].append(self.active_widget.get(i).split()[-1])

        # dialog elements are no longer needed, destroy them. Else, new dialogs will not open!
        self.active_widget.destroy()
        del self.active_widget
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def select_spi_jobs(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_select_spi_jobs_close(row))
        self.active_dialog.attributes('-topmost',True)
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        self.active_dialog.geometry("+%d+%d" % (0 + x/2, y/16))

        # show all SpiJobs
        self.active_widget = tk.Listbox(self.active_dialog, selectmode=tk.MULTIPLE, width=40, height=15)
        for i, j_cfg in enumerate(self.spijobtab.tab.configs):
            job = j_cfg.datavar["SpiJobId"]
            job_str = "SpiJob: "+str(job)
            self.active_widget.insert(i, job_str)
            if row < len(self.configs) and self.configs[row].datavar["SpiJobAssignment"]:
                if job in self.configs[row].datavar["SpiJobAssignment"]:
                    self.active_widget.selection_set(i)
        self.active_widget.pack()



    def save_data(self):
        self.tab_struct.save_cb(self.gui)
