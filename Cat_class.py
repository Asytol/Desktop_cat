#imports
from random import randint, choice,choices
from pyautogui import position,move,size,write
from pygame import image,display
from os import open,path
from win32gui import MoveWindow, GetWindowRect

#My own imports (:
from Logic_handler import delta_time,Get_delta_time
import Logic_handler

Cat_list = []



class Cat:
    Base_dir = path.dirname(path.realpath(__file__))
    Window_weights = [1,5]
    Window_directories = [f"{Base_dir}/dist/Mini_slug_react.exe",f"{Base_dir}/dist/Image_window.exe"]
    Action_time = 30
    Random_Action_Interval = (-5, 5)
    Screen_size = size() 
    Extra_win_walk_distance = 400

    Walking_time = 30
    Direction_change_time = 15
    Direction_change_interval = (-10,10)
    walk_stop_time = 5
    walk_current_stop_time = 0

    Sleep_time = 30

    Keys = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','backspace','ctrlleft','ctrlright','decimal','\n']
    Amount_of_presses = 1000
    def Load_pics():    
        Cat.Cat_laying = image.load("Pictures/Laying_cat.png").convert_alpha()
        Cat.Cat_jumping = image.load("Pictures/Cat_jumping.png").convert_alpha()
        Cat.Cat_grabbing = image.load("Pictures/Cat_grabbing.png").convert_alpha()
        Cat.Cat_awake = image.load("Pictures/Awake_cat.png").convert_alpha()
        Cat.Cat_walking = image.load("Pictures/Cat_walking.png").convert_alpha()
        Cat.Cat_keyboard = image.load("Pictures/Cat_keyboard.png").convert_alpha()
        Cat.Cat_ready = image.load("Pictures/Cat_ready.png").convert_alpha()

    def __init__(self,current_pic,x,y):
        self.current_pic = current_pic
        self.x = x
        self.y = y

        self.xvelocity = 0
        self.yvelocity = 0
        self.xvelocity_to_set = 0
        self.yvelocity_to_set = 0
        self.speed: int = 150

        #General action logic
        self.current_action_timer = 0
        self.Current_action_time = Cat.Action_time
        self.func: function = self.nothing

        #Attack logic
        self.Att_direct = 1
        self.Has_parabola = False
        self.Att_StartX = 0
        self.Att_StartY = 0

        self.Extra_distance = 40

        self.Current_X_relation = 0
        self.Parabola_A = 0
        self.Parabola_B = 0
        self.Started_dragging = False

        #Window_grab logic
        self.In_position = False
        self.Created_window = False
        self.Picked_win_drag_side = False
        self.drag_side = 1

        self.Drag_speed: int = 20 
        self.Current_hwnd = 0
        self.Current_win_width = 0
        self.Current_win_height = 0

        self.window_creator = Logic_handler.Window_creator()
        #Move_around logic
        self.walk_speed: int = 30
        self.Started_walking = False

        self.session_current_time = 0 
        self.Session_direction_chg_time = Cat.Direction_change_time
        self.walking_direction = 1
        self.current_walk_time = 0
        self.walk_stop = False
        #Sleeping logic
        self.Current_sleep_time = 0 

        #Button_mash_keyboard logic
        self.Current_press_amount = 0

        Cat_list.append(self)

    def Update_xny(self):
        self.x += self.xvelocity * Get_delta_time()
        self.y += self.yvelocity * Get_delta_time()
    def nothing(self):
        pass
    # ):<
    # - 1 UwU
    def Attack_cursor(self):
        if self.Has_parabola == False:
            #-
            self.current_pic = Cat.Cat_jumping
            self.Current_X_relation = 0
            self.Att_StartX = self.x
            self.Att_StartY = self.y
            Attack_point = position()
            #-
            if self.x < Attack_point[0]:
                self.Att_direct = 1
            else:
                self.Att_direct = -1
            if Attack_point[0] == self.x:
                self.x += 1
            self.Parabola_A,self.Parabola_B = Logic_handler.Caculate_parabola_2p(abs(Attack_point[0] - (self.Extra_distance*self.Att_direct) - self.x)*self.Att_direct,
                                               abs(Cat.Screen_size[1] - Attack_point[1] + self.Extra_distance - (Cat.Screen_size[1] - self.Att_StartY)),
                                               abs(Attack_point[0] - self.x)*self.Att_direct, abs(Cat.Screen_size[1] - Attack_point[1] - (Cat.Screen_size[1] - self.Att_StartY)))    
            self.Has_parabola = True
            Logic_handler.Frame_logic_handler.Lock_cursor = True

        if self.Has_parabola == True:
            if self.x * self.Att_direct < position()[0] * self.Att_direct and self.Started_dragging == False:
                self.Jump_To_cursor()              
            elif self.y < Cat.Screen_size[1] - Cat.Cat_laying.get_height()/2:
                Logic_handler.Frame_logic_handler.Lock_cursor = False
                self.Drag_Mouse_down()
            else:
                self.func = self.nothing
                self.Has_parabola = False
                self.Started_dragging = False
                self.current_pic = Cat.Cat_laying

    # - 2 U-U
    def Jump_To_cursor(self):
        self.xvelocity_to_set += self.speed * self.Att_direct
        self.Update_xny()
        self.Current_X_relation += self.xvelocity * Get_delta_time()
        self.y = self.Att_StartY - (self.Current_X_relation**2 * self.Parabola_A + self.Parabola_B * self.Current_X_relation)
    # - 3 U-U
    def Drag_Mouse_down(self):
        if self.Started_dragging == False:
            self.current_pic = Cat.Cat_grabbing
            self.x = position()[0]
            self.y = position()[1]
            self.xvelocity_to_set = 0
            self.xvelocity = 0
            self.Started_dragging = True

        dist = self.speed * Get_delta_time()
        if dist > 1:
            move(0,yOffset=dist,_pause=False)
        else:
            move(0,yOffset=1,_pause=False)
        self.x,self.y = position()
    # (:<   hehehe, goofy window opener
    # -- 1 UwU
    def Drag_in_window(self):
        self.Update_xny()
        if self.In_position == False:
            #-
            if self.Picked_win_drag_side == False:
                self.current_pic = Cat.Cat_walking
                self.drag_side = choice([1,-1])
                self.Picked_win_drag_side = True
            self.xvelocity_to_set = self.speed * self.drag_side
            if self.x < 0 - Cat.Extra_win_walk_distance or self.x > Cat.Screen_size[0] + Cat.Extra_win_walk_distance:
                self.In_position = True
            #-__-
        else:
            if self.Created_window == False:
                self.CreateWindow()
            else:
                self.Cat_Move_window()
    # -- 2 U-U
    def CreateWindow(self):
        
        #if self.window_creator.File_to_check == None:
        #    window = choices(Cat.Window_directories,Cat.Window_weights,k=1)
        #    
        #else:
        #    hwnd = self.window_creator.try_getting_hwnd()
        hwnd = 0
        if self.window_creator.Has_file == False:
            window = choices(Cat.Window_directories,Cat.Window_weights,k=1)
            self.window_creator.Soft_create_window_no_hwnd(window[0])
        else:
            hwnd = self.window_creator.try_getting_hwnd()
        print(hwnd)
        #hwnd = Logic_handler.Hard_create_window_get_hwnd(window[0])

        if hwnd != 0:
            rect = GetWindowRect(hwnd)
            self.Current_win_width = rect[2] - rect[0]
            self.Current_win_height = rect[3] - rect[1]
            MoveWindow(hwnd,int(self.x),int(self.y),self.Current_win_width,self.Current_win_height,False)
            self.Current_hwnd = hwnd
            self.Created_window = True
    # -- 3 U-U
    def Cat_Move_window(self):
        C_size = Cat.Screen_size[0]/2
        if self.x * -self.drag_side > float((C_size + C_size * self.drag_side)*-self.drag_side) + self.Current_win_width/2:     
            self.func = self.nothing
            #- K -
            self.In_position = False
            self.Created_window = False
            self.Picked_win_drag_side = False
        #________ 
        self.xvelocity_to_set = self.Drag_speed * -self.drag_side
        xlevel = int(self.x)-self.Current_win_width/2
        ylevel = int(self.y)-self.Current_win_height + self.current_pic.get_height()/2
        try:
            MoveWindow(self.Current_hwnd,int(xlevel),int(ylevel),self.Current_win_width,self.Current_win_height,False)
        except:
            self.Hiss()
            self.func = self.nothing
    # ⌐▨_▨ 
    # -- 1 UwU
    def Move_around(self):
        self.Update_xny()
        if self.walk_stop == False:
            if self.Started_walking == False:
                self.current_pic = Cat.Cat_walking
                self.Session_walk_time = Cat.Direction_change_time - randint(Cat.Direction_change_interval[0],Cat.Direction_change_interval[1])
                self.Started_walking = True
            #-
            if self.session_current_time > self.Session_walk_time:
                self.Session_walk_time = Cat.Direction_change_time - randint(Cat.Direction_change_interval[0],Cat.Direction_change_interval[1])
                self.session_current_time = 0
                self.walking_direction *= -1
                self.walk_stop = True
            else:
                self.session_current_time += Get_delta_time()
            #-
            if self.x < 0 + self.current_pic.get_width()/2:
                self.walking_direction = 1
                self.x = self.current_pic.get_width()/2
            elif self.x >= Cat.Screen_size[0] - self.current_pic.get_width()/2:
                self.walking_direction = -1
                self.x = Cat.Screen_size[0] - self.current_pic.get_width()/2
            
            self.xvelocity_to_set = self.walk_speed * self.walking_direction
            #__--__
            if self.current_walk_time > Cat.Walking_time:
                self.func = self.nothing
                self.current_walk_time = 0
                self.Started_walking = False
            else:
                self.current_walk_time += Get_delta_time()
        else:
            if self.walk_current_stop_time > Cat.walk_stop_time:
                self.walk_stop = False
                self.walk_current_stop_time = 0
                self.current_pic = Cat.Cat_walking
            else:
                self.walk_current_stop_time += Get_delta_time()
                self.current_pic = Cat.Cat_ready
            

    #(ᴗ˳ᴗ)ᶻ𝗓𐰁 -
    def Sleep(self):
        self.current_pic = Cat.Cat_laying
        if self.Current_sleep_time > Cat.Sleep_time:
            self.Current_sleep_time = 0
            self.func = self.nothing
        else:
            self.Current_sleep_time += Get_delta_time()
    # ₊✩‧₊ 
    def Button_mash_keyboard(self):
        if self.Current_press_amount < Cat.Amount_of_presses:
            self.current_pic = Cat.Cat_keyboard
            self.Current_press_amount += 1
            write(choice(Cat.Keys),_pause=False)
        else:
            self.func = self.nothing
            

    # If the player has done something bad, like closing the window while it's being dragged in
    # causing a pywintypes error!!! why would anyone do that!!!
    def Hiss(self):
        pass

    def Obj_logic(self):
        self.xvelocity_to_set = 0
        self.yvelocity_to_set = 0

        #Action Picking
        if self.func == self.nothing:
            self.current_pic = Cat.Cat_awake
            self.current_action_timer += Get_delta_time()
            if self.current_action_timer > self.Current_action_time:
                self.current_action_timer = 0
                self.Current_action_time = Cat.Action_time + randint(Cat.Random_Action_Interval[0],Cat.Random_Action_Interval[1])
                self.func = choice([self.Attack_cursor,self.Drag_in_window,self.Move_around,self.Sleep,self.Button_mash_keyboard])
                print(f"tried performing:{self.func}")
        
        self.func()
        # -_-  (:<
        self.xvelocity = self.xvelocity_to_set 
        #print(f"self.xvelocity = {self.xvelocity}")
        self.yvelocity = self.yvelocity_to_set 
        
        
        