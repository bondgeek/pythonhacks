# setup.py
import sys

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

if sys.platform == 'darwin':
    INCLUDE_DIRS = ['/usr/local/include', '.']
    LIBRARY_DIRS = ["/usr/local/lib"]
    
ext_modules=[
    Extension("dateparser",
              sources=["dateparser.pyx", "_dateparser.cpp"],
              include_dirs=INCLUDE_DIRS,
              library_dirs=LIBRARY_DIRS,
                libraries = ['boost_regex'], # libraries to link
              language="c++"
              )
    ]

setup(
  name = "dateparser",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)
