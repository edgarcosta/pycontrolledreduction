# distutils: language=c++
# Copyright 2017 Jennifer Balakrishnan, Edgar Costa 
# See LICENSE file for license details.
# distutils: libraries = controlledreduction
# clang c++

from sage.libs.ntl.types cimport ZZX_c, mat_ZZ_c
from libcpp.vector cimport vector
from libc.stdint cimport int64_t
from libcpp cimport bool

cdef extern from "controlledreduction/wrapper.h":
    void zeta_function(
        ZZX_c &zeta,
        mat_ZZ_c &frob,
        const vector[ vector[int64_t] ] &monomials,
        const vector[int64_t] &coef,
        const int64_t &p,
        const bool &verbose,
        const int &thread,
        const int &min_abs_precision,
        const int &find_better_model
    );
