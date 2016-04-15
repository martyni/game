import pygame
import math
import random
import time
from pygame import gfxdraw
from pprint import pprint
from random import randint
pygame.init()
pygame.display.set_caption('Master the dungeon')
game_exit = False
GREEN=(0, 255, 0)
WHITE=(255, 255, 255)
BLUE=(0, 0, 255)
RED=(255, 0, 0)
BLACK=(0, 0, 0)


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
[       h    ]
[            ]
'''



class Level(object):
   def __init__(self, level, biom="grass", verbose=True):
      self.level_raw = level
      self.verbose = verbose
      self.level = self.level_raw.replace("\n","").replace("[","").replace("]","")
      self.biom = biom
      self.scalar = 50
      self.saved = False
      self.block_width = self.level_raw.find("]") - self.level_raw.find("[") - 1
      self.block_height = self.level_raw.count("[") if self.level_raw.count("[") == self.level_raw.count("]") else False
      self.log("Initializing screen")
      self.screen = pygame.display.set_mode((self.block_width  * self.scalar, self.block_height * self.scalar))
      self.log("block_width : {}".format(self.block_width))
      self.log("block_height : {}".format(self.block_height))
      self.blocks = set()
      self.water_blocks = set()
      self.heading = pygame.font.SysFont(None, self.scalar)
      self.sub_heading = pygame.font.SysFont(None, self.scalar/2)
      self.para = pygame.font.SysFont(None, self.scalar/3)
      self.clock = pygame.time.Clock()
      self.old_clock = 0
      self.update = 50
      self.rotation = 0
      self.addition = 0
      if not self.block_height:
         raise Exception("Line openers '[':{opens} don't equal line closes '[':{closes}".format(
            opens = self.level.count("["),
            closes = self.level.count("]")
            ))
      if biom == "grass":
         self.log("Building grass biom {block_width} wide and {block_height} high".format(block_width = self.block_width, block_height=self.block_height))
         self.screen.fill(GREEN)  
         self.filler=GREEN
 
   def log(self, message):
     if self.verbose:
        pprint(message)
  
   def draw_path(self, x , y):
      pygame.draw.rect(self.screen, WHITE, [x * self.scalar, y * self.scalar, self.scalar, self.scalar])
 
   def draw_water(self, x , y):
      pygame.draw.rect(self.screen, BLUE, [x * self.scalar, y * self.scalar, self.scalar, self.scalar])
      self.water_blocks.add((x, y))

   def draw_house(self, x , y):
      pygame.draw.rect(self.screen, RED, [x * self.scalar, y * self.scalar, self.scalar, self.scalar])
      self.blocks.add((x, y))

   def message_to_screen(self,message, x, y):
      screen_text = self.para.render(message, True, BLACK)
      self.screen.blit(screen_text, (x * self.scalar ,y * self.scalar))
   
   def information_to_screen(self, message):
      x = (self.block_width/20) * self.scalar
      y = (self.block_height - self.block_height/5) * self.scalar
      screen_text = self.sub_heading.render(message, True, BLACK)
      self.screen.blit(screen_text, (x , y))
  
   def water_effect(self, x, y):
      x = x * self.scalar
      y = y * self.scalar
      for line in range(3):
         deg = (self.rotation + 1) * 15
         line = line * self.scalar/5
         colour = (5 * self.rotation + 105,) * 3
         if deg > 180:
            pygame.draw.arc(self.screen, colour, [x , line + y, self.scalar, self.scalar/2], math.radians(deg -30), math.radians(deg), 1 ) 

         else:
            pygame.draw.arc(self.screen, colour, [x, line + y, self.scalar, self.scalar/2], math.radians(170 - deg), math.radians(210 - deg ), 1 ) 
         
   
   def slow_clock(self):
      time = pygame.time.get_ticks()
      
      if time > (self.update + self.old_clock):
         self.rotation += 1
         if self.rotation  > 23:
            self.rotation = 0
            self.addition +=1
         self.old_clock = time
      
         
   def draw_level(self, save=False):
      x = 0
      y = 0
      self.log(self.level)
      self.screen.fill(GREEN)
      for pixel in self.level:
         if pixel in {"-","|"} :
            self.draw_path(x, y)    
         elif pixel == "~":
            self.draw_water(x, y)
         elif pixel == "h":
            self.draw_house(x, y)
         x += 1 
         if not x % self.block_width :
            y += 1
            x = 0 
 
      if self.verbose:
         for x, y in self.blocks:
            self.message_to_screen("BLOCK", x, y)

      for x, y in self.water_blocks:
         if not self.verbose:
            self.water_effect(x, y)
         else:
            self.message_to_screen("WATER", x, y)
 
      if save and not self.saved:
         pygame.image.save(self.screen, 'current_background.jpg')
         self.saved = True
            
   def loop(self):
      while not game_exit:
         self.draw_level()
         pygame.display.update()      
         self.slow_clock()
         self.clock.tick(100)

if __name__ == '__main__':
   my_level = Level(level, verbose=False )
   my_level.loop()
 
