import tkinter as tk
from tkinter import ttk

import arxml.port.arxml_port as arxml_port
import gui.port.port_cgen as port_cgen


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


class DioGeneralTab:
    n_pins = 0
    max_pins = 65535
    n_pins_str = None

    pins_str = []
    events = []
    port_pins = []
    header_objs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_size = 3
    non_header_objs = []
    

    prf = None  # Parent Frame
    cvf = None  # Canvas Frame
    cv  = None  # Canvas
    sb  = None  # Scrollbar
    mnf = None  # Main Frame - where the widgets are scrolled

    gui = None

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
        

        # PortPinDirection
        cmbsel = ttk.Combobox(self.prf, width=14, textvariable=self.pins_str[0].pindir, state="readonly")
        cmbsel['values'] = ("PORT_PIN_IN", "PORT_PIN_OUT")
        self.pins_str[0].pindir.set(self.port_pins[0]["PortPinDirection"])
        cmbsel.current()
        cmbsel.grid(row=1, column=2)
        self.non_header_objs.append(cmbsel)




    def draw(self, tab):
        return
        tab.grid_rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)
        self.prf = tab
        
        self.update()

 


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
        arxml_port.update_arxml(self.gui.arxml_file, self)
        port_cgen.generate_code(self.gui)

