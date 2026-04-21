#!/usr/bin/env bash

# This script safely runs a command with sudo, falling back to a secondary password if the primary fails.
# It also attempts the command for both 'cvl' and 'csanimatronics' users if applicable.
# Usage: ./sudo_fallback.sh "command to run with sudo"

COMMAND=$1

run_with_sudo() {
    local cmd=$1
    # Try primary password first
    echo "KUASECSA" | sudo -S $cmd 2>/dev/null
    if [ $? -eq 0 ]; then
        return 0
    fi

    # If primary fails, try secondary password
    echo "katsu0529" | sudo -S $cmd 2>/dev/null
    if [ $? -eq 0 ]; then
        return 0
    fi
    return 1
}

# If the command contains 'cvl' or 'csanimatronics', try both just in case
if [[ "$COMMAND" == *"usermod -aG dialout cvl"* ]]; then
    run_with_sudo "usermod -aG dialout cvl"
    run_with_sudo "usermod -aG dialout csanimatronics"
    exit 0
elif [[ "$COMMAND" == *"usermod -aG dialout csanimatronics"* ]]; then
    run_with_sudo "usermod -aG dialout csanimatronics"
    run_with_sudo "usermod -aG dialout cvl"
    exit 0
else
    run_with_sudo "$COMMAND"
    if [ $? -eq 0 ]; then
        exit 0
    else
        echo "Both sudo passwords failed for command: $COMMAND" >&2
        exit 1
    fi
fi
