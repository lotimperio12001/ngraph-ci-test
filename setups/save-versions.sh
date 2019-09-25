#!/bin/bash
cd ~
# mkdir /root/versions

pip list --format=json > ${RESULTS_DIR}/pip-list.json
cat ${RESULTS_DIR}/pip-list.json
