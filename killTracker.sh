#!/bin/bash

name=$1
kill -SIGKILL -- -$(ps -aux | grep "[t]est.sh $name" | awk '{print $2}')
