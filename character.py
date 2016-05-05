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

    def __init__(self, name, position=[0,0], screen=False, scalar=100, clock=False, verbose=True):
        self.level_raw = str(name)
        self.verbose = verbose
        self.level = self.level_raw.replace(
            "\n", "").replace("[", "").replace("]", "")
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

    def log(self, message):
        if self.verbose:
            pprint(message)

    def slow_clock(self):
        time = pygame.time.get_ticks()

        if time > (self.update + self.old_clock):
            self.rotation += 1
            if self.rotation > 23:
                self.rotation = 0
                self.addition += 1
            self.old_clock = time

    def draw_character(self):
       for func in pygame.gfxdraw.filled_circle, pygame.gfxdraw.aacircle:
          colour = BLACK if func == pygame.gfxdraw.aacircle else YELLOW
          func(self.screen, 
               self.position[0] * self.scalar + self.scalar/2,
               self.position[1] * self.scalar + self.scalar/2,
               self.scalar/2,
               colour) 
    def move_character(self, events):
       for event in events:
          if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_LEFT:
                self.log("Going left")
                self.position[0] -= 1
             if event.key == pygame.K_RIGHT:
                self.log("Going right")
                self.position[0] += 1
             if event.key == pygame.K_UP:
                self.log("Going up")
                self.position[1] -= 1
             if event.key == pygame.K_DOWN:
                self.log("Going down")
                self.position[1] += 1
      

    def loop(self):
        while not game_exit:
            self.screen.fill(BLACK)
            self.draw_character()
            pygame.display.update()
            self.slow_clock()
            self.move_character(pygame.event.get())
            print self.position

if __name__ == '__main__':
    my_character = Character("dave", verbose=False)
    my_character.loop()
