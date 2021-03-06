#!/usr/bin/python
import pygame
import sys
from background import Level
from controls import Controls
from character import Character
import os
import re
from pprint import pprint

pygame.init()

if len(sys.argv) < 2:
   path = os.path.dirname(__file__) if os.path.dirname(__file__) else False
else:
   path = sys.argv[1]

class Game(object):

    def __init__(self, verbose=False, path=path):
        self.levels = {}
        self.home = os.environ['HOME']
        self.path = path if path else os.environ['PWD']
        self.game = pygame.init()
        self.game_exit = False
        self.current_level = "0-0"
        self.levels_loaded = False
        self.main_character_loaded = False
        self.clock = pygame.time.Clock()
        self.verbose = verbose
        self.width = 0
        self.height = 0
        self.scalar = 70
        self.screen = None
        self.controls = Controls(path=path)
        self.game_locations = {}

    def load_levels(self):
        print self.path
        for path, directory, levels in os.walk(self.path + "/assets/levels/"):
            for level in levels:
                match = re.match("(.*)\.lvl", level)

                if match:
                    level_name = match.group(1)
                    file_name = path + match.group(0)
                    with open(file_name, "r") as level_content:
                        self.levels[level_name] = Level(level_name, level_content.read(
                        ), clock=self.clock, scalar=self.scalar, verbose=self.verbose)
                        self.width = self.levels[level_name].block_width * self.scalar if self.levels[
                            level_name].block_width * self.scalar > self.width else self.width
                        self.height = self.levels[level_name].block_height * self.scalar if self.levels[
                            level_name].block_height * self.scalar > self.height else self.height

        self.levels_loaded = True

    def log(self, message):
        pprint(message) if self.verbose else None

    def load_characters(self):
        self.main_character = Character(
            "dave", screen=self.screen, scalar=self.scalar, clock=self.clock)
        self.main_character_loaded = True

    def valid_level(self, level):
        return True if self.levels.get(level, False) else False

    def go_direction(self, vector, direction, limit1, limit2, oldlimit1, oldlimit2):
        vectors = self.current_level.split('-')
        vectors[vector] = str(int(vectors[vector]) + direction)
        new_level = vectors[0] + '-' + vectors[1]
        if self.valid_level(new_level):
            self.current_level = vectors[0] + '-' + vectors[1]
            self.main_character.log('entered ' + self.current_level)
            self.main_character.old_position[vector] = limit1
            self.main_character.position[vector] = limit2
        else:
            self.main_character.old_position[vector] = oldlimit1
            self.main_character.position[vector] = oldlimit2

    def go_right(self):
        self.go_direction(0, 1, -1, 0, self.levels[
                          self.current_level].block_width - 1, self.levels[self.current_level].block_width - 1)

    def go_left(self):
        self.go_direction(0, -1, self.levels[self.current_level].block_width, self.levels[
                          self.current_level].block_width - 1, 0, 0)

    def go_up(self):
        self.go_direction(1, 1, self.levels[self.current_level].block_height, self.levels[
                          self.current_level].block_height - 1, 0, 0)

    def go_down(self):
        self.go_direction(1, -1, -1, 0, self.levels[
                          self.current_level].block_height - 1, self.levels[self.current_level].block_height - 1)
    def save_screen(self):
        pygame.image.save(self.screen, self.home + '/current_screen.jpg')

    def main_loop(self):
        if not self.levels_loaded:
            self.load_levels()
        if not self.main_character_loaded:
            self.load_characters()
        count = 0
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        
        while not self.game_exit:
            try:
               self.main_character.blocks.remove(tuple(self.main_character.position))
            except KeyError:
               pass
            events = pygame.event.get()
            self.last_level = self.current_level
            self.levels[self.current_level].draw_level()
            self.main_character.blocks = self.levels[self.current_level].blocks
            self.main_character.water_blocks = self.levels[
                self.current_level].water_blocks
            self.controls.get_events(events, self.screen, self.levels[self.current_level], self.main_character)
            self.main_character.check_movement()
            self.main_character.draw_character()
            self.levels[self.current_level].draw_foreground()
            pygame.display.update()
            self.levels[self.current_level].slow_clock()
            self.clock.tick(60)
            if self.main_character.position[0] > self.levels[self.current_level].block_width - 1:
                self.go_right()
            if self.main_character.position[0] < 0:
                self.go_left()
            if self.main_character.position[1] < 0:
                self.go_up()
            if self.main_character.position[1] > self.levels[self.current_level].block_height - 1:
                self.go_down()
            self.main_character.blocks.add(tuple(self.main_character.position))

def main():
   my_game = Game()
   my_game.main_loop()

if __name__ == "__main__":
   main()
