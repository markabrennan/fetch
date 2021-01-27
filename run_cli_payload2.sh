#!/bin/bash

##
## Script to wrap the curl command which sends a JSON
## payload (payload #2) of two texts for comparison to the Flask app endpoint.
## Payload data is accessed in the data dir.
##

curl -XPOST -d @data/api_payload2.json http://localhost:5000
