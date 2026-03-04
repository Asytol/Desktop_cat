#base pygame:
from os import path,environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

from pygame import display,image
from sys import stdout
from random import choice
from os import scandir,listdir
from win32gui import MoveWindow
#-_-


image_name = choice(listdir(r"Pictures\Window_pictures"))
image_directory = rf"Pictures\Window_pictures\{image_name}"
screen = display.set_mode((1,1))

Session_image = image.load(image_directory).convert()
#--__--
Image_size = (Session_image.get_width(),Session_image.get_height())
screen = display.set_mode(Image_size)
#-
hwnd = display.get_wm_info()["window"]
print(hwnd)
stdout.flush()


#Non-base:
from pygame import event,KEYDOWN,K_ESCAPE,quit,QUIT


running = True
while running == True:
    screen.blit(Session_image,(0,0))
    for ev in event.get():
        if ev.type == QUIT:
            running = False
    display.flip()

quit()
                