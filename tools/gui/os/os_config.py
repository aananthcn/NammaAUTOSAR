#
# Created on Sat Aug 13 2022 1:03:07 PM
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

import os_builder.scripts.System_Generator as sg
import os_builder.scripts.oil as oil

import gui.os.os_tab as gui_os_tab
import gui.os.am_tab as gui_am_tab
import gui.os.cnt_tab as gui_cr_tab
import gui.os.msg_tab as gui_ms_tab
import gui.os.res_tab as gui_rs_tab
import gui.os.tsk_tab as gui_tk_tab
import gui.os.alm_tab as gui_al_tab
import gui.os.isr_tab as gui_ir_tab


OsTab = AmTab = CtrTab = MsgTab = ResTab = TskTab = AlmTab = IsrTab = None


def show_os_tab_switch(event):
    global OsTab, AmTab, CtrTab, MsgTab, ResTab, TskTab, AlmTab, IsrTab 

    current_tab = None #this variable can be used for debugging!
    if gui.view.window.tab(gui.view.window.select(), "text").strip() == "OS Configs":
        TskTab.backup_data()
        OsTab.backup_data()  # take the lastest stack size updates from Task tab.
        OsTab.update()
        current_tab = OsTab
    if gui.view.window.tab(gui.view.window.select(), "text").strip() == "AppModes":
        current_tab = AmTab
    if gui.view.window.tab(gui.view.window.select(), "text").strip() == "Counters":
        current_tab = CtrTab
    if gui.view.window.tab(gui.view.window.select(), "text").strip() == "Messages":
        current_tab = MsgTab
    if gui.view.window.tab(gui.view.window.select(), "text").strip() == "Resources":
        current_tab = ResTab
    if gui.view.window.tab(gui.view.window.select(), "text").strip() == "Tasks":
        current_tab = TskTab
    if gui.view.window.tab(gui.view.window.select(), "text").strip() == "Alarms":
        AlmTab.update()
        current_tab = AlmTab
    if gui.view.window.tab(gui.view.window.select(), "text").strip() == "ISRs":
        current_tab = IsrTab


    
def show_os_config(gui):
    global OsTab, AmTab, CtrTab, MsgTab, ResTab, TskTab, AlmTab, IsrTab

    # gui.view.destroy_childwindow()
    view = tk.Toplevel()
    view.state('zoomed')
    gui.view.child_window = ttk.Notebook(view)
    
    os_tab = ttk.Frame(gui.view.child_window)
    am_tab = ttk.Frame(gui.view.child_window)
    cr_tab = ttk.Frame(gui.view.child_window)
    ms_tab = ttk.Frame(gui.view.child_window)
    rs_tab = ttk.Frame(gui.view.child_window)
    tk_tab = ttk.Frame(gui.view.child_window)
    al_tab = ttk.Frame(gui.view.child_window)
    ir_tab = ttk.Frame(gui.view.child_window)
    
    gui.view.child_window.add(os_tab, text ='OS Configs')
    gui.view.child_window.add(am_tab, text =' AppModes ')
    gui.view.child_window.add(cr_tab, text =' Counters ')
    gui.view.child_window.add(ms_tab, text =' Messages ')
    gui.view.child_window.add(rs_tab, text =' Resources ')
    gui.view.child_window.add(tk_tab, text ='   Tasks   ')
    gui.view.child_window.add(al_tab, text ='  Alarms  ')
    gui.view.child_window.add(ir_tab, text ='   ISRs   ')
    gui.view.child_window.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    del OsTab
    del AmTab
    del CtrTab
    del MsgTab
    del ResTab
    del TskTab
    del AlmTab
    del IsrTab

    # create new GUI objects
    OsTab = gui_os_tab.OsTab(sg.OS_Cfgs, sg.Tasks)
    OsTab.draw(os_tab)

    AmTab = gui_am_tab.AmTab(sg.AppModes)
    AmTab.draw(am_tab)
    
    CtrTab = gui_cr_tab.CounterTab(sg.Counters)
    CtrTab.draw(cr_tab)

    MsgTab = gui_ms_tab.MessageTab(sg.Tasks)
    MsgTab.draw(ms_tab)

    ResTab = gui_rs_tab.ResourceTab(sg.Tasks)
    ResTab.draw(rs_tab)

    TskTab = gui_tk_tab.TaskTab(sg.Tasks, AmTab, ResTab, MsgTab)
    TskTab.draw(tk_tab)
    
    AlmTab = gui_al_tab.AlarmTab(sg.Alarms, TskTab, AmTab, CtrTab)
    AlmTab.draw(al_tab)

    IsrTab = gui_ir_tab.IsrTab(sg.ISRs, ResTab, MsgTab)
    IsrTab.draw(ir_tab)

    gui.view.window.bind("<<NotebookTabChanged>>", show_os_tab_switch)
    

