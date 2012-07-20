# setup.py
import sys

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

if sys.platform == 'darwin':
    INCLUDE_DIRS = ['/usr/local/include', '.'] + [numpy.get_include()]
    LIBRARY_DIRS = ["/usr/local/lib"]
elif sys.platform == 'win32':
	print("FORMATTING WIN32")
	INCLUDE_DIRS = [r"C:\Program Files (x86)\boost\boost_1_47",]
	LIBRARY_DIRS = [r"C:\Program Files (x86)\\boost\boost_1_47\lib",]
	   
ext_modules=[
    Extension("regex",
              sources=["regex.pyx",],
              include_dirs=INCLUDE_DIRS,
              language="c++"
              )
    ]

setup(
  name = "regex",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)
