#!/bin/bash

if [ "$1" == "run" ]; then
  echo "Running backend"
  go run .
fi
