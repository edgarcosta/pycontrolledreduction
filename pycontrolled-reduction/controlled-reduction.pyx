# Copyright 2017 Jennifer Balakrishnan, Edgar Costa 
# See LICENSE file for license details.


from cysignals.signals cimport sig_on, sig_off
from sage.rings.integer_ring import ZZ

def controlled_reduction(f, p, verbose = False):
    cdef vector[int64_t] coef;
    cdef vector[ vector[int64_t] ] keys;
    for mvec, c in f.dict().iteritems():
        coef.push_back(c % p)
        keys.push_back(mvec)
    cdef ntl_ZZX zeta = ntl_ZZX();
    zeta_function(zeta.x, keys, coef, p);
    # convert zeta to a sage polynomial
    poly=[]
    for i in range(zeta.degree()+1):
        poly.append(zeta[i]._integer_())

    return PolynomialRing(ZZ, 'T')(poly).reverse();
