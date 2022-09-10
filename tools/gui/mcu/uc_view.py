#
# Created on Sat Aug 13 2022 1:28:33 PM
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

#import gui.lib.asr_view as asr_view
import gui.mcu.uc_cgen as uc_cgen
import arxml.mcu.arxml_mcu as arxml_mcu


class Uc_Info:
    micro = None        # e.g., rp2040, stm32f407vet6 etc
    micro_arch = None   # e.g., cortex-m0, cortex-m4 etc
    micro_maker = None  # e.g., Broadcom, ST etc



FreeAUTOSAR_Boards = {
    "Generic" :
        ["qemu-versatilepb"],
    "RaspberryPi" :
        ["rp2040"],
    "ST" :
        ["stm32f407vet6"]
}

MicroController_Arch = {
    "rp2040"            : "cortex-m0",
    "stm32f407vet6"     : "cortex-m4",
    "qemu-versatilepb"  : "arm"
}

UcView = None

# widget & data
SoC_ComboBox = None
SoCMaker_ComboBox = None
SoCMaker_ComboList = []

# widget strings
SoCStr = None
SoCMakerStr = None


###############################################################################
# Local Functions
def uc_maker_selected(event, gui):
    global SoCMakerStr, FreeAUTOSAR_Boards, SoCStr, SoC_ComboBox

    micro_maker = FreeAUTOSAR_Boards[SoCMakerStr.get()]
    SoC_ComboBox['values'] = micro_maker
    gui.uc_info.micro_maker = SoCMakerStr.get()
    SoCStr.set("")
    
    
def uc_selected(event, gui):
    gui.uc_info.micro = SoCStr.get()
    gui.uc_info.micro_arch = MicroController_Arch[gui.uc_info.micro]

    # since micro-controller is selected, let us update the arch. view
    new_label = uc_block_get_updated_label(gui)
    if new_label != None:
        gui.asr_blocks["uC"].update_label(gui, new_label)


def on_uc_view_close():
    global UcView

    UcView.destroy()
    UcView = None


def uc_block_get_updated_label(gui):
    new_name = None
    if gui.uc_info.micro != None:
        cur_name = gui.asr_blocks["uC"].label
        upd_name = cur_name.split("[")[0].strip() + " [" + gui.uc_info.micro + "]"
        if cur_name != upd_name:
            new_name = upd_name
    return new_name


###############################################################################
# Main Entry Points
def uc_block_constructor(gui, uc_blk):
    arxml_mcu.parse_arxml(gui.arxml_file, gui.uc_info)
    new_label = uc_block_get_updated_label(gui)
    if new_label != None:
        uc_blk.label = new_label



def uc_block_click_handler(gui):
    global SoCMakerStr, FreeAUTOSAR_Boards, SoCStr, UcView, SoC_ComboBox

    # If previous view is active return
    if UcView != None:
        return

    # Create a child window
    width = 370
    height = 70
    UcView = tk.Toplevel()
    UcView.geometry("%dx%d+%d+%d" % (width, height, gui.main_view.xsize*25/90, gui.main_view.ysize - height*4))
    UcView.title("Microcontroller Configs")
    UcView.protocol("WM_DELETE_WINDOW", on_uc_view_close)

    col1_width = 22
    col2_width = 30

    # Label - SoC Manufacturer
    row = 1
    label = tk.Label(UcView, text="SoC Manufacturer", width=col1_width, anchor="e")
    label.grid(row=row, column=1, sticky="w")

    # Combobox - SoC Manufacturer
    if SoCMakerStr == None:
        SoCMakerStr = tk.StringVar()
    SoCMakerStr.set(gui.uc_info.micro_maker)
    SoCMaker_ComboBox = ttk.Combobox(UcView, width=col2_width, textvariable=SoCMakerStr, state="readonly")
    for item in FreeAUTOSAR_Boards:
        SoCMaker_ComboList.append(item)
    SoCMaker_ComboBox['values'] = SoCMaker_ComboList
    SoCMaker_ComboBox.current()
    SoCMaker_ComboBox.grid(row=row, column=2)
    SoCMaker_ComboBox.bind("<<ComboboxSelected>>", lambda ev: uc_maker_selected(ev, gui))

    # Label - SoC
    row = 2
    label = tk.Label(UcView, text="SoC variant", width=col1_width, anchor="e")
    label.grid(row=row, column=1, sticky="w")

    # Combobox - SoC
    if SoCStr == None:
        SoCStr = tk.StringVar()
    SoCStr.set(gui.uc_info.micro)
    SoC_ComboBox = ttk.Combobox(UcView, width=col2_width, textvariable=SoCStr, state="readonly")
    if gui.uc_info.micro_maker != None:
        if gui.uc_info.micro_maker in FreeAUTOSAR_Boards:
	        SoC_ComboBox['values'] = FreeAUTOSAR_Boards[gui.uc_info.micro_maker]
    else:
        SoC_ComboBox['values'] = []
    SoC_ComboBox.current()
    SoC_ComboBox.grid(row=row, column=2)
    SoC_ComboBox.bind("<<ComboboxSelected>>", lambda ev: uc_selected(ev, gui))

    # Generate Makefile Button
    row = 4
    genm = tk.Button(UcView, width=int(3*col2_width/5), text="Save Configs",
                     command=lambda:uc_cgen.create_source(gui), bg="#206020", fg='white')
    genm.grid(row=row, column=2)
