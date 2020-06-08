# pycontrolledreduction

[![Build Status](https://travis-ci.org/edgarcosta/pycontrolledreduction.svg?branch=master)](https://travis-ci.org/edgarcosta/pycontrolledreduction)

This package is a simple wrapper to integrate most of [controlled reduction](https://github.com/edgarcosta/controlledreduction/) library code into SageMath.
Given an hypersurface it computes the characteristic polynomial (and matrix) of the Frobenius action on the primitive cohomology group.



## Install



```
sage -pip install --upgrade git+https://github.com/edgarcosta/pycontrolledreduction.git@master#egg=pycontrolledreduction
```

If you don't have permissions to install it system wide, please add the flag ``--user`` to install it just for you.

```
sage -pip install --user --upgrade git+https://github.com/edgarcosta/pycontrolledreduction.git@master#egg=pycontrolledreduction
```



## Examples


```
sage: from pycontrolledreduction import controlledreduction
sage: R.<x,y,z,w> = ZZ[]
sage: controlledreduction(x^4 + y^4 + z^4 + w^4 + 1*x*y*z*w, 11, False).factor()  # long time
(-1) * (11*T + 1)^6 * (11*T - 1)^13 * (121*T^2 + 18*T + 1)
sage: R.<x,y,z> = ZZ[]
sage: controlledreduction(x^4 + y^4 + z^4 + 1*x^2*y*z, next_prime(10000), False).factor()
(10007*T^2 - 192*T + 1) * (10007*T^2 - 128*T + 1) * (10007*T^2 + 192*T + 1)
sage: controlledreduction(y^2*z + y*z^2 - (x^3 + y*x^2 -2*x*z^2), 97, false).list() == EllipticCurve([0, 1, 1, -2, 0]).change_ring(GF(97)).frobenius_polynomial().reverse().list()
True

```
