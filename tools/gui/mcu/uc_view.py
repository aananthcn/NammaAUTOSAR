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

import gui.autosar.asr_view as asr_view
import gui.mcu.uc_cgen as uc_cgen


class Uc_Info:
    micro = None        # e.g., rp2040, stm32f407vet6 etc
    micro_arch = None   # e.g., cortex-m0, cortex-m4 etc
    micro_maker = None  # e.g., Broadcom, ST etc



FreeAUTOSAR_Boards = {
    "Generic" :
        ["qemu-versatilepb"],
    "Broadcom" :
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
SoCMakerStr = None
SoC_ComboBox = None
SoCStr = None


###############################################################################
# Local Functions
def uc_maker_selected(event, gui):
    global SoCMakerStr, FreeAUTOSAR_Boards, SoCStr, SoC_ComboBox

    micro_maker = FreeAUTOSAR_Boards[SoCMakerStr.get()]
    SoC_ComboBox['values'] = micro_maker
    gui.uc_info.micro_maker = SoCMakerStr.get()
    
    
def uc_selected(event, gui):
    gui.uc_info.micro = SoCStr.get()
    gui.uc_info.micro_arch = MicroController_Arch[gui.uc_info.micro]

    # since micro-controller is selected, let us update the arch. view
    gui.micro_block.destroy()
    asr_view.redraw_microcontroller_block(gui)


def on_uc_view_close():
    global UcView

    UcView.destroy()
    UcView = None



###############################################################################
# Main Entry Point
def show_microcontroller_block(gui):
    global SoCMakerStr, FreeAUTOSAR_Boards, SoCStr, UcView, SoC_ComboBox

    # If previous view is active return
    if UcView != None:
        return

    # Create a child window
    UcView = tk.Toplevel()
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
    cmbsel = ttk.Combobox(UcView, width=col2_width, textvariable=SoCMakerStr, state="readonly")
    chipmakers = []
    for item in FreeAUTOSAR_Boards:
        chipmakers.append(item)
    cmbsel['values'] = chipmakers
    cmbsel.current()
    cmbsel.grid(row=row, column=2)
    cmbsel.bind("<<ComboboxSelected>>", lambda ev: uc_maker_selected(ev, gui))

    # Label - SoC
    row = 2
    label = tk.Label(UcView, text="SoC variant", width=col1_width, anchor="e")
    label.grid(row=row, column=1, sticky="w")

    # Combobox - SoC
    if SoCStr == None:
        SoCStr = tk.StringVar()
    SoC_ComboBox = ttk.Combobox(UcView, width=col2_width, textvariable=SoCStr, state="readonly")
    SoC_ComboBox['values'] = gui.uc_info.micro_maker
    SoC_ComboBox.current()
    SoC_ComboBox.grid(row=row, column=2)
    SoC_ComboBox.bind("<<ComboboxSelected>>", lambda ev: uc_selected(ev, gui))

    # Generate Makefile Button
    row = 4
    genm = tk.Button(UcView, width=int(2*col2_width/3), text="Generate Source",
                     command=lambda:uc_cgen.create_source(gui), bg="#206020", fg='white')
    genm.grid(row=row, column=2)
