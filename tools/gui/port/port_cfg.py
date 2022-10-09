#
# Created on Sun Oct 02 2022 10:05:56 AM
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

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box


StdPinModes = (
    "PORT_PIN_MODE_ADC",
    "PORT_PIN_MODE_CAN",
    "PORT_PIN_MODE_DIO",
    "PORT_PIN_MODE_DIO_GPT",
    "PORT_PIN_MODE_DIO_WDG",
    "PORT_PIN_MODE_FLEXRAY",
    "PORT_PIN_MODE_ICU",
    "PORT_PIN_MODE_LIN",
    "PORT_PIN_MODE_MEM",
    "PORT_PIN_MODE_PWM",
    "PORT_PIN_MODE_SPI" 
)


class PortConfigSetTab:
    n_pins = 0
    max_pins = 65535
    n_pins_str = None

    # pins_str = []
    events = []
    port_pins = []

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["PortPinId", "PortPinDirection", "PortPinDirectionChangeable", "PortPinLevelValue",
               "PortPinMode", "PortPinInitialMode", "PortPinModeChangeable"]
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False

    header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_size = 3
    non_header_objs = []


    def __init__(self, gui):
        self.gui = gui
        self.configs = []
        self.n_pins_str = tk.StringVar()

        self.n_pins, ports, general = arxml_port.parse_arxml(gui.arxml_file)
        # print(self.n_pins)
        # print(ports)
        if self.n_pins == None or ports == None:
            self.n_pins = 0
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))

        self.n_pins = len(ports)
        for port in ports:
            self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, port))


    def __del__(self):
        del self.n_pins_str
        # del self.pins_str[:]
        del self.non_header_objs[:]
        del self.configs[:]


    def create_empty_configs(self):
        portpin = {}
        
        portpin["PortPinDirection"] = "PORT_PIN_IN"
        portpin["PortPinDirectionChangeable"] = "FALSE"
        portpin["PortPinId"] = "65535"
        portpin["PortPinInitialMode"] = "PORT_PIN_MODE_DIO"
        portpin["PortPinLevelValue"] = "PORT_PIN_LEVEL_LOW"
        portpin["PortPinMode"] = "PORT_PIN_MODE_DIO"
        portpin["PortPinModeChangeable"] = "FALSE"

        return portpin



    def delete_dappa_row(self):
        objlist = self.non_header_objs[-self.dappas_per_row:]
        for obj in objlist:
            obj.destroy()
        del self.non_header_objs[-self.dappas_per_row:]



    def draw_dappa_row(self, i):
        dappa.label(self, "Pin #", self.header_size+i, 0, "e")

        # PortPinId
        dappa.entry(self, "PortPinId", i, self.header_size+i, 1, 10, "normal")

        # PortPinDirection
        dappa.combo(self, "PortPinDirection", i, self.header_size+i, 2, 18, ("PORT_PIN_IN", "PORT_PIN_OUT"))

        # PortPinDirectionChangeable
        dappa.combo(self, "PortPinDirectionChangeable", i, self.header_size+i, 3, 20, ("FALSE", "TRUE"))

        # PortPinLevelValue
        values = ("PORT_PIN_LEVEL_LOW", "PORT_PIN_LEVEL_HIGH")
        dappa.combo(self, "PortPinLevelValue", i, self.header_size+i, 4, 22, values)

        # PortPinMode
        dappa.combo(self, "PortPinMode", i, self.header_size+i, 5, 28, StdPinModes)

        # PortPinInitialMode
        dappa.combo(self, "PortPinInitialMode", i, self.header_size+i, 6, 28, StdPinModes)

        # PortPinModeChangeable
        dappa.combo(self, "PortPinModeChangeable", i, self.header_size+i, 7, 18, StdPinModes)



    def update(self):
        self.n_pins = int(self.n_pins_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_pins > n_dappa_rows:
            for i in range(self.n_pins - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_pins:
            for i in range(n_dappa_rows - self.n_pins):
                self.delete_dappa_row()
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()


    def draw(self, tab):
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        self.tab_struct = tab
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Pins:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_pins_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_pins+1)))
        self.n_pins_str.set(self.n_pins)
        spinb.grid(row=0, column=1, sticky="w")

        # Save Button
        genm = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=0, column=2)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()
        self.scrollw.scroll()



    def save_data(self):
        self.tab_struct.save_cb(self.gui)

