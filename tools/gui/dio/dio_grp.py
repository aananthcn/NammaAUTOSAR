#
# Created on Sun Oct 02 2022 10:05:32 AM
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

import arxml.port.arxml_port as arxml_port
import arxml.dio.arxml_dio as arxml_dio

import gui.lib.window as window


class ChGrpStr:
    port_pin_id = None
    chan_grp_id = None
    chan_grp_port_offset = None
    chan_grp_port_mask = None

    def __init__(self):
        self.port_pin_id = tk.StringVar()
        self.chan_grp_id = tk.StringVar()
        self.chan_grp_port_offset = tk.StringVar()
        self.chan_grp_port_mask = tk.StringVar()

    def __del__(self):
        del self.port_pin_id
        del self.chan_grp_id
        del self.chan_grp_port_offset
        del self.chan_grp_port_mask


class DioChannelGroupTab:
    n_chgrps = 0
    max_chgrps = 65535
    n_chgrps_str = None

    chgrps_str = []
    port_chgrps = []
    port_pin_ids = []
    header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_size = 3
    non_header_objs = []
    gui = None
    tabstr = None

    def __init__(self, gui):
        self.gui = gui
        self.n_chgrps = 0
        self.n_chgrps_str = tk.StringVar()
        pins, ports, general = arxml_port.parse_arxml(gui.arxml_file)
        if pins == None or ports == None:
            return
        for port in ports:
            if port['PortPinMode'] == "PORT_PIN_MODE_DIO":
                self.port_pin_ids.append(port["PortPinId"])
        dio_pins, dio_ports, dio_gen = arxml_dio.parse_arxml(gui.arxml_file)
        for diop in dio_ports:
            if "DioChannelGroupIdentification" in diop:
                self.init_chgrp(diop)


    def __del__(self):
        del self.n_chgrps_str
        del self.chgrps_str[:]
        del self.port_chgrps[:]
        del self.non_header_objs[:]


    def init_chgrp(self, dioport):
        self.n_chgrps += 1
        
        # create new objects
        chgrp = {}
        chgrp_str = ChGrpStr()
        
        # initialize objects
        chgrp["PortPinId"] = dioport["DioPortId"]
        chgrp_str.port_pin_id.set(dioport["DioPortId"])
        chgrp["DioChannelGroupIdentification"] = dioport["DioChannelGroupIdentification"]
        chgrp_str.chan_grp_id.set(dioport["DioChannelGroupIdentification"])
        chgrp["DioPortOffset"] = dioport["DioPortOffset"]
        chgrp_str.chan_grp_port_offset.set(dioport["DioPortOffset"])
        chgrp["DioPortMask"] = dioport["DioPortMask"]
        chgrp_str.chan_grp_port_mask.set(dioport["DioPortMask"])
        
        # add them to self for gui update
        self.chgrps_str.append(chgrp_str)
        self.port_chgrps.append(chgrp)


    def create_empty_chgrp(self):
        chgrp = {}
        chgrp["PortPinId"] = "65535"
        chgrp["DioChannelGroupIdentification"] = "ChGrp_"
        chgrp["DioPortOffset"] = "e.g., 0x4"
        chgrp["DioPortMask"] = "e.g., 0xF0F"
        return chgrp


    def update(self):
        # Backup current task entries from GUI
        self.backup_data()

        # destroy most old gui widgets
        self.n_chgrps = int(self.n_chgrps_str.get())
        for obj in self.non_header_objs:
            obj.destroy()

        # Tune memory allocations based on number of rows or boxes
        n_chgrps_str = len(self.chgrps_str)
        if self.n_chgrps > n_chgrps_str:
            for i in range(self.n_chgrps - n_chgrps_str):
                self.chgrps_str.insert(len(self.chgrps_str), ChGrpStr())
                self.port_chgrps.insert(len(self.port_chgrps), self.create_empty_chgrp())
        elif n_chgrps_str > self.n_chgrps:
            for i in range(n_chgrps_str - self.n_chgrps):
                del self.chgrps_str[-1]
                del self.port_chgrps[-1]

        # Draw new objects
        for i in range(0, self.n_chgrps):
            label = tk.Label(self.scrollw.mnf, text="Channel Group #")
            label.grid(row=self.header_size+i, column=0, sticky="e")
            self.non_header_objs.append(label)

            # PortPinId
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=14, textvariable=self.chgrps_str[i].port_pin_id, state="readonly")
            cmbsel['values'] = self.port_pin_ids
            # self.config.masked_write_port_api.set("FALSE")
            cmbsel.current(0)
            cmbsel.grid(row=self.header_size+i, column=1)

            # DioChannelGroupIdentification
            entry = tk.Entry(self.scrollw.mnf, width=30, textvariable=self.chgrps_str[i].chan_grp_id)
            self.chgrps_str[i].chan_grp_id.set(self.port_chgrps[i]["DioChannelGroupIdentification"])
            entry.grid(row=self.header_size+i, column=2)
            self.non_header_objs.append(entry)

            # Channel Group - DioPortOffset
            entry = tk.Entry(self.scrollw.mnf, width=15, textvariable=self.chgrps_str[i].chan_grp_port_offset)
            self.chgrps_str[i].chan_grp_port_offset.set(self.port_chgrps[i]["DioPortOffset"])
            entry.grid(row=self.header_size+i, column=3)
            self.non_header_objs.append(entry)

            # Channel Group - DioPortMask
            entry = tk.Entry(self.scrollw.mnf, width=15, textvariable=self.chgrps_str[i].chan_grp_port_mask)
            self.chgrps_str[i].chan_grp_port_mask.set(self.port_chgrps[i]["DioPortMask"])
            entry.grid(row=self.header_size+i, column=4)
            self.non_header_objs.append(entry)
            
        # Set the self.cv scrolling region
        self.scrollw.scroll()


    def draw(self, tab):
        self.tabstr = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Chan. Groups:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_chgrps_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_chgrps+1)))
        self.n_chgrps_str.set(self.n_chgrps)
        spinb.grid(row=0, column=1, sticky="w")

        # Save Button
        genm = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=0, column=2)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading
        label = tk.Label(self.scrollw.mnf, text=" ")
        label.grid(row=2, column=0, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="PortPinId")
        label.grid(row=2, column=1, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="Channel Group ID")
        label.grid(row=2, column=2, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="DioPortOffset")
        label.grid(row=2, column=3, sticky="we")
        label = tk.Label(self.scrollw.mnf, text="DioPortMask")
        label.grid(row=2, column=4, sticky="w")

        self.update()



    def backup_data(self):
        n_chgrps_str = len(self.chgrps_str)
        for i in range(n_chgrps_str):
            if len(self.chgrps_str[i].port_pin_id.get()):
                self.port_chgrps[i]["PortPinId"] = self.chgrps_str[i].port_pin_id.get()
            if len(self.chgrps_str[i].chan_grp_id.get()):
                self.port_chgrps[i]["DioChannelGroupIdentification"] = self.chgrps_str[i].chan_grp_id.get()
            if len(self.chgrps_str[i].chan_grp_port_offset.get()):
                self.port_chgrps[i]["DioPortOffset"] = self.chgrps_str[i].chan_grp_port_offset.get()
            if len(self.chgrps_str[i].chan_grp_port_mask.get()):
                self.port_chgrps[i]["DioPortMask"] = self.chgrps_str[i].chan_grp_port_mask.get()


    def save_data(self):
        self.backup_data()
        self.tabstr.save_cb(self.gui)
