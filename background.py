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

level = '''
[       |||           ]
[       |||           ]
[    -  |||           ]
[       |||           ]
[-------|||           ]
[---------|           ]
[~~~~~~~~-~~~         ]
[~~h~~~~~~~~~         ]
[~~~~~~~~~~~~         ]
[  h~~~~~~~~~         ]
[       hh-           ]
[                     ]
'''


class Level(object):

    def __init__(self, level, screen=False, scalar=100, clock=False, biom="grass", verbose=True):
        self.level_raw = level
        self.verbose = verbose
        self.level = self.level_raw.replace(
            "\n", "").replace("[", "").replace("]", "")
        self.biom = biom
        self.map = {}
        self.scalar = scalar
        self.saved_level = False
        self.block_width = self.level_raw.find(
            "]") - self.level_raw.find("[") - 1
        self.block_height = self.level_raw.count("[") if self.level_raw.count(
            "[") == self.level_raw.count("]") else False
        self.log("Initializing screen")
        self.screen = pygame.display.set_mode(
            (self.block_width * self.scalar, self.block_height * self.scalar)) if not screen else screen
        self.log("block_width : {}".format(self.block_width))
        self.log("block_height : {}".format(self.block_height))
        self.blocks = set()
        self.water_blocks = set()
        self.heading = pygame.font.SysFont(None, self.scalar)
        self.sub_heading = pygame.font.SysFont(None, self.scalar / 2)
        self.para = pygame.font.SysFont(None, self.scalar / 3)
        self.clock = pygame.time.Clock() if not clock else clock
        self.old_clock = 0
        self.update = 50
        self.rotation = 0
        self.addition = 0
        if not self.block_height:
            raise Exception("Line openers '[':{opens} don't equal line closes '[':{closes}".format(
                opens=self.level.count("["),
                closes=self.level.count("]")
            ))
        if biom == "grass":
            self.log("Building grass biom {block_width} wide and {block_height} high".format(
                block_width=self.block_width, block_height=self.block_height))
            self.screen.fill(GREEN)
            self.filler = GREEN

    def log(self, message):
        if self.verbose:
            pprint(message)

    def draw_path(self, x, y):
        pygame.draw.rect(self.screen, WHITE, [
                         x * self.scalar, y * self.scalar, self.scalar, self.scalar])
        left_pixel = self.map.get((x -1, y), "off screen")
        right_pixel = self.map.get((x + 1, y), "off screen")
        top_pixel = self.map.get((x, y -1), "off screen")
        bottom_pixel = self.map.get((x, y + 1), "off screen")
        indent = 7
        if not left_pixel == "path" and left_pixel != "off screen" and left_pixel !="house":
           pygame.gfxdraw.vline(self.screen, indent + x * self.scalar, y * self.scalar, (1 + y) * self.scalar, BLACK)
        if not right_pixel == "path" and right_pixel != "off screen":
           pygame.gfxdraw.vline(self.screen,  (1 + x) * self.scalar - indent, y * self.scalar, (1 + y) * self.scalar, BLACK)
        if not top_pixel == "path" and top_pixel != "off screen":
           pygame.gfxdraw.hline(self.screen, x * self.scalar, (x + 1) * self.scalar,  y * self.scalar + indent, BLACK)
        if not bottom_pixel == "path" and bottom_pixel != "off screen":
           pygame.gfxdraw.hline(self.screen, x * self.scalar, (x + 1) * self.scalar,  (y +1)  * self.scalar - indent, BLACK)

    def draw_water(self, x, y):
        pygame.draw.rect(self.screen, BLUE, [
                         x * self.scalar, y * self.scalar, self.scalar, self.scalar])
           

        self.water_blocks.add((x, y))
        self.water_effect(x, y)

    def draw_house(self, x, y):
        right_pixel = self.map.get((x + 1, y), "off screen")
        if right_pixel == "biom":
           self.draw_biom(x, y)
        elif right_pixel == "water":
           self.draw_water(x, y)
        elif right_pixel == "path":
           self.draw_path(x, y)

        self.blocks.add((x, y))
        
        def draw_roof():
           for func in pygame.gfxdraw.filled_trigon,  pygame.gfxdraw.aatrigon:
              colour = DARK_RED if func == pygame.gfxdraw.filled_trigon else BLACK
              func(self.screen,
                 (x +1) * self.scalar,
                 y * self.scalar,
                 (x + 1) * self.scalar - self.scalar/6,
                 y * self.scalar + self.scalar/4,
                 (x + 1) * self.scalar,
                 y * self.scalar - self.scalar/2,
                 colour)
              colour = RED if func == pygame.gfxdraw.filled_trigon else BLACK
           for func in  [pygame.gfxdraw.filled_polygon, pygame.gfxdraw.aapolygon]:
              colour = RED if func == pygame.gfxdraw.filled_polygon else BLACK
              func(self.screen,
                  (
                   ((x + 1) * self.scalar, y * self.scalar - self.scalar/2), 
                   (x * self.scalar, y * self.scalar - self.scalar/2), 
                   (x  * self.scalar - self.scalar/6, y * self.scalar + self.scalar/4),
                   ((x +1)  * self.scalar - self.scalar/6, y * self.scalar + self.scalar/4),
                  ),
                  colour)
        def draw_front():
           for func in  [pygame.gfxdraw.filled_polygon, pygame.gfxdraw.aapolygon]:
              colour = YELLOW if func == pygame.gfxdraw.filled_polygon else BLACK
              func(self.screen,
                  (
                   (x  * self.scalar - self.scalar/6, y * self.scalar + self.scalar/4),
                   ((x + 1)  * self.scalar - self.scalar/6, y * self.scalar + self.scalar/4),
                   ((x + 1)  * self.scalar - self.scalar/6, (y + 1)  * self.scalar),
                   (x  * self.scalar - self.scalar/6, (y + 1) * self.scalar),
                   ),
                   colour
                  )
              #door
              colour = BROWN if func == pygame.gfxdraw.filled_polygon else BLACK
              func(self.screen,
                  (
                   (x  * self.scalar + self.scalar/2, (y + 1) * self.scalar),
                   (x  * self.scalar + self.scalar/3, (y + 1) * self.scalar),
                   (x  * self.scalar + self.scalar/3, (y + 1) * self.scalar - self.scalar/3),
                   (x  * self.scalar + self.scalar/2, (y + 1) * self.scalar - self.scalar/3),
                   ),
                   colour
                  )
        def draw_side():
           for func in  [pygame.gfxdraw.filled_polygon, pygame.gfxdraw.aapolygon]:
              colour = DARK_YELLOW if func == pygame.gfxdraw.filled_polygon else BLACK
              func(self.screen,
                  (
                   ((x + 1)  * self.scalar - self.scalar/6, (y + 1)  * self.scalar),
                   ((x + 1)  * self.scalar, (y + 1)  * self.scalar - self.scalar/4),
                   ((x + 1)  * self.scalar, y   * self.scalar),
                   ((x + 1)  * self.scalar - self.scalar/6, y   * self.scalar + self.scalar/4),
                   ),
                   colour
                  )


        draw_front()
        draw_roof()  
        draw_side() 

    def draw_grass(self, x, y, colour):
        points = []
        wobble = self.scalar/10 if self.rotation > 12 else 0
        for point in range(0, 20, self.scalar/10):
           points.append((x + point, y))
           points.append((x + point - self.scalar/10, wobble + y - self.scalar/10))
           points.append((x + wobble + point - self.scalar/7, y - self.scalar/5))
           points.append((x + wobble + point - self.scalar/5, y - self.scalar/10))
           points.append((x + point - self.scalar/10, y))
        points.append((x + point + 5, y))
        pygame.gfxdraw.filled_polygon(self.screen,
                              points,
                              colour)
        pygame.gfxdraw.aapolygon(self.screen,
                              points, 
                              BLACK)

    def wavy_line(self, x, y, colour, wavyness):
        ran = colour[1]
        shake = wavyness if self.rotation > 12 else -wavyness
        for line in range(10):
           path_colour = numpy.add(colour , (line)*3)  
           pygame.gfxdraw.bezier(self.screen, 
           ((shake + line + x + self.scalar/2 + self.scalar/ran, y ),
            (shake + line + x , y + self.scalar/4),
            (shake + line + x + self.scalar, y + 3 * self.scalar/4),
            (shake + line + x + self.scalar/2 + self.scalar/ran, y + self.scalar)
           ),
            3, 
           path_colour)

    def draw_biom(self, x, y):
        x_scaled = x * self.scalar
        y_scaled = y * self.scalar
        seed = self.sudo_random(x, y)
        seed2 = self.sudo_random(x_scaled, y_scaled)
        if self.biom == "grass":
            grass_green = numpy.subtract(GREEN, (0, 100, 0))
            if seed % 3:
                for stem in range(int(repr(seed2)[-3]) / 2):
                    self.draw_grass(x_scaled + self.scalar/2 + self.scalar/3 * math.sin(stem *10),
                                    y_scaled + self.scalar/2 + self.scalar/3 * math.cos(stem *10),
                                    grass_green)
                    #pygame.draw.arc(self.screen, (0, 100, 0), [
                    #                x_scaled - stem * 10 , y_scaled + 5 * math.sin(stem *10) , self.scalar * 2, self.scalar + stem], math.radians(0), math.radians(35), self.scalar /5)

    def sudo_random(self, x, y, limit=None):
        if not limit:
            return hash((x, y))
        elif hash((x, y)) > limit:
            return int(limit * float(repr(hash((x, y)))[-3]) / 10) + 1

    def message_to_screen(self, message, x, y):
        screen_text = self.para.render(message, True, BLACK)
        self.screen.blit(screen_text, (x * self.scalar, y * self.scalar))

    def information_to_screen(self, message):
        x = (self.block_width / 20) * self.scalar
        y = (self.block_height - self.block_height / 5) * self.scalar
        screen_text = self.sub_heading.render(message, True, BLACK)
        self.screen.blit(screen_text, (x, y))

    def water_effect(self, x, y):
        x = x * self.scalar
        y = y * self.scalar
        seed = self.sudo_random(x, y, 3)
        water_colour = numpy.subtract(BLUE, (100,0,0))
        for line in range(seed):
            deg = (self.rotation + 1) * 15
            line = line * self.scalar / 5
            if deg > 180:
                colour = (deg/2, deg/2, 255)
                pygame.draw.arc(self.screen, colour, [
                                x, line + y, self.scalar, self.scalar / 2], math.radians(deg - 30), math.radians(deg), self.scalar / 10)
                pygame.draw.arc(self.screen, BLACK, [
                                x, line + y, self.scalar, self.scalar / 2], math.radians(deg - 30), math.radians(deg), 1)
                self.wavy_line(x, y, (100,220,220),4)
            else:
                self.wavy_line(x, y, (100,220,220),4)
                colour = (deg , deg,225) 
                pygame.draw.arc(self.screen, colour, [x, line + y, self.scalar, self.scalar / 2], math.radians(
                    170 - deg), math.radians(210 - deg), self.scalar / 5)
                pygame.draw.arc(self.screen, BLACK, [x, line + y, self.scalar, self.scalar / 2], math.radians(
                   170 - deg), math.radians(210 - deg), 1)

    def slow_clock(self):
        time = pygame.time.get_ticks()

        if time > (self.update + self.old_clock):
            self.rotation += 1
            if self.rotation > 23:
                self.rotation = 0
                self.addition += 1
            self.old_clock = time

    def save_level(self):
        pygame.image.save(self.screen, 'current_background.jpg')
        self.information_to_screen('saved')
        pygame.display.update()
        self.saved_level = True

    def draw_level(self,  save=False):
        x = 0
        y = 0
        self.log(self.level)
        self.screen.fill(GREEN)
        for pixel in self.level:
            if pixel in {"-", "|"}:
                self.draw_path(x, y)
                self.map[(x,y)] = "path"
            elif pixel == "~":
                self.draw_water(x, y)
                self.map[(x,y)] = "water"
            elif pixel == "h":
                self.draw_house(x, y)
                self.map[(x,y)] = "house"
            else:
                self.draw_biom(x, y)
                self.map[(x,y)] = "biom"
            x += 1
            if not x % self.block_width:
                y += 1
                x = 0

        if self.verbose:
            for x, y in self.blocks:
                self.message_to_screen("BLOCK", x, y)

        for x, y in self.water_blocks:
            if self.verbose:
                self.message_to_screen("WATER", x, y)

        if save and not self.saved_level:
            self.save_level()

    def draw_foreground(self):
       x = 0
       y = 0
       for pixel in self.level:
            if pixel == "h":
                self.draw_house(x, y)
                self.map[(x,y)] = "house"
            x += 1
            if not x % self.block_width:
                y += 1
                x = 0


    def loop(self):
        while not game_exit:
            self.draw_level(save=True)
            pygame.display.update()
            self.slow_clock()
            #self.clock.tick(1)

if __name__ == '__main__':
    my_level = Level(level, verbose=False)
    my_level.loop()
