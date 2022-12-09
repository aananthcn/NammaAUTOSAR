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
import arxml.dio.arxml_dio_write as arxml_dio

import gui.dio.dio_cfg as dio_cfg
import gui.dio.dio_gen as dio_gen
import gui.dio.dio_grp as dio_grp
import gui.dio.dio_code_gen as dio_code_gen


TabList = []
DioConfigViewActive = False


class DioTab:
    tab = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h):
        self.save_cb = dio_save_callback
        self.frame = f
        self.xsize = w
        self.ysize = h

    def __del__(self):
        del self.tab
        del self.frame


def dio_config_close_event(gui, view):
    global DioConfigViewActive, TabList

    DioConfigViewActive = False
    view.destroy()


def dio_save_callback(gui):
    global TabList
    dio_cfg = None
    dio_grp = None
    dio_gen = None
    for tab in TabList:
        if tab.name == "DioConfig":
            dio_cfg = []
            for cfg in tab.tab.configs:
                dio_cfg.append(cfg.get())
            continue
        if tab.name == "DioChannelGroup":
            dio_grp = []
            for cfg in tab.tab.configs:
                dio_grp.append(cfg.get())
            continue
        if tab.name == "DioGeneral":
            dio_gen = tab.tab.configs[0].get()
            continue
    arxml_dio.update_arxml(gui.arxml_file, dio_cfg, dio_grp, dio_gen)
    dio_code_gen.generate_code(gui)



def show_dio_tabs(gui):
    global DioConfigViewActive, TabList
    
    if DioConfigViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 45 / 100
    height = gui.main_view.ysize * 80 / 100
    view = tk.Toplevel()
    gui.main_view.child_window = view
    view.geometry("%dx%d+%d+%d" % (width, height, gui.main_view.xsize/3, 15))
    view.title("AUTOSAR Dio Configuration Tool")
    DioConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: dio_config_close_event(gui, view))
    notebook = ttk.Notebook(view)
    
    # Create tabs to configure Dio
    cfg_frame = ttk.Frame(notebook)
    cgr_frame = ttk.Frame(notebook)
    gen_frame = ttk.Frame(notebook)
    
    # Add tabs to configure Dio
    notebook.add(cfg_frame, text ='DioConfig')
    notebook.add(cgr_frame, text ='DioChannelGroup')
    notebook.add(gen_frame, text ='DioGeneral')
    notebook.pack(expand = 1, fill ="both")

    # # destroy old GUI objects
    del TabList[:]

    # create new GUI objects
    dtab = DioTab(cfg_frame, width, height)
    dtab.tab = dio_cfg.DioConfigTab(gui)
    dtab.name = "DioConfig"
    TabList.append(dtab)
    dtab.tab.draw(dtab)
    
    dtab = DioTab(cgr_frame, width, height)
    dtab.tab = dio_grp.DioChannelGroupTab(gui)
    dtab.name = "DioChannelGroup"
    TabList.append(dtab)
    dtab.tab.draw(dtab)
    
    dtab = DioTab(gen_frame, width, height)
    dtab.tab = dio_gen.DioGeneralTab(gui)
    dtab.name = "DioGeneral"
    TabList.append(dtab)
    dtab.tab.draw(dtab)

    # gui.main_view.window.bind("<<NotebookTabChanged>>", show_os_tab_switch)
    

# Main Entry Point
def dio_block_click_handler(gui):
    show_dio_tabs(gui)