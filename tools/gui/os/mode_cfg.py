#
# Created on Sun Oct 02 2022 10:06:55 AM
#
# The MIT License (MIT)
# Copyright (c) 2022 Aananth C N
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import tkinter as tk
from tkinter import ttk

class AmTab:
    N_AppModes = 1
    N_AppModes_str = None
    AppModes = None
    MaxAppModes = 16
    header_row = 2
    n_header_objs = 2 #Objects / widgets that are part of the header and shouldn't be destroyed
    AM_StrVar = []

    def __init__(self, appmodes):
        self.N_AppModes_str = tk.StringVar()
        self.AppModes = appmodes
        if "OSDEFAULTAPPMODE" not in self.AppModes:
            self.AppModes.insert(0, "OSDEFAULTAPPMODE")
        self.N_AppModes = len(appmodes)
        n_strvar = self.N_AppModes
        self.destroy_old_strvars()
        for i in range(n_strvar):
            self.AM_StrVar.insert(i, tk.StringVar())
            self.AM_StrVar[i].set(self.AppModes[i])

    def __del__(self):
        self.destroy_old_strvars()
        self.AppModes = None
        self.N_AppModes = 1


    def destroy_old_strvars(self):
        del self.AM_StrVar[:]


    def update_am(self, tab, am_str):
        self.N_AppModes = int(am_str.get())
        for i, item in enumerate(tab.winfo_children()):
            if i >= self.n_header_objs:
                item.destroy()
        self.update(tab)
        

    def draw(self, tab):
        #Number of modes - Label + Spinbox
        label = tk.Label(tab, text="Number of Modes ")
        label.grid(row=1, column=1, sticky="w")
        spinb = tk.Spinbox(tab, width=28, values=tuple(range(1,self.MaxAppModes+1)), textvariable=self.N_AppModes_str, 
                        command=lambda: self.update_am(tab, self.N_AppModes_str))
        self.N_AppModes_str.set(self.N_AppModes)
        spinb.grid(row=1, column=2)
        self.update(tab)    

            
    def update(self, tab):
        # Backup current entries
        self.backup_data()

        # StrVar memory allocation checks
        n_am_strvar = len(self.AM_StrVar)
        if self.N_AppModes > n_am_strvar:
            for i in range(self.N_AppModes - n_am_strvar):
                self.AM_StrVar.insert(len(self.AM_StrVar), tk.StringVar())
                self.AppModes.insert(len(self.AppModes), "AM_")
        elif n_am_strvar > self.N_AppModes:
            # print("n_am_strvar = "+ str(n_am_strvar) + ", N_AppModes = " + str(self.N_AppModes))
            for i in range(n_am_strvar - self.N_AppModes):
                del self.AM_StrVar[-1]
                del self.AppModes[-1]

        # Draw new objects
        for i in range(0, self.N_AppModes):
            label = tk.Label(tab, text="Mode "+str(i)+": ")
            label.grid(row=self.header_row+i, column=1, sticky="w")
            entry = tk.Entry(tab, width=30, textvariable=self.AM_StrVar[i])
            self.AM_StrVar[i].set(self.AppModes[i])
            entry.grid(row=self.header_row+i, column=2)


    def backup_data(self):
        n_am_strvar = len(self.AM_StrVar)
        for i in range(n_am_strvar):
            self.AppModes[i] = self.AM_StrVar[i].get()
