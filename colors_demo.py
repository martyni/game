import pygame
import math
import random
from pygame import gfxdraw
from pprint import pprint
SIZE = 300
gameDisplay = pygame.display.set_mode((SIZE, SIZE))
gameExit = False

def red(x, y, time):
   return time

def green(x, y, time):
   return 255 *float(y)/SIZE

def blue(x, y, time):
   return 255 *float(x)/SIZE

time = 1
lead_x = SIZE/2
lead_y = SIZE/2
lead_y_change = 0
lead_x_change = 0
verbose_flag = True

def verbose(text):
  if verbose_flag:
     pprint(text)


while not gameExit:
   for x in range(SIZE):
      for y in range(SIZE):
         col = (red(x, y, time), green(x, y, time), blue(x, y, time))
         gfxdraw.pixel(gameDisplay, x, y, col)   
           
      time = time + 1 if time < 255 else 0
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         verbose("Quiting")
         gameExit = True
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_LEFT:
            verbose("Going left")
            lead_x_change = -2
         elif event.key == pygame.K_RIGHT:
            verbose("Going right")
            lead_x_change = 2
         elif event.key == pygame.K_UP:
            verbose("Going up")
            lead_y_change = -2
         elif event.key == pygame.K_DOWN:
            verbose("Going down")
            lead_y_change = 2
         col =(random.randint(0, 255), random.randint(0, 255),random.randint(0, 255))
      if event.type == pygame.KEYUP:
         if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            verbose("Stopping")
            lead_x_change = 0
            lead_y_change = 0
   lead_x += lead_x_change
   lead_y += lead_y_change
   pygame.draw.rect(gameDisplay, col, [lead_x, lead_y, 10, 10])
   pygame.display.update()
