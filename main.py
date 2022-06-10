 
# The following is a Python code with these features: 
# 1. Allows a user to run python scripts on a schedule that the user defines.
# 2. The scripts are imported and run at the specific days and times.
# 3. The scripts are run in a separate thread.
#Test


import threading
import multiprocessing
import time
import datetime
import os
import sys
import importlib
import traceback
from multiprocessing import Process
import pandas as pd

#This class is used to represent a script that will be run
global ledger

class Script:
    def __init__(self, scriptName, day, time, arguments):
        self.scriptName = scriptName
        self.moduleName = self.scriptName.replace('.py', '')
        self.days = day
        self.time = time
        self.arguments = arguments
    
    def run(self):
        module = importlib.import_module(self.moduleName)
        p = multiprocessing.Process(target=module.main(), args=self.arguments)
            
        try:
            p.start()
        except Exception:
            traceback.print_exc()

def parse_script_time(script_time):
    while (len(script_time) < 2):
        script_time.append('00') 
    return script_time

def get_day_of_week():
    day_of_week = time.strftime("%A")
    return day_of_week

def get_time_of_day():
    time_of_day = time.strftime("%H:%M")
    time_of_day = time_of_day.split(':')
    time_of_day = parse_script_time(time_of_day)
    return time_of_day


def compare_time(time_of_day, script_time):
    if (time_of_day == script_time):
        return True
    else:
        return False

def compare_day_of_week(day_of_week, script_day):
    if (day_of_week == script_day):
        return True
    else:
        return False

def main():
    global ledger
    ledger = {'DayOfWeek' : ["Monday", "Monday"], 'Time' : ["14:00", "15:00"], 'ScriptName' : ["testScript.py", "test2.py"]}
    
    ledgerDataFrame = pd.DataFrame(data=ledger)
    
    while True:
        #actual time of day and day of week
        time_of_day = get_time_of_day()
        day_of_week = get_day_of_week()
        for index, item in ledgerDataFrame.iterrows():
            #We cracked it boys
            if item["DayOfWeek"] == day_of_week and item["Time"] == time_of_day:
                script = Script("testScript.py", "Monday", "16:00", "")
                script.run()

        time.sleep(60)


main()    