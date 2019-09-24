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
ENV ONNX_BACKEND="ngraph_onnx.onnx_importer.backend"

# Install dependencies
RUN pip install ngraph-core
RUN pip install ngraph-onnx
####################################################

CMD . /root/setups/docker-setup.sh && \
    pytest /root/test/test_backend.py --onnx_backend=${ONNX_BACKEND} -k 'not _cuda' -v
