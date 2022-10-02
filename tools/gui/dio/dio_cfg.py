#
# Created on Sun Oct 02 2022 10:05:21 AM
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


    
class DioPortStr:
    port_id = None
    chan_id = None

    def __init__(self):
        self.port_id = tk.StringVar()
        self.chan_id = tk.StringVar()

    def __del__(self):
        del self.port_id
        del self.chan_id


class DioConfigTab:
    n_pins = 0
    max_pins = 65535
    n_pins_str = None

    dio_str = []    # dio pin GUI str structure
    dio_pins = []   # pins info structure from Dio ARXML & info pulled from Port ARXML
    dio_ports = []  # copy of port info
    header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_size = 3
    non_header_objs = []
    
    toplvl = None
    scrollw = None

    gui = None

    def __init__(self, gui):
        self.gui = gui
        self.toplvl = gui.main_view.child_window
        self.n_pins_str = tk.StringVar()
        pins, ports, general = arxml_port.parse_arxml(gui.arxml_file) # Temporary
        dio_pins, dio_ports, dio_gen = arxml_dio.parse_arxml(gui.arxml_file)
        if pins == None or dio_pins == None:
            return
        if pins != dio_pins:
            print("Error: dio_cfg -- Pins as per Dio ARXML = ", dio_pins, ". But as per Port ARXML = ", pins)
        for port in ports:
            if port['PortPinMode'] == "PORT_PIN_MODE_DIO":
                self.n_pins += 1
                # add the port info from Port module to a local port list
                self.dio_ports.append(port)
                # create new dio pin GUI str and dio pin info
                diostr = DioPortStr()
                diopin = self.create_empty_diopin()
                # now, pull out info from local port and populate local dio & str list
                diostr.port_id.set(port["PortPinId"])
                diopin["DioPortId"] = port["PortPinId"]
                diostr.chan_id.set(self.get_chan_id(port["PortPinId"], dio_ports))
                diopin["DioChannelId"] = self.get_chan_id(port["PortPinId"], dio_ports)
                self.dio_str.append(diostr)
                self.dio_pins.append(diopin)


    def get_chan_id(self, port_id, dio_ports):
        chan_id = None
        for port in dio_ports:
            if port["DioPortId"] == port_id:
                chan_id = port["DioChannelId"]
                break
        return chan_id


    def __del__(self):
        del self.n_pins_str
        del self.dio_str[:]
        del self.dio_pins[:]
        del self.dio_ports[:]
        del self.non_header_objs[:]


    def create_empty_diopin(self):
        diopin = {}
        diopin["DioPortId"] = "65535"
        diopin["DioChannelId"] = "65535"
        return diopin


    def draw(self, tab):
        self.tabstr = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)

        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Dio Pins:")
        label.grid(row=0, column=0, sticky="w")
        dio_entry = tk.Entry(self.scrollw.mnf, width=10, justify='center')
        dio_entry.insert(0, str(self.n_pins))
        dio_entry.config(state='readonly')
        dio_entry.grid(row=0, column=1, sticky="w")

        # Save Button
        genm = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=0, column=2)

        self.scrollw.update()
        
        if self.n_pins == 0:
            label = tk.Label(self.scrollw.mnf, text="No ports are configured as DIO in Port module. Please open "
                             "Port module and configure pins as DIO to see them here.""", justify="left")
            label.grid(row=2, column=3, sticky="w")
            return

        # Table heading
        label = tk.Label(self.scrollw.mnf, text=" ")
        label.grid(row=2, column=0, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="DioPortId")
        label.grid(row=2, column=1, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="DioChannelId")
        label.grid(row=2, column=2, sticky="we")

        self.update()


    def update(self):
        # Backup current task entries from GUI
        self.backup_data()

        # destroy most old gui widgets
        for obj in self.non_header_objs:
            obj.destroy()

        # Draw new objects
        for i in range(0, self.n_pins):
            label = tk.Label(self.scrollw.mnf, text="Pin #")
            label.grid(row=self.header_size+i, column=0, sticky="e")
            self.non_header_objs.append(label)

            # DioPortId
            entry = tk.Entry(self.scrollw.mnf, width=10, textvariable=self.dio_str[i].port_id)
            self.dio_str[i].port_id.set(self.dio_pins[i]["DioPortId"])
            entry.config(state='readonly')
            entry.grid(row=self.header_size+i, column=1)
            self.non_header_objs.append(entry)
            
            # DioChannelId
            entry = tk.Entry(self.scrollw.mnf, width=10, textvariable=self.dio_str[i].chan_id)
            self.dio_str[i].chan_id.set(self.dio_pins[i]["DioChannelId"])
            entry.grid(row=self.header_size+i, column=2)
            self.non_header_objs.append(entry)

        # Set the self.cv scrolling region
        self.scrollw.scroll()


    def backup_data(self):
        n_pins_str = len(self.dio_str)
        for i in range(n_pins_str):
            if len(self.dio_str[i].port_id.get()):
                self.dio_pins[i]["DioPortId"] = self.dio_str[i].port_id.get()
            if len(self.dio_str[i].chan_id.get()):
                self.dio_pins[i]["DioChannelId"] = self.dio_str[i].chan_id.get()

        
    def save_data(self):
        self.backup_data()
        self.tabstr.save_cb(self.gui)
        