# distutils: language=c++
# Copyright 2017 Jennifer Balakrishnan, Edgar Costa 
# See LICENSE file for license details.
# distutils: libraries = controlled-reduction
# clang c++

from sage.libs.ntl.types cimport ZZX_c
from libcpp.vector cimport vector
from libc.stdint cimport int64_t
from libcpp cimport bool

cdef extern from "controlledreduction/wrapper.h":
    void zeta_function(ZZX_c &zeta, const vector[ vector[int64_t] ] &monomials, const vector[int64_t] &coef, const int64_t &p,  bool verbose);
