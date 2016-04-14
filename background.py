import pygame
import math
import random
import time
from pygame import gfxdraw
from pprint import pprint
pygame.init()
pygame.display.set_caption('Master the dungeon')
game_exit = False
GREEN=(0, 255, 0)
WHITE=(255, 255, 255)
BLUE=(0, 0, 255)
RED=(255, 0, 0)
verbose_flag = True



level = '''
[       |||  ]
[       |||  ]
[       |||  ]
[       |||  ]
[-------|||  ]
[---------|  ]
[~~~~~~~~~~~~]
[~~~~~~~~~~~~]
[~~~~~~~~~~~~]
[~~~~~~~~~~~~]
[            ]
[            ]
'''
def verbose(text):
  if verbose_flag:
     pprint(text)



class Level(object):
   def __init__(self, level, biom="grass"):
      self.level_raw = level
      self.level = self.level_raw.replace("\n","").replace("[","").replace("]","")
      self.biom = biom
      self.scalar = 50
      self.block_width = self.level_raw.find("]") - self.level_raw.find("[") - 1
      self.block_height = self.level_raw.count("[") if self.level_raw.count("[") == self.level_raw.count("]") else False
      
      verbose("Initializing screen")
      self.screen = pygame.display.set_mode((self.block_width  * self.scalar, self.block_height * self.scalar))
      verbose("block_width : {}".format(self.block_width))
      verbose("block_height : {}".format(self.block_height))
      if not self.block_height:
         raise Exception("Line openers '[':{opens} don't equal line closes '[':{closes}".format(
            opens = self.level.count("["),
            closes = self.level.count("]")
            ))
      if biom == "grass":
         verbose("Building grass biom {block_width} wide and {block_height} high".format(block_width = self.block_width, block_height=self.block_height))
         self.screen.fill(GREEN)  
 
   def draw_path(self, x , y):
      pygame.draw.rect(self.screen, WHITE, [x * self.scalar, y * self.scalar, self.scalar, self.scalar])
 
   def draw_water(self, x , y):
      pygame.draw.rect(self.screen, BLUE, [x * self.scalar, y * self.scalar, self.scalar, self.scalar])

   def draw_house(self, x , y):
      pygame.draw.rect(self.screen, RED, [x * self.scalar, y * self.scalar, self.scalar, self.scalar])

   def draw_level(self, save=False):
      x = 0
      y = 0
      #verbose(self.level)
      for pixel in self.level:
         if pixel in {"-","|"} :
            self.draw_path(x, y)    
            #verbose("x:{x},\ny:{y},\npixel:{pixel}".format(x=x, y=y, pixel=pixel))
         elif pixel == "~":
            self.draw_water(x, y)
         elif pixel == "h":
            self.draw_house(x, y)
           
         x += 1 
         if not x % self.block_width :
            y += 1
            x = 0 
      if save:
         pygame.image.save(self.screen, 'current_background.jpg')
            
   def loop(self):
      #while not game_exit:
      self.draw_level()
      pygame.display.update()      
         
if __name__ == '__main__':
   my_level = Level(level)
   for i in range(10000000):
      my_level.loop()
   
