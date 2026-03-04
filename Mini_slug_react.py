from os import environ
import win32gui
import win32con
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
from sys import stdout
from time import sleep

from pygame import display,image,transform, event,QUIT,quit

screen = display.set_mode((262,193))
hwnd = display.get_wm_info()["window"]
print(hwnd)
stdout.flush()


screen_width = 262
Slug = image.load("LiveSluggReaction.jpg").convert_alpha()
running = True

stdout.flush()
while running == True:
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    Slug = transform.flip(Slug,1,0)
    screen.blit(Slug,(0,0))
    
    for ev in event.get():
        if ev.type == QUIT:   
            running = False
    display.flip()


quit()