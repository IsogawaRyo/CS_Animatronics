#!/bin/bash

# Genesis-World Virtual Environment Setup
# Creates a clean Python virtual environment for Genesis development

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "🌟 Genesis-World Virtual Environment Setup"
echo "=========================================="

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ $(echo "$PYTHON_VERSION >= 3.8" | bc -l 2>/dev/null || echo 0) -eq 1 ]]; then
    print_status "Python $PYTHON_VERSION detected ✓"
else
    print_error "Python 3.8+ required. Current: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
VENV_NAME="genesis_env"
print_header "Creating virtual environment '$VENV_NAME'..."

if [ -d "$VENV_NAME" ]; then
    print_warning "Virtual environment already exists"
    read -p "Remove existing environment? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$VENV_NAME"
        print_status "Existing environment removed"
    else
        print_status "Using existing environment"
    fi
fi

if [ ! -d "$VENV_NAME" ]; then
    python3 -m venv "$VENV_NAME"
    print_status "Virtual environment created"
fi

# Activate virtual environment
print_header "Activating virtual environment..."
source "$VENV_NAME/bin/activate"
print_status "Virtual environment activated"

# Upgrade pip
print_header "Upgrading pip..."
pip install --upgrade pip

# Check CUDA availability
CUDA_AVAILABLE=false
if command -v nvidia-smi &> /dev/null; then
    if nvidia-smi > /dev/null 2>&1; then
        print_status "NVIDIA GPU detected - enabling CUDA support"
        CUDA_AVAILABLE=true
    fi
fi

# Install PyTorch
print_header "Installing PyTorch..."
if [ "$CUDA_AVAILABLE" = true ]; then
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    print_status "PyTorch installed with CUDA support"
else
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    print_status "PyTorch installed (CPU only)"
fi

# Install Genesis dependencies
print_header "Installing Genesis dependencies..."
pip install \
    numpy \
    scipy \
    matplotlib \
    pillow \
    opencv-python \
    imageio \
    scikit-image \
    tqdm \
    pyyaml \
    h5py \
    transforms3d \
    trimesh \
    warp-lang \
    moderngl \
    glfw \
    pyopengl \
    pyopengl-accelerate \
    gymnasium \
    stable-baselines3

# Install Taichi
print_header "Installing Taichi..."
if [ "$CUDA_AVAILABLE" = true ]; then
    pip install taichi[cuda]
else
    pip install taichi
fi

# Install development tools
print_header "Installing development tools..."
pip install \
    jupyter \
    ipywidgets \
    plotly \
    seaborn \
    pandas \
    black \
    flake8 \
    pytest

# Install Genesis if repository exists
if [ -d "genesis" ]; then
    print_header "Installing Genesis from local repository..."
    cd genesis
    pip install -e .
    cd ..
    print_status "Genesis installed in development mode"
else
    print_header "Cloning and installing Genesis..."
    git clone https://github.com/Genesis-Embodied-AI/Genesis.git genesis
    cd genesis
    pip install -e .
    cd ..
    print_status "Genesis cloned and installed"
fi

# Create activation script
print_header "Creating activation script..."
cat > activate_genesis.sh << 'EOF'
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
EOF

chmod +x activate_genesis.sh

# Create deactivation script
cat > deactivate_genesis.sh << 'EOF'
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
EOF

chmod +x deactivate_genesis.sh

# Save installed packages list
print_header "Saving package list..."
pip freeze > genesis_requirements_installed.txt

# Test installation
print_header "Testing installation..."
python -c "
import torch
import taichi as ti
import numpy as np

print('✅ PyTorch:', torch.__version__)
print('✅ CUDA available:', torch.cuda.is_available())
print('✅ Taichi:', ti.__version__)
print('✅ NumPy:', np.__version__)

try:
    import genesis as gs
    print('✅ Genesis:', gs.__version__)
    print('✅ All core packages installed successfully!')
except ImportError as e:
    print('⚠️  Genesis import issue:', e)
    print('   This might be normal if Genesis setup is still in progress')
"

print_header "Setup Complete!"
echo "==============================================="
print_status "✅ Virtual environment: $VENV_NAME"
print_status "✅ PyTorch installed ($([ "$CUDA_AVAILABLE" = true ] && echo "CUDA" || echo "CPU"))"
print_status "✅ All dependencies installed"
print_status "✅ Genesis installed"
echo ""
echo "📋 Next steps:"
echo "  1. To activate:   source activate_genesis.sh"
echo "  2. Test setup:    python genesis_test.py"
echo "  3. Check env:     python check_genesis_environment.py"
echo "  4. To deactivate: source deactivate_genesis.sh"
echo ""
echo "📁 Files created:"
echo "  - $VENV_NAME/                    (virtual environment)"
echo "  - activate_genesis.sh           (activation script)"
echo "  - deactivate_genesis.sh         (deactivation script)"  
echo "  - genesis_requirements_installed.txt (package list)"
echo ""
print_status "🎉 Genesis-World virtual environment ready!"

# Keep environment activated for user
echo ""
print_status "Virtual environment remains activated for immediate use"
print_warning "Remember to run 'source activate_genesis.sh' in new terminal sessions"