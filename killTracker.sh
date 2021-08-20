#!/bin/bash

# Identify the users processes using the name of the file, then KILL IT
name=$1
kill -SIGKILL -- -$(ps -aux | grep "[t]est.sh $name" | awk '{print $2}')
