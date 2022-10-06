#
# Created on Thu Oct 06 2022 6:53:58 AM
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




class SpiChanStr:
    spi_channel_id = None
    spi_chann_type = None
    spi_chan_width = None
    spi_deflt_data = None
    spi_eb_max_len = None
    spi_ib_n_buffs = None
    spi_tran_start = None

    def __init__(self):
        self.spi_channel_id = tk.StringVar()
        self.spi_chann_type = tk.StringVar()
        self.spi_chan_width = tk.StringVar()
        self.spi_deflt_data = tk.StringVar()
        self.spi_eb_max_len = tk.StringVar()
        self.spi_ib_n_buffs = tk.StringVar()
        self.spi_tran_start = tk.StringVar()

    def __del__(self):
        del self.spi_channel_id
        del self.spi_chann_type
        del self.spi_chan_width
        del self.spi_deflt_data
        del self.spi_eb_max_len
        del self.spi_ib_n_buffs
        del self.spi_tran_start


class SpiChannelTab:
    n_spi_chans = 0
    max_spi_chans = 255
    n_spi_chans_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    
    spi_chans_str = []
    spi_chans = []
    
    header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_size = 3
    non_header_objs = []

    def __init__(self, gui):
        self.gui = gui
        self.n_spi_chans = 0
        self.n_spi_chans_str = tk.StringVar()
        #spi_channel = arxml_spi.parse_arxml(gui.arxml_file)
        spi_channel = None
        if spi_channel == None:
            return 
        for chan in spi_channel:
            if "SpiChannelId" in chan:
                self.init_spi_chan(chan)


    def __del__(self):
        del self.n_spi_chans_str
        del self.spi_chans_str[:]
        del self.spi_chans[:]
        del self.non_header_objs[:]


    def init_spi_chan(self, chan):
        self.n_spi_chans += 1
        
        # create new objects
        spi_chan = {}
        spi_chan_str = SpiChanStr()
        
        # initialize objects
        spi_chan["SpiChannelId"] = chan["SpiChannelId"]
        spi_chan_str.spi_channel_id.set(chan["SpiChannelId"])
        spi_chan["SpiChannelType"] = chan["SpiChannelType"]
        spi_chan_str.spi_chann_type.set(chan["SpiChannelType"])
        spi_chan["SpiDataWidth"] = chan["SpiDataWidth"]
        spi_chan_str.spi_chan_width.set(chan["SpiDataWidth"])
        spi_chan["SpiDefaultData"] = chan["SpiDefaultData"]
        spi_chan_str.spi_deflt_data.set(chan["SpiDefaultData"])
        spi_chan["SpiEbMaxLength"] = chan["SpiEbMaxLength"]
        spi_chan_str.spi_eb_max_len.set(chan["SpiEbMaxLength"])
        spi_chan["SpiIbNBuffers"] = chan["SpiIbNBuffers"]
        spi_chan_str.spi_ib_n_buffs.set(chan["SpiIbNBuffers"])
        spi_chan["SpiTransferStart"] = chan["SpiTransferStart"]
        spi_chan_str.spi_tran_start.set(chan["SpiTransferStart"])
        
        # add them to self for gui update
        self.spi_chans_str.append(spi_chan_str)
        self.spi_chans.append(spi_chan)


    def create_empty_spi_chan(self):
        spi_chan = {}
        spi_chan["SpiChannelId"] = str(self.n_spi_chans-1)
        spi_chan["SpiChannelType"] = "IB"
        spi_chan["SpiDataWidth"] = "4" # bytes
        spi_chan["SpiDefaultData"] = "0xAA551234"
        spi_chan["SpiEbMaxLength"] = "65535"
        spi_chan["SpiIbNBuffers"] = "65535"
        spi_chan["SpiTransferStart"] = "MSB"
        return spi_chan


    def update(self):
        # Backup current task entries from GUI
        self.backup_data()

        # destroy most old gui widgets
        self.n_spi_chans = int(self.n_spi_chans_str.get())
        for obj in self.non_header_objs:
            obj.destroy()

        # Tune memory allocations based on number of rows or boxes
        n_spi_chans_str = len(self.spi_chans_str)
        if self.n_spi_chans > n_spi_chans_str:
            for i in range(self.n_spi_chans - n_spi_chans_str):
                self.spi_chans_str.insert(len(self.spi_chans_str), SpiChanStr())
                self.spi_chans.insert(len(self.spi_chans), self.create_empty_spi_chan())
        elif n_spi_chans_str > self.n_spi_chans:
            for i in range(n_spi_chans_str - self.n_spi_chans):
                del self.spi_chans_str[-1]
                del self.spi_chans[-1]

        # Draw new objects
        for i in range(0, self.n_spi_chans):
            label = tk.Label(self.scrollw.mnf, text="Spi Sequence #")
            label.grid(row=self.header_size+i, column=0, sticky="e")
            self.non_header_objs.append(label)

            # SpiChannelId
            entry = tk.Entry(self.scrollw.mnf, width=10, textvariable=self.spi_chans_str[i].spi_channel_id, state="readonly")
            self.spi_chans_str[i].spi_channel_id.set(self.spi_chans[i]["SpiChannelId"])
            entry.grid(row=self.header_size+i, column=1)
            self.non_header_objs.append(entry)

            # SpiChannelType
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=18, textvariable=self.spi_chans_str[i].spi_chann_type, state="readonly")
            cmbsel['values'] = ("IB (Internal Buffer)", "EB (External Buffer")
            self.spi_chans_str[i].spi_chann_type.set(self.spi_chans[i]["SpiChannelType"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=2)
            self.non_header_objs.append(cmbsel)

            # SpiDataWidth
            spinb = tk.Spinbox(self.scrollw.mnf, width=13, textvariable=self.spi_chans_str[i].spi_chan_width,
                               values=tuple(range(1,33)))
            self.spi_chans_str[i].spi_chan_width.set(self.spi_chans[i]["SpiDataWidth"])
            spinb.grid(row=self.header_size+i, column=3)
            self.non_header_objs.append(spinb)

            # SpiDefaultData
            entry = tk.Entry(self.scrollw.mnf, width=17, textvariable=self.spi_chans_str[i].spi_deflt_data)
            self.spi_chans_str[i].spi_deflt_data.set(self.spi_chans[i]["SpiDefaultData"])
            entry.grid(row=self.header_size+i, column=4)
            self.non_header_objs.append(entry)

            # SpiEbMaxLength
            spinb = tk.Spinbox(self.scrollw.mnf, width=13, textvariable=self.spi_chans_str[i].spi_eb_max_len,
                               values=tuple(range(0,65536)))
            self.spi_chans_str[i].spi_eb_max_len.set(self.spi_chans[i]["SpiEbMaxLength"])
            spinb.grid(row=self.header_size+i, column=5)
            self.non_header_objs.append(spinb)

            # SpiIbNBuffers
            spinb = tk.Spinbox(self.scrollw.mnf, width=13, textvariable=self.spi_chans_str[i].spi_ib_n_buffs,
                               values=tuple(range(0,65536)))
            self.spi_chans_str[i].spi_ib_n_buffs.set(self.spi_chans[i]["SpiIbNBuffers"])
            spinb.grid(row=self.header_size+i, column=6)
            self.non_header_objs.append(spinb)

            # SpiTransferStart
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=10, textvariable=self.spi_chans_str[i].spi_tran_start, state="readonly")
            cmbsel['values'] = ("MSB", "LSB")
            self.spi_chans_str[i].spi_tran_start.set(self.spi_chans[i]["SpiTransferStart"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=7)
            self.non_header_objs.append(cmbsel)
            
        # Set the self.cv scrolling region
        self.scrollw.scroll()


    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Channels:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_spi_chans_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_spi_chans+1)))
        self.n_spi_chans_str.set(self.n_spi_chans)
        spinb.grid(row=0, column=1, sticky="w")

        # Save Button
        genm = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=0, column=2)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading
        label = tk.Label(self.scrollw.mnf, text=" ")
        label.grid(row=2, column=0, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="SpiChannelId")
        label.grid(row=2, column=1, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="SpiChannelType")
        label.grid(row=2, column=2, sticky="we")
        label = tk.Label(self.scrollw.mnf, text="SpiDataWidth")
        label.grid(row=2, column=3, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="SpiDefaultData")
        label.grid(row=2, column=4, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="SpiEbMaxLength")
        label.grid(row=2, column=5, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="SpiIbNBuffers")
        label.grid(row=2, column=6, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="SpiTransferStart")
        label.grid(row=2, column=7, sticky="w")

        self.update()


    def backup_data(self):
        n_spi_chans_str = len(self.spi_chans_str)
        for i in range(n_spi_chans_str):
            if len(self.spi_chans_str[i].spi_channel_id.get()):
                self.spi_chans[i]["SpiChannelId"] = self.spi_chans_str[i].spi_channel_id.get()
            if len(self.spi_chans_str[i].spi_chann_type.get()):
                self.spi_chans[i]["SpiChannelType"] = self.spi_chans_str[i].spi_chann_type.get()
            if len(self.spi_chans_str[i].spi_chan_width.get()):
                self.spi_chans[i]["SpiDataWidth"] = self.spi_chans_str[i].spi_chan_width.get()


    def save_data(self):
        self.backup_data()
        self.tab_struct.save_cb(self.gui)
