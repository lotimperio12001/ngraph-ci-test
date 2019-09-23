#!/bin/bash
echo "Save versions script!"
cd ~
mkdir /root/versions
env VERSIONS_DIR="/root/versions"
pip list --format=json > /root/versions/pip-list.json
cat /root/versions/pip-list.json
printenv
