import tkinter as tk
from tkinter import ttk



class MessageTab:
    n_msgs = 0
    max_msgs = 4*1024
    n_msgs_str = None
    msgs_str = []
    msgs = []
    HeaderObjs = 2 #Objects / widgets that are part of the header and shouldn't be destroyed
    HeaderSize = 1
    prf = None  # Parent Frame
    cvf = None  # Canvas Frame
    cv  = None  # Canvas
    sb  = None  # Scrollbar
    mnf = None  # Main Frame - where the widgets are scrolled

    def __init__(self, tasks):
        self.extract_messages(tasks)
        self.n_msgs = len(self.msgs)
        self.n_msgs_str = tk.StringVar()
        del self.msgs_str[:]
        for i in range(self.n_msgs):
            self.msgs_str.insert(i, tk.StringVar())
            self.msgs_str[i].set(self.msgs[i])


    def __del__(self):
        del self.n_msgs_str
        del self.msgs_str[:]


    def update_msgs(self, mstr):
        self.n_msgs = int(mstr.get())
        # print("Update messages: "+ str(self.n_msgs))        
        for i, item in enumerate(self.mnf.winfo_children()):
            if i >= self.HeaderObjs:
                item.destroy()
        self.update()


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

        # Create a frame to draw message table
        self.mnf = tk.Frame(self.cv)
        self.cv.create_window((0, 0), window=self.mnf, anchor='nw')

        #Number of modes - Label + Spinbox
        label = tk.Label(self.mnf, text="No. of Messages:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.mnf, width=10, textvariable=self.n_msgs_str, command=lambda: self.update_msgs(self.n_msgs_str),
                    values=tuple(range(0,self.max_msgs)))
        self.n_msgs_str.set(self.n_msgs)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.mnf.update_idletasks()
        # Resize the main frame to show contents for FULL SCREEN (Todo: scroll bars won't work in reduced size window)
        canvas_w = tab.winfo_screenwidth()-self.sb.winfo_width()
        canvas_h = tab.winfo_screenheight()-(spinb.winfo_height()*6)
        self.cvf.config(width=canvas_w, height=canvas_h)

        self.update()


    def update(self):
        # backup current entries
        self.backup_data()

        # Tune memory allocations based on number of rows or boxes
        n_msgs_str = len(self.msgs_str)
        if self.n_msgs > n_msgs_str:
            for i in range(self.n_msgs - n_msgs_str):
                self.msgs_str.insert(len(self.msgs_str), tk.StringVar())
                self.msgs.insert(len(self.msgs), "MSG_")
        elif n_msgs_str > self.n_msgs:
            for i in range(n_msgs_str - self.n_msgs):
                del self.msgs_str[-1]
                del self.msgs[-1]

        #print("n_msgs_str = "+ str(n_msgs_str) + ", n_msgs = " + str(self.n_msgs))
        # Draw new objects
        for i in range(0, self.n_msgs):
            label = tk.Label(self.mnf, text="Msg "+str(i)+": ")
            label.grid(row=self.HeaderSize+i, column=0, sticky="w")
            entry = tk.Entry(self.mnf, width=40, textvariable=self.msgs_str[i])
            self.msgs_str[i].set(self.msgs[i])
            entry.grid(row=self.HeaderSize+i, column=1)

        # Set the self.cv scrolling region
        self.cv.config(scrollregion=self.cv.bbox("all"))


    def backup_data(self):
        n_msgs_str = len(self.msgs_str)
        for i in range(n_msgs_str):
            self.msgs[i] = self.msgs_str[i].get()


    def extract_messages(self, tasks):
        for task in tasks:
            if "MESSAGE" in task:
                for msg in task["MESSAGE"]:
                    if msg not in self.msgs:
                        self.msgs.append(msg)
        return tasks