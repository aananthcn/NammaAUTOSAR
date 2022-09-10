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
    xsize = None
    ysize = None
    

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
        self.xsize = xsize
        self.ysize = ysize
        self.scrollw = window.ScrollableWindow(tab, self.xsize, self.ysize)

        #Number of Events - Label + Spinbox
        label = tk.Label(self.mnf, text="No. of Events:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.mnf, width=10, textvariable=self.n_events_str, command=lambda: self.update_events(self.n_events_str),
                    values=tuple(range(0,self.max_events)))
        self.n_events_str.set(self.n_events)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

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
        self.scrollw.scroll()


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