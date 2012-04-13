import os
import sys

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

if sys.platform == 'darwin':
    INCLUDE_DIRS = ['/usr/local/include', '.']
    LIBRARY_DIRS = ["/usr/local/lib"]
    
    os.environ['LDFLAGS'] = "-arch i386"
    os.environ['ARCHFLAGS'] = "-arch i386"
    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.3"

setup(name="PyQuant",
      ext_modules=[Extension(
                   "PyQuant",                 # name of extension
                   ["quantlib/version.pyx"], #  our Cython source
                   language="c++")],  # causes Cython to create C++ source
      cmdclass={'build_ext': build_ext})