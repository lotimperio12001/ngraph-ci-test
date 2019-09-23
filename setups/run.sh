#!/bin/bash
printenv
. /root/setups/save-versions.sh
cd ~/test
pytest test_backend.py --onnx_backend="ngraph_onnx.onnx_importer.backend" -k 'not _cuda' -v
