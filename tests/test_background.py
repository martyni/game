import pygame
from background import Level
pygame.init()
test_level = pygame.image.load('test.jpg')
random_image = pygame.image.load('random.jpg')
level = '''
[       |||  ]
[       |||  ]
[       |||  ]
[       |||  ]
[-------|||  ]
[---------|  ]
[            ]
[            ]
[            ]
'''
my_level = Level(level)
my_level.draw_level(save=True)
current_level = pygame.image.load('current_background.jpg')
if current_level.get_view().raw == test_level.get_view().raw:
  print "they're the same"
else:
  print current_level
  print test_level

if current_level.get_view().raw == random_image.get_view().raw:
  print current_level.get_view().raw
  print random_image.get_view().raw
else:
  print "current level and dog not the same"
