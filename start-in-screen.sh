#!/bin/bash

# Name for the screen session
SESSION_NAME="mqtt-backend"

# Start the screen session and run the Python script
screen -dmS $SESSION_NAME python your_script.py

# Optionally, you can add some delay here to ensure the Python script starts properly
# sleep 1

# Print a message to confirm that the script has started
echo "Python script started in screen session: $SESSION_NAME"

# Exit the bash script
exit 0
