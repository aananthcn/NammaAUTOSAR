import tkinter as tk
from tkinter import ttk

from copy import copy



class EventWindow:
    n_events = 1
    max_events = 64
    n_events_str = None
    events_str = []
    events = []
    HeaderObjs = 2 #Objects / widgets that are part of the header and shouldn't be destroyed
    HeaderSize = 1
    prf = None  # Parent Frame
    cvf = None  # Canvas Frame
    cv  = None  # Canvas
    sb  = None  # Scrollbar
    mnf = None  # Main Frame - where the widgets are scrolled

    def __init__(self, task):
        self.extract_events(task)
        # print("constructor: " + str(self.events))
        self.n_events = len(self.events)
        self.n_events_str = tk.StringVar()
        for i in range(self.n_events):
            self.events_str.insert(i, tk.StringVar())
            self.events_str[i].set(self.events[i])

    def __del__(self):
        del self.n_events_str
        del self.events_str[:]

    def update_events(self, mstr):
        self.n_events = int(mstr.get())
        # print("Update events: "+ str(self.n_events))        
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

        #Number of Events - Label + Spinbox
        label = tk.Label(self.mnf, text="No. of Events:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.mnf, width=10, textvariable=self.n_events_str, command=lambda: self.update_events(self.n_events_str),
                    values=tuple(range(0,self.max_events)))
        self.n_events_str.set(self.n_events)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.mnf.update_idletasks()
        # Resize the main frame to show contents for FULL SCREEN (Todo: scroll bars won't work in reduced size window)
        canvas_w = tab.winfo_screenwidth()/2-(3*self.sb.winfo_width())
        canvas_h = tab.winfo_screenheight()*14/16-(spinb.winfo_height()*6)
        # print("screen: "+str(tab.winfo_screenwidth())+" x "+str(tab.winfo_screenheight()))
        # print("canvas: "+str(canvas_w)+" x "+str(canvas_h))
        self.cvf.config(width=canvas_w, height=canvas_h)

        self.update()


    def update(self):
        # backup current entries
        self.backup_data()

        # Tune memory allocations based on number of rows or boxes
        n_events_str = len(self.events_str)
        if self.n_events > n_events_str:
            for i in range(self.n_events - n_events_str):
                self.events_str.insert(len(self.events_str), tk.StringVar())
                self.events.insert(len(self.events), "EVT_")
        elif n_events_str > self.n_events:
            for i in range(n_events_str - self.n_events):
                del self.events_str[-1]
                del self.events[-1]

        # print("n_events_str = "+ str(n_events_str) + ", n_events = " + str(self.n_events))
        # Draw new objects
        for i in range(0, self.n_events):
            label = tk.Label(self.mnf, text="Event "+str(i)+": ")
            label.grid(row=self.HeaderSize+i, column=0, sticky="w")
            entry = tk.Entry(self.mnf, width=40, textvariable=self.events_str[i])
            self.events_str[i].set(self.events[i])
            entry.grid(row=self.HeaderSize+i, column=1)

        # Set the self.cv scrolling region
        self.cv.config(scrollregion=self.cv.bbox("all"))


    def backup_data(self):
        n_events_str = len(self.events_str)
        for i in range(n_events_str):
            self.events[i] = self.events_str[i].get()


    def extract_events(self, task):
        if "EVENT" in task:
            # print(task["EVENT"])
            self.events = copy(task["EVENT"])
        else:
            self.events = []