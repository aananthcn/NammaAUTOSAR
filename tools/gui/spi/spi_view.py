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
import gui.spi.spi_chan as spi_chn
import gui.spi.spi_chan_list as spi_chlist
import gui.spi.spi_jobs as spi_job
import gui.spi.spi_ext_dev as spi_exd
import gui.spi.spi_drv as spi_drv

import arxml.spi.arxml_spi as arxml_spi


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
    spi_configs = {}
    for tab in TabList:
        spi_configs[tab.name] = tab.tab.configs
    
    arxml_spi.update_arxml(gui.arxml_file, spi_configs)
    # spi_cgen.generate_code(gui)


    
def show_spi_tabs(gui):
    global PortConfigViewActive, TabList
    
    if PortConfigViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 90 / 100
    height = gui.main_view.ysize * 80 / 100
    view = tk.Toplevel()
    gui.main_view.child_window = view
    xoff = (gui.main_view.xsize - width)/2
    view.geometry("%dx%d+%d+%d" % (width, height, xoff, xoff))
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
    notebook.add(exd_frame, text ='SpiExternalDevice')
    notebook.add(chn_frame, text ='SpiChannel')
    # notebook.add(clst_frame, text ='SpiChannelList')
    notebook.add(job_frame, text ='SpiJob')
    notebook.add(seq_frame, text ='SpiSequence')
    notebook.add(drv_frame, text ='SpiDriver')
    notebook.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    for obj in TabList:
        del obj

    # read Spi content from ARXML file
    spi_configs = arxml_spi.parse_arxml(gui.arxml_file)
    
    # create new GUI objects
    spigen_tab = SpiTab(gen_frame, width, height)
    spigen_tab.tab = spi_gen.SpiGeneralTab(gui)
    spigen_tab.name = "SpiGeneral"
    TabList.append(spigen_tab)

    # SpiChannel Tab and few Tabs are inter dependent, hence creating it early, draw later
    spidrv_tab   = SpiTab(drv_frame, width, height)
    spijob_tab = SpiTab(job_frame, width, height)
    
    spidev_tab = SpiTab(exd_frame, width, height)
    spidev_tab.tab = spi_exd.SpiExternalDeviceTab(gui, spidrv_tab, spijob_tab)
    spidev_tab.name = "SpiExternalDevice"
    TabList.append(spidev_tab)

    spichn_tab    = SpiTab(chn_frame, width, height)
    spichn_tab.tab = spi_chn.SpiChannelTab(gui, spidrv_tab)
    spichn_tab.name = "SpiChannel"
    TabList.append(spichn_tab)

    spijob_tab.tab = spi_job.SpiJobTab(gui, spidrv_tab, spidev_tab, spichn_tab)
    spijob_tab.name = "SpiJob"
    TabList.append(spijob_tab)

    spiseq_tab = SpiTab(seq_frame, width, height)
    spiseq_tab.tab = spi_seq.SpiSequenceTab(gui, spidrv_tab, spijob_tab)
    spiseq_tab.name = "SpiSequence"
    TabList.append(spiseq_tab)

    spidrv_tab.tab = spi_drv.SpiDriverTab(gui)
    spidrv_tab.name = "SpiDriver"
    TabList.append(spidrv_tab)

    # Draw all tabs
    spigen_tab.tab.draw(spigen_tab)
    spidev_tab.tab.draw(spidev_tab)
    spichn_tab.tab.draw(spichn_tab)
    spijob_tab.tab.draw(spijob_tab)
    spiseq_tab.tab.draw(spiseq_tab)
    spidrv_tab.tab.draw(spidrv_tab)
    # gui.main_view.window.bind("<<NotebookTabChanged>>", show_os_tab_switch)



# Main Entry Point
def spi_block_click_handler(gui):
    show_spi_tabs(gui)