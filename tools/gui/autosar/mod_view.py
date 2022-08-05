import tkinter as tk
import tkinter.font as tkfont
from tkinter import *
import tkinter.ttk as ttk


LeftMargin = 50
RightMargin = 50
TopMargin = 10
BottomMargin = 10
MiscYmargin = 75 # I don't know the reason for this number, but this is the measured value.


def show_application_block():
    print("show_application_block() is under construction!")

def show_rte_block():
    print("show_rte_block() is under construction!")

def show_system_services_block():
    print("show_system_services_block() is under construction!")

def show_hardware_block():
    print("show_hardware_block() is under construction!")



def draw_application_block(gui, yoffset, height):
    view = gui.view.root
    bfont = tkfont.Font(family='Helvetica', size=16)
    
    #view.geometry(str(gui.view.xsize)+'x'+str(gui.view.ysize))
    button = tk.Button(view, text="Applications", command=show_application_block, bg='#A0A0A0', fg='white')
    button['font'] = bfont
    yval = gui.view.ysize-height-BottomMargin-yoffset - MiscYmargin 
    button.place(x=LeftMargin, y=yval, width=gui.view.xsize-LeftMargin-RightMargin, height=height)



def draw_rte_block(gui, yoffset, height):
    view = gui.view.root
    bfont = tkfont.Font(family='Helvetica', size=16)
    
    #view.geometry(str(gui.view.xsize)+'x'+str(gui.view.ysize))
    button = tk.Button(view, text="Run Time Environment (RTE)", command=draw_rte_block, bg='#A0A000', fg='white')
    button['font'] = bfont
    yval = gui.view.ysize-height-BottomMargin-yoffset - MiscYmargin 
    button.place(x=LeftMargin, y=yval, width=gui.view.xsize-LeftMargin-RightMargin, height=height)



def draw_system_services_block(gui, yoffset, height):
    view = gui.view.root
    bfont = tkfont.Font(family='Helvetica', size=16)
    
    #view.geometry(str(gui.view.xsize)+'x'+str(gui.view.ysize))
    button = tk.Button(view, text="System Services", command=show_system_services_block, bg="#5060FF", fg='white')
    button['font'] = bfont
    yval = gui.view.ysize-height-BottomMargin-yoffset - MiscYmargin 
    button.place(x=LeftMargin, y=yval, width=gui.view.xsize/8, height=height)



def draw_hardware_block(gui, yoffset, height):
    view = gui.view.root
    bfont = tkfont.Font(family='Helvetica', size=16)
    
    #view.geometry(str(gui.view.xsize)+'x'+str(gui.view.ysize))
    button = tk.Button(view, text="Hardware Block", command=show_hardware_block, bg='#403030', fg='white')
    button['font'] = bfont
    yval = gui.view.ysize-height-BottomMargin-yoffset - MiscYmargin 
    button.place(x=LeftMargin, y=yval, width=gui.view.xsize-LeftMargin-RightMargin, height=height)



def show_autosar_modules_view(gui):
    print("X = ", gui.view.xsize)
    print("Y = ", gui.view.ysize)
    gui.view.destroy_view()
    gui.view.window = ttk.Frame(gui.view.root) #dummy
   
    # Hardware block 
    yoffset = BottomMargin
    hw_height = 40
    draw_hardware_block(gui, yoffset, 40)
    
    # System Services block
    yoffset += hw_height
    bsw_height = 3 * gui.view.ysize / 5
    draw_system_services_block(gui, yoffset, bsw_height)
    
    # RTE block
    yoffset += bsw_height
    rte_height = 40
    draw_rte_block(gui, yoffset, rte_height)
    
    # Applications block
    yoffset += rte_height
    app_height = 80
    draw_application_block(gui, yoffset, app_height)