#!/usr/bin/env python
## -*- encoding: utf-8 -*-

import os
import sys
from setuptools import setup
from codecs import open # To open the README file with proper encoding
from setuptools.command.test import test as TestCommand # for tests
from setuptools.extension import Extension

try:
    from Cython.Build import cythonize as cython_cythonize
except ImportError:
    cython_cythonize = None

def _sage_include_directories():
    try:
        from sage.env import sage_include_directories
        return sage_include_directories()
    except Exception:
        include_dirs = []
        sage_local = os.environ.get("SAGE_LOCAL")
        if sage_local:
            include_dirs.append(os.path.join(sage_local, "include"))
        sage_root = os.environ.get("SAGE_ROOT")
        if sage_root:
            include_dirs.append(os.path.join(sage_root, "src"))
        if not include_dirs:
            raise RuntimeError(
                "Sage include directories not found. "
                "Run inside Sage or set SAGE_LOCAL/SAGE_ROOT."
            )
        return include_dirs

def _sage_library_directories():
    library_dirs = []
    sage_local = os.environ.get("SAGE_LOCAL")
    if not sage_local:
        return library_dirs
    for libdir in ("lib", "lib64"):
        candidate = os.path.join(sage_local, libdir)
        if os.path.isdir(candidate):
            library_dirs.append(candidate)
    return library_dirs

def _openmp_enabled(include_dirs):
    if os.environ.get("PYCONTROLLEDREDUCTION_OPENMP") == "0":
        return False
    for include_dir in include_dirs:
        if os.path.exists(os.path.join(include_dir, "omp.h")):
            return True
    return False

def cythonize(*args, **kwargs):
    try:
        from sage.misc.package_dir import cython_namespace_package_support
    except ImportError:
        return cython_cythonize(*args, **kwargs)
    with cython_namespace_package_support():
        return cython_cythonize(*args, **kwargs)

# Get information from separate files (README, VERSION)
def readfile(filename):
    with open(filename,  encoding='utf-8') as f:
        return f.read()

# For the tests
class SageTest(TestCommand):
    def run_tests(self):
        errno = os.system("sage -t --force-lib pycontrolledreduction")
        if errno != 0:
            sys.exit(1)


cythonize_dir = "build"



controlledreduction_sources = [
        "tools/binomial.cc",
        "tools/default_args.cc",
        "tools/binomial_ZZ.cc",
        "tools/factorial_p_adic.cc",
        "tools/tuple_list_generator.cc",
        "tools/valuation_of_factorial.cc",
        "tools/change_of_variables_monomial.cc",
        "tools/geometric_picard.cc",
        "dr/init.cc",
        "dr/monomial_to_basis_J.cc",
        "dr/reduce_vector_J_poly.cc",
        "dr/get_reduction_matrix_J.cc",
        "dr/constructors.cc",
        "dr/get_inclusion_matrix_J.cc",
        "dr/reduce_vector_J_ZZ.cc",
        "dr/compute_everything_J.cc",
        "dr/compute_reduction_matrix_J_ZZ.cc",
        "dr/reduce_vector_J.cc",
        "dr/get_solve_J.cc",
        "dr/reduce_vector_J_poly_ZZ.cc",
        "dr/get_reduction_matrix_J_ZZ.cc",
        "dr/matrix_J.cc",
        "dr/compute_inclusion_matrix_J.cc",
        "dr/isSmooth.cc",
        "dr/compute_reduction_matrix_J.cc",
        "dr/get_final_reduction_matrix_J.cc",
        "dr/save.cc",
        "dr/compute_final_reduction_matrix_J.cc",
        "vec_int64/diff.cc",
        "vec_int64/tweak.cc",
        "vec_int64/tweak_step.cc",
        "wrapper/zeta_function.cc",
        "hypersurface/frob_J_ZZ_p.cc",
        "hypersurface/frob_matrix_J.cc",
        "hypersurface/constructors.cc",
        "hypersurface/compute_fpow.cc",
        "hypersurface/frob_J_ZZ.cc",
        "hypersurface/save.cc",
        "solve_system/solve_system.cc",
        "conv/conv.cc",
        "dr_nd/dr_nd.cc",
        "hypersurface_nd/hypersurface_nd.cc",
        "matrix/charpoly.cc",
        "matrix/transpose_mul_tranpose.cc",
        "matrix/mul_tranpose.cc",
        "matrix/mul.cc",
        "matrix/random_SL_matric.cc",
        "matrix/trace.cc",
        "matrix/charpoly_frob.cc"
    ]
include_dirs = _sage_include_directories() + [
    'pycontrolledreduction',
    'pycontrolledreduction/lib/',
]
use_openmp = _openmp_enabled(include_dirs)
libopenmp = ["omp"] if use_openmp and sys.platform == "darwin" else []
openmpflags = ["-Xpreprocessor", "-fopenmp"] if use_openmp and sys.platform == "darwin" else (["-fopenmp"] if use_openmp else [])

pyx_source = "pycontrolledreduction/controlledreduction.pyx"
cpp_source = "pycontrolledreduction/controlledreduction.cpp"
use_cython = cython_cythonize is not None and os.path.exists(pyx_source)

pycontrolledreduction = Extension('pycontrolledreduction.controlledreduction',
                                  language="c++",
                                  sources=[
                                      pyx_source if use_cython else cpp_source,
                                  ] + [
                                      'pycontrolledreduction/lib/' + elt for elt in controlledreduction_sources
                                  ],
                                  libraries=["gmp", "flint", "ntl"] + libopenmp,
                                  extra_compile_args=["-std=c++11"] + openmpflags,
                                  extra_link_args=["-std=c++11"] + openmpflags,
                                  include_dirs=include_dirs,
                                  library_dirs=_sage_library_directories(),
                                  )

setup(
    name="pycontrolledreduction",
    author="Jennifer Balakrishnan, Edgar Costa",
    author_email="edgarcosta@math.dartmouth.edu",
    url="https://github.com/edgarcosta/pycontrolledreduction",
    license="GNU General Public License, version 2 or 3",
    description="Wrapper for controlled reduction library by Edgar Costa",
    long_description = readfile("README.md"), # get the long description from the README
    version = readfile("VERSION").strip(), # the VERSION file is shared with the documentation
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 4 - Beta',
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering :: Mathematics',
      'License :: OSI Approved :: GNU General Public License v2 or v3',
      'Programming Language :: Python :: 3.7',
    ], # classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords = "sagemath controlled reduction",
    setup_requires=[],
    install_requires=[],
    packages=["pycontrolledreduction"],
    include_package_data = True,
    ext_modules = cythonize([pycontrolledreduction], language="c++") if use_cython else [pycontrolledreduction],
    cmdclass = {'test': SageTest} # adding a special setup command for tests
    #ext_modules = extensions,
    #cmdclass = {'test': SageTest, 'build_ext': Cython.Build.build_ext} # adding a special setup command for tests and build_ext
)
