import pygame
import numpy
import math
import random
import time
from pygame import gfxdraw
from pprint import pprint
from random import randint
pygame.init()
pygame.display.set_caption('Master the dungeon')
game_exit = False
GREEN = (100, 200, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_RED = (128, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (128, 128, 0)
BROWN = (255, 128, 0)



class Character(object):

    def __init__(self, name, position=[2,4], screen=False, scalar=100, clock=False, verbose=True):
        self.name = str(name)
        self.verbose = verbose
        self.scalar = scalar
        self.log("Initializing character")
        self.screen = pygame.display.set_mode(
            (10 * self.scalar,  10 * self.scalar)) if not screen else screen
        self.clock = pygame.time.Clock() if not clock else clock
        self.old_clock = 0
        self.update = 50
        self.rotation = 0
        self.addition = 0
        self.position = position
        self.old_position = list(position)
        self.moving = False
        self.mv = [0, 0]
        self.facing = "down"
        self.vertical = False
        self.horizontal = False

    def log(self, message):
        if self.verbose:
            pprint(self.name + " : " + message)

    def slow_clock(self):
        time = pygame.time.get_ticks()

        if time > (self.update + self.old_clock):
            self.rotation += 1
            if self.rotation > 23:
                self.rotation = 0
                self.addition += 1
            self.old_clock = time

    def draw_character(self):
       x = self.old_position[0] * self.scalar + self.mv[0] + self.scalar/2
       y = self.old_position[1] * self.scalar + self.mv[1] + self.scalar/2
       size = self.scalar/2
       for func in pygame.gfxdraw.filled_circle, pygame.gfxdraw.aacircle:
          colour = BLACK if func == pygame.gfxdraw.aacircle else YELLOW
          func(self.screen, 
               x,
               y,
               size,
               colour)
       if self.facing == "down":
          pygame.gfxdraw.aatrigon(self.screen,
                 x + size, y,
                 x , y + size,
                 x - size, y,
                 RED)
       elif self.facing == "up":   
          pygame.gfxdraw.aatrigon(self.screen,
                 x + size, y,
                 x , y - size,
                 x - size, y,
                 RED)
       elif self.facing == "left":   
          pygame.gfxdraw.aatrigon(self.screen,
                 x, y + size,
                 x - size, y ,
                 x , y - size,
                 RED)
       elif self.facing == "right":   
          pygame.gfxdraw.aatrigon(self.screen,
                 x, y + size,
                 x + size, y ,
                 x , y - size,
                 RED)

    def check_movement(self):
       step = self.scalar / 25
       if (self.scalar * self.old_position[0]) + self.mv[0] < self.scalar * self.position[0]:
          self.mv[0] += step
       if (self.scalar * self.old_position[0]) + self.mv[0] > self.scalar * self.position[0]:
          self.mv[0] -= step
       if (self.scalar * self.old_position[0]) + self.mv[0] == self.scalar * self.position[0]:
          self.old_position[0] = int(self.position[0])
          self.mv[0] = 0
          if self.horizontal == "left":
             self.position[0] -=1
          elif self.horizontal == "right":
             self.position[0] +=1

       if (self.scalar * self.old_position[1]) + self.mv[1] < self.scalar * self.position[1]:
          self.mv[1] += step
       if (self.scalar * self.old_position[1]) + self.mv[1] > self.scalar * self.position[1]:
          self.mv[1] -= step
       if (self.scalar * self.old_position[1]) + self.mv[1] == self.scalar * self.position[1]:
          self.old_position[1] = int(self.position[1])
          self.mv[1] = 0
          if self.vertical == "up":
             self.position[1] -=1
          elif self.vertical == "down":   
             self.position[1] +=1

    def move_character(self, events):
       for event in events:
          if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_LEFT:
                self.log("Going left")
                self.position[0] -= 1
                self.facing = "left"
                self.horizontal = "left"
             if event.key == pygame.K_RIGHT:
                self.log("Going right")
                self.position[0] += 1
                self.facing = "right"
                self.horizontal = "right"
             if event.key == pygame.K_UP:
                self.log("Going up")
                self.position[1] -= 1
                self.facing = "up"
                self.vertical = "up"
             if event.key == pygame.K_DOWN:
                self.log("Going down")
                self.position[1] += 1
                self.facing = "down"
                self.vertical ="down"
          if event.type == pygame.KEYUP:
             if event.key == pygame.K_LEFT:
                self.log("Stop going left")
                self.horizontal = "stop" 
             if event.key == pygame.K_RIGHT:
                self.log("Stop going right")
                self.horizontal = "stop"
             if event.key == pygame.K_UP:
                self.log("Stop going up")
                self.vertical = "stop"
             if event.key == pygame.K_DOWN:
                self.log("Stop going down")
                self.vertical = "stop"
   

    def loop(self):
        while not game_exit:
            self.screen.fill(BLACK)
            self.check_movement()
            self.draw_character()
            pygame.display.update()
            self.slow_clock()
            self.move_character(pygame.event.get())
            self.clock.tick(100)

if __name__ == '__main__':
    my_character = Character("dave", verbose=True)
    my_character.loop()
