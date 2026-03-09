from pygame import time
import pyautogui
from ctypes import windll
from os import startfile,environ
import subprocess
from win32gui import MoveWindow
import threading
import win32api
#ehmmmm, idk if this is a good thing to do but... ehh... Fail-safe off?
pyautogui.FAILSAFE = False

clock = time.Clock()
delta_time = 0.1

Last_click_state = 1

Cursor_pos = pyautogui.position()

Left_click_down = False
class Frame_logic_handler:
    Lock_cursor = False
    Locked_cursor = False
    Lock_position = 0,0

    def Frame_logic():
        global Left_click_down
        Set_delta_time()
        Set_cursor_pos()
        Left_click_down = Check_left_click()

        if Frame_logic_handler.Lock_cursor == True:
            if Frame_logic_handler.Locked_cursor == False:
                Frame_logic_handler.Lock_position = pyautogui.position()
                Frame_logic_handler.Locked_cursor = True

            Lock_cursor_func(Frame_logic_handler.Lock_position)
        else:
            Frame_logic_handler.Locked_cursor = False

#Fix later
def Check_left_click():
    global Last_click_state
    state = win32api.GetKeyState(0x01)
    if state != Last_click_state:
        Last_click_state = state
        return True
    else:
        return False
    
def Caculate_parabola_2p(x1,y1,x2,y2):
    #substitutions formeln
    yn1 = y1 * x2
    yn2 = y2 * x1

    an = ((x1**2) * x2) - ((x2**2) * x1)

    a_multiplier = (yn1 - yn2) / an
    b_multiplier = (y1 - (x1**2 * a_multiplier)) / x1
    print(f"Point1:{x1,y1},Point2:{x2,y2},Multipliers:{a_multiplier,b_multiplier}")
    return a_multiplier, b_multiplier

def Calculate_parabola_3p(x1,y1,x2,y2,x3,y3):
    #fuh nah im too tired to do this
    pass

def Hard_create_window_get_hwnd(directory):
    hwnd = 0
    file = subprocess.Popen('start',executable=directory,stdout=subprocess.PIPE)
    while True:
        line = file.stdout.readline()
        print(line.strip())
        if file.poll() == None and line.strip() == b"EXE Loaded.":
            print(hwnd)
            return hwnd
        else:
            hwnd = line.strip()

def Check_AABB(obj_points,point):
    #X axis
    if obj_points[0][0] < point[0] < obj_points[1][0] and obj_points[0][1] < point[1] < obj_points[2][1]:
        return True

def Lock_cursor_func(Current_pos_lock):
    pyautogui.moveTo(Current_pos_lock,_pause=False)

def Set_delta_time():
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

def Get_delta_time():
    return delta_time

def Set_cursor_pos():
    global Cursor_pos
    Cursor_pos = pyautogui.position()

def Get_cursor_pos():
    return Cursor_pos

class Window_creator:
    def __init__(self): 
        self.Has_file = False
        self.hwnd = 0
        self.line: bytes = b"empty"
    
    def Popen_and_get_hwnd(self,directory):
        environ["PYTHONUNBUFFERED"] = "1"
        file = subprocess.Popen('start',executable=directory,stdout=subprocess.PIPE)

        self.hwnd = file.stdout.readline().strip()

    def Soft_create_window_no_hwnd(self,directory):
        thread = threading.Thread(target=self.Popen_and_get_hwnd,kwargs={"directory": directory})
        thread.start()
        self.Has_file = True

    def try_getting_hwnd(self):
        self.hwnd_to_set = self.hwnd
        if self.hwnd_to_set != 0:
            self.hwnd = 0
            self.Has_file = False
            return self.hwnd_to_set

        return 0