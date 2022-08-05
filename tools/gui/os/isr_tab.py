import tkinter as tk
from tkinter import ttk

from .evt_wn import EventWindow


class IsrStr:
    id = 0
    name = None
    irqn = None
    category = None
    priority = None
    n_resources = None
    stack_size = None

    def __init__(self, id):
        self.id = id
        self.name = tk.StringVar()
        self.irqn = tk.StringVar()
        self.category = tk.StringVar()
        self.priority = tk.StringVar()
        self.n_resources = 0
        self.stack_size = tk.StringVar()

    def __del__(self):
        del self.name
        del self.irqn
        del self.category
        del self.priority
        del self.stack_size


class IsrTab:
    n_isrs = 0
    max_isrs = 1024
    n_isrs_str = None
    isrs_str = []
    resources = []
    sg_isrs = None
    HeaderObjs = 10 #Objects / widgets that are part of the header and shouldn't be destroyed
    HeaderSize = 3
    prf = None  # Parent Frame
    cvf = None  # Canvas Frame
    cv  = None  # Canvas
    sb  = None  # Scrollbar
    mnf = None  # Main Frame - where the widgets are scrolled

    active_dialog = None
    active_widget = None

    rstab = None
    mstab = None


    def __init__(self, isrs, rstab, mstab):
        self.sg_isrs = isrs
        # if not self.sg_isrs:
        #     nisr = self.create_empty_isr()
        #     self.sg_isrs.append(nisr)
        self.n_isrs = len(self.sg_isrs)
        self.n_isrs_str = tk.StringVar()
        del self.isrs_str[:]
        for i in range(self.n_isrs):
            self.isrs_str.insert(i, IsrStr(i))
        
        # collect all info from other tabs
        self.rstab = rstab
        self.mstab = mstab


    def __del__(self):
        del self.n_isrs_str
        del self.isrs_str[:]


    def create_empty_isr(self):
        isr = {}
        
        # Use the last isr's name and numbers to ease the edits made by user 
        isr["ISR Name"] = "ISR_"
        if not self.sg_isrs:
            isr["IRQn"] = "1"
        else:
            isr["IRQn"] = int(self.sg_isrs[len(self.sg_isrs)-1]["IRQn"]) + 1
        isr["CATEGORY"] = "1"
        isr["RESOURCE"] = []
        isr["OsIsrInterruptPriority"] = "0"
        isr["OsIsrStackSize"] = 0

        return isr


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

        # Create a frame to draw isr table
        self.mnf = tk.Frame(self.cv)
        self.cv.create_window((0, 0), window=self.mnf, anchor='nw')

        #Number of modes - Label + Spinbox
        label = tk.Label(self.mnf, text="No. of Tasks:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.mnf, width=10, textvariable=self.n_isrs_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_isrs+1)))
        self.n_isrs_str.set(self.n_isrs)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle isrs to let tkinter calculate buttons sizes
        self.mnf.update_idletasks()
        # Resize the main frame to show contents for FULL SCREEN (Todo: scroll bars won't work in reduced size window)
        canvas_w = tab.winfo_screenwidth()-self.sb.winfo_width()
        canvas_h = tab.winfo_screenheight()-(spinb.winfo_height()*6)
        # print("screen: "+str(tab.winfo_screenwidth())+" x "+str(tab.winfo_screenheight()))
        # print("canvas: "+str(canvas_w)+" x "+str(canvas_h))
        self.cvf.config(width=canvas_w, height=canvas_h)

        # Table heading
        label = tk.Label(self.mnf, text=" ")
        label.grid(row=2, column=0, sticky="w")
        label = tk.Label(self.mnf, text="ISR Name")
        label.grid(row=2, column=1, sticky="w")
        label = tk.Label(self.mnf, text="IRQn")
        label.grid(row=2, column=2, sticky="we")
        label = tk.Label(self.mnf, text="CATEGORY")
        label.grid(row=2, column=3, sticky="we")
        label = tk.Label(self.mnf, text="PRIORITY")
        label.grid(row=2, column=4, sticky="we")
        label = tk.Label(self.mnf, text="RESOURCE(S)")
        label.grid(row=2, column=5, sticky="we")
        label = tk.Label(self.mnf, text="STACK SIZE")
        label.grid(row=2, column=6, sticky="we")

        self.update()


    def update(self):
        # Backup current isr entries from GUI
        self.backup_data()

        # destroy most old gui widgets
        self.n_isrs = int(self.n_isrs_str.get())
        for i, item in enumerate(self.mnf.winfo_children()):
            if i >= self.HeaderObjs:
                item.destroy()

        # Tune memory allocations based on number of rows or boxes
        n_isrs_str = len(self.isrs_str)
        if self.n_isrs > n_isrs_str:
            for i in range(self.n_isrs - n_isrs_str):
                self.isrs_str.insert(len(self.isrs_str), IsrStr(n_isrs_str+i))
                self.sg_isrs.insert(len(self.sg_isrs), self.create_empty_isr())
        elif n_isrs_str > self.n_isrs:
            for i in range(n_isrs_str - self.n_isrs):
                del self.isrs_str[-1]
                del self.sg_isrs[-1]

        #print("n_isrs_str = "+ str(n_isrs_str) + ", n_isrs = " + str(self.n_isrs))
        # Draw new objects
        for i in range(0, self.n_isrs):
            label = tk.Label(self.mnf, text="ISR "+str(i)+": ")
            label.grid(row=self.HeaderSize+i, column=0, sticky="e")
            
            # ISR Name
            entry = tk.Entry(self.mnf, width=30, textvariable=self.isrs_str[i].name)
            self.isrs_str[i].name.set(self.sg_isrs[i]["ISR Name"])
            entry.grid(row=self.HeaderSize+i, column=1)

            # IRQn
            entry = tk.Entry(self.mnf, width=10, textvariable=self.isrs_str[i].irqn, justify='center')
            self.isrs_str[i].irqn.set(self.sg_isrs[i]["IRQn"])
            entry.grid(row=self.HeaderSize+i, column=2)

            # CATEGORY
            cmbsel = ttk.Combobox(self.mnf, width=8, textvariable=self.isrs_str[i].category, state="readonly", justify='center')
            cmbsel['values'] = ("1", "2")
            self.isrs_str[i].category.set(self.sg_isrs[i]["CATEGORY"])
            cmbsel.current()
            cmbsel.grid(row=self.HeaderSize+i, column=3)

            # PRIORITY
            entry = tk.Entry(self.mnf, width=10, textvariable=self.isrs_str[i].priority, justify='center')
            self.isrs_str[i].priority.set(self.sg_isrs[i]["OsIsrInterruptPriority"])
            entry.grid(row=self.HeaderSize+i, column=4)

            # RESOURCE[]
            if "RESOURCE" in self.sg_isrs[i]:
                self.isrs_str[i].n_resources = len(self.sg_isrs[i]["RESOURCE"])
            text = "Resources["+str(self.isrs_str[i].n_resources)+"]"
            select = tk.Button(self.mnf, width=12, text=text, command=lambda id = i: self.select_resources(id))
            select.grid(row=self.HeaderSize+i, column=5)

            # PRIORITY
            entry = tk.Entry(self.mnf, width=10, textvariable=self.isrs_str[i].stack_size, justify='center')
            self.isrs_str[i].stack_size.set(self.sg_isrs[i]["OsIsrStackSize"])
            entry.grid(row=self.HeaderSize+i, column=6)
            
        # Set the self.cv scrolling region
        self.cv.config(scrollregion=self.cv.bbox("all"))


    def backup_data(self):
        n_isrs_str = len(self.isrs_str)
        for i in range(n_isrs_str):
            if len(self.isrs_str[i].name.get()):
                self.sg_isrs[i]["ISR Name"] = self.isrs_str[i].name.get()
            if len(self.isrs_str[i].irqn.get()):
                self.sg_isrs[i]["IRQn"] = self.isrs_str[i].irqn.get()
            if len(self.isrs_str[i].category.get()):
                self.sg_isrs[i]["CATEGORY"] = self.isrs_str[i].category.get()
            if len(self.isrs_str[i].priority.get()):
                self.sg_isrs[i]["OsIsrInterruptPriority"] = self.isrs_str[i].priority.get()


    def on_resource_dialog_close(self, isr_id):
        # remove old selections
        if "RESOURCE" in self.sg_isrs[isr_id]:
            del self.sg_isrs[isr_id]["RESOURCE"][:]
        else:
            self.sg_isrs[isr_id]["RESOURCE"] = []

        # update new selections
        if len(self.active_widget.curselection()):
            for i in self.active_widget.curselection():
                self.sg_isrs[isr_id]["RESOURCE"].append(self.active_widget.get(i))
        
        # dialog elements are no longer needed, destroy them. Else, new dialogs will not open!
        self.active_widget.destroy()
        del self.active_widget
        self.active_dialog.destroy()
        del self.active_dialog

        # refresh screen
        self.update()


    def select_resources(self, id):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_resource_dialog_close(id))

        # show all app modes
        self.active_widget = tk.Listbox(self.active_dialog, selectmode=tk.MULTIPLE, width=40, height=15)
        for i, obj in enumerate(self.rstab.ress_str):
            res = obj.get()
            self.active_widget.insert(i, res)
            if "RESOURCE" in self.sg_isrs[id]:
                if res in self.sg_isrs[id]["RESOURCE"]:
                    self.active_widget.selection_set(i)
        self.active_widget.pack()


    # def on_message_dialog_close(self, isr_id):
    #     # remove old selections
    #     if "MESSAGE" in self.sg_isrs[isr_id]:
    #         del self.sg_isrs[isr_id]["MESSAGE"][:]
    #     else:
    #         self.sg_isrs[isr_id]["MESSAGE"] = []

    #     # update new selections
    #     if len(self.active_widget.curselection()):
    #         for i in self.active_widget.curselection():
    #             self.sg_isrs[isr_id]["MESSAGE"].append(self.active_widget.get(i))
        
    #     # dialog elements are no longer needed, destroy them. Else, new dialogs will not open!
    #     self.active_widget.destroy()
    #     del self.active_widget
    #     self.active_dialog.destroy()
    #     del self.active_dialog

    #     # refresh screen
    #     self.update()


    # def select_messages(self, id):
    #     if self.active_dialog != None:
    #         return

    #     # function to create dialog window
    #     self.active_dialog = tk.Toplevel() # create an instance of toplevel
    #     self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_message_dialog_close(id))

    #     # show all app modes
    #     self.active_widget = tk.Listbox(self.active_dialog, selectmode=tk.MULTIPLE, width=40, height=15)
    #     for i, obj in enumerate(self.mstab.msgs_str):
    #         msg = obj.get()
    #         self.active_widget.insert(i, msg)
    #         if "MESSAGE" in self.sg_isrs[id]:
    #             if msg in self.sg_isrs[id]["MESSAGE"]:
    #                 self.active_widget.selection_set(i)
    #     self.active_widget.pack()


