#!/bin/bash
# Quick Setup Script for CYC_BUILDER MCP
# CYC_BUILDER: Structure-based cyclic peptide design framework
# Uses seed preparation, fragment-based assembly, and MCTS for cyclic peptide binder design
# Source: https://github.com/wfh1998/CYC_BUILDER_v1.0

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Setting up CYC_BUILDER MCP ==="

# Step 1: Create Python environment
echo "[1/4] Creating Python 3.11 environment..."
(command -v mamba >/dev/null 2>&1 && mamba create -p ./env python=3.11 -y) || \
(command -v conda >/dev/null 2>&1 && conda create -p ./env python=3.11 -y) || \
(echo "Warning: Neither mamba nor conda found, creating venv instead" && python3 -m venv ./env)

# Step 2: Install core Python packages
echo "[2/4] Installing core dependencies..."
./env/bin/pip install loguru click pandas numpy tqdm biopython requests pyyaml omegaconf joblib scikit-learn scipy

# Step 3: Install fastmcp
echo "[3/4] Installing fastmcp..."
./env/bin/pip install --ignore-installed fastmcp

# Step 4: Install RDKit
echo "[4/4] Installing RDKit..."
(command -v mamba >/dev/null 2>&1 && ./env/bin/mamba install -c conda-forge rdkit -y) || \
(command -v conda >/dev/null 2>&1 && ./env/bin/conda install -c conda-forge rdkit -y) || \
./env/bin/pip install rdkit

echo ""
echo "=== CYC_BUILDER MCP Setup Complete ==="
echo "Note: CYC_BUILDER requires PyRosetta for full functionality"
echo "To run the MCP server: ./env/bin/python src/server.py"
