"""ONNX backend test initialization."""

import unittest

import onnxruntime.backend.backend as backend
import onnx.backend.test


# Import all test cases at global scope to make them visible to python.unittest
backend_test = onnx.backend.test.BackendTest(backend, __name__)
# backend_test.exclude(r'test_compress_negative_axis[a-z,_]*')

globals().update(backend_test.enable_report().test_cases)


if __name__ == "__main__":
    unittest.main()
