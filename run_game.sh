#!/bin/bash
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install pygame
python3 alien_invasion.py
