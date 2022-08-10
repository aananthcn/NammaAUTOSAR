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

def show_system_services_block(ev):
    ev.widget.configure(relief="sunken")
    print("show_system_services_block() is under construction!")

def show_microcontroller_block():
    print("show_microcontroller_block() is under construction!")



def draw_application_block(gui, yoffset, height):
    view = gui.view.root
    bfont = tkfont.Font(family='Helvetica', size=16)
    
    #view.geometry(str(gui.view.xsize)+'x'+str(gui.view.ysize))
    button = tk.Button(view, text="Applications", command=show_application_block, bg='#4D4D4D', fg='white')
    button['font'] = bfont
    yval = gui.view.ysize-height-BottomMargin-yoffset - MiscYmargin 
    button.place(x=LeftMargin, y=yval, width=gui.view.xsize-LeftMargin-RightMargin, height=height)



def draw_rte_block(gui, yoffset, height):
    view = gui.view.root
    bfont = tkfont.Font(family='Helvetica', size=16)
    
    #view.geometry(str(gui.view.xsize)+'x'+str(gui.view.ysize))
    button = tk.Button(view, text="Run Time Environment (RTE)", command=draw_rte_block, bg='#FF5008', fg='white')
    button['font'] = bfont
    yval = gui.view.ysize-height-BottomMargin-yoffset - MiscYmargin 
    button.place(x=LeftMargin, y=yval, width=gui.view.xsize-LeftMargin-RightMargin, height=height)



def draw_system_services_block(gui, yoffset, height):
    view = gui.view.root
    bfont = tkfont.Font(family='Helvetica', size=16)
    
    yval = gui.view.ysize-height-BottomMargin-yoffset - MiscYmargin 
    label = "AUTOSAR OS"
    width=gui.view.xsize/32
    border = 2
    canvas = tk.Canvas(view, height=height, width=width, background="SystemButtonFace", borderwidth=border,
                       relief="raised", bg="#9999FF")
    canvas.create_text((width/2, height/2), angle="90", anchor="center", text=label, fill="SystemButtonText", font=bfont)
    canvas.bind("<ButtonPress-1>", show_system_services_block)
    canvas.bind("<ButtonRelease-1>", lambda ev: ev.widget.configure(relief="raised"))
    canvas.place(x=LeftMargin-border, y=yval, width=width, height=height)



def draw_microcontroller_block(gui, yoffset, height):
    view = gui.view.root
    bfont = tkfont.Font(family='Helvetica', size=16)
    
    #view.geometry(str(gui.view.xsize)+'x'+str(gui.view.ysize))
    button = tk.Button(view, text="Microcontroller", command=show_microcontroller_block, bg='#000000', fg='white')
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
    draw_microcontroller_block(gui, yoffset, 40)
    
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