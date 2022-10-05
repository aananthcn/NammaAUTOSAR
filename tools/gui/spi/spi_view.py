#
# Created on Wed Oct 05 2022 4:48:30 PM
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
#
import tkinter as tk
from tkinter import ttk

import gui.spi.spi_gen as spi_gen
import gui.spi.spi_seq as spi_seq


TabList = []
PortConfigViewActive = False


class SpiTab:
    tab = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h):
        self.save_cb = spi_save_callback
        self.frame = f
        self.xsize = w
        self.ysize = h


def spi_config_close_event(gui, view):
    global PortConfigViewActive

    PortConfigViewActive = False
    view.destroy()


def spi_save_callback(gui):
    spi_chn = None
    spi_seq = None
    spi_gen = None
    for tab in TabList:
        if tab.name == "SpiChannel":
            spi_chn = tab.tab
            continue
        if tab.name == "SpiSequence":
            spi_seq = tab.tab
            continue
        if tab.name == "SpiGeneral":
            spi_gen = tab.tab
            continue

    arxml_spi.update_arxml(gui.arxml_file, spi_chn, spi_seq, spi_gen)
    spi_cgen.generate_code(gui)

    
def show_spi_tabs(gui):
    global PortConfigViewActive, TabList
    
    if PortConfigViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 55 / 100
    height = gui.main_view.ysize * 80 / 100
    view = tk.Toplevel()
    gui.main_view.child_window = view
    view.geometry("%dx%d+%d+%d" % (width, height, gui.main_view.xsize/3, 15))
    view.title("AUTOSAR Spi Configuration Tool")
    PortConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: spi_config_close_event(gui, view))
    notebook = ttk.Notebook(view)
    
    # Create tabs to configure Spi
    gen_frame  = ttk.Frame(notebook)
    seq_frame  = ttk.Frame(notebook)
    chn_frame  = ttk.Frame(notebook)
    clst_frame = ttk.Frame(notebook)
    job_frame  = ttk.Frame(notebook)
    exd_frame  = ttk.Frame(notebook)
    drv_frame  = ttk.Frame(notebook)
    
    # Add tabs to configure Spi
    notebook.add(gen_frame, text ='SpiGeneral')
    notebook.add(seq_frame, text ='SpiSequence')
    notebook.add(chn_frame, text ='SpiChannel')
    notebook.add(clst_frame, text ='SpiChannelList')
    notebook.add(job_frame, text ='SpiJob')
    notebook.add(exd_frame, text ='SpiExternalDevice')
    notebook.add(drv_frame, text ='SpiDriver')
    notebook.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    for obj in TabList:
        del obj


    # create new GUI objects
    dtab = SpiTab(gen_frame, width, height)
    dtab.tab = spi_gen.SpiGeneralTab(gui)
    dtab.name = "SpiGeneral"
    TabList.append(dtab)
    dtab.tab.draw(dtab)
    
    dtab = SpiTab(seq_frame, width, height)
    dtab.tab = spi_seq.SpiSequenceTab(gui)
    dtab.name = "SpiSequence"
    TabList.append(dtab)
    dtab.tab.draw(dtab)
    
    return
    dtab = SpiTab(chn_frame, width, height)
    dtab.tab = spi_chn.SpiConfigTab(gui)
    dtab.name = "SpiChannel"
    TabList.append(dtab)
    dtab.tab.draw(dtab)

    dtab = SpiTab(clst_frame, width, height)
    dtab.tab = spi_clst.xxxxxx(gui)
    dtab.name = "SpiChannelList"
    TabList.append(dtab)
    dtab.tab.draw(dtab)

    dtab = SpiTab(job_frame, width, height)
    dtab.tab = spi_job.xxxxxx(gui)
    dtab.name = "SpiJob"
    TabList.append(dtab)
    dtab.tab.draw(dtab)

    dtab = SpiTab(exd_frame, width, height)
    dtab.tab = spi_exd.xxxxxx(gui)
    dtab.name = "SpiExternalDevice"
    TabList.append(dtab)
    dtab.tab.draw(dtab)

    dtab = SpiTab(drv_frame, width, height)
    dtab.tab = spi_drv.xxxxxx(gui)
    dtab.name = "SpiDriver"
    TabList.append(dtab)
    dtab.tab.draw(dtab)

    # gui.main_view.window.bind("<<NotebookTabChanged>>", show_os_tab_switch)
    

# Main Entry Point
def spi_block_click_handler(gui):
    show_spi_tabs(gui)