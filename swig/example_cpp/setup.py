'''
setup.py

'''
from distutils.core import setup, Extension

example_module = Extension('_example', sources=['example_wrap.cxx', 
                                                'example.cpp'])

setup(name='example', version='0.1.666', 
      author='bondgeek', 
      description="""Example SWIG Module. with c++""", 
      ext_modules=[example_module], py_modules=['example'])