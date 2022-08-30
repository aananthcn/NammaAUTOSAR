import tkinter as tk
from tkinter import ttk


class CounterStr:
    name = None
    mincycle = None
    maxallowed = None
    ticksperbase = None
    cntr_type = None
    comment = None


    def __init__(self, nm, mi, ma, tb, ty, cm):
        self.name = tk.StringVar(value=nm)
        self.mincycle = tk.StringVar(value=mi)
        self.maxallowed = tk.StringVar(value=ma)
        self.ticksperbase = tk.StringVar(value=tb)
        self.cntr_type = tk.StringVar(value=ty)
        self.comment = tk.StringVar(value=cm)

    def __del__(self):
        del self.name
        del self.mincycle
        del self.maxallowed
        del self.ticksperbase
        del self.cntr_type
        del self.comment



class CounterTab:
    N_Counters = 1
    N_Counters_str = None
    MaxCounters = 16
    HeaderSize = 2
    HeaderObjs = 9 #Objects / widgets that are part of the header and shouldn't be destroyed

    Counters = None
    Ctr_StrVar = []


    def __init__(self, cntrs):
        self.N_Counters_str = tk.StringVar(value=self.N_Counters)
        self.Counters = cntrs
        if not cntrs:
            ctr = self.create_empty_counter()
            self.Counters.append(ctr)

        self.N_Counters = len(self.Counters)
        del self.Ctr_StrVar[:]
        for i in range(self.N_Counters):
            self.Ctr_StrVar.insert(i, CounterStr(self.Counters[i]['Counter Name'],
                self.Counters[i]['MINCYCLE'],
                self.Counters[i]['MAXALLOWEDVALUE'],
                self.Counters[i]['TICKSPERBASE'],
                self.Counters[i]['OsCounterType'],
                ""))


    def __del__(self):
        del self.N_Counters_str
        del self.Ctr_StrVar[:]


    def update_ctrs(self, tab):
        self.N_Counters = self.N_Counters_str.get()
        for i, item in enumerate(tab.winfo_children()):
            if i > self.HeaderObjs:
                item.destroy()
        self.update(tab)
        

    def draw(self, tab):
        #Number of modes - Label + Spinbox
        label = tk.Label(tab, text="Number of Counters ")
        label.grid(row=1, column=1, sticky="w")
        spinb = tk.Spinbox(tab, width=10, values=tuple(range(1,self.MaxCounters+1)), 
                        command=lambda: self.update_ctrs(tab), textvariable=self.N_Counters_str)
        self.N_Counters_str.set(self.N_Counters)
        spinb.grid(row=1, column=2, sticky="w")

        # Table heading
        label = tk.Label(tab, text=" ")
        label.grid(row=2, column=1, sticky="w")
        label = tk.Label(tab, text="Counter Name")
        label.grid(row=2, column=2, sticky="w")
        label = tk.Label(tab, text="MINCYCLE")
        label.grid(row=2, column=3, sticky="we")
        label = tk.Label(tab, text="MAXALLOWEDVALUE")
        label.grid(row=2, column=4, sticky="we")
        label = tk.Label(tab, text="TICKSPERBASE")
        label.grid(row=2, column=5, sticky="we")
        label = tk.Label(tab, text="OsCounterType")
        label.grid(row=2, column=6, sticky="we")
        label = tk.Label(tab, text="Comments")
        label.grid(row=2, column=7, sticky="w")

        self.update(tab)


    def update(self, tab):
        # Backup current entries
        self.backup_data()

        # StrVar memory allocation checks
        n_strvar = len(self.Ctr_StrVar)
        if int(self.N_Counters) > n_strvar:
            for i in range(int(self.N_Counters) - n_strvar):
                self.Ctr_StrVar.insert(len(self.Ctr_StrVar), CounterStr("", "", "", "", "", ""))
                self.Counters.append(self.create_empty_counter())
        elif n_strvar > int(self.N_Counters):
            # print("n_strvar = "+ str(n_strvar) + ", N_Counters = " + str(self.N_Counters))
            for i in range(n_strvar - int(self.N_Counters)):
                del self.Ctr_StrVar[-1]
                del self.Counters[-1]

        # Draw counter objects
        for i in range(0, int(self.N_Counters)):
            label = tk.Label(tab, text="Counter "+str(i)+" : ")
            label.grid(row=self.HeaderSize+i+1, column=1, sticky="e")
            entry = tk.Entry(tab, width=30, textvariable=self.Ctr_StrVar[i].name) # Counter Name
            self.Ctr_StrVar[i].name.set(self.Counters[i]["Counter Name"])
            entry.grid(row=self.HeaderSize+i+1, column=2)
            entry = tk.Entry(tab, width=15, textvariable=self.Ctr_StrVar[i].mincycle) # MINCYCLE
            self.Ctr_StrVar[i].mincycle.set(self.Counters[i]["MINCYCLE"])
            entry.grid(row=self.HeaderSize+i+1, column=3)
            entry = tk.Entry(tab, width=20, textvariable=self.Ctr_StrVar[i].maxallowed) # MAXALLOWEDVALUE
            self.Ctr_StrVar[i].maxallowed.set(self.Counters[i]["MAXALLOWEDVALUE"])
            entry.grid(row=self.HeaderSize+i+1, column=4)
            entry = tk.Entry(tab, width=15, textvariable=self.Ctr_StrVar[i].ticksperbase) # TICKSPERBASE
            self.Ctr_StrVar[i].ticksperbase.set(self.Counters[i]["TICKSPERBASE"])
            entry.grid(row=self.HeaderSize+i+1, column=5)

            cmbsel = ttk.Combobox(tab, width=20, textvariable=self.Ctr_StrVar[i].cntr_type, state="readonly") # Hardware / Software
            cmbsel['values'] = ("HARDWARE", "SOFTWARE")
            self.Ctr_StrVar[i].cntr_type.set(self.Counters[i]["OsCounterType"])
            cmbsel.current()
            cmbsel.grid(row=self.HeaderSize+i+1, column=6)

            entry = tk.Entry(tab, width=40, textvariable=self.Ctr_StrVar[i].comment) # Comments
            self.Ctr_StrVar[i].comment.set("") # comments not yet supported!
            entry.grid(row=self.HeaderSize+i+1, column=7)


    def backup_data(self):
        n_strvar = len(self.Ctr_StrVar)
        for i in range(n_strvar):
            self.Counters[i]["Counter Name"] = self.Ctr_StrVar[i].name.get()
            self.Counters[i]["MINCYCLE"] = self.Ctr_StrVar[i].mincycle.get()
            self.Counters[i]["MAXALLOWEDVALUE"] = self.Ctr_StrVar[i].maxallowed.get()
            self.Counters[i]["TICKSPERBASE"] = self.Ctr_StrVar[i].ticksperbase.get()
            self.Counters[i]["OsCounterType"] = self.Ctr_StrVar[i].cntr_type.get()


    def create_empty_counter(self):
        counter = {}
        
        # Use the last counter's name and numbers to ease the edits made by user 
        counter["Counter Name"] = "COUNTER_"
        counter["MINCYCLE"] = "1"
        counter["MAXALLOWEDVALUE"] = "0xFFFFFFFF" 
        counter["TICKSPERBASE"] = "1"
        counter["OsCounterType"] = "HARDWARE"


        return counter