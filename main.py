import pygame
import time
import random
from pprint import pprint
pygame.init()

SIZE = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

colours =  BLACK, BLUE, GREEN, RED
gameDisplay = pygame.display.set_mode((SIZE, SIZE))

pygame.display.set_caption('Master the dungeon')
pygame.display.update()
gameExit = False


lead_x_change = 0
lead_y_change = 0
lead_x = 300
lead_y = 300
pos = 0
col = BLACK
clock = pygame.time.Clock()
tick = "tick"
verbose_flag = True
font = pygame.font.SysFont(None, 25)

def verbose(text):
  if verbose_flag:
     pprint(text)

def message_to_screen(msg, colour):
   screen_text = font.render(msg, True, colour)
   gameDisplay.blit(screen_text, [SIZE/2, SIZE/2])
while not gameExit:
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
   lead_y += lead_y_change      
   lead_x += lead_x_change       
   gameDisplay.fill(WHITE)
   pygame.draw.rect(gameDisplay, col, [lead_x, lead_y, 10, 10])
   message_to_screen(str([lead_x, lead_y]), GREEN)
   pygame.display.update()
   clock.tick(100)
   tick = "tock" if tick == "tick" else "tick"
pygame.quit()
quit()
