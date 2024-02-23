#!/bin/bash

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --colab)
            COLAB="$2"
            shift
            shift
            ;;
        --platform)
            PLATFORM="$2"
            shift
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Function to export path based on platform
export_path() {
    if [ "$PLATFORM" = "mac" ]; then
        # Get the path to the Python binary folder on Mac
        PYTHON_BIN_PATH=$(dirname "$(which python3)")
        export PATH="$PATH:$PYTHON_BIN_PATH"
    elif [ "$PLATFORM" = "windows" ]; then
        # Get the path to the Python binary folder on Windows
        PYTHON_BIN_PATH=$(where python | head -n 1)
        PYTHON_BIN_PATH=$(dirname "$PYTHON_BIN_PATH")
        setx PATH "%PATH%;%PYTHON_BIN_PATH%"
    fi
}

# Export the path only if COLAB is not set or set to false
if [ -z "$COLAB" ] || [ "$COLAB" = false ]; then
    export_path
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