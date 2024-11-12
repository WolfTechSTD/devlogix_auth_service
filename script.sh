#!/bin/bash

# Script for local running
filename=.env.dev

if [ ! -f ./$filename ]; then
    echo "File ${filename} not found!"
else
    export $(grep -v '^#' $filename | xargs)
fi
