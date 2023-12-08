#
# Created on Sat Jan 14 2023 9:57:00 PM
#
# The MIT License (MIT)
# Copyright (c) 2023 Aananth C N
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

import gui.ethif.ethif_gen as ethif_gen
import gui.ethif.ethif_configset as ethif_cs

import arxml.ethif.arxml_ethif_parse as arxml_ethif_r
import arxml.ethif.arxml_ethif_write as arxml_ethif_w

import gui.ethif.ethif_code_gen as ethif_cgen


TabList = []
EthIfConfigViewActive = False


class EthIfTab:
    tab = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h):
        self.save_cb = ethif_save_callback
        self.frame = f
        self.xsize = w
        self.ysize = h



def ethif_config_close_event(gui, view):
    global EthIfConfigViewActive

    EthIfConfigViewActive = False
    view.destroy()



def ethif_save_callback(gui):
    ethif_configs = {}

    # pull all configs from UI tabs
    for tab in TabList:
	    # backup configs (i.e, pull from dispvar to datavar)
        for cfg in tab.tab.configs:
            cfg.get()

        # copy to configs to dict
        ethif_configs[tab.name] = tab.tab.configs

    # write to file
    arxml_ethif_w.update_arxml(gui.arxml_file, ethif_configs)

    # generate code
    ethif_cgen.generate_code(gui, ethif_configs)


    
def show_ethif_tabs(gui):
    global EthIfConfigViewActive, TabList
    
    if EthIfConfigViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 50 / 100
    height = gui.main_view.ysize * 55 / 100
    view = tk.Toplevel()
    gui.main_view.child_window = view
    xoff = (gui.main_view.xsize - width)/2
    yoff = (gui.main_view.ysize - height)/3
    view.geometry("%dx%d+%d+%d" % (width, height, xoff, yoff))
    view.title("AUTOSAR Ethernet Interface Configuration Tool")
    EthIfConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: ethif_config_close_event(gui, view))
    notebook = ttk.Notebook(view)

    # Create tabs to configure EthIf
    gen_frame = ttk.Frame(notebook)
    cfg_frame = ttk.Frame(notebook)
    
    # Add tabs to configure EthIf
    notebook.add(gen_frame, text ='EthIfGeneral')
    notebook.add(cfg_frame, text ='EthIfConfigSet')
    notebook.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    del TabList[:]

    # read EthIf content from ARXML file
    ethif_configs = arxml_ethif_r.parse_arxml(gui.arxml_file)
    
    # create the EthIfGeneral GUI tab
    ethif_gen_view = EthIfTab(gen_frame, width, height)
    ethif_gen_view.tab = ethif_gen.EthIfGeneralView(gui, ethif_configs)
    ethif_gen_view.name = "EthIfGeneral"
    TabList.append(ethif_gen_view)

    # create the EthIfGeneral GUI tab
    ethif_configset_view = EthIfTab(cfg_frame, width, height)
    ethif_configset_view.tab = ethif_cs.EthIfConfigSetView(gui, ethif_configs)
    ethif_configset_view.name = "EthIfConfigSet"
    TabList.append(ethif_configset_view)

    # Draw all tabs
    ethif_gen_view.tab.draw(ethif_gen_view)
    ethif_configset_view.tab.draw(ethif_configset_view)

    # gui.main_view.child_window.bind("<<NotebookTabChanged>>", show_os_tab_switch)



# Main Entry Point
def ethif_block_click_handler(gui):
    show_ethif_tabs(gui)