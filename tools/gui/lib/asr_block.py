#
# Created on Fri Aug 19 2022 11:21:25 PM
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



class Margin:
    left = 50
    right = 50
    top = 10
    bottom = 100



class AsrBlock:
    gui = None
    widget = None
    label = None
    label_anchor = None
    txtfont = None
    orientation = None
    xpos = None
    ypos = None
    width = None
    height = None
    margin = None
    fg_color = None
    bg_color = None
    callback = None

    def __init__(self, gui, txt, txta, ori, x, y, w, h, fg, bg, cb):
        self.margin = Margin()
        self.gui = gui
        self.label = txt
        self.label_anchor = txta
        self.orientation = ori
        self.xpos = x
        self.ypos = y
        self.width = w
        self.height = h
        self.fg_color = fg
        self.bg_color = bg
        if cb != None:
            self.callback = cb
        else:
            self.callback = self.asr_block_cb_null
        self.txtfont = tkfont.Font(family='Helvetica', size=16)

    def draw(self, gui):
        view   = gui.main_view.tk
        width  = (gui.main_view.xsize-self.margin.left-self.margin.right)*self.width/100 
        height = (gui.main_view.ysize-self.margin.bottom-self.margin.top)*self.height/100
        xval = self.margin.left + gui.main_view.xsize*self.xpos/100  # x begins at left, hence add
        yval = gui.main_view.ysize-self.margin.bottom-height - gui.main_view.ysize*self.ypos/100   # y begins at top, hence subtract
        
        if self.widget != None:
            self.widget.destroy()

        border = 2
        self.widget = tk.Canvas(view, height=height, width=width, background="gray40", borderwidth=border,
                        relief="raised", bg=self.bg_color)

        angle = "0"
        if self.orientation == "V":
            angle = "90"

        text_x = width/2
        text_y = height/2
        if self.label_anchor != "c" and self.label_anchor != "center":
            text_y = 2
            self.txtfont = tkfont.Font(family='Helvetica', size=14)

        self.widget.create_text((text_x, text_y), angle=angle, anchor=self.label_anchor,
                                text=self.label, fill=self.fg_color, font=self.txtfont)
        self.widget.bind("<ButtonPress-1>", lambda ev: self.asr_block_cb_facade(ev, self.callback, gui))
        self.widget.bind("<ButtonRelease-1>", lambda ev: ev.widget.configure(relief="raised"))
        self.widget.place(x=xval-border, y=yval, width=width, height=height)
        return self.widget

    def asr_block_cb_facade(self, ev, cb, gui):
        ev.widget.configure(relief="sunken")
        cb(gui)
    
    def update_label(self, gui, label):
        self.label = label
        self.draw(gui)
        
    def asr_block_cb_null(self, gui):
        print("Info: click callback not registered for "+self.label+"!")
