#!/bin/bash

# Define the python version to use
PYTHON_BIN="python3.12"

# Check if python3.12 is installed
if ! command -v $PYTHON_BIN &> /dev/null; then
    echo "Error: $PYTHON_BIN not found. Please install it or update this script."
    exit 1
fi

# Create venv if it doesn't exist or is broken (missing activate)
if [ ! -f "venv/bin/activate" ]; then
    echo "Creating virtual environment with $PYTHON_BIN..."
    rm -rf venv
    $PYTHON_BIN -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install pygame if not present
if ! python3 -c "import pygame" &> /dev/null; then
    echo "Installing pygame..."
    pip install pygame
fi

# Run the game
echo "Starting Alien Invasion..."
python3 alien_invasion.py
