# coding=utf-8
"""
appinstance
-
Active8 (04-03-15)
author: erik@a8.nl
license: GNU-GPL2
"""
from setuptools import setup
setup(name='historybash',
      version='76',
      description='Bash history command colorized on levenshtein distance of last 10 commands',
      url='https://github.com/erikdejonge/historybash',
      author='Erik de Jonge',
      author_email='erik@a8.nl',
      license='GPL',
      entry_points={
          'console_scripts': [
              'hist=historybash:main',
          ],
      },
      packages=['historybash'],
      zip_safe=True,
      install_requires=['sh', 'arguments', 'python-Levenshtein', 'docopt', 'ujson', 'consoleprinter', 'future', 'pygments', 'pyyaml'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Operating System :: POSIX",
          "Environment :: MacOS X",
          "Topic :: System",
      ])
