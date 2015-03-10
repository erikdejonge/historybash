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
      version='0',
      description='Bash history command colorized on levenshtein distance of last 10 commands',
      url='https://github.com/erikdejonge/history',
      author='Erik de Jonge',
      author_email='erik@a8.nl',
      license='GPL',
      scripts=['history/hist'],
      packages=['history'],
      zip_safe=True,
      install_requires=['python-Levenshtein'],
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Development Status :: 4 - Beta ",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Operating System :: POSIX",
          "Topic :: System",
      ])
