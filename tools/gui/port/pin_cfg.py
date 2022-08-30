import tkinter as tk
from tkinter import ttk


class PinStr:
    id = 0
    name = None

    def __init__(self, id):
        self.id = id
        self.name = tk.StringVar()

    def __del__(self):
        del self.name


class PortConfgSetTab:
    n_pins = 0
    max_pins = 65535
    n_pins_str = None

    pins_str = []
    events = []
    port_pins = None
    HeaderObjs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    HeaderSize = 3

    prf = None  # Parent Frame
    cvf = None  # Canvas Frame
    cv  = None  # Canvas
    sb  = None  # Scrollbar
    mnf = None  # Main Frame - where the widgets are scrolled

    active_dialog = None
    active_widget = None

    amtab = None
    rstab = None
    mstab = None


    def __init__(self):
        self.n_pins = 0
        self.n_pins_str = tk.StringVar()

    def __del__(self):
        del self.n_pins_str
        del self.pins_str[:]


    def create_empty_portpin(self):
        portpin = {}
        
        # Use the last task's name and numbers to ease the edits made by user 
        portpin["Task Name"] = "Task_"
        portpin["PRIORITY"] = "0"
        portpin["SCHEDULE"] = "NON" # Pre-emption (NON / FULL)
        portpin["ACTIVATION"] = "1"
        portpin["AUTOSTART"] = "FALSE"
        portpin["AUTOSTART_APPMODE"] = []
        portpin["RESOURCE"] = []
        portpin["EVENT"] = []
        portpin["MESSAGE"] = []
        portpin["STACK_SIZE"] = "512"

        return portpin


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

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.mnf.update_idletasks()
        # Resize the main frame to show contents for FULL SCREEN (Todo: scroll bars won't work in reduced size window)
        canvas_w = tab.winfo_screenwidth()-self.sb.winfo_width()
        canvas_h = tab.winfo_screenheight()-(spinb.winfo_height()*6)
        self.cvf.config(width=canvas_w, height=canvas_h)

        # Table heading
        label = tk.Label(self.mnf, text=" ")
        label.grid(row=2, column=0, sticky="w")
        label = tk.Label(self.mnf, text="Task Name")
        label.grid(row=2, column=1, sticky="w")
        label = tk.Label(self.mnf, text="PRIORITY")
        label.grid(row=2, column=2, sticky="we")
        label = tk.Label(self.mnf, text="PREMPTION")
        label.grid(row=2, column=3, sticky="we")
        label = tk.Label(self.mnf, text="ACTIVATION")
        label.grid(row=2, column=4, sticky="we")
        label = tk.Label(self.mnf, text="AUTOSTART[]")
        label.grid(row=2, column=5, sticky="we")
        label = tk.Label(self.mnf, text="EVENT[]")
        label.grid(row=2, column=6, sticky="we")
        label = tk.Label(self.mnf, text="RESOURCE[]")
        label.grid(row=2, column=7, sticky="we")
        label = tk.Label(self.mnf, text="MESSAGE[]")
        label.grid(row=2, column=8, sticky="we")
        label = tk.Label(self.mnf, text="Stack Size")
        label.grid(row=2, column=9, sticky="we")

        self.update()


    def update(self):
        # Backup current task entries from GUI
        self.backup_data()

        # destroy most old gui widgets
        self.n_pins = int(self.n_pins_str.get())
        for i, item in enumerate(self.mnf.winfo_children()):
            if i >= self.HeaderObjs:
                item.destroy()

        # Tune memory allocations based on number of rows or boxes
        n_pins_str = len(self.pins_str)
        if self.n_pins > n_pins_str:
            for i in range(self.n_pins - n_pins_str):
                self.pins_str.insert(len(self.pins_str), PinStr(n_pins_str+i))
                self.port_pins.insert(len(self.port_pins), self.create_empty_portpin())
        elif n_pins_str > self.n_pins:
            for i in range(n_pins_str - self.n_pins):
                del self.pins_str[-1]
                del self.port_pins[-1]

        #print("n_pins_str = "+ str(n_pins_str) + ", n_pins = " + str(self.n_pins))
        # Draw new objects
        for i in range(0, self.n_pins):
            label = tk.Label(self.mnf, text="Task "+str(i)+": ")
            label.grid(row=self.HeaderSize+i, column=0, sticky="e")
            
            # Task Name
            entry = tk.Entry(self.mnf, width=30, textvariable=self.pins_str[i].name)
            self.pins_str[i].name.set(self.port_pins[i]["Task Name"])
            entry.grid(row=self.HeaderSize+i, column=1)

            # PRIORITY
            entry = tk.Entry(self.mnf, width=10, textvariable=self.pins_str[i].prio, justify='center')
            self.pins_str[i].prio.set(self.port_pins[i]["PRIORITY"])
            entry.grid(row=self.HeaderSize+i, column=2)

            # SCHEDULE
            cmbsel = ttk.Combobox(self.mnf, width=8, textvariable=self.pins_str[i].schedule, state="readonly")
            cmbsel['values'] = ("NON", "FULL")
            self.pins_str[i].schedule.set(self.port_pins[i]["SCHEDULE"])
            cmbsel.current()
            cmbsel.grid(row=self.HeaderSize+i, column=3)

            # ACTIVATION
            entry = tk.Entry(self.mnf, width=11, textvariable=self.pins_str[i].activation, justify='center')
            self.pins_str[i].activation.set(self.port_pins[i]["ACTIVATION"])
            entry.grid(row=self.HeaderSize+i, column=4)

            # AUTOSTART[]
            if "AUTOSTART_APPMODE" in self.port_pins[i]:
                self.pins_str[i].n_appmod = len(self.port_pins[i]["AUTOSTART_APPMODE"])
            text = "AppModes["+str(self.pins_str[i].n_appmod)+"]"
            select = tk.Button(self.mnf, width=13, text=text, command=lambda id = i: self.select_autostart_modes(id))
            select.grid(row=self.HeaderSize+i, column=5)

            # EVENT[]
            if "EVENT" in self.port_pins[i]:
                self.pins_str[i].n_events = len(self.port_pins[i]["EVENT"])
            text = "Events["+str(self.pins_str[i].n_events)+"]"
            select = tk.Button(self.mnf, width=13, text=text, command=lambda id = i: self.select_events(id))
            select.grid(row=self.HeaderSize+i, column=6)

            # RESOURCE[]
            if "RESOURCE" in self.port_pins[i]:
                self.pins_str[i].n_resources = len(self.port_pins[i]["RESOURCE"])
            text = "Resources["+str(self.pins_str[i].n_resources)+"]"
            select = tk.Button(self.mnf, width=13, text=text, command=lambda id = i: self.select_resources(id))
            select.grid(row=self.HeaderSize+i, column=7)

            # MESSAGE[]
            if "MESSAGE" in self.port_pins[i]:
                self.pins_str[i].n_messages = len(self.port_pins[i]["MESSAGE"])
            text = "Messages["+str(self.pins_str[i].n_messages)+"]"
            select = tk.Button(self.mnf, width=13, text=text, command=lambda id = i: self.select_messages(id))
            select.grid(row=self.HeaderSize+i, column=8)
            
            # STACK_SIZE
            entry = tk.Entry(self.mnf, width=11, textvariable=self.pins_str[i].stack_sz, justify='center')
            self.pins_str[i].stack_sz.set(self.port_pins[i]["STACK_SIZE"])
            entry.grid(row=self.HeaderSize+i, column=9)

        # Set the self.cv scrolling region
        self.cv.config(scrollregion=self.cv.bbox("all"))


    def backup_data(self):
        n_pins_str = len(self.pins_str)
        # print("tsk_cfg.py: backup_data called! || n_pins_str = "+ str(n_pins_str))
        for i in range(n_pins_str):
            if len(self.pins_str[i].name.get()):
                self.port_pins[i]["Task Name"] = self.pins_str[i].name.get()
            if len(self.pins_str[i].prio.get()):
                self.port_pins[i]["PRIORITY"] = self.pins_str[i].prio.get()
            if len(self.pins_str[i].schedule.get()):
                self.port_pins[i]["SCHEDULE"] = self.pins_str[i].schedule.get()
            if len(self.pins_str[i].activation.get()):
                self.port_pins[i]["ACTIVATION"] = self.pins_str[i].activation.get()
            if "AUTOSTART_APPMODE" in self.port_pins[i]:
                if len(self.port_pins[i]["AUTOSTART_APPMODE"]):
                    self.port_pins[i]["AUTOSTART"] = "TRUE"
                else:
                    self.port_pins[i]["AUTOSTART"] = "FALSE"
            else:
                self.port_pins[i]["AUTOSTART"] = "FALSE"
            if len(self.pins_str[i].stack_sz.get()):
                self.port_pins[i]["STACK_SIZE"] = self.pins_str[i].stack_sz.get()
                # print(self.port_pins[i]["STACK_SIZE"])

