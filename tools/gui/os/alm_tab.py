import tkinter as tk
from tkinter import ttk

from .evt_wn import EventWindow
from copy import copy


class AlarmStr:
    id = None
    name = None
    counter = None
    action_type = None
    action_arg1 = None
    action_arg2 = None
    is_autostart = None
    alarm_time = None
    cycle_time = None
    n_appmodes = None
    appmodes = None

    def __init__(self, id):
        self.id = id
        self.name = tk.StringVar()
        self.counter = tk.StringVar()
        self.action_type = tk.StringVar()
        self.action_arg1 = tk.StringVar()
        self.action_arg2 = tk.StringVar()
        self.is_autostart = tk.StringVar()
        self.alarm_time = tk.StringVar()
        self.cycle_time = tk.StringVar()
        self.n_appmodes = 0  # start with zero appmodes
        self.appmodes = []

    def __del__(self):
        del self.id
        del self.name
        del self.counter
        del self.action_type
        del self.action_arg1
        del self.action_arg2
        del self.is_autostart
        del self.alarm_time
        del self.cycle_time
        del self.n_appmodes
        del self.appmodes


class AlarmTab:
    n_alarms = None
    max_alarms = 1024
    n_alarms_str = None
    alarms_str = []
    sg_alarms = None
    HeaderObjs = 12 #Objects / widgets that are part of the header and shouldn't be destroyed
    HeaderSize = 3
    prf = None  # Parent Frame
    cvf = None  # Canvas Frame
    cv  = None  # Canvas
    sb  = None  # Scrollbar
    mnf = None  # Main Frame - where the widgets are scrolled

    active_dialog = None
    active_widget = None

    amtab = None
    crtab = None
    tktab = None
    counter_names = []
    task_names = []
    task_events = []


    def __init__(self, alarms, tktab, amtab, crtab):
        self.sg_alarms = alarms
        if not self.sg_alarms:
            nalarm = self.create_empty_alarm()
            self.sg_alarms.append(nalarm)
        self.n_alarms = len(self.sg_alarms)
        self.n_alarms_str = tk.StringVar()
        for i in range(self.n_alarms):
            self.alarms_str.insert(i, AlarmStr(i))
        
        # collect all info from other tabs
        self.amtab = amtab
        self.crtab = crtab
        self.tktab = tktab


    def __del__(self):
        del self.n_alarms_str
        del self.alarms_str[:]


    def create_empty_alarm(self):
        alarm = {}
        
        # Use the last alarm's name and numbers to ease the edits made by user 
        alarm["Alarm Name"] = "ALARM_"
        alarm["COUNTER"] = "" # self.sg_alarms[-1]["COUNTER"]
        alarm["Action-Type"] = "OsAlarmActivateTask" 
        alarm["arg1"] = ""
        alarm["arg2"] = "FALSE"
        alarm["IsAutostart"] = "FALSE"
        alarm["ALARMTIME"] = "0"
        alarm["CYCLETIME"] = "0"
        alarm["APPMODE"] = []

        return alarm

    
    def extract_counter_names(self):
        del self.counter_names[:]
        for cntr in self.crtab.Ctr_StrVar:
            self.counter_names.append(cntr.name.get())
        return self.counter_names


    def extract_task_names(self):
        del self.task_names[:]
        for tsk in self.tktab.tasks_str:
            self.task_names.append(tsk.name.get())
        return self.task_names


    def extract_task_events(self, aid):
        events = []
        alarm_id = int(aid)

        # For action type == ALARMCALLBACK, there are no events associated!
        if self.sg_alarms[alarm_id]["Action-Type"] == "ALARMCALLBACK":
            return events

        # get events from tasks configured in Alarm[alarm_id]
        task_name = self.sg_alarms[alarm_id]["arg1"]
        for task in self.tktab.sg_tasks:
            if task_name == task["Task Name"]:
                if "EVENT" in task:
                    events = copy(task["EVENT"])
                    break

        return events


    def draw(self, tab):
        tab.grid_rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)
        self.prf = tk.Frame(tab)
        self.prf.grid(sticky="news")

        # Create a frame for the canvas with non-zero row&column weights
        self.cvf = tk.Frame(self.prf)
        self.cvf.grid(row=2, column=0, pady=(5, 0), sticky='nw')
        self.cvf.grid_rowconfigure(0, weight=1)
        self.cvf.grid_columnconfigure(0, weight=1)

        # Set grid_propagate to False to allow canvas frame resizing later
        self.cvf.grid_propagate(False)

        # Add a canvas in that frame
        self.cv = tk.Canvas(self.cvf)
        self.cv.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.sb = tk.Scrollbar(self.cvf, orient="vertical", command=self.cv.yview)
        self.sb.grid(row=0, column=1, sticky='ns')
        self.cv.configure(yscrollcommand=self.sb.set)

        # Create a frame to draw task table
        self.mnf = tk.Frame(self.cv)
        self.cv.create_window((0, 0), window=self.mnf, anchor='nw')

        #Number of modes - Label + Spinbox
        label = tk.Label(self.mnf, text="No. of Alarms:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.mnf, width=10, textvariable=self.n_alarms_str, command=lambda : self.update(),
                    values=tuple(range(1,self.max_alarms+1)))
        self.n_alarms_str.set(self.n_alarms)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle sg_alarms to let tkinter calculate buttons sizes
        self.mnf.update_idletasks()
        # Resize the main frame to show contents for FULL SCREEN (Todo: scroll bars won't work in reduced size window)
        canvas_w = tab.winfo_screenwidth()-self.sb.winfo_width()
        canvas_h = tab.winfo_screenheight()-(spinb.winfo_height()*6)
        self.cvf.config(width=canvas_w, height=canvas_h)

        # Table heading
        label = tk.Label(self.mnf, text=" ")
        label.grid(row=2, column=0, sticky="w")
        label = tk.Label(self.mnf, text="Alarm Name")
        label.grid(row=2, column=1, sticky="w")
        label = tk.Label(self.mnf, text="COUNTER")
        label.grid(row=2, column=2, sticky="we")
        label = tk.Label(self.mnf, text="Action-Type")
        label.grid(row=2, column=3, sticky="we")
        label = tk.Label(self.mnf, text="arg1")
        label.grid(row=2, column=4, sticky="we")
        label = tk.Label(self.mnf, text="arg2")
        label.grid(row=2, column=5, sticky="we")
        label = tk.Label(self.mnf, text="IsAutoStart")
        label.grid(row=2, column=6, sticky="we")
        label = tk.Label(self.mnf, text="ALARMTIME")
        label.grid(row=2, column=7, sticky="we")
        label = tk.Label(self.mnf, text="CYCLETIME")
        label.grid(row=2, column=8, sticky="we")
        label = tk.Label(self.mnf, text="APPMODE")
        label.grid(row=2, column=9, sticky="we")

        self.update()


    def update(self):
        # Backup current task entries from GUI
        self.backup_data()
                
        # destroy most old gui widgets
        self.n_alarms = int(self.n_alarms_str.get())
        for i, item in enumerate(self.mnf.winfo_children()):
            if i >= self.HeaderObjs:
                item.destroy()

        # Tune memory allocations based on number of rows or boxes
        n_alarms_str = len(self.alarms_str)
        if self.n_alarms > n_alarms_str:
            for i in range(self.n_alarms - n_alarms_str):
                self.alarms_str.insert(len(self.alarms_str), AlarmStr(n_alarms_str+i))
                self.sg_alarms.insert(len(self.sg_alarms), self.create_empty_alarm())
        elif n_alarms_str > self.n_alarms:
            for i in range(n_alarms_str - self.n_alarms):
                del self.alarms_str[-1]
                del self.sg_alarms[-1]

        #print("n_alarms_str = "+ str(n_alarms_str) + ", n_alarms = " + str(self.n_alarms))
        # Draw new objects
        for i in range(0, self.n_alarms):
            label = tk.Label(self.mnf, text="Alarm "+str(i)+": ")
            label.grid(row=self.HeaderSize+i, column=0, sticky="e")
            
            # Alarm Name
            entry = tk.Entry(self.mnf, width=30, textvariable=self.alarms_str[i].name)
            self.alarms_str[i].name.set(self.sg_alarms[i]["Alarm Name"])
            entry.grid(row=self.HeaderSize+i, column=1)

            # COUNTER
            cmbsel = ttk.Combobox(self.mnf, width=17, textvariable=self.alarms_str[i].counter, state="readonly")
            cmbsel['values'] = self.extract_counter_names()
            self.alarms_str[i].counter.set(self.sg_alarms[i]["COUNTER"])
            cmbsel.current()
            cmbsel.grid(row=self.HeaderSize+i, column=2)

            # Action-Type
            cmbsel = ttk.Combobox(self.mnf, width=17, textvariable=self.alarms_str[i].action_type, state="readonly")
            cmbsel['values'] = ("ACTIVATETASK", "SETEVENT", "ALARMCALLBACK")
            self.alarms_str[i].action_type.set(self.sg_alarms[i]["Action-Type"])
            cmbsel.current()
            cmbsel.grid(row=self.HeaderSize+i, column=3)
            cmbsel.bind("<<ComboboxSelected>>", self.action_type_selected)

            # arg1
            if self.sg_alarms[i]["Action-Type"] == "ALARMCALLBACK":
                # Draw Entry box for ALARMCALLBACK
                entry = tk.Entry(self.mnf, width=30, textvariable=self.alarms_str[i].action_arg1)
                self.alarms_str[i].action_arg1.set(self.sg_alarms[i]["arg1"])
                entry.grid(row=self.HeaderSize+i, column=4)
            else: 
                # Draw Combobox for Task select
                cmbsel = ttk.Combobox(self.mnf, width=30-3, textvariable=self.alarms_str[i].action_arg1, state="readonly")
                cmbsel['values'] = self.extract_task_names()
                self.alarms_str[i].action_arg1.set(self.sg_alarms[i]["arg1"])
                cmbsel.current()
                cmbsel.grid(row=self.HeaderSize+i, column=4)
                cmbsel.bind("<<ComboboxSelected>>", self.arg1_task_selected)

            # arg2
            if self.sg_alarms[i]["Action-Type"] == "SETEVENT":
                # Draw Combobox for Event select
                cmbsel = ttk.Combobox(self.mnf, width=25-3, textvariable=self.alarms_str[i].action_arg2, state="readonly")
                event_list = self.extract_task_events(i)
                cmbsel['values'] = event_list
                if self.sg_alarms[i]["arg2"] in event_list:
                    self.alarms_str[i].action_arg2.set(self.sg_alarms[i]["arg2"])
                else:
                    self.alarms_str[i].action_arg2.set("")
                cmbsel.current()
                cmbsel.grid(row=self.HeaderSize+i, column=5)


            # IsAutoStart
            cmbsel = ttk.Combobox(self.mnf, width=8, textvariable=self.alarms_str[i].is_autostart, state="readonly")
            cmbsel['values'] = ("TRUE", "FALSE")
            self.alarms_str[i].is_autostart.set(self.sg_alarms[i]["IsAutostart"])
            cmbsel.current()
            cmbsel.grid(row=self.HeaderSize+i, column=6)
            cmbsel.bind("<<ComboboxSelected>>", self.isautostart_changed)

            # ALARMTIME, CYCLETIME AND APPMODE are not required if IsAutostart is False
            if self.sg_alarms[i]["IsAutostart"] == "FALSE":
                continue

            # ALARMTIME
            entry = tk.Entry(self.mnf, width=11, textvariable=self.alarms_str[i].alarm_time, justify='center')
            self.alarms_str[i].alarm_time.set(self.sg_alarms[i]["ALARMTIME"])
            entry.grid(row=self.HeaderSize+i, column=7)

            # CYCLETIME
            entry = tk.Entry(self.mnf, width=11, textvariable=self.alarms_str[i].cycle_time, justify='center')
            self.alarms_str[i].cycle_time.set(self.sg_alarms[i]["CYCLETIME"])
            entry.grid(row=self.HeaderSize+i, column=8)

            # APPMODE[]
            if "APPMODE[]" in self.sg_alarms[i]:
                self.alarms_str[i].n_appmodes = len(self.sg_alarms[i]["APPMODE[]"])
            text = "SELECT["+str(self.alarms_str[i].n_appmodes)+"]"
            select = tk.Button(self.mnf, width=10, text=text, command=lambda id = i: self.select_autostart_modes(id))
            select.grid(row=self.HeaderSize+i, column=9)

        # Set the self.cv scrolling region
        self.cv.config(scrollregion=self.cv.bbox("all"))


    def backup_data(self):
        n_alarms_str = len(self.alarms_str)
        for i in range(n_alarms_str):
            if len(self.alarms_str[i].name.get()):
                self.sg_alarms[i]["Alarm Name"] = self.alarms_str[i].name.get()
            if len(self.alarms_str[i].counter.get()):
                self.sg_alarms[i]["COUNTER"] = self.alarms_str[i].counter.get()
            if len(self.alarms_str[i].action_type.get()):
                self.sg_alarms[i]["Action-Type"] = self.alarms_str[i].action_type.get()
            if len(self.alarms_str[i].action_arg1.get()):
                self.sg_alarms[i]["arg1"] = self.alarms_str[i].action_arg1.get()
            if len(self.alarms_str[i].action_arg2.get()):
                self.sg_alarms[i]["arg2"] = self.alarms_str[i].action_arg2.get()
            if self.sg_alarms[i]["IsAutostart"] == "FALSE":
                continue
            if len(self.alarms_str[i].alarm_time.get()):
                self.sg_alarms[i]["ALARMTIME"] = self.alarms_str[i].alarm_time.get()
            if len(self.alarms_str[i].cycle_time.get()):
                self.sg_alarms[i]["CYCLETIME"] = self.alarms_str[i].cycle_time.get()


    def on_autostart_dialog_close(self, task_id):
        # remove old selections
        if "APPMODE[]" in self.sg_alarms[task_id]:
            del self.sg_alarms[task_id]["APPMODE[]"][:]
        else:
            self.sg_alarms[task_id]["APPMODE[]"] = []

        # update new selections
        if len(self.active_widget.curselection()):
            for i in self.active_widget.curselection():
                self.sg_alarms[task_id]["APPMODE[]"].append(self.active_widget.get(i))
        
        # dialog elements are no longer needed, destroy them. Else, new dialogs will not open!
        self.active_widget.destroy()
        del self.active_widget
        self.active_dialog.destroy()
        del self.active_dialog

        # refresh screen
        self.update()


    def select_autostart_modes(self, id):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_autostart_dialog_close(id))

        # show all app modes
        self.active_widget = tk.Listbox(self.active_dialog, selectmode=tk.MULTIPLE, width=40, height=15)
        for i, obj in enumerate(self.amtab.AM_StrVar):
            appmode = obj.get()
            self.active_widget.insert(i, appmode)
            if "APPMODE[]" in self.sg_alarms[id]:
                if appmode in self.sg_alarms[id]["APPMODE[]"]:
                    self.active_widget.selection_set(i)
        self.active_widget.pack()


    def action_type_selected(self, event):
        # backup all action_type selects and update the screen
        for i, alm in enumerate(self.sg_alarms):
            alm["Action-Type"] = self.alarms_str[i].action_type.get()
            if "arg2" not in alm:
                alm["arg2"] = ""
        self.update()


    def arg1_task_selected(self, event):
        self.update()


    def isautostart_changed(self, event):
        for i, alm in enumerate(self.sg_alarms):
            alm["IsAutostart"] = self.alarms_str[i].is_autostart.get()
            if "ALARMTIME" not in alm:
                alm["ALARMTIME"] = "50"
            if "CYCLETIME" not in alm:
                alm["CYCLETIME"] = "1000"
            if "APPMODE[]" not in alm:
                alm["APPMODE[]"] = []
        self.update()