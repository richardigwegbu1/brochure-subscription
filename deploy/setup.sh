#!/bin/bash

# Navigate to app directory
cd /var/www/brochure-subscription

# Ensure Python dependencies are installed
pip3 install --user -r requirements.txt

# Optional: Ensure Gunicorn is executable
chmod +x ~/.local/bin/gunicorn

