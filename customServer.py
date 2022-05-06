import time
import keyboard
import shutil
import os
import importlib
import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk
from tkinter import Scrollbar
from tkinter import BooleanVar
from tkinter import StringVar
from tkinter import Text


import sys
import threading
import datetime
import unidecode


global root 
global masterButton
global MasterList

def main():

    
    global root
    global masterButton

    global MasterList
    MasterList = "MasterList.txt"
    
    root = tk.Tk()
    

    root.geometry("700x500")
    root.pack_propagate(0)
    root.title('Candy Kingdom v0.1')
    root.configure(bg='pink')
    p1 = PhotoImage(file = 'pb-2.jpg')
    root.iconphoto(False, p1)

    MasterFrame = ttk.Frame(root, padding=10, border = 2)
    MasterFrame.grid()
    
    Frame = tk.Frame(root, border = 2)
    Frame.configure(bg='pink')
    Frame.grid()

    #--------------------------Console Window
    textbox = Console(MasterFrame)
    
    v=Scrollbar(MasterFrame, orient='vertical', command=textbox.yview, width = 10)
    v.grid(row = 1, column = 2, sticky = "e", rowspan=2)
    textbox.grid(row = 1, column = 0, sticky = "nsew", columnspan = 3)
    textbox["yscrollcommand"] = v.set

    #The boolean that decides whether the server is running
    masterButton = BooleanVar()
    
    #Greeting Message
    ttk.Label(MasterFrame, text="- Welcome - ", borderwidth = 10).grid(column=0, row=0)
    
    #Server Console
    ttk.Button(MasterFrame, text="Start", command=Server).grid(column=2, row=0)
    ttk.Button(MasterFrame, text="Stop", command=stop).grid(column=3, row=0)
    ttk.Button(MasterFrame, text="Quit", command=root.destroy).grid(column=4, row=0)


    arrayOfDays = [BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar(), BooleanVar(),BooleanVar()]
    all_CheckBox = BooleanVar()
    all_CheckBox.set(1)
    
    def checkButtonChanger2022():

        if all_CheckBox.get() == 1:
            for day in arrayOfDays:
                day.set(1)

        if all_CheckBox.get() == 0:
            for day in arrayOfDays:
                day.set(0)

    def checkButtonChanger_helper():
        counter = 0

        for day in arrayOfDays:
            if day.get() == 0:
                all_CheckBox.set(0)

        for day in arrayOfDays:
            if day.get() == 1:
                counter = counter + 1

        if counter == 7:
            all_CheckBox.set(1)
            
    W = "W"
    ttk.Checkbutton(Frame, text="Monday", variable=arrayOfDays[0], command=checkButtonChanger_helper).grid(row=6,column=0, sticky=W)
    ttk.Checkbutton(Frame, text="Tuesday", variable=arrayOfDays[1], command=checkButtonChanger_helper).grid(row=6,column=1, sticky=W)
    ttk.Checkbutton(Frame, text="Wednesday", variable=arrayOfDays[2], command=checkButtonChanger_helper).grid(row=6,column=2, sticky=W)
    ttk.Checkbutton(Frame, text="Thursday", variable=arrayOfDays[3], command=checkButtonChanger_helper).grid(row=6,column=3, sticky=W)
    ttk.Checkbutton(Frame, text="Friday", variable=arrayOfDays[4], command=checkButtonChanger_helper).grid(row=6,column=4, sticky=W)
    ttk.Checkbutton(Frame, text="Saturday", variable=arrayOfDays[5], command=checkButtonChanger_helper).grid(row=6,column=5, sticky=W)
    ttk.Checkbutton(Frame, text="Sunday", variable=arrayOfDays[6], command=checkButtonChanger_helper).grid(row=6,column=6, sticky=W)
    ttk.Checkbutton(Frame, text="All", variable=all_CheckBox, command=checkButtonChanger2022).grid(row=6,column=7, sticky=W)


    
    

    global scriptName
    global timeSchedule

    scriptName = StringVar()
    timeSchedule = StringVar()
    
    ttk.Label(Frame, text="Add New Script😎").grid(row = 3, column = 0)
    ttk.Label(Frame, text="      ").grid(row=4, column = 0)

    ttk.Label(Frame, text="Enter Script Path: ").grid(row=5, column = 0)
    
    ttk.Entry(Frame, textvariable = scriptName).grid(row=5, column = 1, columnspan=2, sticky="nesw")

    ttk.Label(Frame, text="Enter Time: ", ).grid(row=7, column = 0)
    
    ttk.Entry(Frame, textvariable = timeSchedule).grid(row=7, column = 1, columnspan=2, sticky="nesw")
    
    ttk.Button(Frame, command = writeToMasterFile, text="Submit").grid(column=0, row=8)

    
    for buttons in arrayOfDays:
        buttons.set(1)

    #Place to enter new scripts and decide what time they run
    ttk.Entry(MasterFrame)


    
    
    root.mainloop()

def importModules(MasterList = None):
    
    print("Importing modules...")
    
    if MasterList is None:
        print("CRITICAL ERROR: No MasterList")
        stop()
        return

    MasterList = open(MasterList, "r")
    items = MasterList.read()
    MasterList.close()

    for scripts in items:
        try:
            importlib.import_module(scripts)
            print("\tImporting {} at {}".format(str(scripts), datetime.datetime.now()))
          
        except ImportError:
            print ("ERROR: {} not found".format(scripts))

    print("Finished modules...")

def Server(scriptName = None, timeThing = None):
    
    if masterButton.get() == True:
        print("Server already running")
        return
    
    print("Server Start")
    masterButton.set(True)
    global MasterList 


    importModules(MasterList)

    print("Starting Server - {}".format(datetime.datetime.now()))
    #the heartbeat
    while masterButton.get() == True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('x'):  # if key 'q' is pressed 
                print('Server Closed')
                break  # finishing the loop
        except:
            print('Server Closed')
            break  # if user pressed a key other than the given key the loop will break

        root.update_idletasks()
        root.update()

    print("Server Stopped - {}".format(datetime.datetime.now()))

def runscript(theScript = None, argies = None):
        th = threading.Thread(target=theScript, args=argies)
        #add threading
        #theScript
        th.start()
        th.join()
        
def stop():
    masterButton.set(False)

def fromAListOfPathsOnTheSharedDrive_ImportThemAllIntoRunningDirectory(ListThing = None):
    currentDirectory = os.getcwd()

    if ListThing:
        for files in ListThing:
            shutil.copy(files, currentDirectory)

def importFileToCurrentDirectory(FileName = None):
    currentDirectory = os.getcwd()
    shutil.copy(FileName, currentDirectory)

def writeToMasterFile(Text = None):
    global scriptName
    global timeSchedule

    if scriptName is None or timeSchedule is None:
        return



    Text = scriptName.get() + "" +  timeSchedule.get()

    #if MasterList
    global MasterList

    file1 = open(MasterList, "a")
    unaccented_string = unidecode.unidecode(Text)
    file1.write(unaccented_string + "\n")
    file1.close()

def addNewScriptToRunningServer(ScriptPath = None, Time = None, Day = None):
    print("Adding {} to run at {} on {}".format(ScriptPath, Time, Day))

class Console(Text):
    def __init__(self, *args, **kwargs):
        kwargs.update({"state": "disabled"})
        Text.__init__(self, *args, **kwargs)
        self.bind("<Destroy>", self.reset)
        self.old_stdout = sys.stdout
        
        
        self.config(height = 10, width= 20, borderwidth=10)


        sys.stdout = self
    
    def delete(self, *args, **kwargs):
        self.config(state="normal")
        self.delete(*args, **kwargs)
        self.config(state="disabled")
    
    def write(self, content):
        self.config(state="normal")
        self.insert("end", content)
        self.config(state="disabled")
        self.see('end')      
    
    def reset(self, event):
        sys.stdout = self.old_stdout    

    def flush(self):
        pass

    def start(self):
        self.refresh()

main()
