=============
pycontrolledreduction
=============

This package is a simple wrapper to integrate Edgar Costa's controlled reduction code into SageMath.


============

Install ``controlled-reduction``

::

  git clone https://github.com/edgarcosta/controlledreduction
  cd controlledreduction
  sage -sh
  ./configure --prefix=$SAGE_LOCAL && make install


then use pip to install `pycontrolledreduction`

::
  sage -pip install --upgrade git+https://github.com/edgarcosta/pycontrolledreduction.git@master#egg=pycontrolledreduction
