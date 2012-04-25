# setup.py
import sys

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

if sys.platform == 'darwin':
    INCLUDE_DIRS = ['/usr/local/include', '.'] + [numpy.get_include()]
    LIBRARY_DIRS = ["/usr/local/lib"]
    
ext_modules=[
    Extension("matrix",
              sources=["matrix.pyx"],
              include_dirs=INCLUDE_DIRS
              )
    ]

setup(
  name = "Matrix",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)
