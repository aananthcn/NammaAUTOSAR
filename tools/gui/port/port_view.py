#
# Created on Tue Aug 30 2022 10:19:34 PM
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

import gui.port.pin_cfg as pin_cfg
import arxml.port.arxml_port as arxml_port


TabList = []
PortConfigViewActive = False


class PortTab:
    tab = None
    name = None



def port_config_close_event(gui, view):
    global PortConfigViewActive

    PortConfigViewActive = False
    view.destroy()


    
def show_port_config(gui):
    global PortConfigViewActive, TabList
    
    if PortConfigViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 80 / 100
    height = gui.main_view.ysize * 80 / 100
    view = tk.Toplevel()
    view.geometry("%dx%d+%d+%d" % (width, height, width/5, 15))
    view.title("AUTOSAR Port Configuration Tool")
    PortConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: port_config_close_event(gui, view))
    gui.main_view.child_window = ttk.Notebook(view)
    
    # Create tabs to configure OS
    cs_tab = ttk.Frame(gui.main_view.child_window)
    
    # Add tabs to configure OS
    gui.main_view.child_window.add(cs_tab, text ='PortConfigSet')
    gui.main_view.child_window.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    for obj in TabList:
        del obj

    # parse port info from arxml file
    pins, pin_info = arxml_port.parse_arxml(gui.arxml_file)

    # create new GUI objects
    ptab = PortTab()
    ptab.tab = pin_cfg.PortConfigSetTab(gui)
    if pins > 0:
        ptab.tab.init(pins, pin_info)
    ptab.name = "PortConfigSet"
    ptab.tab.draw(cs_tab, width, height)
    TabList.append(ptab)

    # gui.main_view.window.bind("<<NotebookTabChanged>>", show_os_tab_switch)
    

# Main Entry Point
def port_block_click_handler(gui):
    show_port_config(gui)