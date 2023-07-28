#!/bin/bash

# Name of the screen session where the Python script is running
SESSION_NAME="mqtt-backend"

# Find the PID of the Python process running in the screen session
PID=$(screen -list | grep $SESSION_NAME | cut -f1 -d'.')

if [ -n "$PID" ]; then
    # Kill the Python process
    kill $PID

    # Wait for the process to terminate (optional)
    sleep 2

    # Terminate the screen session
    screen -X -S $SESSION_NAME quit

    echo "Daemon terminated and screen session closed."
else
    echo "Daemon is not running."
fi

