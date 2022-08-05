import tkinter as tk
from tkinter import ttk

class OsTab:
    N_StrVar = 13
    OS_StrVar = []
    sg_oscfg = None
    sg_tasks = None
    stack_idx = 0

    def __init__(self, oscfg, tasks):
        self.sg_oscfg = oscfg
        if not oscfg:
            self.create_empty_os_config()
        self.sg_tasks = tasks
        self.stack_idx = self.N_StrVar - 1
        for i in range(self.N_StrVar):
            self.OS_StrVar.insert(i, tk.StringVar())


    def __del__(self):
        del self.OS_StrVar[:]
        self.sg_oscfg = None


    def draw(self, tab):
        # 1) CPU / SoC - Label + Edit-box
        row = 1
        label = tk.Label(tab, text="CPU / SoC name")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab,text="Entry", width=30, textvariable=self.OS_StrVar[row-1])
        if "CPU" in self.sg_oscfg:
            self.OS_StrVar[row-1].set(self.sg_oscfg["CPU"])
        else:
            print("Error: OS_Cfg does't have key: CPU")
        textb.grid(row=row, column=2)
    
        # 2) OS Name - Label + Edit-box
        row = 2
        label = tk.Label(tab, text="Image Name")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[row-1])
        if "OS" in self.sg_oscfg:
            self.OS_StrVar[row-1].set(self.sg_oscfg["OS"])
        else:
            print("Error: OS_Cfg does't have key: OS")
        textb.grid(row=row, column=2)
    
        # 3) OSEK Standard - Label + Combo-box
        row = 3
        label = tk.Label(tab, text="OSEK Standard")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("STANDARD", "EXTENDED")
        if "STATUS" in self.sg_oscfg:
            self.OS_StrVar[row-1].set(self.sg_oscfg["STATUS"])
        else:
            print("Error: OS_Cfg does't have key: STATUS")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 4) STARTUPHOOK - Label + Combo-box
        row = 4
        label = tk.Label(tab, text="STARTUPHOOK")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "STARTUPHOOK" in self.sg_oscfg:
            self.OS_StrVar[row-1].set(self.sg_oscfg["STARTUPHOOK"])
        else:
            print("Error: OS_Cfg does't have key: STARTUPHOOK")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)
    
        # 5) ERRORHOOK - Label + Combo-box
        row = 5
        label = tk.Label(tab, text="ERRORHOOK")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "ERRORHOOK" in self.sg_oscfg:
            self.OS_StrVar[row-1].set(self.sg_oscfg["ERRORHOOK"])
        else:
            print("Error: OS_Cfg does't have key: ERRORHOOK")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 6) SHUTDOWNHOOK - Label + Combo-box
        row = 6
        label = tk.Label(tab, text="SHUTDOWNHOOK")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "SHUTDOWNHOOK" in self.sg_oscfg:
            self.OS_StrVar[row-1].set(self.sg_oscfg["SHUTDOWNHOOK"])
        else:
            print("Error: OS_Cfg does't have key: SHUTDOWNHOOK")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 7) PRETASKHOOK - Label + Combo-box
        row = 7
        label = tk.Label(tab, text="PRETASKHOOK")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "PRETASKHOOK" in self.sg_oscfg:
            self.OS_StrVar[row-1].set(self.sg_oscfg["PRETASKHOOK"])
        else:
            print("Error: OS_Cfg does't have key: PRETASKHOOK")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 8) POSTTASKHOOK - Label + Combo-box
        row = 8
        label = tk.Label(tab, text="POSTTASKHOOK")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "POSTTASKHOOK" in self.sg_oscfg:
            self.OS_StrVar[row-1].set(self.sg_oscfg["POSTTASKHOOK"])
        else:
            print("Error: OS_Cfg does't have key: POSTTASKHOOK")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 9) OsProtectionHook - Label + Combo-box
        row = 9
        label = tk.Label(tab, text="OsProtectionHook")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "OsProtectionHook" in self.sg_oscfg:
            self.OS_StrVar[row-1].set(self.sg_oscfg["OsProtectionHook"])
        else:
            print("Warn: OS_Cfg does't have key: OsProtectionHook")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 10) OS_STACK_SIZE - Label + Edit-box
        row = 10
        label = tk.Label(tab, text="OS STACK SIZE")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[row-1])
        if "OS_STACK_SIZE" not in self.sg_oscfg:
            print("Error: OS_Cfg does't have key: OS_STACK_SIZE")
            self.sg_oscfg["OS_STACK_SIZE"] = 512
        self.OS_StrVar[row-1].set(self.sg_oscfg["OS_STACK_SIZE"])
        textb.grid(row=row, column=2)
        
        # 11) IRQ_STACK_SIZE - Label + Edit-box
        row = 11
        label = tk.Label(tab, text="IRQ STACK SIZE")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[row-1])
        if "IRQ_STACK_SIZE" not in self.sg_oscfg:
            print("Error: OS_Cfg does't have key: IRQ_STACK_SIZE")
            self.sg_oscfg["IRQ_STACK_SIZE"] = 512
        self.OS_StrVar[row-1].set(self.sg_oscfg["IRQ_STACK_SIZE"])
        textb.grid(row=row, column=2)
        
        # 12) OS_CTX_SAVE_SZ - Label + Edit-box
        row = 12
        label = tk.Label(tab, text="CONTEXT SAVE SIZE FOR TASKS", width=30, anchor="w")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[row-1])
        if "OS_CTX_SAVE_SZ" not in self.sg_oscfg:
            print("Error: OS_Cfg does't have key: OS_CTX_SAVE_SZ")
            self.sg_oscfg["OS_CTX_SAVE_SZ"] = 512
        self.OS_StrVar[row-1].set(self.sg_oscfg["OS_CTX_SAVE_SZ"])
        textb.grid(row=row, column=2)

        # 13) TASK_STACK_SIZE - Label + Edit-box
        row = 13
        self.stack_idx = row - 1
        label = tk.Label(tab, text="TASK STACK SIZE (Total)")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[self.stack_idx], state="readonly")
        if "TASK_STACK_SIZE" not in self.sg_oscfg:
            print("Error: OS_Cfg does't have key: TASK_STACK_SIZE")
            self.sg_oscfg["TASK_STACK_SIZE"] = 0
        self.OS_StrVar[self.stack_idx].set(self.sg_oscfg["TASK_STACK_SIZE"])
        textb.grid(row=row, column=2)
        select = tk.Button(tab, width=6, text="Update", command=self.update)
        select.grid(row=row, column=3)


    def update(self):
        self.backup_data()
        # Recalculate parameters and update
        task_stack_size = 0
        for tsk in self.sg_tasks:
            try:
                task_stack_size += int(self.sg_oscfg["OS_CTX_SAVE_SZ"])
                task_stack_size += int(tsk["STACK_SIZE"])
            except:
                print("Error: stack size computation input validation error!")
        
        if self.stack_idx > 0:
            self.OS_StrVar[self.stack_idx].set(task_stack_size)


    def backup_data(self):
        # Backup to system generator global variables
        self.sg_oscfg["CPU"]                   = self.OS_StrVar[0].get()
        self.sg_oscfg["OS"]                    = self.OS_StrVar[1].get()
        self.sg_oscfg["STATUS"]                = self.OS_StrVar[2].get()
        self.sg_oscfg["STARTUPHOOK"]           = self.OS_StrVar[3].get()
        self.sg_oscfg["ERRORHOOK"]             = self.OS_StrVar[4].get()
        self.sg_oscfg["SHUTDOWNHOOK"]          = self.OS_StrVar[5].get()
        self.sg_oscfg["PRETASKHOOK"]           = self.OS_StrVar[6].get()
        self.sg_oscfg["POSTTASKHOOK"]          = self.OS_StrVar[7].get()
        self.sg_oscfg["OsProtectionHook"]      = self.OS_StrVar[8].get()
        self.sg_oscfg["OS_STACK_SIZE"]         = self.OS_StrVar[9].get()
        self.sg_oscfg["IRQ_STACK_SIZE"]        = self.OS_StrVar[10].get()
        self.sg_oscfg["OS_CTX_SAVE_SZ"]        = self.OS_StrVar[11].get()
        self.sg_oscfg["TASK_STACK_SIZE"]       = self.OS_StrVar[12].get()
    
    
    def create_empty_os_config(self):
        self.sg_oscfg["CPU"]                   = ""
        self.sg_oscfg["OS"]                    = ""
        self.sg_oscfg["STATUS"]                = "STANDARD"
        self.sg_oscfg["STARTUPHOOK"]           = "FALSE"
        self.sg_oscfg["ERRORHOOK"]             = "FALSE"
        self.sg_oscfg["SHUTDOWNHOOK"]          = "FALSE"
        self.sg_oscfg["PRETASKHOOK"]           = "FALSE"
        self.sg_oscfg["POSTTASKHOOK"]          = "FALSE"
        self.sg_oscfg["OS_STACK_SIZE"]         = "512"
        self.sg_oscfg["IRQ_STACK_SIZE"]        = "512"
        self.sg_oscfg["OS_CTX_SAVE_SZ"]        = "128"
        self.sg_oscfg["TASK_STACK_SIZE"]       = "0"