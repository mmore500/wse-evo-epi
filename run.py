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
for y in range(3):
    for x in range(1, 4):
        result_recv = np.zeros([1], dtype=np.uint32)
        runner.memcpy_d2h(
            result_recv, result_symbol, x, y, 1, 1, 1,
            streaming=False,
            order=MemcpyOrder.ROW_MAJOR,
            data_type=MemcpyDataType.MEMCPY_32BIT,
            nonblock=False,
        )
        print(f"result{x},{y} recv: {result_recv}")
        np.testing.assert_equal(result_recv, np.array([y], dtype=np.uint32))


runner.stop()

print("SUCCESS!")
