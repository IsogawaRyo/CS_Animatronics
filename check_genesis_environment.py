#!/usr/bin/env python3
"""
Genesis-World Environment Checker
Check if your system meets all requirements for Genesis-World development.
"""

import sys
import subprocess
import importlib
import platform
import os
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}=== {text} ==={Colors.END}")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def check_python_version():
    """Check Python version compatibility."""
    print_header("Python Environment")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major == 3 and version.minor >= 8:
        print_success(f"Python {version_str} (✓ Compatible)")
    else:
        print_error(f"Python {version_str} (✗ Requires Python 3.8+)")
        return False
    
    print_info(f"Platform: {platform.platform()}")
    print_info(f"Architecture: {platform.machine()}")
    return True

def check_system_requirements():
    """Check system-level requirements."""
    print_header("System Requirements")
    
    # Check OS
    if platform.system() == "Linux":
        print_success("Linux OS detected")
        
        # Check if Ubuntu
        try:
            with open("/etc/lsb-release", "r") as f:
                content = f.read()
                if "Ubuntu" in content:
                    # Extract Ubuntu version
                    for line in content.split('\n'):
                        if line.startswith('DISTRIB_RELEASE='):
                            version = line.split('=')[1]
                            print_info(f"Ubuntu {version}")
                            break
        except FileNotFoundError:
            print_warning("Ubuntu version detection failed")
    else:
        print_warning(f"Non-Linux OS detected: {platform.system()}")
        print_warning("Genesis-World is optimized for Linux environments")

def check_nvidia_gpu():
    """Check NVIDIA GPU availability."""
    print_header("GPU Support")
    
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print_success("NVIDIA GPU detected")
            
            # Parse GPU information
            lines = result.stdout.split('\n')
            for line in lines:
                if 'NVIDIA' in line and 'Driver Version' in line:
                    # Extract driver version
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if 'Driver' in part and i + 2 < len(parts):
                            driver_version = parts[i + 2]
                            print_info(f"Driver Version: {driver_version}")
                            break
                    break
            
            # Check CUDA
            try:
                result_cuda = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
                if result_cuda.returncode == 0:
                    # Extract CUDA version
                    for line in result_cuda.stdout.split('\n'):
                        if 'release' in line.lower():
                            cuda_version = line.split('release')[1].strip().split(',')[0]
                            print_success(f"CUDA toolkit detected: {cuda_version}")
                            break
                else:
                    print_warning("CUDA toolkit not found")
            except FileNotFoundError:
                print_warning("CUDA compiler (nvcc) not found")
                
            return True
        else:
            print_warning("nvidia-smi command failed")
            return False
    except FileNotFoundError:
        print_warning("NVIDIA drivers not detected")
        return False

def check_python_package(package_name, import_name=None, version_attr='__version__'):
    """Check if a Python package is installed and get its version."""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, version_attr, 'Unknown')
        print_success(f"{package_name}: {version}")
        return True, version
    except ImportError:
        print_error(f"{package_name}: Not installed")
        return False, None
    except AttributeError:
        print_warning(f"{package_name}: Installed (version unknown)")
        return True, 'Unknown'

def check_python_dependencies():
    """Check Python package dependencies."""
    print_header("Python Dependencies")
    
    # Essential packages
    essential_packages = [
        ('numpy', 'numpy'),
        ('PyTorch', 'torch'),
        ('Taichi', 'taichi'),
        ('matplotlib', 'matplotlib'),
        ('Pillow', 'PIL'),
        ('OpenCV', 'cv2'),
    ]
    
    all_essential_found = True
    for package_name, import_name in essential_packages:
        found, version = check_python_package(package_name, import_name)
        if not found:
            all_essential_found = False
    
    # Check PyTorch CUDA support
    try:
        import torch
        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0) if device_count > 0 else "Unknown"
            print_success(f"PyTorch CUDA support: Available ({device_count} device(s))")
            print_info(f"Primary GPU: {device_name}")
        else:
            print_warning("PyTorch CUDA support: Not available (CPU only)")
    except ImportError:
        pass
    
    # Optional packages
    print_info("Optional packages:")
    optional_packages = [
        ('scipy', 'scipy'),
        ('gymnasium', 'gymnasium'),
        ('stable-baselines3', 'stable_baselines3'),
        ('trimesh', 'trimesh'),
        ('moderngl', 'moderngl'),
        ('glfw', 'glfw'),
    ]
    
    for package_name, import_name in optional_packages:
        check_python_package(f"  {package_name}", import_name)
    
    return all_essential_found

def check_genesis_installation():
    """Check Genesis-World installation."""
    print_header("Genesis-World Installation")
    
    # Check if Genesis is installed
    found, version = check_python_package('Genesis', 'genesis')
    
    # Check Genesis directory
    genesis_dir = Path('genesis')
    if genesis_dir.exists() and genesis_dir.is_dir():
        print_success(f"Genesis directory found: {genesis_dir.absolute()}")
        
        # Check for key files
        key_files = [
            'setup.py',
            'genesis/__init__.py',
            'README.md'
        ]
        
        for file_path in key_files:
            full_path = genesis_dir / file_path
            if full_path.exists():
                print_info(f"  ✓ {file_path}")
            else:
                print_warning(f"  ✗ {file_path} (missing)")
    else:
        print_warning("Genesis directory not found")
        print_info("Run the installation script: ./install_genesis_dependencies.sh")
    
    return found

def check_development_tools():
    """Check development tools."""
    print_header("Development Tools")
    
    tools = [
        ('Jupyter', 'jupyter'),
        ('IPython', 'IPython'),
        ('pytest', 'pytest'),
        ('black', 'black'),
        ('flake8', 'flake8'),
    ]
    
    for tool_name, import_name in tools:
        check_python_package(tool_name, import_name)

def generate_report():
    """Generate environment report."""
    print_header("Environment Report")
    
    # System info
    print_info(f"OS: {platform.system()} {platform.release()}")
    print_info(f"Architecture: {platform.machine()}")
    print_info(f"Python: {sys.version.split()[0]}")
    print_info(f"Working Directory: {os.getcwd()}")
    
    # GPU info
    try:
        import torch
        if torch.cuda.is_available():
            print_info(f"PyTorch CUDA: {torch.version.cuda}")
            for i in range(torch.cuda.device_count()):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory // (1024**3)
                print_info(f"GPU {i}: {gpu_name} ({gpu_memory}GB)")
    except ImportError:
        print_warning("PyTorch not available for GPU info")

def main():
    """Main function to run all checks."""
    print(f"{Colors.PURPLE}{Colors.BOLD}")
    print("🔍 Genesis-World Environment Checker")
    print("=====================================")
    print(f"{Colors.END}")
    
    all_checks_passed = True
    
    # Run all checks
    all_checks_passed &= check_python_version()
    check_system_requirements()
    gpu_available = check_nvidia_gpu()
    all_checks_passed &= check_python_dependencies()
    genesis_installed = check_genesis_installation()
    check_development_tools()
    
    generate_report()
    
    # Final summary
    print_header("Summary")
    
    if all_checks_passed and genesis_installed:
        print_success("🎉 Your environment is ready for Genesis-World development!")
        print_info("Try running: python3 genesis_test.py")
    elif all_checks_passed and not genesis_installed:
        print_warning("⚙️  Core dependencies are ready. Install Genesis-World:")
        print_info("Run: ./install_genesis_dependencies.sh")
    else:
        print_error("❌ Some requirements are missing.")
        print_info("Run the installation script: ./install_genesis_dependencies.sh")
        if not gpu_available:
            print_warning("⚠️  GPU acceleration will not be available")

if __name__ == "__main__":
    main()