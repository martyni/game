from setuptools import setup
import rustyvale
setup(name='rustyvale',
      version=rustyvale.version,
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
      
