FROM ubuntu:18.04

# Disable interactive installation mode
ENV DEBIAN_FRONTEND=noninteractive

# Set proxy
ARG http_proxy
ARG https_proxy
ENV http_proxy ${http_proxy}
ENV https_proxy ${https_proxy}

#Python dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip

RUN pip3 install --upgrade pip setuptools wheel

# Download onnx-runtime
RUN pip3 install --no-cache-dir onnx && \
    pip3 install --no-cache-dir onnxruntime && \
    pip3 install --no-cache-dir pytest && \
    pip3 install --no-cache-dir tabulate

# ONNX-backend test results dir
RUN mkdir -p /root/results
ENV RESULTS_DIR=/root/results
ENV CSVDIR=/root/results

# Save version
RUN mkdir -p /root/version
ENV VERSION_DIR=/root/version
WORKDIR /root/version
RUN pip3 list --format=json > /root/version/version.json

# Run pytest
WORKDIR /root/test
COPY ./test/conftest.py /root/test
COPY ./test/test_backend.py /root/test
# CMD file -i /root/version/version.json && cat /root/version/version.json
CMD pytest test_backend.py --onnx_backend="onnxruntime.backend.backend" -k 'not _cuda' -v
