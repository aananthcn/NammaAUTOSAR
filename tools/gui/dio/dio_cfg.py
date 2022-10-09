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
import gui.lib.asr_widget as dappa # dappa in Tamil means box

    

class DioConfigTab:
    n_pins = 0
    max_pins = 65535
    n_pins_str = None

    dio_ports = []  # copy of port info

    header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_size = 3
    non_header_objs = []
    
    toplvl = None
    scrollw = None

    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["DioPortId", "DioChannelId"]
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels

    def __init__(self, gui):
        self.gui = gui
        self.configs = []
        self.toplvl = gui.main_view.child_window
        self.n_pins_str = tk.StringVar()
        pins, ports, general = arxml_port.parse_arxml(gui.arxml_file) # Temporary
        dio_pins, dio_ports, dio_grps, dio_gen = arxml_dio.parse_arxml(gui.arxml_file)
        if pins == None or dio_pins == None:
            return
        if pins != dio_pins:
            print("Error: dio_cfg -- Pins as per Dio ARXML = ", dio_pins, ". But as per Port ARXML = ", pins)

        # scan all Dorts and add them to self.configs list for display
        for port in ports:
            if port['PortPinMode'] == "PORT_PIN_MODE_DIO":
                self.n_pins += 1

                # add the port info from Port module to a local port list
                self.dio_ports.append(port)
                diopin = self.create_empty_configs()
                diopin["DioPortId"] = port["PortPinId"]
                diopin["DioChannelId"] = self.get_chan_id(port["PortPinId"], dio_ports)

                # create new dio pin GUI str and dio pin info
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, diopin))


    def __del__(self):
        del self.n_pins_str
        del self.dio_ports[:]
        del self.non_header_objs[:]
        del self.configs[:]


    def create_empty_configs(self):
        diopin = {}
        diopin["DioPortId"] = "65535"
        diopin["DioChannelId"] = "65535"
        return diopin


    def get_chan_id(self, port_id, dio_ports):
        chan_id = None
        for port in dio_ports:
            if port["DioChannelId"] == port_id:
                chan_id = port["DioChannelId"]
                break
        return chan_id



    def delete_dappa_row(self):
        objlist = self.non_header_objs[-self.dappas_per_row:]
        for obj in objlist:
            obj.destroy()
        del self.non_header_objs[-self.dappas_per_row:]



    def draw_dappa_row(self, i):
        dappa.label(self, "Pin #", self.header_size+i, 0, "e")

        # DioPortId
        dappa.entry(self, "DioPortId", i, self.header_size+i, 1, 10, "readonly")

        # DioChannelId
        dappa.entry(self, "DioChannelId", i, self.header_size+i, 2, 10, "normal")



    def update(self):
        # Draw new objects
        for i in range(0, self.n_pins):
            self.draw_dappa_row(i)

        # Set the self.cv scrolling region
        self.scrollw.scroll()


    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)

        #Number of Dio pins
        label = tk.Label(self.scrollw.mnf, text="No. of Dio Pins:")
        label.grid(row=0, column=0, sticky="w")
        dio_entry = tk.Entry(self.scrollw.mnf, width=10, textvariable=self.n_pins_str, justify='center', state="readonly")
        self.n_pins_str.set(self.n_pins)
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

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()



    def save_data(self):
        self.tab_struct.save_cb(self.gui)
        