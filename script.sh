#!/bin/bash

# Script for local running
filename=.env

if [ ! -f ./$filename ]; then
    echo "File ${filename} not found!"
else
    export $(grep -v '^#' $filename | xargs)
fi
