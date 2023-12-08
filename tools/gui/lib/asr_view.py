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
import gui.lib.asr_block as asr_block

import gui.main.ui_uc_view as uc_view
import gui.os.os_view as os_view
import gui.app.app_view as app_view

import gui.port.port_view as port_view
import gui.dio.dio_view as dio_view
import gui.spi.spi_view as spi_view
import gui.lin.lin_view as lin_view

import gui.eth.eth_view as eth_view
import gui.ethif.ethif_view as ethif_view
import gui.soad.soad_view as soad_view

import gui.dcm.dcm_view as dcm_view




# ###############################################################################
# # AUTOSAR BLOCKS configuration
# -----------------------------------------------------------------------------
# X-axis params
hbh  = 5                    # horizontal block height
# Y-axis params
hbw  = 6                    # horizontal block width
vbw  = 2.5                  # vertical block width
hbwl = 98                   # horizontal block width long

#==============================================================================
# Total height = 100 %, the screen pixels (X,Y) will be mapped to 100%,100%
# x: 0 (left) to 100 (right) is the valid range
# y: 0 (top) to 100 (bottom) is the valid range
# -----------------------------------------------------------------------------
# Application layer
la_x = 2                    # layer 1 (App) x-offset
la_y = 1                    # layer 1 (App) y-offset
la_h = 22

# RTE layer
lr_h = 8
lr_y = la_y + la_h            # layer 2 (RTE) y-offset

# Service layer
ls_y = lr_y + lr_h             # layer 3 (Service) y-offset
ls_h = (100 - ls_y) * 0.60

# ECU abstraction layer
le_y = ls_y + ls_h           # layer 4 (ECU AL) y-offset
le_h = (100 - ls_y) * 0.20

# MCAL layer
lm_y = le_y + le_h           # layer 5 (MCAL) y-offset
lm_h = (100 - ls_y) * 0.20

# Micro-controller layer
lu_y = lm_y + lm_h           # layer 6 (Micro-controller) y-offset
lu_h = hbw # think twice about ls_h before changing this.



# This configuration controls the overall view of the AUTOSAR blocks, so please follow thiese rules
AsrBlocksConfigList = [
    {
        # Application Layer
        "name": "App", "text": "Applications", "txta": "n", "ori": "H",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": la_x, "y": la_y, "w": hbwl, "h": la_h, "bgc": '#4D4D4D', "fgc": 'white',
        # click callback & constructor
        "cb": app_view.app_block_click_handler, "cons": app_view.app_block_constructor,
        "postdraw": app_view.app_post_draw_handler
    },
    {
        # RTE
        "name": "Rte", "text": "Run Time Environment (RTE)", "txta": "center", "ori": "H",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": la_x, "y": lr_y, "w": hbwl, "h": lr_h, "bgc": '#FF5008', "fgc": 'white',
        # click callback & constructor
        "cb": None, "cons": None,
        "postdraw": None
    },
    {
        # AUTOSAR Os
        "name": "Os", "text": "AUTOSAR OS", "txta": "center", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": la_x, "y": ls_y, "w": vbw, "h": ls_h+le_h+lm_h, "bgc": '#9999FF', "fgc": 'black',
        # click callback & constructor
        "cb": os_view.os_block_click_handler, "cons": None,
        "postdraw": None
    },
    {
        # EcuM
        "name": "EcuM", "text": "EcuM", "txta": "center", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": la_x+vbw, "y": le_y, "w": vbw, "h": le_h+lm_h, "bgc": '#9999FF', "fgc": 'black',
        # click callback & constructor
        "cb": None, "cons": None,
        "postdraw": None
    },
    {
        # Mcu
        "name": "Mcu", "text": "Mcu", "txta": "center", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": la_x+(2*vbw), "y": lm_y, "w": vbw, "h": lm_h, "bgc": '#FF7C80', "fgc": 'black',
        # click callback & constructor
        "cb": None, "cons": None,
        "postdraw": None
    },
    {
        # Port
        "name": "Port", "text": "Port", "txta": "center", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 74, "y": lm_y, "w": vbw, "h": lm_h, "bgc": '#FF7C80', "fgc": 'black',
        # click callback & constructor
        "cb": port_view.port_block_click_handler, "cons": None,
        "postdraw": None
    },
    {
        # Dio
        "name": "Dio", "text": "Dio", "txta": "center", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 71, "y": lm_y, "w": vbw, "h": lm_h, "bgc": '#FF7C80', "fgc": 'black',
        # click callback & constructor
        "cb": dio_view.dio_block_click_handler, "cons": None,
        "postdraw": None
    },
    {
        # Spi
        "name": "Spi", "text": "Spi", "txta": "center", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 30, "y": lm_y, "w": vbw, "h": lm_h, "bgc": '#FF7C80', "fgc": 'black',
        # click callback & constructor
        "cb": spi_view.spi_block_click_handler, "cons": None,
        "postdraw": None
    },
    {
        # Lin
        "name": "Lin", "text": "Lin", "txta": "center", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 42, "y": lm_y, "w": vbw, "h": lm_h, "bgc": '#FF7C80', "fgc": 'black',
        # click callback & constructor
        "cb": lin_view.lin_block_click_handler, "cons": None,
        "postdraw": None
    },
    {
        # LinIf
        "name": "LinIf", "text": "LinIf", "txta": "center", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 42, "y": le_y, "w": vbw, "h": le_h, "bgc": '#00CC99', "fgc": 'black',
        # click callback & constructor
        "cb": None, "cons": None,
        "postdraw": None
    },
    {
        # Eth
        "name": "Eth", "text": "Eth", "txta": "center", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 50, "y": lm_y, "w": vbw, "h": lm_h, "bgc": '#FF7C80', "fgc": 'black',
        # click callback & constructor
        "cb": eth_view.eth_block_click_handler, "cons": None,
        "postdraw": None
    },
    {
        # EthIf
        "name": "EthIf", "text": "EthIf", "txta": "center", "ori": "V",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 50, "y": le_y, "w": vbw, "h": le_h, "bgc": '#00CC99', "fgc": 'black',
        # click callback & constructor
        "cb": ethif_view.ethif_block_click_handler, "cons": None,
        "postdraw": None
    },
    {
        # TcpIp
        "name": "TcpIp", "text": "TcpIp", "txta": "center", "ori": "H",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 50-(hbw/2)+(vbw/2), "y": le_y-(1*hbh), "w": hbw, "h": hbh, "bgc": '#9999FF', "fgc": 'black',
        # click callback & constructor
        "cb": None, "cons": None,
        "postdraw": None
    },
    {
        # SoAd
        "name": "SoAd", "text": "Socket Adapter", "txta": "center", "ori": "H",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 50-(hbw)+(vbw/2), "y": le_y-(2*hbh), "w": 2*hbw, "h": hbh, "bgc": '#9999FF', "fgc": 'black',
        # click callback & constructor
        "cb": soad_view.soad_block_click_handler, "cons": None,
        "postdraw": None
    },
    {
        # PDU Router
        "name": "PduR", "text": "PDU Router", "txta": "center", "ori": "H",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 50-(hbw)+(vbw/2), "y": le_y-(3*hbh), "w": 2*hbw, "h": hbh, "bgc": '#9999FF', "fgc": 'black',
        # click callback & constructor
        "cb": None, "cons": None,
        "postdraw": None
    },
    {
        # Dcm
        "name": "Dcm", "text": "Dcm", "txta": "center", "ori": "H",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": 50-(hbw/2)+(vbw/2), "y": ls_y+(0*hbh), "w": hbw, "h": hbh, "bgc": '#9999FF', "fgc": 'black',
        # click callback & constructor
        "cb": dcm_view.dcm_block_click_handler, "cons": None,
        "postdraw": None
    },
    {
        # Micro-controller Block
        "name": "uC", "text": "MicroController Block", "txta": "center", "ori": "H",
        # Position (offset % of screen size), size (% of screen size) & colors
        "x": la_x, "y": 100, "w": hbwl, "h": lu_h, "bgc": '#000000', "fgc": 'white',
        # click callback & constructor
        "cb": uc_view.uc_block_click_handler, "cons": uc_view.uc_block_constructor,
        "postdraw": None
    }
]



###############################################################################
# Main Entry Point
def show_autosar_modules_view(gui):
    x_size = gui.main_view.xsize
    y_size = gui.main_view.ysize

    # This function will start a new view, hence destroying old ones
    gui.main_view.destroy_childwindow()
    
    for blk in AsrBlocksConfigList:
        # create block view objects from AsrBlocksConfigList
        key = blk["name"]
        obj = asr_block.AsrBlock(gui, blk["text"], blk["txta"], blk["ori"], blk["x"], blk["y"], 
                                 blk["w"], blk["h"], blk["fgc"], blk["bgc"], blk["cb"])
        gui.asr_blocks[key] = obj

        # call the block view constructor
        if blk["cons"] != None:
            blk["cons"](gui, obj)

        # draw the block
        obj.draw(gui)

        # post draw callback
        if blk["postdraw"] != None:
            blk["postdraw"](gui)
   