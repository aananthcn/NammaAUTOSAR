import tkinter as tk
from tkinter import ttk

import arxml.port.arxml_port as arxml_port

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
            label = tk.Label(self.mnf, text="Pin #")
            label.grid(row=self.header_size+i, column=0, sticky="e")
            self.non_header_objs.append(label)
            
            # PortPinId
            entry = tk.Entry(self.mnf, width=10, textvariable=self.pins_str[i].id)
            self.pins_str[i].id.set(self.port_pins[i]["PortPinId"])
            entry.grid(row=self.header_size+i, column=1)
            self.non_header_objs.append(entry)

            # PortPinDirection
            cmbsel = ttk.Combobox(self.mnf, width=14, textvariable=self.pins_str[i].pindir, state="readonly")
            cmbsel['values'] = ("PORT_PIN_IN", "PORT_PIN_OUT")
            self.pins_str[i].pindir.set(self.port_pins[i]["PortPinDirection"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=2)
            self.non_header_objs.append(cmbsel)

            # PortPinDirectionChangeable
            cmbsel = ttk.Combobox(self.mnf, width=8, textvariable=self.pins_str[i].dir_changeable, state="readonly")
            cmbsel['values'] = ("FALSE", "TRUE")
            self.pins_str[i].dir_changeable.set(self.port_pins[i]["PortPinDirectionChangeable"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=3)
            self.non_header_objs.append(cmbsel)

            # PortPinLevelValue
            cmbsel = ttk.Combobox(self.mnf, width=22, textvariable=self.pins_str[i].pin_level, state="readonly")
            cmbsel['values'] = ("PORT_PIN_LEVEL_LOW", "PORT_PIN_LEVEL_HIGH")
            self.pins_str[i].pin_level.set(self.port_pins[i]["PortPinLevelValue"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=4)
            self.non_header_objs.append(cmbsel)

            # PortPinMode
            cmbsel = ttk.Combobox(self.mnf, width=28, textvariable=self.pins_str[i].pin_mode, state="readonly")
            cmbsel['values'] = StdPinModes
            self.pins_str[i].pin_mode.set(self.port_pins[i]["PortPinMode"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=5)
            self.non_header_objs.append(cmbsel)

            # PortPinInitialMode
            cmbsel = ttk.Combobox(self.mnf, width=28, textvariable=self.pins_str[i].pin_initial_mode, state="readonly")
            cmbsel['values'] = StdPinModes
            self.pins_str[i].pin_initial_mode.set(self.port_pins[i]["PortPinInitialMode"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=6)
            self.non_header_objs.append(cmbsel)

            # PortPinModeChangeable
            cmbsel = ttk.Combobox(self.mnf, width=8, textvariable=self.pins_str[i].mode_changeable, state="readonly")
            cmbsel['values'] = ("FALSE", "TRUE")
            self.pins_str[i].mode_changeable.set(self.port_pins[i]["PortPinModeChangeable"])
            cmbsel.current()
            cmbsel.grid(row=self.header_size+i, column=7)
            self.non_header_objs.append(cmbsel)

        # Set the self.cv scrolling region
        self.cv.config(scrollregion=self.cv.bbox("all"))


    def draw(self, tab):
        tab.grid_rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)
        self.prf = tk.Frame(tab)
        self.prf.grid(sticky="news")

        # Create a frame for the canvas with non-zero row&column weights
        self.cvf = tk.Frame(self.prf)
        self.cvf.grid(row=2, column=0, pady=(5, 0), sticky='nw')
        self.cvf.grid_rowconfigure(0, weight=1)
        self.cvf.grid_columnconfigure(0, weight=1)

        # Set grid_propagate to False to allow canvas frame resizing later
        self.cvf.grid_propagate(False)

        # Add a canvas in that frame
        self.cv = tk.Canvas(self.cvf)
        self.cv.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.sb = tk.Scrollbar(self.cvf, orient="vertical", command=self.cv.yview)
        self.sb.grid(row=0, column=1, sticky='ns')
        self.cv.configure(yscrollcommand=self.sb.set)

        # Create a frame to draw task table
        self.mnf = tk.Frame(self.cv)
        self.cv.create_window((0, 0), window=self.mnf, anchor='nw')

        #Number of modes - Label + Spinbox
        label = tk.Label(self.mnf, text="No. of Pins:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.mnf, width=10, textvariable=self.n_pins_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_pins+1)))
        self.n_pins_str.set(self.n_pins)
        spinb.grid(row=0, column=1, sticky="w")

        # Save Button
        genm = tk.Button(self.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        genm.grid(row=0, column=2)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.mnf.update_idletasks()
        # Resize the main frame to show contents for FULL SCREEN (Todo: scroll bars won't work in reduced size window)
        canvas_w = tab.winfo_screenwidth()-self.sb.winfo_width()
        canvas_h = tab.winfo_screenheight()-(spinb.winfo_height()*6)
        self.cvf.config(width=canvas_w, height=canvas_h)

        # Table heading
        label = tk.Label(self.mnf, text=" ")
        label.grid(row=2, column=0, sticky="w")
        label = tk.Label(self.mnf, text="PortPinId")
        label.grid(row=2, column=1, sticky="w")
        label = tk.Label(self.mnf, text="PinDirection")
        label.grid(row=2, column=2, sticky="we")
        label = tk.Label(self.mnf, text="DirChangeable")
        label.grid(row=2, column=3, sticky="w")
        label = tk.Label(self.mnf, text="PinLevelValue")
        label.grid(row=2, column=4, sticky="w")
        label = tk.Label(self.mnf, text="PortPinMode")
        label.grid(row=2, column=5, sticky="w")
        label = tk.Label(self.mnf, text="PinInitialMode")
        label.grid(row=2, column=6, sticky="w")
        label = tk.Label(self.mnf, text="ModeChangeable")
        label.grid(row=2, column=7, sticky="w")

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

