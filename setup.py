from setuptools import setup

setup(name='adventure',
      version='0.1',
      description='basic adventure game',
      url='http://github.com/martyni/game',
      author='martyni',
      author_email='martynjamespratt@gmail.com',
      license='MIT',
      packages=['adventure'],
      zip_safe=False,
      entry_points = {
         'console_scripts': ['adventure=adventure.main:main'],
      },
      include_package_data=True
      )
      
