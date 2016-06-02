from yaml import load, dump
import os
import pygame
path = os.path.dirname(__file__) if os.path.dirname(__file__) else "."

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper   


class Controls(object):
   def __init__(self, path=path):
      self.path = path + "/assets/controls.yaml" if path else "assets/controls.yaml"
      self.data = load(open(self.path,"r").read())
      self.reverse_data = { self.data[key]:key for key in self.data }
         
   def get_events(self, events, screen, background, character):
      self.my_game_events = []
      for e in events:
         if e.type == pygame.QUIT:
            quit()
         if e.type == pygame.VIDEORESIZE:
            background.xscalar = e.size[0]
            background.yscalar = e.size[1] 
         if e.type == pygame.KEYDOWN:
            key = self.reverse_data.get(e.key, False)
            if key in ("left","right") and character.position[0] == character.old_position[0] and not character.horizontal:
               character.key_map[key]()
            elif key in ("up", "down") and character.position[1] == character.old_position[1] and not character.vertical:
               character.key_map[key]()
         elif e.type == pygame.KEYUP:
            key = self.reverse_data.get(e.key, False)
            if key == character.horizontal or key == character.vertical:
               character.stop_direction(key)

      return self.my_game_events


if __name__ == "__main__":
   my_controls = Controls()
   
