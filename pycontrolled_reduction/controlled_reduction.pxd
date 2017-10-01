# Copyright 2017 Jennifer Balakrishnan, Edgar Costa 
# See LICENSE file for license details.
# distutils: language = C++
# distutils: libraries = controlled-reduction

from sage.libs.ntl.types cimport ZZX_c
from libcpp.vector cimport vector
from libcpp.cstdint cimport int64_t

cdef extern from "controlled-reduction/wrapper.h":
    void zeta_function(ZZX_c &zeta, vector[ vector[int64_t] ] &monomials, vector[int64_t] &coef, int64_t p,  bool verbose);
