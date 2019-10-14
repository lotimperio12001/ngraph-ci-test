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

# Copy local directories
COPY ./test /root/test
COPY ./setup /root/setup

# Install test report dependencies
RUN pip3 install --no-cache-dir -r /root/setup/requirements_report.txt

############## ONNX Backend dependencies ###########
ENV ONNX_BACKEND="onnxruntime.backend.backend"

# Install dependencies
RUN pip3 install onnx

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update && apt-get -y upgrade

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    clang-3.9 \
    git \
    unzip \
    curl \
    autogen \
    automake \
    autoconf \
    zlib1g \
    zlib1g-dev \
    libtool \
    libtinfo-dev && \
    apt-get clean autoclean && apt-get autoremove -y

# ONNX dependencies
RUN apt-get update && apt-get -y install \
    protobuf-compiler \
    libprotobuf-dev && \
    apt-get clean autoclean && apt-get autoremove -y



# Build
WORKDIR /root
RUN git clone --recursive https://github.com/Microsoft/onnxruntime
WORKDIR /root/onnxruntime

RUN ./build.sh --config RelWithDebInfo --build_shared_lib --enable_onnx_tests --build_wheel


####################################################

CMD . /root/setup/docker-setup.sh && \
    pytest /root/test/test_backend.py --onnx_backend=${ONNX_BACKEND} -k 'not _cuda' -v
