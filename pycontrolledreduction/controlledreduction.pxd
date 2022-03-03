# distutils: language=c++
# clang c++
# Copyright 2017 Jennifer Balakrishnan, Edgar Costa
# See LICENSE file for license details.

from sage.libs.ntl.types cimport ZZ_c, ZZX_c, mat_ZZ_c
from libcpp.vector cimport vector
from libc.stdint cimport int64_t
from libcpp cimport bool

cdef extern from "lib/wrapper.h":
    void zeta_function(
        ZZX_c &zeta,
        mat_ZZ_c &frob,
        const vector[ vector[int64_t] ] &monomials,
        const vector[ZZ_c] &coef,
        const int64_t &p,
        const bool &verbose,
        const int &thread,
        const int &abs_precision,
        const bool &increase_precision_to_deduce_zeta,
        const bool &find_better_model
    );
