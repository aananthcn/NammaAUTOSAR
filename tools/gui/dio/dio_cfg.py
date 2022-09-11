import tkinter as tk
from tkinter import ttk

import arxml.port.arxml_port as arxml_port

import gui.lib.window as window
import gui.port.port_cgen as port_cgen


class DioPort:
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


class DioConfigTab:
    n_pins = 0
    max_pins = 65535
    n_pins_str = None

    pins_str = []
    events = []
    dio_pins = []
    dio_ports = []
    header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_size = 3
    non_header_objs = []
    
    toplvl = None
    scrollw = None

    gui = None

    def __init__(self, gui):
        self.gui = gui
        self.toplvl = gui.main_view.child_window
        pins, ports = arxml_port.parse_arxml(gui.arxml_file)
        for port in ports:
            if port['PortPinMode'] == "PORT_PIN_MODE_DIO":
                self.n_pins += 1
                self.dio_ports.append(port)
        self.n_pins_str = tk.StringVar()

    def __del__(self):
        del self.n_pins_str
        del self.pins_str[:]


    def create_empty_portpin(self):
        diopin = {}
        
        diopin["DioPortId"] = "int"
        diopin["DioChannelId"] = "int"
        diopin["DioChannelGroupIdentification"] = "str"
        diopin["DioPortOffset"] = "int"
        diopin["DioPortMask"] = "int"

        return diopin


    def draw(self, tab, xsize, ysize):
        self.scrollw = window.ScrollableWindow(tab, xsize, ysize)

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
        label = tk.Label(self.scrollw.mnf, text="DioChannelGroupIdentification")
        label.grid(row=2, column=3, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="DioPortOffset")
        label.grid(row=2, column=4, sticky="w")
        label = tk.Label(self.scrollw.mnf, text="DioPortMask")
        label.grid(row=2, column=5, sticky="w")

        self.update()


    def update(self):
        return
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
                self.dio_pins.insert(len(self.dio_pins), self.create_empty_portpin())
        elif n_pins_str > self.n_pins:
            for i in range(n_pins_str - self.n_pins):
                del self.pins_str[-1]
                del self.dio_pins[-1]

        # Draw new objects
        for i in range(0, self.n_pins):
            label = tk.Label(self.scrollw.mnf, text="Pin #")
            label.grid(row=self.header_size+i, column=0, sticky="e")
            self.non_header_objs.append(label)
            
            # PortPinId
            entry = tk.Entry(self.scrollw.mnf, width=10, textvariable=self.pins_str[i].id)
            self.pins_str[i].id.set(self.dio_pins[i]["PortPinId"])
            entry.grid(row=self.header_size+i, column=1)
            self.non_header_objs.append(entry)

            # PortPinDirection
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=14, textvariable=self.pins_str[i].pindir, state="readonly")
            cmbsel['values'] = ("PORT_PIN_IN", "PORT_PIN_OUT")
            self.pins_str[i].pindir.set(self.dio_pins[i]["PortPinDirection"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=2)
            self.non_header_objs.append(cmbsel)

            # PortPinDirectionChangeable
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=8, textvariable=self.pins_str[i].dir_changeable, state="readonly")
            cmbsel['values'] = ("FALSE", "TRUE")
            self.pins_str[i].dir_changeable.set(self.dio_pins[i]["PortPinDirectionChangeable"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=3)
            self.non_header_objs.append(cmbsel)

            # PortPinLevelValue
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=22, textvariable=self.pins_str[i].pin_level, state="readonly")
            cmbsel['values'] = ("PORT_PIN_LEVEL_LOW", "PORT_PIN_LEVEL_HIGH")
            self.pins_str[i].pin_level.set(self.dio_pins[i]["PortPinLevelValue"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=4)
            self.non_header_objs.append(cmbsel)

            # PortPinMode
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=28, textvariable=self.pins_str[i].pin_mode, state="readonly")
            cmbsel['values'] = StdPinModes
            self.pins_str[i].pin_mode.set(self.dio_pins[i]["PortPinMode"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=5)
            self.non_header_objs.append(cmbsel)

            # PortPinInitialMode
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=28, textvariable=self.pins_str[i].pin_initial_mode, state="readonly")
            cmbsel['values'] = StdPinModes
            self.pins_str[i].pin_initial_mode.set(self.dio_pins[i]["PortPinInitialMode"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=6)
            self.non_header_objs.append(cmbsel)

            # PortPinModeChangeable
            cmbsel = ttk.Combobox(self.scrollw.mnf, width=8, textvariable=self.pins_str[i].mode_changeable, state="readonly")
            cmbsel['values'] = ("FALSE", "TRUE")
            self.pins_str[i].mode_changeable.set(self.dio_pins[i]["PortPinModeChangeable"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=7)
            self.non_header_objs.append(cmbsel)

        # Set the self.cv scrolling region
        self.scrollw.scroll()


    def backup_data(self):
        n_pins_str = len(self.pins_str)
        for i in range(n_pins_str):
            if len(self.pins_str[i].id.get()):
                self.dio_pins[i]["PortPinId"] = self.pins_str[i].id.get()
            if len(self.pins_str[i].pindir.get()):
                self.dio_pins[i]["PortPinDirection"] = self.pins_str[i].pindir.get()
            if len(self.pins_str[i].dir_changeable.get()):
                self.dio_pins[i]["PortPinDirectionChangeable"] = self.pins_str[i].dir_changeable.get()
            if len(self.pins_str[i].pin_level.get()):
                self.dio_pins[i]["PortPinLevelValue"] = self.pins_str[i].pin_level.get()
            if len(self.pins_str[i].pin_mode.get()):
                self.dio_pins[i]["PortPinMode"] = self.pins_str[i].pin_mode.get()
            if len(self.pins_str[i].mode_changeable.get()):
                self.dio_pins[i]["PortPinModeChangeable"] = self.pins_str[i].mode_changeable.get()
            if len(self.pins_str[i].pin_initial_mode.get()):
                self.dio_pins[i]["PortPinInitialMode"] = self.pins_str[i].pin_initial_mode.get()


    def save_data(self):
        arxml_port.update_arxml(self.gui.arxml_file, self)
        port_cgen.generate_code(self.gui)

