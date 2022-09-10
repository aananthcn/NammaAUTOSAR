#
# Created on Sat Sep 10 2022 7:46:17 AM
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


class ScrollableWindow:
    rtf = None  # Root Frame
    cvf = None  # Canvas Frame
    cv  = None  # Canvas
    sb  = None  # Scrollbar
    mnf = None  # Main Frame - where the widgets are scrolled
    
    xsize = None
    ysize = None


    def __init__(self, root, xsize, ysize):
        self.rtf = root
        self.xsize = xsize
        self.ysize = ysize
        self.rtf.grid_rowconfigure(0, weight=1)
        self.rtf.columnconfigure(0, weight=1)
        
        self.cvf = tk.Frame(self.rtf, width=self.xsize-10, height=self.ysize)
        self.cvf.grid(row=0, column=0, pady=(5, 0), sticky='nw')

        # Set grid_propagate to False to allow canvas frame resizing later
        self.cvf.grid_propagate(False)

        # Add a canvas in that frame
        self.cv = tk.Canvas(self.cvf, scrollregion=(0, 0, self.xsize-10, self.ysize))

        # Link a scrollbar to the canvas
        self.sb = tk.Scrollbar(self.cvf, orient=tk.VERTICAL)
        self.sb.grid(row=0, column=1, sticky='ns')
        self.sb.config(command=self.cv.yview)

        # self.cv.configure(yscrollcommand=self.sb.set)
        self.cv.config(width=self.xsize, height=self.ysize)
        self.cv.config(yscrollcommand=self.sb.set)
        self.cv.grid(row=0, column=0, sticky="news")

        # Create a frame to draw task table
        self.mnf = tk.Frame(self.cv)
        self.cv.create_window((0, 0), window=self.mnf, anchor='nw')

        
    def update(self):
        # Update widgets frames idle tasks to let tkinter calculate widget sizes
        self.mnf.update_idletasks()

        # Resize the main frame to show contents for FULL SCREEN (Todo: scroll bars won't work in reduced size window)
        canvas_w = self.rtf.winfo_screenwidth()-self.sb.winfo_width()
        # canvas_h = self.rtf.winfo_screenheight()-(widget.winfo_height()*6) # leave spinbox region from scrolling
        canvas_h = self.rtf.winfo_screenheight()
        self.cvf.config(width=canvas_w, height=canvas_h)


    def scroll(self):
        # Set the self.cv scrolling region
        self.cv.config(scrollregion=self.cv.bbox("all"))
    