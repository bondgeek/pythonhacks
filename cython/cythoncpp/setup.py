from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
  name = 'Demos',
  ext_modules=[
    Extension("rectangle",
              sources=["rectangle.pyx", "cpp_rect.cpp"], # Note, you can link against a c++ library instead of including the source
              include_dirs=["."],
              language="c++"),
    ],
  cmdclass = {'build_ext': build_ext},

)
