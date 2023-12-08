import tkinter as tk
from tkinter import ttk

import gui.dcm.dcm_gen as dcm_gen
import gui.dcm.dcm_cfgset as dcm_cfgset

# import arxml.dcm.arxml_dcm_parse as arxml_dcm_r
# import arxml.dcm.arxml_dcm_write as arxml_dcm_w

# import gui.dcm.dcm_code_gen as dcm_cgen


TabList = []
DcmConfigSetViewActive = False


class DcmTab:
    tab = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h):
        self.save_cb = dcm_save_callback
        self.frame = f
        self.xsize = w
        self.ysize = h



def dcm_config_close_event(gui, view):
    global DcmConfigSetViewActive

    DcmConfigSetViewActive = False
    view.destroy()



def dcm_save_callback(gui):
    dcm_configs = {}

    # pull all configs from UI tabs
    for tab in TabList:
	    # backup configs (i.e, pull from dispvar to datavar)
        for cfg in tab.tab.configs:
            cfg.get()

        # copy to configs to dict
        dcm_configs[tab.name] = tab.tab.configs

    # write to file
    arxml_dcm_w.update_arxml(gui.arxml_file, dcm_configs)

    # generate code
    dcm_cgen.generate_code(gui, dcm_configs)


    
def show_dcm_tabs(gui):
    global DcmConfigSetViewActive, TabList
    
    if DcmConfigSetViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 60 / 100
    height = gui.main_view.ysize * 55 / 100
    view = tk.Toplevel()
    gui.main_view.child_window = view
    xoff = (gui.main_view.xsize - width)/2
    yoff = (gui.main_view.ysize - height)/3
    view.geometry("%dx%d+%d+%d" % (width, height, xoff, yoff))
    view.title("AUTOSAR Socket Adapter Configuration Tool")
    DcmConfigSetViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: dcm_config_close_event(gui, view))
    notebook = ttk.Notebook(view)

    # Create tabs to configure Dcm
    gen_frame = ttk.Frame(notebook)
    cfgset_frame = ttk.Frame(notebook)
    
    # Add tabs to configure Dcm
    notebook.add(gen_frame, text ='DcmGeneral')
    notebook.add(cfgset_frame, text ='DcmConfigSet')
    notebook.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    del TabList[:]

    # read Dcm content from ARXML file
    # dcm_configs = arxml_dcm_r.parse_arxml(gui.arxml_file)
    dcm_configs = None
    
    # create the DcmGeneral GUI tab
    dcm_gen_view = DcmTab(gen_frame, width, height)
    dcm_gen_view.tab = dcm_gen.DcmGeneralView(gui, dcm_configs)
    dcm_gen_view.name = "DcmGeneral"
    TabList.append(dcm_gen_view)

    # create the DcmGeneral GUI tab
    dcm_configset_view = DcmTab(cfgset_frame, width, height)
    dcm_configset_view.tab = dcm_cfgset.DcmConfigSetView(gui, dcm_configs)
    dcm_configset_view.name = "DcmConfigSet"
    TabList.append(dcm_configset_view)

    # Draw all tabs
    dcm_gen_view.tab.draw(dcm_gen_view)
    dcm_configset_view.tab.draw(dcm_configset_view)

    # gui.main_view.child_window.bind("<<NotebookTabChanged>>", show_os_tab_switch)



# Main Entry Point
def dcm_block_click_handler(gui):
    show_dcm_tabs(gui)