#
# Created on Fri Oct 07 2022 6:46:16 AM
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



###############################################################################
# AUTOSAR Configuration Strings (tkinter strings)
###############################################################################
class AsrCfgStr:
    # dispvar - display variable associated with the entry widget
    dispvar = None
	# datavar - string variable that contains the data
    datavar = None

    # initialize keys and create display (tkinter string) objects
    def __init__(view, headings, values):
        view.dispvar = {}
        view.datavar = {}
        # if headings == None or values == None or len(headings) > len(values):
        if headings == None or values == None:
            print("ConfigStr.__init__(): invalid argument!")
            return
        
        for key in headings:
            view.dispvar[key] = tk.StringVar()
            if key in values:
                view.datavar[key] = values[key]
            else:
                view.datavar[key] = None

    # remove all tkinter string objects
    def __del__(view):
        for key in view.dispvar:
            view.dispvar[key].__del__()
        del view.dispvar
        del view.datavar

    def set(view, values):
        # if values == None or len(view.dispvar) > len(values):
        if values == None:
            print("ConfigStr.set(): invalid argument!")
            return

        for key in view.dispvar:
            view.dispvar[key].set(values[key])

    def get(view):
        for key in view.dispvar:
            if isinstance(view.datavar[key], str):
	            view.datavar[key] = view.dispvar[key].get()
        return view.datavar




###############################################################################
# Scrollable Widgets
###############################################################################
def label(view, label, row, col, align):
    label = tk.Label(view.scrollw.mnf, text=label)
    label.grid(row=row, column=col, sticky=align)
    # view.non_header_objs.append(label)
    insert_widget_to_nh_objs(row, col, view, label)
    return label


def entry(view, key, index, row, col, width, state):
    entry = tk.Entry(view.scrollw.mnf, width=width, textvariable=view.configs[index].dispvar[key], state=state)
    view.configs[index].dispvar[key].set(view.configs[index].datavar[key])
    entry.grid(row=row, column=col)
    # view.non_header_objs.append(entry)
    insert_widget_to_nh_objs(row, col, view, entry)
    return entry


def combo(view, key, index, row, col, width, values):
    cmbsel = ttk.Combobox(view.scrollw.mnf, width=width, textvariable=view.configs[index].dispvar[key], state="readonly")
    cmbsel['values'] = values
    view.configs[index].dispvar[key].set(view.configs[index].datavar[key])
    cmbsel.current()
    cmbsel.grid(row=row, column=col)
    # view.non_header_objs.append(cmbsel)
    insert_widget_to_nh_objs(row, col, view, cmbsel)
    return cmbsel


def spinb(view, key, index, row, col, width, values):
    spinb = tk.Spinbox(view.scrollw.mnf, width=width, textvariable=view.configs[index].dispvar[key], values=values)
    view.configs[index].dispvar[key].set(view.configs[index].datavar[key])
    spinb.grid(row=row, column=col)
    # view.non_header_objs.append(spinb)
    insert_widget_to_nh_objs(row, col, view, spinb)
    return spinb


def button(view, key, index, row, col, width, text, cb):
    select = tk.Button(view.scrollw.mnf, width=width, text=text, command=lambda id = index : cb(id))
    view.configs[index].dispvar[key].set(view.configs[index].datavar[key])
    select.grid(row=row, column=col)
    # view.non_header_objs.append(select)
    insert_widget_to_nh_objs(row, col, view, select)
    return select



###############################################################################
# Asr Widget Utilities
###############################################################################
def insert_widget_to_nh_objs(row, col, view, widget):
    # last point - kadeysee edam
    lastp = len(view.non_header_objs)
    # insert point 
    instp = (row - view.header_row) * view.dappas_per_row + col
    
    # warn if the user trying to insert beyond the append point (i.e., max_row = 4, but ins_row = 6 or 5)
    if instp > lastp and view.header_orientation == "h":
        print("Error: view with following config keys, trying to insert beyond limit")
        print("\t", view.cfgkeys)
        print("insert point:", instp)
        print("last point:", lastp)
        print("row = ", row, "col = ", col)
        instp = lastp
    
    view.non_header_objs.insert(instp, widget)


def delete_dappa_row(view, row):
    beg = row * view.dappas_per_row
    end = beg+view.dappas_per_row
    #print("dappas:",view.dappas_per_row, "row:", row, "beg:", beg, "end:", end, "total:", len(view.non_header_objs))

    # go in reverse loop as you delete the entries, the index may go out of range
    for x in reversed(range(beg, end)):
        #print("index:", x, "total:", len(view.non_header_objs))
        view.non_header_objs[x].destroy()
        del view.non_header_objs[x]


def button_selections(view, idx, cfg_label):
    n_btn_entries = 0
    if idx < len(view.configs) and view.configs[idx].datavar[cfg_label]:
        n_btn_entries = len(view.configs[idx].datavar[cfg_label])
    return n_btn_entries


###############################################################################
# headings and column-headings
###############################################################################
def place_heading(view, row, col):
    # place all the keys as column @row & @col
    for i, label in enumerate(view.cfgkeys):
        label = tk.Label(view.scrollw.mnf, text=label)
        label.grid(row=row, column=col+i, sticky="w")
    
    # store the number of widgets including the header labels
    view.n_header_objs = len(view.scrollw.mnf.winfo_children())
    view.header_row = row+1
    view.header_orientation = "h"  # horizontal


def place_column_heading(view, row, col):
    # place all the keys as column @row & @col
    for i, label in enumerate(view.cfgkeys):
        label = tk.Label(view.scrollw.mnf, text=label)
        label.grid(row=row+i, column=col, sticky="e")

    # for column heading, the concept of header or row is invalid, hence 0
    view.n_header_objs = 0
    view.header_row = 0
    view.dappas_per_row = 0
    view.header_orientation = "v"  # vertical