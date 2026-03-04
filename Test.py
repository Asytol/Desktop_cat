import ctypes 
from os import startfile,path,environ
import psutil
import win32gui
import win32process
from time import sleep
import subprocess
from sys import stdout
import threading
import pexpect

dir_path = path.dirname(path.realpath(__file__))
#startfile(rf"{dir_path}/dist/SlugReact.exe")
file = None
hwnd = 0
def Open_file(something):
    global file  
    global hwnd
    print(something)
    environ["PYTHONUNBUFFERED"] = "1"
    file = subprocess.Popen(
        rf"{dir_path}/dist/Test_Image_window copy.exe", 
        stdout=subprocess.PIPE
    )
    print("Started file")
    hwnd = file.stdout.readline().strip()
    print(hwnd)
    

#Open_file()

thread = threading.Thread(target=Open_file,kwargs={"something": "bop"})
thread.start()

print("thread started, starting loop")
while True:
    pass
    #print("weh")
    #print(hwnd)


#{
#while True:
#    file.stdout.flush()
#    output = file.stdout.read()
#    print(output)
    #print("q")
    #if output == b"EXE Loaded.": #reminder for future Adam after shower, put a /n in slugreact.
    #    print("hehehehehaw")
    #if file.poll() == None and output == b"E Loaded.":
    #    print("broke") 
#}  
        
print("yes")

def check_for_slugs():
    
    hwnds_list = []
    def callback(hwnd,nothing):
        if win32gui.IsWindowVisible(hwnd):
            thread_id,process_id = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(process_id)
            if process.name() == "SlugReact.exe":
                print(hwnd)
                hwnds_list.append(hwnd)
    win32gui.EnumWindows(callback,None)
    return hwnds_list

hwnds = check_for_slugs()
#print(f"hwnds = {hwnds[0]}")

if len(hwnds) > 0:
    win32gui.MoveWindow(hwnds[0],0,0,0,0,False)
