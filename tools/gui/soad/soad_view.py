#
# Created on Sat Feb 04 2023 6:35:41 PM
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

import gui.soad.soad_gen as soad_gen
import gui.soad.soad_config as soad_cfg
import gui.soad.soad_bsw_mod as soad_bswm

import arxml.soad.arxml_soad_parse as arxml_soad_r
import arxml.soad.arxml_soad_write as arxml_soad_w

# import gui.soad.soad_code_gen as soad_cgen


TabList = []
SoAdConfigViewActive = False


class SoAdTab:
    tab = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h):
        self.save_cb = soad_save_callback
        self.frame = f
        self.xsize = w
        self.ysize = h



def soad_config_close_event(gui, view):
    global SoAdConfigViewActive

    SoAdConfigViewActive = False
    view.destroy()



def soad_save_callback(gui):
    soad_configs = {}

    # pull all configs from UI tabs
    for tab in TabList:
	    # backup configs (i.e, pull from dispvar to datavar)
        for cfg in tab.tab.configs:
            cfg.get()

        # copy to configs to dict
        soad_configs[tab.name] = tab.tab.configs

    # write to file
    arxml_soad_w.update_arxml(gui.arxml_file, soad_configs)

    return

    # generate code
    soad_cgen.generate_code(gui, soad_configs)


    
def show_soad_tabs(gui):
    global SoAdConfigViewActive, TabList
    
    if SoAdConfigViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 80 / 100
    height = gui.main_view.ysize * 55 / 100
    view = tk.Toplevel()
    gui.main_view.child_window = view
    xoff = (gui.main_view.xsize - width)/2
    yoff = (gui.main_view.ysize - height)/3
    view.geometry("%dx%d+%d+%d" % (width, height, xoff, yoff))
    view.title("AUTOSAR Socket Adapter Configuration Tool")
    SoAdConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: soad_config_close_event(gui, view))
    notebook = ttk.Notebook(view)

    # Create tabs to configure SoAd
    gen_frame = ttk.Frame(notebook)
    bswm_frame = ttk.Frame(notebook)
    cfg_frame = ttk.Frame(notebook)
    
    # Add tabs to configure SoAd
    notebook.add(gen_frame, text ='SoAdGeneral')
    notebook.add(bswm_frame, text ='SoAdBswModules')
    notebook.add(cfg_frame, text ='SoAdConfig')
    notebook.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    del TabList[:]

    # read SoAd content from ARXML file
    soad_configs = arxml_soad_r.parse_arxml(gui.arxml_file)
    
    # create the SoAdGeneral GUI tab
    soad_gen_view = SoAdTab(gen_frame, width, height)
    soad_gen_view.tab = soad_gen.SoAdGeneralView(gui, soad_configs)
    soad_gen_view.name = "SoAdGeneral"
    TabList.append(soad_gen_view)

    # create the SoAdBswModules GUI tab
    soad_bswm_view = SoAdTab(bswm_frame, width, height)
    soad_bswm_view.tab = soad_bswm.SaOdBswModulesView(gui, soad_configs)
    soad_bswm_view.name = "SoAdBswModules"
    TabList.append(soad_bswm_view)

    # create the SoAdGeneral GUI tab
    soad_configset_view = SoAdTab(cfg_frame, width, height)
    soad_configset_view.tab = soad_cfg.SoAdConfigView(gui, soad_configs)
    soad_configset_view.name = "SoAdConfig"
    TabList.append(soad_configset_view)

    # Draw all tabs
    soad_gen_view.tab.draw(soad_gen_view)
    soad_bswm_view.tab.draw(soad_bswm_view)
    soad_configset_view.tab.draw(soad_configset_view)

    # gui.main_view.child_window.bind("<<NotebookTabChanged>>", show_os_tab_switch)



# Main Entry Point
def soad_block_click_handler(gui):
    show_soad_tabs(gui)