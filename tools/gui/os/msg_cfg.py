import tkinter as tk
from tkinter import ttk

import gui.lib.window as window


class MessageTab:
    n_msgs = 0
    max_msgs = 4*1024
    n_msgs_str = None
    msgs_str = []
    msgs = []
    HeaderObjs = 2 #Objects / widgets that are part of the header and shouldn't be destroyed
    HeaderSize = 1
    xsize = None
    ysize = None

    def __init__(self, tasks):
        self.extract_messages(tasks)
        self.n_msgs = len(self.msgs)
        self.n_msgs_str = tk.StringVar()
        del self.msgs_str[:]
        for i in range(self.n_msgs):
            self.msgs_str.insert(i, tk.StringVar())
            self.msgs_str[i].set(self.msgs[i])


    def __del__(self):
        del self.n_msgs_str
        del self.msgs_str[:]


    def update_msgs(self, mstr):
        self.n_msgs = int(mstr.get())
        # print("Update messages: "+ str(self.n_msgs))        
        for i, item in enumerate(self.scrollw.mnf.winfo_children()):
            if i >= self.HeaderObjs:
                item.destroy()
        self.update()


    def draw(self, tab, xsize, ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.scrollw = window.ScrollableWindow(tab, self.xsize, self.ysize)

        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. of Messages:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_msgs_str, command=lambda: self.update_msgs(self.n_msgs_str),
                    values=tuple(range(0,self.max_msgs)))
        self.n_msgs_str.set(self.n_msgs)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()
        self.update()


    def update(self):
        # backup current entries
        self.backup_data()

        # Tune memory allocations based on number of rows or boxes
        n_msgs_str = len(self.msgs_str)
        if self.n_msgs > n_msgs_str:
            for i in range(self.n_msgs - n_msgs_str):
                self.msgs_str.insert(len(self.msgs_str), tk.StringVar())
                self.msgs.insert(len(self.msgs), "MSG_")
        elif n_msgs_str > self.n_msgs:
            for i in range(n_msgs_str - self.n_msgs):
                del self.msgs_str[-1]
                del self.msgs[-1]

        #print("n_msgs_str = "+ str(n_msgs_str) + ", n_msgs = " + str(self.n_msgs))
        # Draw new objects
        for i in range(0, self.n_msgs):
            label = tk.Label(self.scrollw.mnf, text="Msg "+str(i)+": ")
            label.grid(row=self.HeaderSize+i, column=0, sticky="w")
            entry = tk.Entry(self.scrollw.mnf, width=40, textvariable=self.msgs_str[i])
            self.msgs_str[i].set(self.msgs[i])
            entry.grid(row=self.HeaderSize+i, column=1)

        # Set the self.cv scrolling region
        self.scrollw.scroll()


    def backup_data(self):
        n_msgs_str = len(self.msgs_str)
        for i in range(n_msgs_str):
            self.msgs[i] = self.msgs_str[i].get()


    def extract_messages(self, tasks):
        for task in tasks:
            if "MESSAGE" in task:
                for msg in task["MESSAGE"]:
                    if msg not in self.msgs:
                        self.msgs.append(msg)
        return tasks