#!/bin/bash

# Genesis-World Environment Deactivation Script

if [[ "$VIRTUAL_ENV" != "" ]]; then
    deactivate
    echo "✅ Genesis virtual environment deactivated"
else
    echo "⚠️  No virtual environment currently active"
fi

unset GENESIS_DATA_DIR
unset PYTHONPATH
