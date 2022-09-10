import tkinter as tk
from tkinter import ttk

import gui.lib.window as window



class ResourceTab:
    n_ress = 1
    max_ress = 1024
    n_ress_str = None
    ress_str = []
    ress = []
    HeaderObjs = 2 #Objects / widgets that are part of the header and shouldn't be destroyed
    HeaderSize = 1
    xsize = None
    ysize = None

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
        for i, item in enumerate(self.scrollw.mnf.winfo_children()):
            if i >= self.HeaderObjs:
                item.destroy()
        self.update()


    def draw(self, tab, xsize, ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.scrollw = window.ScrollableWindow(tab, self.xsize, self.ysize)

        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Resources:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_ress_str, command=lambda: self.update_ress(self.n_ress_str),
                    values=tuple(range(1,self.max_ress+1)))
        self.n_ress_str.set(self.n_ress)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

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
            label = tk.Label(self.scrollw.mnf, text="Msg "+str(i)+": ")
            label.grid(row=self.HeaderSize+i, column=0, sticky="w")
            entry = tk.Entry(self.scrollw.mnf, width=40, textvariable=self.ress_str[i])
            self.ress_str[i].set(self.ress[i])
            entry.grid(row=self.HeaderSize+i, column=1)

        # Set the self.cv scrolling region
        self.scrollw.scroll()


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