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
import gui.main.ui_uc_cgen as uc_cgen
import arxml.mcu.arxml_mcu as arxml_mcu

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box


class Uc_Info:
    micro = None        # e.g., rp2040, stm32f407vet6 etc
    micro_arch = None   # e.g., cortex-m0, cortex-m4 etc
    micro_maker = None  # e.g., Broadcom, ST etc


Uc_Manufacturers = [
    "Generic",
    "RaspberryPi",
    "ST Micro"
]

Uc_Products = {
    "Generic"       : ["qemu-versatilepb"],
    "RaspberryPi"   : ["rp2040"],
    "ST Micro"      : ["stm32f407vet6"]
}

Uc_Arch = {
    "rp2040"            : "cortex-m0",
    "stm32f407vet6"     : "cortex-m4",
    "qemu-versatilepb"  : "arm"
}


UcViewWindow = None
Uc_ComboBox = None


###############################################################################
# Local Functions
def uc_manufacturer_selected(event, gui, view):
    global Uc_Products, Uc_ComboBox

    soc_maker = view.configs[0].dispvar["SoC Manufacturer"].get()
    micro_variants = Uc_Products[soc_maker]
    Uc_ComboBox['values'] = micro_variants
    view.configs[0].dispvar["SoC variant"].set("Please select")
    
    
# this function will be called when the UcViewWindow Toplevel() object is closed.
def on_uc_view_close():
    global UcViewWindow

    UcViewWindow.destroy()
    UcViewWindow = None


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

    # Update the Microcontroller block in main Gui
    new_label = uc_block_get_updated_label(gui)
    if new_label != None:
        uc_blk.label = new_label



def uc_block_click_handler(gui):
    global UcViewWindow

    if UcViewWindow != None:
        return

    # function to create dialog window
    UcViewWindow = tk.Toplevel() # create an instance of toplevel
    UcViewWindow.protocol("WM_DELETE_WINDOW", on_uc_view_close)
    UcViewWindow.attributes('-topmost',True)

    # set the geometry
    x = UcViewWindow.winfo_screenwidth()
    y = UcViewWindow.winfo_screenheight()
    width = 300
    height = 100
    UcViewWindow.geometry("%dx%d+%d+%d" % (width, height, 2*x/5, 7*y/10))
    UcViewWindow.title("Microcontroller Configs")

    # create views and draw
    uc_view = UcConfig_View(gui)
    uc_view.draw(UcViewWindow, width, height)



# Microcontroller Configs
class UcConfig_View:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SoC Manufacturer", "SoC variant"]
    uc_info = Uc_Info()

    non_header_objs = []
    dappas_per_col = len(cfgkeys)


    def __init__(self, gui):
        self.gui = gui
        self.configs = []
        arxml_mcu.parse_arxml(gui.arxml_file, self.uc_info)
        if self.uc_info.micro == None:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            uc_view = {}
            uc_view["SoC Manufacturer"] = self.uc_info.micro_maker
            uc_view["SoC variant"]      = self.uc_info.micro
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, uc_view))


    def __del__(self):
        del self.configs[:]


    def create_empty_configs(self):
        uc_view = {}
        uc_view["SoC Manufacturer"] = "Please select"
        uc_view["SoC variant"]      = "Please select"
        return uc_view


    def draw_dappas(self):
        global Uc_Manufacturers, Uc_ComboBox

        # SoC Manufacturer
        cmb_mak = dappa.combo(self, "SoC Manufacturer", 0, 0, 1, 25, Uc_Manufacturers)
        cmb_mak.bind("<<ComboboxSelected>>", lambda ev: uc_manufacturer_selected(ev, self.gui, self))

        # SoC variant
        Uc_ComboBox = dappa.combo(self, "SoC variant", 0, 1, 1, 25, self.uc_info.micro)
        # Uc_ComboBox.bind("<<ComboboxSelected>>", lambda ev: uc_selected(ev, self.gui, self))

        # empty space
        label = tk.Label(self.scrollw.mnf, text="")
        label.grid(row=6, column=0, sticky="e")

        # Save Button
        # saveb = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=lambda:uc_cgen.create_source(self.gui),
        saveb = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_configs,
                    bg="#206020", fg='white')
        saveb.grid(row=7, column=1)


    def draw(self, view, xsize, ysize):
        self.tab_struct = None
        self.scrollw = window.ScrollableWindow(view, xsize, ysize)

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()


    def save_configs(self):
        global Uc_Arch

        # get the last selected values from GUI view at the time of pressing save button
        soc_maker = self.configs[0].dispvar["SoC Manufacturer"].get()
        soc_name  = self.configs[0].dispvar["SoC variant"].get()

        # update global micro info
        self.gui.uc_info.micro_maker = soc_maker
        self.gui.uc_info.micro = soc_name
        self.gui.uc_info.micro_arch = Uc_Arch[soc_name]

        # since micro-controller is selected, let us update the arch. view
        new_label = uc_block_get_updated_label(self.gui)
        if new_label != None:
            self.gui.asr_blocks["uC"].update_label(self.gui, new_label)

        # generate code (i.e., update arxml and other artifacts)
        uc_cgen.create_source(self.gui)

