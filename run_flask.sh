#!/bin/bash

##
## Startup script for the Flask app to run an API endpoint for 
## text comparison, reusing core functionsl
##
##  The script also ensures the module search path includes the source
##  dir.
##

export FLASK_APP=src/flask_app.py
export PYTHONPATH='./src/':$PYTHONPATH
flask run
