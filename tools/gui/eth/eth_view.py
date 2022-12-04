#
# Created on Mon Nov 28 2022 6:57:24 PM
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

import gui.eth.eth_gen as eth_gen
# import gui.eth.eth_seq as eth_seq
# import gui.eth.eth_chan as eth_chn
# import gui.eth.eth_chan_list as eth_chlist
# import gui.eth.eth_jobs as eth_job
# import gui.eth.eth_ext_dev as eth_exd
# import gui.eth.eth_drv as eth_drv

# import arxml.eth.arxml_eth_parse as arxml_eth_r
# import arxml.eth.arxml_eth_write as arxml_eth_w

# import gui.eth.eth_code_gen as eth_cgen


TabList = []
PortConfigViewActive = False

EthNoteBook = None
EthCtrlStr = None
EthView_InitDone = False
EthConfigs = None
Eth_X = None
Eth_Y = None
Gui = None


class EthTab:
    tab = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h):
        self.save_cb = eth_save_callback
        self.frame = f
        self.xsize = w
        self.ysize = h



def eth_config_close_event(gui, view):
    global PortConfigViewActive

    PortConfigViewActive = False
    view.destroy()



def eth_save_callback(gui):
    print("Ethernet Save Callback called!")
    return
    eth_configs = {}
    for tab in TabList:
        eth_configs[tab.name] = tab.tab.configs
    
    arxml_eth_w.update_arxml(gui.arxml_file, eth_configs)
    eth_cgen.generate_code(gui, eth_configs)



def draw_eth_tab(name, eth_configs, idx):
    global TabList, EthNoteBook, Eth_X, Eth_Y, Gui
    
    # Create tab Frame to configure Eth
    tab_frame  = ttk.Frame(EthNoteBook)
    
    # Add tabs to configure Eth
    EthNoteBook.add(tab_frame, text=name)
    EthNoteBook.pack(expand = 1, fill ="both")

    # create new GUI objects
    ethtab_gui = EthTab(tab_frame, Eth_X, Eth_Y)
    ethtab_gui.tab = eth_gen.EthGeneralTab(Gui, eth_configs, idx)
    ethtab_gui.name = name
    TabList.append(ethtab_gui)

    # Draw eth tab
    ethtab_gui.tab.draw(ethtab_gui)
    EthNoteBook.select(tab_frame)



def update_eth_tab():
    global EthView_InitDone, TabList, EthCtrlStr, EthConfigs, EthNoteBook
    
    # get tabs to be added or removed
    req_tabs = int(EthCtrlStr.get())

    # Tune memory allocations based on number of rows or boxes
    cur_tabs = len(TabList)
    name = "EthCtrl-"
    if not EthView_InitDone:
        for i in range(cur_tabs):
            draw_eth_tab(name+str(i+cur_tabs), EthConfigs, i+cur_tabs)
            cur_tabs += 1
        EthView_InitDone = True
    elif req_tabs > cur_tabs:
        for i in range(req_tabs - cur_tabs):
            draw_eth_tab(name+str(i+cur_tabs), EthConfigs, i+cur_tabs)
            cur_tabs += 1
    elif cur_tabs > req_tabs:
        for i in range(cur_tabs - req_tabs):
            EthNoteBook.forget(TabList[-1].frame)
            del TabList[-1].tab
            del TabList[-1].frame
            del TabList[-1]
            cur_tabs -= 1

    # update common data
    for tab in TabList:
        tab.tab.update_ethernet_config(EthCtrlStr.get())


def show_eth_tabs(gui):
    global PortConfigViewActive, TabList, EthCtrlStr, EthConfigs, EthNoteBook, Eth_X, Eth_Y, Gui
    
    if PortConfigViewActive:
        return

    # Create a child window (tabbed view)
    Eth_X = gui.main_view.xsize * 90 / 100
    Eth_Y = gui.main_view.ysize * 80 / 100
    Gui = gui
    view = tk.Toplevel()
    gui.main_view.child_window = view
    xoff = (gui.main_view.xsize - Eth_X)/2
    view.geometry("%dx%d+%d+%d" % (Eth_X, Eth_Y, xoff, xoff))
    view.title("AUTOSAR Ethernet Driver (MAC) Configuration Tool")
    PortConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: eth_config_close_event(gui, view))

    #Number of modes - Label + Spinbox
    top_frame = tk.Frame(view)
    label = tk.Label(top_frame, text="No. Ethernet Controllers:")
    label.grid(row=0, column=0, sticky="w")
    EthCtrlStr = tk.StringVar()
    spinb = tk.Spinbox(top_frame, width=10, textvariable=EthCtrlStr, command=lambda : update_eth_tab(), values=tuple(range(0,256)))
    EthCtrlStr.set(0)
    spinb.grid(row=0, column=1, sticky="w")
    saveb = tk.Button(top_frame, width=10, text="Save Configs", command=lambda : eth_save_callback(gui), bg="#206020", fg='white')
    saveb.grid(row=0, column=2)
    top_frame.pack(side=tk.TOP)
    
    # Tabbed views for Ethernet Controllers
    EthNoteBook = ttk.Notebook(view)
    EthNoteBook.pack(side=tk.BOTTOM)
    
    # read Eth content from ARXML file
    # EthConfigs = arxml_eth_r.parse_arxml(gui.arxml_file)
    EthConfigs = None

    update_eth_tab()



# Main Entry Point
def eth_block_click_handler(gui):
    show_eth_tabs(gui)