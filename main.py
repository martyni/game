import pygame
from background import Level
from character import Character
import os
import re
from pprint import pprint


pygame.init()



class Game(object):

    def __init__(self, verbose=False, path='assets/levels/'):
        self.levels = {}
        self.path = path
        self.game = pygame.init()
        self.game_exit = False
        self.current_level = "1"
        self.levels_loaded = False
        self.main_character_loaded = False
        self.clock = pygame.time.Clock()
        self.verbose = verbose
        self.width = 0
        self.height = 0
        self.scalar = 100
        self.screen = None
        

    def load_levels(self):
        for path, directory, levels in os.walk(self.path):
            for level in levels:
                match = re.match("(.*)\.lvl", level)
                if match:
                    level_name = match.group(1)
                    file_name = path + match.group(0)
                    with open(file_name, "r") as level_content:
                        self.levels[level_name] = Level(level_content.read(
                        ), clock=self.clock, scalar=self.scalar, verbose=self.verbose)
                        self.width = self.levels[level_name].block_width * self.scalar if self.levels[
                            level_name].block_width * self.scalar > self.width else self.width
                        self.height = self.levels[level_name].block_height * self.scalar if self.levels[
                            level_name].block_height * self.scalar > self.height else self.height

        self.load_levels = True

    def log(self, message):
        pprint(message) if self.verbose else None

    def load_characters(self):
        self.main_character = Character("dave", screen=self.screen, scalar=self.scalar, clock=self.clock)
        self.main_character_loaded = True

    def main_loop(self):
        if not self.levels_loaded:
            self.load_levels()
        if not self.main_character_loaded:
            self.load_characters()
        count = 0
        self.screen =pygame.display.set_mode((self.width, self.height))

        while not self.game_exit:
            events = pygame.event.get()
            self.levels[self.current_level].draw_level()
            self.main_character.move_character(events)
            self.main_character.draw_character() 
            self.levels[self.current_level].draw_foreground()
            pygame.display.update()
            self.levels[self.current_level].slow_clock()
            self.clock.tick(100)
            count += 1
            if count > 100:
                self.current_level = '1' if self.current_level == '3' else str(
                    int(self.current_level) + 1)
                count = 0
if __name__ == "__main__":
    my_game = Game()
    my_game.main_loop()
