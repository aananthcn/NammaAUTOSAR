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

import arxml.mcu.arxml_mcu as arxml_mcu
import gui.autosar.asr_block as asr_block

import gui.mcu.uc_view as uc_view
import gui.os.os_view as os_view
import gui.app.app_view as app_view




# ###############################################################################
# # AUTOSAR BLOCKS configuration
AsrBlocksConfigList = [
    {
        # Name and orientation
        "name": "uC", "text": "MicroController Block", "ori": "H",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 0.0, "y": 0.0, "w": 100.0, "h": 4.7, "bgc": '#000000', "fgc": 'white',
        # click callback & constructor
        "cb": uc_view.uc_block_click_handler, "cons": uc_view.uc_block_constructor
    },
    {
        # Name and orientation
        "name": "Os", "text": "AUTOSAR OS", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 0.0, "y": 4.06, "w": 2.5, "h": 68.8, "bgc": '#9999FF', "fgc": 'black',
        # click callback & constructor
        "cb": os_view.os_block_click_handler, "cons": None
    },
    {
        # Name and orientation
        "name": "Os", "text": "EcuM", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 2.5, "y": 4.06, "w": 2.5, "h": 45, "bgc": '#9999FF', "fgc": 'black',
        # click callback & constructor
        "cb": None, "cons": None
    },
    {
        # Name and orientation
        "name": "Os", "text": "Mcu", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 5.0, "y": 4.06, "w": 2.5, "h": 25, "bgc": '#FF7C80', "fgc": 'black',
        # click callback & constructor
        "cb": None, "cons": None
    },
    {
        # Name and orientation
        "name": "Rte", "text": "Run Time Environment (RTE)", "ori": "H",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 0.0, "y": 64.1, "w": 100.0, "h": 4.7, "bgc": '#FF5008', "fgc": 'white',
        # click callback & constructor
        "cb": None, "cons": None
    },
    {
        # Name and orientation
        "name": "App", "text": "Applications", "ori": "H",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 0.0, "y": 68.4, "w": 100.0, "h": 10, "bgc": '#4D4D4D', "fgc": 'white',
        # click callback & constructor
        "cb": app_view.app_block_click_handler, "cons": None
    }
]



###############################################################################
# Main Entry Point
def show_autosar_modules_view(gui):
    global UcBlk_yoffset, UcBlk_height
    print("Info: X = ", gui.main_view.xsize)
    print("Info: Y = ", gui.main_view.ysize)
    gui.main_view.destroy_childwindow()
    gui.main_view.window = ttk.Frame(gui.main_view.tk) #dummy
    
    for blk in AsrBlocksConfigList:
        # create block view objects from AsrBlocksConfigList
        key = blk["name"]
        obj = asr_block.AsrBlock(gui, blk["text"], blk["ori"], blk["x"], blk["y"], blk["w"], blk["h"], blk["fgc"], blk["bgc"], blk["cb"])
        gui.asr_blocks[key] = obj

        # call the block view constructor
        if blk["cons"] != None:
            blk["cons"](gui, obj)

        # draw the block
        obj.draw(gui)
   