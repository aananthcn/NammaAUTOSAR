#
# Created on Sun Aug 21 2022 7:14:37 PM
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

import gui.app.app_gen as app_gen
import gui.lib.window as window

import subprocess

import json
import os


class AppInfo:
    git = None
    arxml = None


AppView = None
N_AppsStr = None
N_Apps = 0
n_header_objs = 3   # Objects / widgets that are part of the header and shouldn't be destroyed
header_row = 2   # Number of rows in Header Area of view
MaxApps = 1024

AppRepoStr_List = []
AppInfo_List = []
AppChild_list = [] # widgets

Parent_Frame = None
Canvas_Frame = None
Child_Frame = None
Canvas = None
Gui = None

AppLayerPath = os.getcwd()+"/submodules/AL/"
AppsJsonFile = AppLayerPath+"/applications.json"



# Show app configuration window
def child_app_press_handler(gui, app_id):
    view = tk.Toplevel()
    view.geometry("%dx%d+%d+%d" % (600, 300, 10, 50))
    view.title(AppInfo_List[app_id].git.split("/")[-1].split(".")[0]+" Configs")



# This function will draw blocks inside app block
def app_draw_childrens(gui):
    # get the app block's widget (canvas) for drawing more blocks inside it
    view = gui.asr_blocks["App"].widget

    for ch_app in AppChild_list:
        ch_app.destroy()

    last_widget_w = 0
    for i, app in enumerate(AppInfo_List):
        if app.git == None:
            continue
        name = app.git.split("/")[-1].split(".")[0]
        button = tk.Button(view, text=name, command= lambda id = i: child_app_press_handler(gui, id))
        AppChild_list.append(button)
        button.place(x=10+last_widget_w, y=28)
        last_widget_w += button.winfo_reqwidth()+2



def update_or_clone_app(app_id, gui):
    app_name = AppInfo_List[app_id].git.split("/")[-1].split(".")[0]
    app_path = AppLayerPath+"/"+app_name
    if os.path.exists(app_path):
        # git pull
        subprocess.call(["git", "pull"], cwd=app_path)
    else:
        # git clone app
        subprocess.call(["git", "clone", AppInfo_List[app_id].git], cwd=AppLayerPath)

    # generate code to build
    app_gen.create_source(app_name, gui)

 
    
def select_arxml_file(app_id):
    print("clone git repo ("+str(app_id)+") is under construction!")


def contains_any(str, set):
    return True in [c in str for c in set]

def validate_git_path(path):
    if ".git" not in path:
        return None
    if contains_any(path, '<>'):
        return None
    return path


def backup_data():
    data = []
    for i in range(N_Apps):
        AppInfo_List[i].git = validate_git_path(AppRepoStr_List[i].get())
        appinfo = {}
        appinfo["git"] = AppInfo_List[i].git
        appinfo["arxml"] = AppInfo_List[i].arxml
        data.append(appinfo)
    
    with open(AppsJsonFile, "w") as jfile:
        json.dump(data, jfile)



def restore_data_from_disk():
    global N_Apps, AppsJsonFile, AppInfo_List
    
    data = None
    with open(AppsJsonFile) as jfile:
        data = json.load(jfile)
        
    N_Apps = len(data)
    
    AppInfo_List.clear()
    AppRepoStr_List.clear()
    for item in data:
        appinfo = AppInfo()
        appinfo.git = item["git"]
        appinfo.arxml = item["arxml"]
        AppInfo_List.append(appinfo)
        AppRepoStr_List.append(tk.StringVar())



def app_draw(view, gui, xsize, ysize):
    global Parent_Frame, Canvas_Frame, Child_Frame, N_Apps, N_AppsStr, n_header_objs, MaxApps
    global Canvas

    Child_Frame = window.ScrollableWindow(view, xsize, ysize)
    
    #Number of modes - Label + Spinbox
    label = tk.Label(Child_Frame.mnf, text="No. of Application SWCs:")
    label.grid(row=0, column=0, sticky="w")
    N_AppsStr = tk.StringVar()
    spinb = tk.Spinbox(Child_Frame.mnf, width=10, textvariable=N_AppsStr, command=lambda: update_apps(N_AppsStr, gui, xsize),
                values=tuple(range(0,MaxApps)))
    N_AppsStr.set(N_Apps)
    spinb.grid(row=0, column=1, sticky="w")
    
    label_spc = tk.Label(Child_Frame.mnf, text="---")
    label_spc.grid(row=1, column=0, sticky="w")

    Child_Frame.update()

    app_update(gui, xsize)



def update_apps(mstr, gui, xsize):
    global Parent_Frame, Canvas_Frame, Child_Frame, N_Apps, N_AppsStr, n_header_objs, MaxApps
    
    N_Apps = int(mstr.get())
    # print("No of Apps: "+ str(N_Apps))        
    for i, item in enumerate(Child_Frame.mnf.winfo_children()):
        if i >= n_header_objs:
            item.destroy()
    app_update(gui, xsize)



def app_update(gui, xsize):
    global Parent_Frame, Canvas_Frame, Child_Frame, N_Apps, N_AppsStr, n_header_objs, MaxApps
    global AppInfo_List, Canvas

    # Tune memory allocations based on number of rows or boxes
    n_apps_str = len(AppRepoStr_List)
    if N_Apps > n_apps_str:
        for i in range(N_Apps - n_apps_str):
            AppRepoStr_List.append(tk.StringVar())
            appinfo = AppInfo()
            appinfo.git = "<Enter the git clone path here>"
            appinfo.arxml = None
            AppInfo_List.append(appinfo)
    elif n_apps_str > N_Apps:
        for i in range(n_apps_str - N_Apps):
            del AppRepoStr_List[-1]
            del AppInfo_List[-1]

    #print("n_apps_str = "+ str(n_apps_str) + ", n_apps = " + str(N_Apps))
    # Draw new objects
    for i in range(0, N_Apps):
        # Label
        label = tk.Label(Child_Frame.mnf, text="App "+str(i)+": ")
        label.grid(row=header_row+i, column=0, sticky="e")

        # Edit box
        entry = tk.Entry(Child_Frame.mnf, width=int(xsize/(2*5)), textvariable=AppRepoStr_List[i])
        AppRepoStr_List[i].set(AppInfo_List[i].git)
        entry.grid(row=header_row+i, column=1)

        # Button - Update / Clone
        select = tk.Button(Child_Frame.mnf, width=10, text="Update", command=lambda id = i : update_or_clone_app(id, gui))
        select.grid(row=header_row+i, column=2)

        # Button - Update / Clone
        select = tk.Button(Child_Frame.mnf, width=20, text="Select ARXML File", command=lambda id = i : select_arxml_file(id))
        select.grid(row=header_row+i, column=3)

    # Set the Canvas scrolling region
    # Canvas.config(scrollregion=Canvas.bbox("all"))
    Child_Frame.scroll()


def on_app_view_close(gui):
    global AppView

    AppView.destroy()
    AppView = None
    backup_data()
    app_draw_childrens(gui)
    

###############################################################################
# Main Entry Points
def app_block_constructor(gui, app_blk):
    restore_data_from_disk()



def app_block_click_handler(gui):
    global AppView
    
    # If previous view is active return
    if AppView != None:
        return

    # Create a child window
    width = gui.main_view.xsize * 70 / 100
    height = gui.main_view.ysize * 70 / 100
    AppView = tk.Toplevel()
    AppView.geometry("%dx%d+%d+%d" % (width, height, 10, 50))
    AppView.title("Applications Configs")
    AppView.protocol("WM_DELETE_WINDOW", lambda: on_app_view_close(gui))

    app_draw(AppView, gui, width, height)


def app_post_draw_handler(gui):
    app_draw_childrens(gui)
