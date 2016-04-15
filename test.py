import pygame
import unittest
from background import Level
from time import sleep
pygame.init()
test_level = pygame.image.load('assets/test.jpg')
random_image = pygame.image.load('assets/random.jpg')
level = '''
[       |||  ]
[  h    |||  ]
[       |||  ]
[       |||  ]
[-------|||  ]
[---------|  ]
[~~~~~~~~~~~~]
[~~~~~~~~~~~~]
[            ]
'''
current_level = Level(level, verbose=False)
block_size = current_level.scalar

def update_delay():
   pygame.display.update()
   sleep(0.1)


class TestBackgroundMethods(unittest.TestCase): 
   def make_level(self, level):
       return Level(level, verbose=False)

   def test_background_draws(self):
       '''Checks that background exports correct image compared to previously rendered image'''
       current_level.draw_level(save=True)
       level_copy = pygame.image.load('current_background.jpg')
       self.assertEqual(level_copy.get_view().raw, test_level.get_view().raw )
       self.assertNotEqual(level_copy.get_view().raw, random_image.get_view().raw)
       update_delay()
       
   def test_proportions(self):
       '''Checks blocksizes of level object are correct'''
       self.assertEqual(current_level.block_width, 12)
       self.assertEqual(current_level.block_height, 9)

   def test_path(self):
       '''Checks that a path gets correctly rendered'''
       current_level.draw_path(0, 0)
       self.assertEqual(current_level.screen.get_at((0,0)), (255, 255, 255, 255))
       update_delay()
   
   def test_water(self):
       '''Checks that a path gets correctly rendered'''
       current_level.draw_water(0, 0)
       self.assertEqual(current_level.screen.get_at((0,0)), (0, 0, 255, 255))
       update_delay()

   def test_house(self):
       '''Checks that a path gets correctly rendered'''
       current_level.draw_house(0, 0)
       self.assertEqual(current_level.screen.get_at((0,0)), (255, 0, 0, 255))
       update_delay()
   
   def test_render(self):
       '''Checks texture triggers'''
       for terrain in ['|', '-', '~', 'h', ' ']:
          level = '[{}]'.format(terrain)
          new_level = self.make_level(level)
          new_level.draw_level()
          self.assertNotEqual(new_level.screen.get_at((0,0)), (0, 255, 0, 255)) if terrain != ' ' else self.assertEqual(new_level.screen.get_at((0,0)), (0, 255, 0, 255))
          update_delay()

   def test_background_update(self):
       '''Checks texture triggers'''
       background_update = self.make_level(level)
       for draw_function in background_update.draw_level(), background_update.draw_house(0,0), background_update.draw_level():
          update_delay()
       self.assertEqual(background_update.screen.get_at((0,0)), (0, 255, 0, 255))

   def test_house_update(self):
       '''Checks texture triggers'''
       background_update = self.make_level(level)
       for draw_function in background_update.draw_level(), background_update.draw_house(0,0):
          update_delay()
       self.assertNotEqual(background_update.screen.get_at((0,0)), (0, 255, 0, 255))

   @unittest.expectedFailure
   def test_no_left_bracket(self):
      '''Checks badly formatted levels don't draw'''
      l = self.make_level("]")

   @unittest.expectedFailure
   def test_no_right_bracket(self):
      '''Checks badly formatted levels don't draw'''
      l = self.make_level("[")

   @unittest.expectedFailure
   def test_brackets_misalign(self):
      l = self.make_level("][")

if __name__ == '__main__':
    unittest.main()
