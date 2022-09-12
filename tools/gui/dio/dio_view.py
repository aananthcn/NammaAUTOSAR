#
# Created on Fri Sep 09 2022 8:37:10 PM
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

import arxml.port.arxml_port as arxml_port
import gui.dio.dio_cfg as dio_cfg
import gui.dio.dio_cfggen as dio_cfggen
import gui.dio.dio_chgrp as dio_chgrp


TabList = []
PortConfigViewActive = False


class DioTab:
    tab = None
    name = None



def dio_config_close_event(gui, view):
    global PortConfigViewActive

    PortConfigViewActive = False
    view.destroy()


    
def show_dio_tabs(gui):
    global PortConfigViewActive, TabList
    
    if PortConfigViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 45 / 100
    height = gui.main_view.ysize * 80 / 100
    view = tk.Toplevel()
    gui.main_view.child_window = view
    view.geometry("%dx%d+%d+%d" % (width, height, gui.main_view.xsize/3, 15))
    view.title("AUTOSAR Dio Configuration Tool")
    PortConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: dio_config_close_event(gui, view))
    notebook = ttk.Notebook(view)
    
    # Create tabs to configure Dio
    cfg_tab = ttk.Frame(notebook)
    cgr_tab = ttk.Frame(notebook)
    gen_tab = ttk.Frame(notebook)
    
    # Add tabs to configure Dio
    notebook.add(cfg_tab, text ='DioConfig')
    notebook.add(cgr_tab, text ='DioChannelGroup')
    notebook.add(gen_tab, text ='DioGeneral')
    notebook.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    for obj in TabList:
        del obj

    # create new GUI objects
    dtab = DioTab()
    dtab.tab = dio_cfg.DioConfigTab(gui)
    dtab.name = "DioConfig"
    dtab.tab.draw(cfg_tab, width, height)
    TabList.append(dtab)
    
    dtab = DioTab()
    dtab.tab = dio_chgrp.DioChannelGroupTab(gui)
    dtab.name = "DioChannelGroup"
    dtab.tab.draw(cgr_tab, width, height)
    
    dtab = DioTab()
    dtab.tab = dio_cfggen.DioGeneralTab(gui)
    dtab.name = "DioGeneral"
    dtab.tab.draw(gen_tab, width, height)

    # gui.main_view.window.bind("<<NotebookTabChanged>>", show_os_tab_switch)
    

# Main Entry Point
def dio_block_click_handler(gui):
    show_dio_tabs(gui)