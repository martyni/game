from setuptools import setup

setup(name='rustyvale',
      version='0.1',
      description='basic adventure game',
      url='http://github.com/martyni/game',
      author='martyni',
      author_email='martynjamespratt@gmail.com',
      license='MIT',
      packages=['rustyvale'],
      zip_safe=False,
      entry_points = {
         'console_scripts': ['rustyvale=rustyvale.main:main'],
      },
      include_package_data=True
      )
      
