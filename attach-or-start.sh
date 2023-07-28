#!/bin/bash

# Name of the screen session to create
SESSION_NAME="mqtt-backend"

# Check if the screen session already exists
if ! screen -list | grep -q "$SESSION_NAME"; then
    # Create a new screen session and run the Python program inside it
    screen -S $SESSION_NAME -dm bash -c "python3 your_script.py; exec sh"

    echo "Python program started in a new screen session."
else
    # Attach to the existing screen session
    screen -r $SESSION_NAME

    echo "Attached to the existing screen session."
fi

