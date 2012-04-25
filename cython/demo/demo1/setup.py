# setup.py

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
    Extension("demo",
              ["demo.pyx"])
    ]

setup(
  name = "Demos",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)
