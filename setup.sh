#!/bin/bash

# Get the path to the Python binary folder
PYTHON_BIN_PATH=$(dirname "$(which python3)")

# Export the path only if COLAB is not set or set to false
if [ -z "$COLAB" ] || [ "$COLAB" = false ]; then
    export PATH="$PATH:$PYTHON_BIN_PATH"
fi

# Check if local-req.txt exists
if [ -f "local-req.txt" ]; then
    # Install packages from local-req.txt
    pip3 install -r local-req.txt --no-warn-script-location
else
    echo "local-req.txt not found."
    exit 1
fi

git config --global user.name "interactive-dsa-book"
git config --global user.email "kumar6017drive@gmail.com"