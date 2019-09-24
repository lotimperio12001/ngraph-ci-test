FROM ubuntu:18.04

# Disable interactive installation mode
ENV DEBIAN_FRONTEND=noninteractive

# Install Python dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip

RUN pip3 install --upgrade pip setuptools wheel

# Install test report dependencies
RUN pip install --no-cache-dir pytest && \
    pip install --no-cache-dir tabulate

# Copy local directotries
COPY ./test /root/test
COPY ./setups /root/setups
RUN chmod +x /root/setups/*.sh

############## ONNX Backend dependencies ###########
# Set Python backend module to import in test script
ENV ONNX_BACKEND="caffe2.python.onnx.backend"

# Install dependencies
RUN pip install onnx

# Listed in docs
# https://caffe2.ai/docs/getting-started.html?platform=ubuntu&configuration=compile

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libgoogle-glog-dev \
    libgtest-dev \
    libiomp-dev \
    libleveldb-dev \
    liblmdb-dev \
    libopencv-dev \
    libopenmpi-dev \
    libsnappy-dev \
    libprotobuf-dev \
    openmpi-bin \
    openmpi-doc \
    protobuf-compiler


RUN pip install --no-cache-dir \
      future \
      numpy \
      protobuf \
      typing \
      hypothesis \
      six \
      pyyaml \
      pytest \
      tabulate

# Download pytorch
RUN git clone https://github.com/pytorch/pytorch.git
WORKDIR /pytorch
RUN git submodule update --init --recursive
RUN python3 setup.py install
####################################################

CMD . /root/setups/docker-setup.sh && \
    pytest /root/test/test_backend.py --onnx_backend=${ONNX_BACKEND} -k 'not _cuda' -v
