import pyautogui
import pygame

#All my lovely win32's, goddddd i love these fuckers
import win32gui
import win32con
import win32api
pygame.init()

#My own script imports (:
import Cat_class
from Logic_handler import Frame_logic_handler
import subprocess

#Standard Pygame Stuffy stuff, idk what to call it dawg
clock = pygame.time.Clock()
delta_time = 0.1


#Screen Setting:
screen = pygame.display.set_mode((pyautogui.size()),pygame.NOFRAME)
Cat_class.Cat.Load_pics()
#Images 
Cat_laying = pygame.image.load("Pictures/Laying_cat.png").convert_alpha()


transparent = (255, 0, 128)
Arial_font = pygame.font.SysFont("Arial",30)
LastPos = pyautogui.position()
pyautogui.click(100,200)
pyautogui.moveTo(LastPos)
# Setting transparent window using win32gui
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparent), 0, win32con.LWA_COLORKEY)
#  O_O

Test_cat = Cat_class.Cat(Cat_laying,100, (screen.get_height() - Cat_laying.get_height()/2))
Test_cat2 = Cat_class.Cat(Cat_laying,200, (screen.get_height() - Cat_laying.get_height()/2))
Test_cat3 = Cat_class.Cat(Cat_laying,300, (screen.get_height() - Cat_laying.get_height()/2))

# ---  :J  ---
def Draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

def Blit_objects(Objects):
    for object in Objects:
        screen.blit(object.current_pic,(object.x - object.current_pic.get_width()/2,object.y - object.current_pic.get_height()/2))
        #pygame.draw.circle(screen,(255,0,0),(object.x,object.y),5)

Running = True
pyautogui.moveTo(600,600)

CurserPos = 0,0
while Running:
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    CurserPos = pyautogui.position()
    print(CurserPos)
    screen.fill(transparent)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        # (:  ): 
        if event.type == pygame.KEYDOWN:
            # /:
            if event.key == pygame.K_ESCAPE:
                Running = False
            # ((((:
    
    Draw_text("Testing",Arial_font,(0,0,0),0,0)
    #print(Test_cat.x,Test_cat.y)

    Blit_objects(Cat_class.Cat_list)
    #pygame.draw.circle(screen,(0,0,255),CurserPos,5)
    #pygame.draw.circle(screen,(0,0,235),(CurserPos[0]-40,CurserPos[1]-40),5)

    for cat in Cat_class.Cat_list:
        cat.Obj_logic()
    

    # --__--
    Frame_logic_handler.Frame_logic()
    pygame.display.update()

pygame.quit()