#
# Created on Mon Dec 19 2022 7:18:20 AM
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

import gui.lin.lin_maincfg as lin_cfg

import arxml.lin.arxml_lin_parse as arxml_lin_r
import arxml.lin.arxml_lin_write as arxml_lin_w

import gui.lin.lin_code_gen as lin_cgen


TabList = []
LinConfigViewActive = False


class LinTab:
    tab = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h):
        self.save_cb = lin_save_callback
        self.frame = f
        self.xsize = w
        self.ysize = h



def lin_config_close_event(gui, view):
    global LinConfigViewActive

    LinConfigViewActive = False
    view.destroy()



def lin_save_callback(gui, lin_configs):
    arxml_lin_w.update_arxml(gui.arxml_file, lin_configs)
    lin_cgen.generate_code(gui, lin_configs)


    
def show_lin_tabs(gui):
    global LinConfigViewActive, TabList
    
    if LinConfigViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 30 / 100
    height = gui.main_view.ysize * 60 / 100
    view = tk.Toplevel()
    gui.main_view.child_window = view
    xoff = (gui.main_view.xsize - width)/2
    yoff = (gui.main_view.ysize - height)/3
    view.geometry("%dx%d+%d+%d" % (width, height, xoff, yoff))
    view.title("AUTOSAR Lin Driver Configuration Tool")
    LinConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: lin_config_close_event(gui, view))

    # destroy old GUI objects
    for obj in TabList:
        del obj

    # read Lin content from ARXML file
    lin_configs = arxml_lin_r.parse_arxml(gui.arxml_file)
    
    # create the main Lin GUI object
    lincfg_view = LinTab(view, width, height)
    lincfg_view.tab = lin_cfg.LinConfigMainView(gui, lin_configs, lincfg_view.save_cb)
    lincfg_view.name = "LinConfigs"
    TabList.append(lincfg_view)

    # Draw all tabs
    lincfg_view.tab.draw(lincfg_view)
    # gui.main_view.child_window.bind("<<NotebookTabChanged>>", show_os_tab_switch)



# Main Entry Point
def lin_block_click_handler(gui):
    show_lin_tabs(gui)