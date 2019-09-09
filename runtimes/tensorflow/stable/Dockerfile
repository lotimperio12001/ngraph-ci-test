FROM ubuntu:18.04

# Disable interactive installation mode
ENV DEBIAN_FRONTEND=noninteractive

# Set proxy
ARG http_proxy
ARG https_proxy
ENV http_proxy ${http_proxy}
ENV https_proxy ${https_proxy}

# Python dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

# Install ONNX-tf and dependencies
RUN pip3 install --no-cache-dir \
    onnx \
    tensorflow \
    onnx-tf

# Install test dependencies
RUN pip3 install --no-cache-dir \
    pytest \
    tabulate

# Save packages version
RUN mkdir -p /root/version
ENV VERSION_DIR=/root/version
WORKDIR /root/version
RUN pip3 list --format=json > /root/version/pip-list.json

# ONNX-backend test results dir
RUN mkdir -p /root/results
ENV RESULTS_DIR=/root/results
ENV CSVDIR=/root/results

# Run pytest
WORKDIR /root/test
COPY ./test/conftest.py /root/test
COPY ./test/test_backend.py /root/test

CMD /usr/bin/time -v pytest test_backend.py --onnx_backend="onnx_tf.backend" -k 'not _cuda' -v
