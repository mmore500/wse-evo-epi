#!/usr/bin/env bash

set -e

$CSLC --arch=wse2 ./layout.csl --fabric-dims=11,5 --fabric-offsets=4,1 -o out \
--memcpy --channels=1 --width-west-buf=0 --width-east-buf=0
$CS_PYTHON run.py --name out
