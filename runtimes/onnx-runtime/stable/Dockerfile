FROM ubuntu:18.04

# Disable interactive installation mode
ENV DEBIAN_FRONTEND=noninteractive

# Install Python dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip && \
    apt-get clean autoclean && apt-get autoremove -y

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir pytest

# Copy test script
COPY onnxruntime_test_backend.py /root/test/

############## ONNX Backend dependencies ###########
RUN pip3 install onnx
# RUN pip3 install onnxruntime
RUN pip3 install -i https://test.pypi.org/simple/ ort-nightly==0.5.0.dev1013####################################################

# Run all cpu tests
CMD pytest /root/test/onnxruntime_test_backend.py -k 'not _cuda' -v

# Run only one test
# CMD pytest /root/test/onnxruntime_test_backend.py::OnnxBackendNodeModelTest::test_compress_negative_axis_cpu -v
