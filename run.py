#!/usr/bin/env cs_python

import argparse
import numpy as np

from cerebras.sdk.runtime.sdkruntimepybind import SdkRuntime, MemcpyDataType # pylint: disable=no-name-in-module
from cerebras.sdk.runtime.sdkruntimepybind import MemcpyOrder # pylint: disable=no-name-in-module

parser = argparse.ArgumentParser()
parser.add_argument('--name', help='the test name')
parser.add_argument("--cmaddr", help="IP:port for CS system")
args = parser.parse_args()
dirname = args.name

runner = SdkRuntime(dirname, cmaddr=args.cmaddr)

# Get symbol for copying recv results off device
result_symbol = runner.get_id('result')

runner.load()
runner.run()

runner.launch('main_fn', nonblock=False)

# Copy arr back from PEs that received wlts
result0 = np.zeros([1], dtype=np.uint32)
runner.memcpy_d2h(result0, result_symbol, 2, 0, 1, 1, 1, streaming=False,
  order=MemcpyOrder.ROW_MAJOR, data_type=MemcpyDataType.MEMCPY_32BIT, nonblock=False)

result1 = np.zeros([1], dtype=np.uint32)
runner.memcpy_d2h(result1, result_symbol, 2, 1, 1, 1, 1, streaming=False,
  order=MemcpyOrder.ROW_MAJOR, data_type=MemcpyDataType.MEMCPY_32BIT, nonblock=False)

result2 = np.zeros([1], dtype=np.uint32)
runner.memcpy_d2h(result2, result_symbol, 2, 2, 1, 1, 1, streaming=False,
  order=MemcpyOrder.ROW_MAJOR, data_type=MemcpyDataType.MEMCPY_32BIT, nonblock=False)

runner.stop()

print("result0: ", result0)
print("result1: ", result1)
print("result2: ", result2)

np.testing.assert_equal(result0, np.array([0], dtype=np.uint32))
np.testing.assert_equal(result1, np.array([1], dtype=np.uint32))
np.testing.assert_equal(result2, np.array([2], dtype=np.uint32))

print("SUCCESS!")
