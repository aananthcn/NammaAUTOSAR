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

class PinStr:
    id = None
    pindir = None
    dir_changeable = None
    pin_level = None
    pin_mode = None
    pin_initial_mode = None
    mode_changeable = None

    def __init__(self):
        self.id = tk.StringVar()
        self.pindir = tk.StringVar()
        self.dir_changeable = tk.StringVar()
        self.pin_level = tk.StringVar()
        self.pin_mode = tk.StringVar()
        self.pin_initial_mode = tk.StringVar()
        self.mode_changeable = tk.StringVar()

    def __del__(self):
        del self.id
        del self.pindir
        del self.dir_changeable
        del self.pin_level
        del self.pin_mode
        del self.pin_initial_mode
        del self.mode_changeable


class PortConfigSetTab:
    n_pins = 0
    max_pins = 65535
    n_pins_str = None

    pins_str = []
    events = []
    port_pins = []
    header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_size = 3
    non_header_objs = []
    gui = None
    tab_struct = None # passed from *_view.py file

    def __init__(self, gui):
        self.gui = gui
        self.n_pins = 0
        self.n_pins_str = tk.StringVar()


    def init(self, n, pinlist):
        self.n_pins = n
        for i in range(n):
            self.port_pins.insert(i, pinlist[i])


    def __del__(self):
        del self.n_pins_str
        del self.pins_str[:]


    def create_empty_portpin(self):
        portpin = {}
        
        portpin["PortPinDirection"] = "PORT_PIN_IN"
        portpin["PortPinDirectionChangeable"] = "FALSE"
        portpin["PortPinId"] = "65535"
        portpin["PortPinInitialMode"] = "PORT_PIN_MODE_DIO"
        portpin["PortPinLevelValue"] = "PORT_PIN_LEVEL_LOW"
        portpin["PortPinMode"] = "PORT_PIN_MODE_DIO"
        portpin["PortPinModeChangeable"] = "FALSE"

        return portpin


    def update(self):
        # Backup current task entries from GUI
        self.backup_data()

        # destroy most old gui widgets
        self.n_pins = int(self.n_pins_str.get())
        for obj in self.non_header_objs:
            obj.destroy()

        # Tune memory allocations based on number of rows or boxes
        n_pins_str = len(self.pins_str)
        if self.n_pins > n_pins_str:
            for i in range(self.n_pins - n_pins_str):
                self.pins_str.insert(len(self.pins_str), PinStr())
                self.port_pins.insert(len(self.port_pins), self.create_empty_portpin())
        elif n_pins_str > self.n_pins:
            for i in range(n_pins_str - self.n_pins):
                del self.pins_str[-1]
                del self.port_pins[-1]

        # Draw new objects
        for i in range(0, self.n_pins):
            label = tk.Label(self.scrollw.mnf, text="Pin #")
            label.grid(row=self.header_size+i, column=0, sticky="e")
            self.non_header_objs.append(label)
            
            # PortPinId
            entry = tk.Entry(self.scrollw.mnf, width=10, textvariable=self.pins_str[i].id)
            self.pins_str[i].id.set(self.port_pins[i]["PortPinId"])
            entry.grid(row=self.header_size+i, column=1)
            self.non_header_objs.append(entry)

            # PortPinDirection
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=14, textvariable=self.pins_str[i].pindir, state="readonly")
            cmbsel['values'] = ("PORT_PIN_IN", "PORT_PIN_OUT")
            self.pins_str[i].pindir.set(self.port_pins[i]["PortPinDirection"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=2)
            self.non_header_objs.append(cmbsel)

            # PortPinDirectionChangeable
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=8, textvariable=self.pins_str[i].dir_changeable, state="readonly")
            cmbsel['values'] = ("FALSE", "TRUE")
            self.pins_str[i].dir_changeable.set(self.port_pins[i]["PortPinDirectionChangeable"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=3)
            self.non_header_objs.append(cmbsel)

            # PortPinLevelValue
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=22, textvariable=self.pins_str[i].pin_level, state="readonly")
            cmbsel['values'] = ("PORT_PIN_LEVEL_LOW", "PORT_PIN_LEVEL_HIGH")
            self.pins_str[i].pin_level.set(self.port_pins[i]["PortPinLevelValue"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=4)
            self.non_header_objs.append(cmbsel)

            # PortPinMode
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=28, textvariable=self.pins_str[i].pin_mode, state="readonly")
            cmbsel['values'] = StdPinModes
            self.pins_str[i].pin_mode.set(self.port_pins[i]["PortPinMode"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=5)
            self.non_header_objs.append(cmbsel)

            # PortPinInitialMode
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=28, textvariable=self.pins_str[i].pin_initial_mode, state="readonly")
            cmbsel['values'] = StdPinModes
            self.pins_str[i].pin_initial_mode.set(self.port_pins[i]["PortPinInitialMode"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=6)
            self.non_header_objs.append(cmbsel)

            # PortPinModeChangeable
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=8, textvariable=self.pins_str[i].mode_changeable, state="readonly")
            cmbsel['values'] = ("FALSE", "TRUE")
            self.pins_str[i].mode_changeable.set(self.port_pins[i]["PortPinModeChangeable"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=7)
            self.non_header_objs.append(cmbsel)

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

        # Table heading
        label = tk.Label(self.scrollw.mnf, text=" ")
        label.grid(row=2, column=0, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="PortPinId")
        label.grid(row=2, column=1, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="PinDirection")
        label.grid(row=2, column=2, sticky="we")
        label = tk.Label(self.scrollw.mnf, text="DirChangeable")
        label.grid(row=2, column=3, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="PinLevelValue")
        label.grid(row=2, column=4, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="PortPinMode")
        label.grid(row=2, column=5, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="PinInitialMode")
        label.grid(row=2, column=6, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="ModeChangeable")
        label.grid(row=2, column=7, sticky="w")

        self.update()
        self.scrollw.scroll()



    def backup_data(self):
        n_pins_str = len(self.pins_str)
        for i in range(n_pins_str):
            if len(self.pins_str[i].id.get()):
                self.port_pins[i]["PortPinId"] = self.pins_str[i].id.get()
            if len(self.pins_str[i].pindir.get()):
                self.port_pins[i]["PortPinDirection"] = self.pins_str[i].pindir.get()
            if len(self.pins_str[i].dir_changeable.get()):
                self.port_pins[i]["PortPinDirectionChangeable"] = self.pins_str[i].dir_changeable.get()
            if len(self.pins_str[i].pin_level.get()):
                self.port_pins[i]["PortPinLevelValue"] = self.pins_str[i].pin_level.get()
            if len(self.pins_str[i].pin_mode.get()):
                self.port_pins[i]["PortPinMode"] = self.pins_str[i].pin_mode.get()
            if len(self.pins_str[i].mode_changeable.get()):
                self.port_pins[i]["PortPinModeChangeable"] = self.pins_str[i].mode_changeable.get()
            if len(self.pins_str[i].pin_initial_mode.get()):
                self.port_pins[i]["PortPinInitialMode"] = self.pins_str[i].pin_initial_mode.get()


    def save_data(self):
        # arxml_port.update_arxml(self.gui.arxml_file, self)
        # port_cgen.generate_code(self.gui)
        self.backup_data()
        self.tab_struct.save_cb(self.gui)

