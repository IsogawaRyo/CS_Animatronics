#!/bin/bash

# Genesis-World Environment Activation Script
# Source this script to activate the Genesis development environment

# Activate virtual environment
if [ -d "genesis_env" ]; then
    source genesis_env/bin/activate
    echo "✅ Genesis virtual environment activated"
else
    echo "❌ Genesis virtual environment not found"
    echo "Run setup_genesis_venv.sh first"
    return 1
fi

# Set Genesis-specific environment variables
export GENESIS_DATA_DIR="$(pwd)/genesis/data"
export PYTHONPATH="$(pwd)/genesis:$PYTHONPATH"

# Add CUDA to PATH if available
if [ -d "/usr/local/cuda" ]; then
    export PATH=/usr/local/cuda/bin:$PATH
    export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
fi

echo "🌟 Genesis-World development environment ready!"
echo "📁 Genesis Data: $GENESIS_DATA_DIR"
echo "🐍 Python: $(python --version)"
echo "🔥 PyTorch: $(python -c 'import torch; print(torch.__version__)')"
echo "⚡ CUDA Available: $(python -c 'import torch; print(torch.cuda.is_available())')"
echo ""
echo "💡 Quick start:"
echo "  python genesis_test.py          # Test installation"
echo "  python check_genesis_environment.py  # Check environment"
echo "  jupyter notebook                # Start Jupyter"
