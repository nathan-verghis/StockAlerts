#!/bin/bash

# First ever call, file name is used to keep track of which background process is running in the even of multiple configurations
filename=$1
python3 setup.py $filename