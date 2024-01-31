from setuptools import setup, Extension
from glob import glob
import os

if os.name == 'nt':
    setup(
        ext_modules=[
            Extension(
                name="MPGrid",
                sources=glob("src/*.c"),
                define_macros=[('MP_PYTHON_LIB', None),],
                extra_compile_args=['-fopenmp'],
                include_dirs=['zlib/include'],
                library_dirs=['zlib/lib/x64'],
                libraries=['zlibstat']
            )
        ]
    )
else:
   setup(
       ext_modules = [
           Extension(
               name="MPGrid",
               sources=glob("src/*.c"),
               define_macros=[('MP_PYTHON_LIB', None),],
               extra_compile_args=['-fopenmp']
           )
       ]
   )

