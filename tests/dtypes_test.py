# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import operator

from absl.testing import absltest
from absl.testing import parameterized

import numpy as onp

import jax
from jax import dtypes
from jax import numpy as np
from jax import test_util as jtu

from jax.config import config
config.parse_flags_with_absl()
FLAGS = config.FLAGS

bool_dtypes = [onp.dtype('bool')]

signed_dtypes = [onp.dtype('int8'), onp.dtype('int16'), onp.dtype('int32'),
                 onp.dtype('int64')]

unsigned_dtypes = [onp.dtype('uint8'), onp.dtype('uint16'), onp.dtype('uint32'),
                   onp.dtype('uint64')]

onp_float_dtypes = [onp.dtype('float16'), onp.dtype('float32'),
                    onp.dtype('float64')]

float_dtypes = [onp.dtype(dtypes.bfloat16)] + onp_float_dtypes

complex_dtypes = [onp.dtype('complex64'), onp.dtype('complex128')]


all_dtypes = (bool_dtypes + signed_dtypes + unsigned_dtypes + float_dtypes +
              complex_dtypes)


class DtypesTest(jtu.JaxTestCase):

  @parameterized.named_parameters(
    {"testcase_name": "_type={}".format(type.__name__), "type": type,
     "dtype": dtype}
    for type, dtype in [(bool, np.bool_), (int, np.int_), (float, np.float_),
                        (complex, np.complex_)])
  def testDefaultTypes(self, type, dtype):
    for f in [np.array, jax.jit(np.array), jax.jit(lambda x: x)]:
      y = f(type(0))
      self.assertTrue(isinstance(y, np.ndarray), msg=(f, y))
      self.assertEqual(y.dtype, dtypes.canonicalize_dtype(dtype), msg=(f, y))

  @parameterized.named_parameters(
    {"testcase_name": "_swap={}_jit={}".format(swap, jit),
     "swap": swap, "jit": jit} 
    for swap in [False, True] for jit in [False, True])
  @jtu.skip_on_devices("tpu")  # F16 not supported on TPU
  def testBinaryPromotion(self, swap, jit):
    testcases = [
      (np.array(1.), 0., np.float_),
      (np.array(1.), np.array(0.), np.float_),
      (np.array(1.), np.array(0., dtype=np.float16), np.float_),
      (np.array(1.), np.array(0., dtype=np.float32), np.float_),
      (np.array(1.), np.array(0., dtype=np.float64), np.float64),
      (np.array(1., dtype=np.float16), 0., np.float16),
      (np.array(1., dtype=np.float32), 0., np.float32),
      (np.array(1., dtype=np.float64), 0., np.float64),
      (np.array(1., dtype=np.float16), np.array(0., dtype=np.float16), np.float16),
      (np.array(1., dtype=np.float16), np.array(0., dtype=np.float32), np.float32),
      (np.array(1., dtype=np.float16), np.array(0., dtype=np.float64), np.float64),
      (np.array(1., dtype=np.float32), np.array(0., dtype=np.float32), np.float32),
      (np.array(1., dtype=np.float32), np.array(0., dtype=np.float64), np.float64),
      (np.array(1., dtype=np.float64), np.array(0., dtype=np.float64), np.float64),
      (np.array([1.]), 0., np.float_),
      (np.array([1.]), np.array(0.), np.float_),
      (np.array([1.]), np.array(0., dtype=np.float16), np.float_),
      (np.array([1.]), np.array(0., dtype=np.float32), np.float_),
      (np.array([1.]), np.array(0., dtype=np.float64), np.float64),
      (np.array([1.], dtype=np.float32), np.array(0., dtype=np.float16), np.float32),
      (np.array([1.], dtype=np.float16), np.array(0., dtype=np.float32), np.float32),
      (np.array([1.], dtype=np.float16), 0., np.float16),
    ]
    op = jax.jit(operator.add) if jit else operator.add
    for x, y, dtype in testcases:
      x, y = (y, x) if swap else (x, y)
      z = x + y
      self.assertTrue(isinstance(z, np.ndarray), msg=(x, y, z))
      self.assertEqual(z.dtype, dtypes.canonicalize_dtype(dtype), msg=(x, y, z))

  def testPromoteDtypes(self):
    for t1 in all_dtypes:
      self.assertEqual(t1, dtypes.promote_types(t1, t1))

      self.assertEqual(t1, dtypes.promote_types(t1, onp.bool_))
      self.assertEqual(onp.dtype(onp.complex128),
                       dtypes.promote_types(t1, onp.complex128))

      for t2 in all_dtypes:
        # Symmetry
        self.assertEqual(dtypes.promote_types(t1, t2),
                         dtypes.promote_types(t2, t1))

    self.assertEqual(onp.dtype(onp.float32),
                     dtypes.promote_types(onp.float16, dtypes.bfloat16))

    # Promotions of non-inexact types against inexact types always prefer
    # the inexact types.
    for t in float_dtypes + complex_dtypes:
      for i in bool_dtypes + signed_dtypes + unsigned_dtypes:
        self.assertEqual(t, dtypes.promote_types(t, i))

    # Promotions between exact types, or between inexact types, match NumPy.
    for groups in [bool_dtypes + signed_dtypes + unsigned_dtypes,
                   onp_float_dtypes + complex_dtypes]:
      for t1, t2 in itertools.combinations(groups, 2):
          self.assertEqual(onp.promote_types(t1, t2),
                           dtypes.promote_types(t1, t2))


if __name__ == "__main__":
  absltest.main()
