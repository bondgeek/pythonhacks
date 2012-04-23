import os
import sys
import glob

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

if sys.platform == 'darwin':
    INCLUDE_DIRS = ['/usr/local/include', '.']
    LIBRARY_DIRS = ["/usr/local/lib"]

def collect_ext_dirpaths():
    cython_extension_directories = []
    for dirpath, directories, files in os.walk('quantlib'):
        print 'Path', dirpath

        # skip the settings package
        if (dirpath.find('settings') > -1 or 
           dirpath.find('test') > -1 or 
           dirpath.find('termstructures') > -1):
            print(">>Skipping %s" % dirpath)
            continue

        # if the directory contains pyx files, cythonise it
        if len(glob.glob('{}/*.pyx'.format(dirpath))) > 0:
            cython_extension_directories.append(dirpath)

    return cython_extension_directories

# Manual Extensions
settings_extension = Extension('quantlib.settings',
        ['quantlib/settings/settings.pyx', 'quantlib/settings/ql_settings.cpp'],
        language='c++',
        include_dirs=INCLUDE_DIRS,
        library_dirs=LIBRARY_DIRS,
        libraries=['QuantLib']
    )

termstructure_names = [
'quantlib.termstructures.volatility.equityfx.black_vol_term_structure',
'quantlib.termstructures.yields.rate_helpers',
'quantlib.termstructures.yields.yield_term_structure',
'quantlib.termstructures.yields.flat_forward',
'quantlib.termstructures.yields.zero_curve',
]

termstructure_extensions = cythonize(
        [Extension(
                ext_name, # name of extension
                sources=['.'.join([ext_name.replace('.', '/'), 
                                   '.pyx'])], #  our Cython source
                include_dirs=INCLUDE_DIRS,
                library_dirs=LIBRARY_DIRS,
                libraries = ['QuantLib'], # libraries to link
                language="c++") # causes Cython to create C++ source
        for ext_name in termstructure_names
        ]
        ) 

piecewise_yield_curve_extension = Extension(
        'quantlib.termstructures.yields.piecewise_yield_curve',
        [
            'quantlib/termstructures/yields/piecewise_yield_curve.pyx',
            'quantlib/termstructures/yields/_piecewise_support_code.cpp'
        ],
        language='c++',
        include_dirs=INCLUDE_DIRS,
        library_dirs=LIBRARY_DIRS,
        libraries=['QuantLib']
    )

# Collect extensions
print("\nCollecting Extensions...\n")
collected_dirpaths = collect_ext_dirpaths()
for dirpath in collected_dirpaths:
    print("\Dirpath: %s" % dirpath)
    
print("\nCythonizing...\n")    
collected_extensions = cythonize(
        [Extension(
                '*', # name of extension
                sources=['{}/*.pyx'.format(dirpath)], #  our Cython source
                include_dirs=INCLUDE_DIRS,
                library_dirs=LIBRARY_DIRS,
                libraries = ['QuantLib'], # libraries to link
                language="c++") # causes Cython to create C++ source
        for dirpath in collected_dirpaths
        ]
        )

# remove  all the manual extensions from the collected ones
manual_extensions = [settings_extension, piecewise_yield_curve_extension] + termstructure_extensions
names = [extension.name for extension in manual_extensions]
for ext in collected_extensions:
    if ext.name in names:   
        print("Dropping %s" % ext.name)
        collected_extensions.remove(ext)
        continue

extensions = collected_extensions + manual_extensions
print("\nAll the extensions are gathered:")
for ext in extensions:
    print ext.name
print("\n\nBeginning\n\n")

setup(name="quantlib",
      ext_modules=extensions,  
      cmdclass={'build_ext': build_ext})