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

RUN pip3 install --no-cache-dir pytest==5.2.1 tabulate==0.8.3

# Copy local directories
COPY ./test /root/test

############## ONNX Backend dependencies ###########
RUN pip3 install onnx
RUN pip3 install onnxruntime
####################################################

CMD pytest /root/test/onnxruntime_test_backend.py -k 'not _cuda' -v
