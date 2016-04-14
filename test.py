import pygame
import unittest
from background import Level
from time import sleep
pygame.init()

test_level = pygame.image.load('assets/test.jpg')
random_image = pygame.image.load('assets/random.jpg')
level = '''
[       |||  ]
[       |||  ]
[       |||  ]
[       |||  ]
[-------|||  ]
[---------|  ]
[~~~~~~~~~~~~]
[~~~~~~~~~~~~]
[            ]
'''
current_level = Level(level)
block_size = current_level.scalar

def update_delay():
   pygame.display.update()
   sleep(0.1)

class TestStringMethods(unittest.TestCase):

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
          new_level = Level(level)
          new_level.draw_level()
          self.assertNotEqual(new_level.screen.get_at((0,0)), (0, 255, 0, 255)) if terrain != ' ' else self.assertEqual(new_level.screen.get_at((0,0)), (0, 255, 0, 255))
          update_delay()

if __name__ == '__main__':
    unittest.main()
