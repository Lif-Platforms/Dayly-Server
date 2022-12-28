from datetime import datetime
from logging import exception
from colorama import Fore
from datetime import date

global appName
appName = ":NA:" 

def setAppName(name):
    global appName
    appName = name

def log(consoleLog):
    global current_time
    global current_date
    global appName
    now = datetime.now()
    current_date = date.today() 
    try:
        current_time = now.strftime("%H:%M:%S")
    except:
        current_time = ":UNKNOWN:"
    
    if appName == ":NA:":
        raise exception("Please Name This App!")
    else:
        print(Fore.WHITE + f"[LOG {current_date} {current_time}][{appName}]: {consoleLog}")

def error(errorLog):
    global current_time
    global current_date
    global appName
    now = datetime.now()
    current_date = date.today() 
    try:
        current_time = now.strftime("%H:%M:%S")
    except:
        current_time = ":UNKNOWN:"

    if appName == ":NA:":
        raise exception("Please Name This App!")
    else:
        print(Fore.RED + f"[ERROR {current_date} {current_time}][{appName}]: {errorLog}" + Fore.WHITE)

def warning(warnLog):
    global current_time
    global current_date
    global appName
    now = datetime.now()
    current_date = date.today() 
    try:
        current_time = now.strftime("%H:%M:%S")
    except:
        current_time = ":UNKNOWN:"

    if appName == ":NA:":
        raise exception("Please Name This App!")
    else:
        print(Fore.YELLOW + f"[WARN {current_date} {current_time}][{appName}]: {warnLog}" + Fore.WHITE)