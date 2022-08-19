#
# Created on Thu Aug 11 2022 10:35:58 PM
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
import tkinter.font as tkfont
from tkinter import *
import tkinter.ttk as ttk


import gui.mcu.uc_view as uc_view


LeftMargin = 50
RightMargin = 50
TopMargin = 10
BottomMargin = 10
MiscYmargin = 75 # I don't know the reason for this number, but this is the measured value.

# Microcontroller Block
UcBlk_yoffset = None
UcBlk_height = None



def show_application_block(gui):
    print("show_application_block() is under construction!")

def show_rte_block(gui):
    print("show_rte_block() is under construction!")

def show_sl_os_config(gui):
    gui.show_os_config()



###############################################################################
# Block view primitives
def draw_hbutton(name, cb, gui, yoffset, height, bgc, fgc):
    view = gui.main_view.tk
    bfont = tkfont.Font(family='Helvetica', size=16)
    button = tk.Button(view, text=name, command=lambda:cb(gui), bg=bgc, fg=fgc)
    button['font'] = bfont
    yval = gui.main_view.ysize-height-BottomMargin-yoffset - MiscYmargin 
    button.place(x=LeftMargin, y=yval, width=gui.main_view.xsize-LeftMargin-RightMargin, height=height)
    return button


# Vertical Button Handler functions
def vbutton_cb_facade(ev, cb, gui):
    ev.widget.configure(relief="sunken")
    cb(gui)

def draw_vbutton(name, cb, gui, yoffset, height, bgc, fgc):
    view = gui.main_view.tk
    bfont = tkfont.Font(family='Helvetica', size=16)
    
    yval   = gui.main_view.ysize-height-BottomMargin-yoffset - MiscYmargin
    width  = gui.main_view.xsize/32
    border = 2
    canvas = tk.Canvas(view, height=height, width=width, background="SystemButtonFace", borderwidth=border,
                       relief="raised", bg=bgc)

    canvas.create_text((width/2, height/2), angle="90", anchor="center", text=name, fill=fgc, font=bfont)
    canvas.bind("<ButtonPress-1>", lambda ev: vbutton_cb_facade(ev, cb, gui))
    canvas.bind("<ButtonRelease-1>", lambda ev: ev.widget.configure(relief="raised"))
    canvas.place(x=LeftMargin-border, y=yval, width=width, height=height)
    return canvas




###############################################################################
# AUTOSAR BLOCKS
def draw_application_block(gui, yoffset, height):
    name = "Applications"
    cb = show_application_block
    draw_hbutton(name, cb, gui, yoffset, height, '#4D4D4D', 'white')


def draw_rte_block(gui, yoffset, height):
    name = "Run Time Environment (RTE)"
    cb = show_rte_block
    draw_hbutton(name, cb, gui, yoffset, height, '#FF5008', 'white')


def draw_sl_os_block(gui, yoffset, height):
    name = "AUTOSAR OS"
    cb = show_sl_os_config
    draw_vbutton(name, cb, gui, yoffset, height, '#9999FF', 'black')


def draw_microcontroller_block(gui, yoffset, height):
    if gui.uc_info.micro == None:
        name = "Microcontroller"
    else:
        name = "Microcontroller ["+gui.uc_info.micro+"]"
    cb = uc_view.show_microcontroller_block
    gui.micro_block = draw_hbutton(name, cb, gui, yoffset, height, '#000000', 'white')
    
def redraw_microcontroller_block(gui):
    global UcBlk_yoffset, UcBlk_height
    draw_microcontroller_block(gui, UcBlk_yoffset, UcBlk_height)



###############################################################################
# Main Entry Point
def show_autosar_modules_view(gui):
    global UcBlk_yoffset, UcBlk_height
    print("Info: X = ", gui.main_view.xsize)
    print("Info: Y = ", gui.main_view.ysize)
    gui.main_view.destroy_childwindow()
    gui.main_view.window = ttk.Frame(gui.main_view.tk) #dummy
   
    # Microcontroller block 
    UcBlk_yoffset = BottomMargin
    UcBlk_height = 40
    draw_microcontroller_block(gui, UcBlk_yoffset, UcBlk_height)
    
    # System Services block
    yoffset = UcBlk_yoffset + UcBlk_height
    bsw_height = 3 * gui.main_view.ysize / 5
    draw_sl_os_block(gui, yoffset, bsw_height)
    
    # RTE block
    yoffset += bsw_height
    rte_height = 40
    draw_rte_block(gui, yoffset, rte_height)
    
    # Applications block
    yoffset += rte_height
    app_height = 80
    draw_application_block(gui, yoffset, app_height)