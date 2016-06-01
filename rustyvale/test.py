import pygame
import unittest
from background import Level
from main import Game
from time import sleep
pygame.init()
test_level = pygame.image.load('test_assets/background.jpg')
random_image = pygame.image.load('test_assets/random.jpg')
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
current_level = Level('level', level, verbose=False)
block_size = current_level.scalar


def update_delay():
    pygame.display.update()


class TestBackgroundMethods(unittest.TestCase):

    def make_level(self, level):
        return Level('level', level, verbose=False)

    def test_background_draws(self):
        '''Checks that background exports correct image compared to previously rendered image'''
        current_level.draw_level(save=True)
        level_copy = pygame.image.load('current_background.jpg')
        self.assertEqual(level_copy.get_view().raw, test_level.get_view().raw)
        self.assertNotEqual(level_copy.get_view().raw,
                            random_image.get_view().raw)
        update_delay()

    def test_proportions(self):
        '''Checks blocksizes of level object are correct'''
        self.assertEqual(current_level.block_width, 12)
        self.assertEqual(current_level.block_height, 9)

    def test_path(self):
        '''Checks that a path gets correctly rendered'''
        current_level.draw_path(0, 0)
        self.assertEqual(current_level.screen.get_at(
            (0, 0)), (255, 255, 255, 255))
        update_delay()

    def test_water(self):
        '''Checks that a path gets correctly rendered'''
        current_level.draw_water(0, 0)
        self.assertEqual(current_level.screen.get_at((0, 0)), (0, 0, 255, 255))
        update_delay()

    def test_house(self):
        '''Checks that a path gets correctly rendered'''
        current_level.draw_house(0, 0)
        self.assertEqual(current_level.screen.get_at((2, 4)), (255, 0, 0, 255))
        update_delay()

    def test_render(self):
        '''Checks texture triggers'''
        for terrain in ['|', '-', '~', 'h', ' ']:
            level = '[{}]'.format(terrain)
            new_level = self.make_level(level)
            new_level.draw_level()
            self.assertNotEqual(new_level.screen.get_at((0, 0)), (0, 255, 0, 255)) if terrain != ' ' else self.assertEqual(
                new_level.screen.get_at((0, 0)), (100, 200, 0, 255))
            update_delay()

    def test_background_update(self):
        '''Checks texture triggers'''
        background_update = self.make_level(level)
        for draw_function in background_update.draw_level(), background_update.draw_house(0, 0), background_update.draw_level():
            update_delay()
        self.assertEqual(
            background_update.screen.get_at((0, 0)), (100, 200, 0))

    def test_house_update(self):
        '''Checks texture triggers'''
        background_update = self.make_level(level)
        for draw_function in background_update.draw_level(), background_update.draw_house(0, 0):
            update_delay()
        self.assertNotEqual(
            background_update.screen.get_at((0, 0)), (0, 255, 0, 255))

    def test_information_to_screen(self):
        '''Checks info is on screen'''
        test_info = self.make_level('[-]')
        test_info.draw_level()
        test_info.information_to_screen('hi')
        update_delay()

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


class TestMain(unittest.TestCase):
    def make_game(self, path='test_assets/assets/levels/'):
        return Game(path=path)

    def test_load_game(self):
        game = self.make_game()
        self.assertTrue(game)
        game.load_levels()
        last_level = 0
        for level in game.levels:
            game.levels[level].draw_level()
            pygame.display.update()
            surface = pygame.display.get_surface()
            self.assertNotEqual(last_level, surface.get_view().raw)
            last_level = surface.get_view().raw
   
if __name__ == '__main__':
    unittest.main()
