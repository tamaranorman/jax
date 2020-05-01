.. currentmodule:: jax

Public API: jax package
=======================

Subpackages
-----------

.. toctree::
    :maxdepth: 1

    jax.numpy
    jax.scipy
    jax.experimental
    jax.lax
    jax.nn
    jax.ops
    jax.random
    jax.tree_util
    jax.dlpack
    jax.profiler

Just-in-time compilation (:code:`jit`)
--------------------------------------

.. autofunction:: jit
.. autofunction:: disable_jit
.. autofunction:: xla_computation
.. autofunction:: make_jaxpr
.. autofunction:: eval_shape
.. autofunction:: device_put

Automatic differentiation
-------------------------

.. autofunction:: grad
.. autofunction:: value_and_grad
.. autofunction:: jacfwd
.. autofunction:: jacrev
.. autofunction:: hessian
.. autofunction:: jvp
.. autofunction:: linearize
.. autofunction:: vjp
.. autofunction:: custom_jvp
.. autofunction:: custom_vjp


Vectorization (:code:`vmap`)
----------------------------

.. autofunction:: vmap
.. autofunction:: jax.numpy.vectorize

Parallelization (:code:`pmap`)
------------------------------

.. autofunction:: pmap
.. autofunction:: devices
.. autofunction:: local_devices
.. autofunction:: host_id
.. autofunction:: host_ids
.. autofunction:: device_count
.. autofunction:: local_device_count
.. autofunction:: host_count
