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




class SpiSeqStr:
    spi_sequence_id = None
    interruptible_seq = None
    seq_end_notifictn = None
    spijob_assignment = None

    def __init__(self):
        self.spi_sequence_id = tk.StringVar()
        self.interruptible_seq = tk.StringVar()
        self.seq_end_notifictn = tk.StringVar()
        self.spijob_assignment = tk.StringVar()

    def __del__(self):
        del self.spi_sequence_id
        del self.interruptible_seq
        del self.seq_end_notifictn
        del self.spijob_assignment


class SpiSequenceTab:
    n_spi_seqs = 0
    max_spi_seqs = 65535
    n_spi_seqs_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    
    spi_seqs_str = []
    spi_seqs = []
    
    header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_size = 3
    non_header_objs = []

    def __init__(self, gui):
        self.gui = gui
        self.n_spi_seqs = 0
        self.n_spi_seqs_str = tk.StringVar()
        #spi_sequence = arxml_spi.parse_arxml(gui.arxml_file)
        spi_sequence = None
        if spi_sequence == None:
            return 
        for seq in spi_sequence:
            if "SpiSequenceId" in seq:
                self.init_spi_seq(seq)


    def __del__(self):
        del self.n_spi_seqs_str
        del self.spi_seqs_str[:]
        del self.spi_seqs[:]
        del self.non_header_objs[:]


    def init_spi_seq(self, seq):
        self.n_spi_seqs += 1
        
        # create new objects
        spi_seq = {}
        spi_seq_str = SpiSeqStr()
        
        # initialize objects
        spi_seq["SpiSequenceId"] = seq["SpiSequenceId"]
        spi_seq_str.spi_sequence_id.set(seq["SpiSequenceId"])
        spi_seq["SpiInterruptibleSequence"] = seq["SpiInterruptibleSequence"]
        spi_seq_str.interruptible_seq.set(seq["SpiInterruptibleSequence"])
        spi_seq["SpiSeqEndNotification"] = seq["SpiSeqEndNotification"]
        spi_seq_str.seq_end_notifictn.set(seq["SpiSeqEndNotification"])
        spi_seq["SpiJobAssignment"] = seq["SpiJobAssignment"]
        spi_seq_str.spijob_assignment.set(seq["SpiJobAssignment"])
        
        # add them to self for gui update
        self.spi_seqs_str.append(spi_seq_str)
        self.spi_seqs.append(spi_seq)


    def create_empty_spi_seq(self):
        spi_seq = {}
        spi_seq["SpiSequenceId"] = str(self.n_spi_seqs-1)
        spi_seq["SpiInterruptibleSequence"] = "FALSE"
        spi_seq["SpiSeqEndNotification"] = "e.g: SeqEndNotificationFunc"
        spi_seq["SpiJobAssignment"] = "SELECT"
        return spi_seq


    def update(self):
        # Backup current task entries from GUI
        self.backup_data()

        # destroy most old gui widgets
        self.n_spi_seqs = int(self.n_spi_seqs_str.get())
        for obj in self.non_header_objs:
            obj.destroy()

        # Tune memory allocations based on number of rows or boxes
        n_spi_seqs_str = len(self.spi_seqs_str)
        if self.n_spi_seqs > n_spi_seqs_str:
            for i in range(self.n_spi_seqs - n_spi_seqs_str):
                self.spi_seqs_str.insert(len(self.spi_seqs_str), SpiSeqStr())
                self.spi_seqs.insert(len(self.spi_seqs), self.create_empty_spi_seq())
        elif n_spi_seqs_str > self.n_spi_seqs:
            for i in range(n_spi_seqs_str - self.n_spi_seqs):
                del self.spi_seqs_str[-1]
                del self.spi_seqs[-1]

        # Draw new objects
        for i in range(0, self.n_spi_seqs):
            label = tk.Label(self.scrollw.mnf, text="Spi Sequence #")
            label.grid(row=self.header_size+i, column=0, sticky="e")
            self.non_header_objs.append(label)

            # SpiSequenceId
            entry = tk.Entry(self.scrollw.mnf, width=10, textvariable=self.spi_seqs_str[i].spi_sequence_id, state="readonly")
            self.spi_seqs_str[i].spi_sequence_id.set(self.spi_seqs[i]["SpiSequenceId"])
            entry.grid(row=self.header_size+i, column=1)
            self.non_header_objs.append(entry)

            # Spi Sequence - SpiInterruptibleSequence
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=15, textvariable=self.spi_seqs_str[i].interruptible_seq, state="readonly")
            cmbsel['values'] = ("FALSE", "TRUE")
            self.spi_seqs_str[i].interruptible_seq.set(self.spi_seqs[i]["SpiInterruptibleSequence"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=2)
            self.non_header_objs.append(cmbsel)
            
            # Spi Sequence - SpiSeqEndNotification
            entry = tk.Entry(self.scrollw.mnf, width=30, textvariable=self.spi_seqs_str[i].seq_end_notifictn)
            self.spi_seqs_str[i].seq_end_notifictn.set(self.spi_seqs[i]["SpiSeqEndNotification"])
            entry.grid(row=self.header_size+i, column=3)
            self.non_header_objs.append(entry)
            
            # Spi Sequence - SpiJobAssignment
            text = "Job [#]"
            select = tk.Button(self.scrollw.mnf, width=13, text=text, command=lambda id = i: self.select_spi_jobs(id))
            self.spi_seqs_str[i].spijob_assignment.set(self.spi_seqs[i]["SpiJobAssignment"])
            select.grid(row=self.header_size+i, column=4)
            self.non_header_objs.append(select)
            # text = "AppModes["+str(self.tasks_str[i].n_appmod)+"]"
            # select = tk.Button(self.scrollw.mnf, width=13, text=text, command=lambda id = i: self.select_autostart_modes(id))
            # select.grid(row=self.HeaderSize+i, column=5)
            
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

        # Table heading
        label = tk.Label(self.scrollw.mnf, text=" ")
        label.grid(row=2, column=0, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="SequenceID")
        label.grid(row=2, column=1, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="SpiInterruptibleSequence")
        label.grid(row=2, column=2, sticky="we")
        label = tk.Label(self.scrollw.mnf, text="SpiSeqEndNotification")
        label.grid(row=2, column=3, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="SpiJobAssignment")
        label.grid(row=2, column=4, sticky="w")

        self.update()


    def select_spi_jobs(self, id):
        print("select_spi_jobs() called with ",id, " as argument!")


    def backup_data(self):
        n_spi_seqs_str = len(self.spi_seqs_str)
        for i in range(n_spi_seqs_str):
            if len(self.spi_seqs_str[i].spi_sequence_id.get()):
                self.spi_seqs[i]["SpiSequenceId"] = self.spi_seqs_str[i].spi_sequence_id.get()
            if len(self.spi_seqs_str[i].interruptible_seq.get()):
                self.spi_seqs[i]["SpiInterruptibleSequence"] = self.spi_seqs_str[i].interruptible_seq.get()
            if len(self.spi_seqs_str[i].seq_end_notifictn.get()):
                self.spi_seqs[i]["SpiSeqEndNotification"] = self.spi_seqs_str[i].seq_end_notifictn.get()


    def save_data(self):
        self.backup_data()
        self.tab_struct.save_cb(self.gui)
