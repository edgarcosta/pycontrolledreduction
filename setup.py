#!/usr/bin/env python
## -*- encoding: utf-8 -*-

import os
import subprocess
import sys
from setuptools import setup
from setuptools.command.install import install
from codecs import open # To open the README file with proper encoding
from setuptools.command.test import test as TestCommand # for tests
from setuptools.extension import Extension
from sage.env import sage_include_directories, SAGE_LOCAL
from Cython.Build import cythonize

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

openmpflag = "-openmp" if sys.platform == "darwin" else "-fopenmp"

pycontrolledreduction = Extension('pycontrolledreduction.controlledreduction',
                                  language="c++",
                                  sources=[
                                      'pycontrolledreduction/controlledreduction.pyx',
                                  ] + [
                                      'pycontrolledreduction/lib/' + elt for elt in controlledreduction_sources
                                  ],
                                  libraries=["gmp", "flint", "ntl", "omp"],
                                  extra_compile_args=["-std=c++11", openmpflag],
                                  extra_link_args=["-std=c++11", openmpflag],
                                  include_dirs=sage_include_directories() + ['pycontrolledreduction/lib/']
                                  )

setup(
    name="pycontrolledreduction",
    author="Jennifer Balakrishnan, Edgar Costa",
    author_email="edgarcosta@math.dartmouth.edu",
    url="https://github.com/edgarcosta/pycontrolledreduction",
    license="GNU General Public License, version 2 or 3",
    description="Wrapper for controlled reduction library by Edgar Costa",
    long_description = readfile("README.rst"), # get the long description from the README
    version = readfile("VERSION"), # the VERSION file is shared with the documentation
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 4 - Beta',
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering :: Mathematics',
      'License :: OSI Approved :: GNU General Public License v2 or v3',
      'Programming Language :: Python :: 2.7',
    ], # classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords = "sagemath controlled reduction",
    setup_requires=["cython", "sagemath"], # currently useless, see https://www.python.org/dev/peps/pep-0518/
    install_requires=["cython", "sagemath"],
    packages=["pycontrolledreduction"],
    include_package_data = True,
    ext_modules = cythonize([pycontrolledreduction], language="c++"),
    cmdclass = {'test': SageTest} # adding a special setup command for tests
    #ext_modules = extensions,
    #cmdclass = {'test': SageTest, 'build_ext': Cython.Build.build_ext} # adding a special setup command for tests and build_ext
)
