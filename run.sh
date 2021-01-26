#!/bin/bash

##
## Startup script for the Fetch coding exericse.
##
## Script takes two file names representing text documents 
## to compare.
##
## The python script checks arguments, though we could also check them
## here. 
##
##  The script also ensures the module search path includes the source
##  dir.
##

export PYTHONPATH='./src/':$PYTHONPATH
python3 ./src/driver.py $1 $2
