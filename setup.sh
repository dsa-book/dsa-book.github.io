#!/bin/bash

# Export the path
export PATH="$PATH:/Users/devulapa/Library/Python/3.9/bin"

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