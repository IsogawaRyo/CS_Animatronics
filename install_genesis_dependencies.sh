#!/bin/bash

# Genesis-World Dependencies Auto Installer
# For Linux/Ubuntu with CUDA support
# Author: CS_Animatronics Project

set -e  # Exit on any error

echo "=========================================="
echo "Genesis-World Dependencies Auto Installer"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_error "This script is designed for Linux/Ubuntu systems only"
    exit 1
fi

# Check Ubuntu version
print_header "Checking system compatibility..."
if [ -f /etc/lsb-release ]; then
    UBUNTU_VERSION=$(lsb_release -rs)
    print_status "Ubuntu version: $UBUNTU_VERSION"
    if [[ $(echo "$UBUNTU_VERSION >= 18.04" | bc -l) -eq 0 ]]; then
        print_warning "Ubuntu 18.04+ recommended for optimal compatibility"
    fi
else
    print_warning "Unable to detect Ubuntu version. Proceeding anyway..."
fi

# Check if NVIDIA GPU is available
print_header "Checking NVIDIA GPU availability..."
if command -v nvidia-smi &> /dev/null; then
    print_status "NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader,nounits
    CUDA_AVAILABLE=true
else
    print_warning "NVIDIA GPU not detected or drivers not installed"
    print_warning "CUDA acceleration will not be available"
    CUDA_AVAILABLE=false
fi

# Update system packages
print_header "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install system dependencies
print_header "Installing system dependencies..."
sudo apt install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    unzip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglu1-mesa \
    freeglut3-dev \
    mesa-common-dev \
    libglfw3 \
    libglfw3-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel

# Install CUDA if NVIDIA GPU is available
if [ "$CUDA_AVAILABLE" = true ]; then
    print_header "Setting up CUDA environment..."
    
    # Check if CUDA is already installed
    if command -v nvcc &> /dev/null; then
        CUDA_VERSION=$(nvcc --version | grep "release" | sed 's/.*release \([0-9]\+\.[0-9]\+\).*/\1/')
        print_status "CUDA $CUDA_VERSION already installed"
    else
        print_status "Installing CUDA toolkit..."
        # Install CUDA keyring
        wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
        sudo dpkg -i cuda-keyring_1.0-1_all.deb
        sudo apt-get update
        
        # Install CUDA toolkit (version 11.8 for broad compatibility)
        sudo apt-get install -y cuda-toolkit-11-8
        
        # Add CUDA to PATH
        echo 'export PATH=/usr/local/cuda-11.8/bin:$PATH' >> ~/.bashrc
        echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
        
        print_status "CUDA installation completed. Please restart your terminal or run:"
        print_status "source ~/.bashrc"
    fi
fi

# Upgrade pip
print_header "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install Python dependencies
print_header "Installing Python dependencies..."

# Install PyTorch with CUDA support if available
if [ "$CUDA_AVAILABLE" = true ]; then
    print_status "Installing PyTorch with CUDA support..."
    python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
else
    print_status "Installing PyTorch (CPU only)..."
    python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

# Install core scientific computing packages
print_status "Installing scientific computing packages..."
python3 -m pip install \
    numpy \
    scipy \
    matplotlib \
    pillow \
    opencv-python \
    imageio \
    scikit-image \
    tqdm \
    pyyaml \
    h5py

# Install Taichi (required for Genesis)
print_status "Installing Taichi..."
if [ "$CUDA_AVAILABLE" = true ]; then
    python3 -m pip install taichi[cuda]
else
    python3 -m pip install taichi
fi

# Install additional Genesis dependencies
print_status "Installing additional Genesis dependencies..."
python3 -m pip install \
    transforms3d \
    trimesh \
    warp-lang \
    moderngl \
    glfw \
    pyopengl \
    pyopengl-accelerate \
    gymnasium \
    stable-baselines3

# Install development tools
print_header "Installing development tools..."
python3 -m pip install \
    jupyter \
    ipywidgets \
    plotly \
    seaborn \
    pandas \
    black \
    flake8 \
    pytest

# Install Genesis-World
print_header "Installing Genesis-World..."
if [ ! -d "genesis" ]; then
    print_status "Cloning Genesis repository..."
    git clone https://github.com/Genesis-Embodied-AI/Genesis.git genesis
    cd genesis
else
    print_status "Genesis repository already exists. Updating..."
    cd genesis
    git pull origin main
fi

# Install Genesis in development mode
print_status "Installing Genesis in development mode..."
python3 -m pip install -e .

cd ..

# Verify installation
print_header "Verifying installation..."
python3 -c "
import torch
import taichi as ti
import numpy as np
import genesis as gs

print('✓ PyTorch version:', torch.__version__)
print('✓ CUDA available:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('✓ CUDA device:', torch.cuda.get_device_name(0))
print('✓ Taichi version:', ti.__version__)
print('✓ NumPy version:', np.__version__)
print('✓ Genesis version:', gs.__version__)

# Test basic Genesis functionality
print('\\n--- Testing Genesis initialization ---')
gs.init(backend=ti.cuda if torch.cuda.is_available() else ti.cpu)
scene = gs.Scene()
print('✓ Genesis scene created successfully')
"

# Create example usage script
print_header "Creating example usage script..."
cat > genesis_test.py << 'EOF'
#!/usr/bin/env python3
"""
Genesis-World Test Script
Run this to verify your installation is working correctly.
"""

import genesis as gs
import torch
import numpy as np

def main():
    print("🚀 Genesis-World Test Script")
    print("=" * 40)
    
    # Initialize Genesis
    print("Initializing Genesis...")
    backend = gs.cuda if torch.cuda.is_available() else gs.cpu
    gs.init(backend=backend)
    
    # Create scene
    print("Creating scene...")
    scene = gs.Scene(
        sim_options=gs.options.SimOptions(
            substeps=2,
            gravity=(0, 0, -9.81),
        ),
        viewer_options=gs.options.ViewerOptions(
            camera_pos=(3.5, 0.0, 2.5),
            camera_lookat=(0.0, 0.0, 0.5),
        ),
        vis_options=gs.options.VisOptions(
            show_world_frame=True,
        ),
    )
    
    # Add ground
    scene.add_entity(gs.morphs.Plane())
    
    # Add simple objects
    franka = scene.add_entity(gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml'))
    
    # Build scene
    scene.build()
    
    print("✅ Scene built successfully!")
    print("🎮 Starting simulation...")
    
    # Run simulation for a few steps
    for i in range(100):
        scene.step()
        if i % 20 == 0:
            print(f"Step {i}: Simulation running...")
    
    print("🎉 Genesis-World installation verified successfully!")
    print("📚 Check the Genesis documentation for more examples:")
    print("    https://genesis-world.readthedocs.io/")

if __name__ == "__main__":
    main()
EOF

chmod +x genesis_test.py

# Create environment setup script
print_header "Creating environment setup script..."
cat > setup_genesis_env.sh << 'EOF'
#!/bin/bash

# Genesis Environment Setup
# Run this script to set up your environment for Genesis development

# Add CUDA to PATH if available
if [ -d "/usr/local/cuda" ]; then
    export PATH=/usr/local/cuda/bin:$PATH
    export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
    echo "✅ CUDA environment variables set"
fi

# Set Genesis-specific environment variables
export GENESIS_DATA_DIR="$(pwd)/genesis/data"
export PYTHONPATH="$(pwd)/genesis:$PYTHONPATH"

echo "✅ Genesis environment setup complete"
echo "📁 Genesis Data Directory: $GENESIS_DATA_DIR"
echo "🐍 Python Path includes Genesis"
echo ""
echo "To activate this environment in your shell, run:"
echo "source setup_genesis_env.sh"
EOF

chmod +x setup_genesis_env.sh

# Create requirements file for future reference
print_header "Creating requirements.txt..."
cat > genesis_requirements.txt << 'EOF'
# Genesis-World Python Dependencies
# Install with: pip install -r genesis_requirements.txt

# Core dependencies
torch>=1.13.0
torchvision
torchaudio
numpy>=1.21.0
scipy
matplotlib
pillow
opencv-python
imageio
scikit-image
tqdm
pyyaml
h5py

# Taichi (physics engine)
taichi>=1.6.0

# Additional scientific packages
transforms3d
trimesh
warp-lang

# Visualization and GUI
moderngl
glfw
pyopengl
pyopengl-accelerate

# ML/RL frameworks
gymnasium
stable-baselines3

# Development tools
jupyter
ipywidgets
plotly
seaborn
pandas
black
flake8
pytest
EOF

print_header "Installation Summary"
echo "=========================================="
print_status "✅ System packages installed"
print_status "✅ Python dependencies installed"
print_status "✅ PyTorch installed ($([ "$CUDA_AVAILABLE" = true ] && echo "with CUDA" || echo "CPU only"))"
print_status "✅ Taichi installed"
print_status "✅ Genesis-World cloned and installed"
print_status "✅ Test scripts created"
echo ""
echo "📋 Next Steps:"
echo "  1. Run the test script: python3 genesis_test.py"
echo "  2. Set up environment: source setup_genesis_env.sh"
echo "  3. Check Genesis documentation: https://genesis-world.readthedocs.io/"
echo ""
echo "📁 Files created:"
echo "  - genesis_test.py (test installation)"
echo "  - setup_genesis_env.sh (environment setup)"
echo "  - genesis_requirements.txt (dependencies list)"
echo "  - genesis/ (Genesis source code)"
echo ""
print_status "🎉 Genesis-World dependencies installation completed!"

if [ "$CUDA_AVAILABLE" = true ]; then
    print_warning "🔄 Please restart your terminal or run 'source ~/.bashrc' to update CUDA paths"
fi