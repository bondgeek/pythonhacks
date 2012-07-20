# setup.py
import sys

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

def get_define_macros():
    defines = [ ('HAVE_CONFIG_H', None)]
    if sys.platform == 'win32':
        # based on the SWIG wrappers
        defines += [
            (name, None) for name in [
                '__WIN32__', 'WIN32', 'NDEBUG', '_WINDOWS', 'NOMINMAX', 'WINNT',
                '_WINDLL', '_SCL_SECURE_NO_DEPRECATE', '_CRT_SECURE_NO_DEPRECATE',
                '_SCL_SECURE_NO_WARNINGS',
            ]
        ]
    return defines

def get_extra_compile_args():
    if sys.platform == 'win32':
        args = ['/GR', '/FD', '/Zm250', '/EHsc' ]
    else:
        args = []

    return args

def get_extra_link_args():
    if sys.platform == 'win32':
        args = ['/subsystem:windows', '/machine:I386']
    else:
        args = []

    return args
 

if sys.platform == 'darwin':
    INCLUDE_DIRS = ['/usr/local/include', '.']
    LIBRARY_DIRS = ["/usr/local/lib"]
    ext_args = dict(
              include_dirs=INCLUDE_DIRS,
              library_dirs=LIBRARY_DIRS,
              libraries = ['boost_regex'], # libraries to link
              language="c++"
              )
              
elif sys.platform == 'win32':
    print("FORMATTING WIN32")
    INCLUDE_DIRS = [r"C:\Program Files (x86)\boost\boost_1_47", '.']
    LIBRARY_DIRS = [r"C:\Program Files (x86)\boost\boost_1_47\lib",]
    ext_args = dict(
              include_dirs=INCLUDE_DIRS,
              library_dirs=LIBRARY_DIRS,
              define_macros = get_define_macros(),
              extra_compile_args = get_extra_compile_args(),
              extra_link_args = get_extra_link_args(),
              # visual c++ uses 'auto linking' libraries to link
              language="c++"
              )
ext_modules=[
    Extension("dateparser",
              sources=["dateparser.pyx", "_dateparser.cpp"],
              **ext_args
              )
    ]

setup(
  name = "dateparser",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)
