import tkinter as tk
from tkinter import ttk



class ResourceTab:
    n_ress = 1
    max_ress = 1024
    n_ress_str = None
    ress_str = []
    ress = []
    HeaderObjs = 2 #Objects / widgets that are part of the header and shouldn't be destroyed
    HeaderSize = 1
    prf = None  # Parent Frame
    cvf = None  # Canvas Frame
    cv  = None  # Canvas
    sb  = None  # Scrollbar
    mnf = None  # Main Frame - where the widgets are scrolled


    def __init__(self, tasks):
        self.extract_resources(tasks)
        self.n_ress = len(self.ress)
        self.n_ress_str = tk.StringVar()
        del self.ress_str[:]
        for i in range(self.n_ress):
            self.ress_str.insert(i, tk.StringVar())
            self.ress_str[i].set(self.ress[i])


    def __del__(self):
        del self.n_ress_str
        del self.ress_str[:]


    def update_ress(self, mstr):
        self.n_ress = int(mstr.get())
        # print("Update resources: "+ str(self.n_ress))        
        for i, item in enumerate(self.mnf.winfo_children()):
            if i >= self.HeaderObjs:
                item.destroy()
        self.update()


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

        # Create a frame to draw resource table
        self.mnf = tk.Frame(self.cv)
        self.cv.create_window((0, 0), window=self.mnf, anchor='nw')

        #Number of modes - Label + Spinbox
        label = tk.Label(self.mnf, text="No. of Resources:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.mnf, width=10, textvariable=self.n_ress_str, command=lambda: self.update_ress(self.n_ress_str),
                    values=tuple(range(1,self.max_ress+1)))
        self.n_ress_str.set(self.n_ress)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.mnf.update_idletasks()
        # Resize the main frame to show contents for FULL SCREEN (Todo: scroll bars won't work in reduced size window)
        canvas_w = tab.winfo_screenwidth()-self.sb.winfo_width()
        canvas_h = tab.winfo_screenheight()-(spinb.winfo_height()*6)
        # print("screen: "+str(tab.winfo_screenwidth())+" x "+str(tab.winfo_screenheight()))
        # print("canvas: "+str(canvas_w)+" x "+str(canvas_h))
        self.cvf.config(width=canvas_w, height=canvas_h)

        self.update()


    def update(self):
        # Backup current entries
        self.backup_data()

        # Tune memory allocations based on number of rows or boxes
        n_ress_str = len(self.ress_str)
        if self.n_ress > n_ress_str:
            for i in range(self.n_ress - n_ress_str):
                self.ress_str.insert(len(self.ress_str), tk.StringVar())
                self.ress.insert(len(self.ress), "RES_")
        elif n_ress_str > self.n_ress:
            for i in range(n_ress_str - self.n_ress):
                del self.ress_str[-1]
                del self.ress[-1]

        #print("n_ress_str = "+ str(n_ress_str) + ", n_ress = " + str(self.n_ress))
        # Draw new objects
        for i in range(0, self.n_ress):
            label = tk.Label(self.mnf, text="Msg "+str(i)+": ")
            label.grid(row=self.HeaderSize+i, column=0, sticky="w")
            entry = tk.Entry(self.mnf, width=40, textvariable=self.ress_str[i])
            self.ress_str[i].set(self.ress[i])
            entry.grid(row=self.HeaderSize+i, column=1)

        # Set the self.cv scrolling region
        self.cv.config(scrollregion=self.cv.bbox("all"))


    def backup_data(self):
        n_ress_str = len(self.ress_str)
        for i in range(n_ress_str):
            self.ress[i] = self.ress_str[i].get()


    def extract_resources(self, tasks):
        for task in tasks:
            if "RESOURCE" in task:
                for res in task["RESOURCE"]:
                    if res not in self.ress:
                        self.ress.append(res)

        # OSEK spec mandates having RES_SCHEDULER as the default/1st resource.
        if "RES_SCHEDULER" not in self.ress:
            self.ress.insert(0, "RES_SCHEDULER")

        return tasks