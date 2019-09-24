#!/bin/bash
cd ~
mkdir /root/versions
pip list --format=json > /root/versions/pip-list.json
cat /root/versions/pip-list.json
