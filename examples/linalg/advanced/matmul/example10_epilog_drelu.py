# Copyright (c) 2024, NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# SPDX-License-Identifier: Apache-2.0

"""
This example demonstrates usage of epilogs that use auxiliary output generated from a previous matmul operation.

In this example we'll use the RELU_AUX epilog, which generates an extra output "relu_aux". The auxiliary output
in this case represent bitflags marking where the input to the RELU function is positive. In general, auxiliary
output should be considered opaque, and is meant to be generated by one matmul operation and used in another with
a compatible epilog.

Here we generate the auxiliary output in a forward pass using RELU, and provide it as epilog input in the corresponding
backward pass using the DRELU epilog.
"""
import cupy as cp

import nvmath

# Prepare sample input data.
m, n, k = 64, 128, 256
a = cp.random.rand(m, k)
b = cp.random.rand(k, n)

# Perform the multiplication with RELU_AUX epilog (forward pass).
epilog = nvmath.linalg.advanced.MatmulEpilog.RELU_AUX
result, auxiliary = nvmath.linalg.advanced.matmul(a, b, epilog=epilog)

# In the backward pass using DRELU epilog, provide the auxiliary output as epilog input.
epilog = nvmath.linalg.advanced.MatmulEpilog.DRELU
result = nvmath.linalg.advanced.matmul(a, b, epilog=epilog, epilog_inputs=auxiliary)

# Synchronize the default stream, since by default the execution is non-blocking for GPU operands.
cp.cuda.get_current_stream().synchronize()
print(f"Inputs were of types {type(a)} and {type(b)}, and the result type is {type(result)}, and the auxiliary output is of type {type(auxiliary)}.")
