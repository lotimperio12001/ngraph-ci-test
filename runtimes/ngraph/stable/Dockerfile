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

RUN pip3 install --upgrade pip setuptools wheel

# Install nGraph-core
RUN pip install ngraph-core

# Install nGraph-ONNX
RUN pip install ngraph-onnx

# Test report dependencies
RUN pip install --no-cache-dir pytest && \
    pip install --no-cache-dir tabulate

# ONNX-backend test results dir
RUN mkdir -p /root/results
ENV RESULTS_DIR=/root/results
ENV CSVDIR=/root/results

# Save packages version
COPY ./bash /root/bash
RUN chmod +x /root/bash/save-versions.sh && ./root/bash/save-versions.sh

RUN printenv

# RUN mkdir -p /root/versions
# ENV VERSIONS_DIR=/root/versions
# WORKDIR /root/version
# RUN pip list --format=json > /root/versions/pip-list.json

# Run pytest
COPY ./test /root/test
COPY ./config.json /root/test
WORKDIR /root/test
CMD pytest test_backend.py --onnx_backend="ngraph_onnx.onnx_importer.backend" -k 'not _cuda' -v
