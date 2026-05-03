#!/bin/bash
set -e  # Stop on any error

echo "🚀 Starting build process..."

# Upgrade pip first
pip install --upgrade pip

# Install NumPy FIRST (critical for chromadb compatibility)
echo "📦 Installing NumPy..."
pip install numpy==1.26.4

# Install remaining dependencies
echo "📚 Installing remaining packages..."
pip install -r requirements.txt

# Verify numpy version (should be 1.x, not 2.x)
python -c "import numpy; print(f'✅ NumPy version: {numpy.__version__}')"

# Create chroma_db from chunks
echo "📚 Building vector database..."
python embedding.py

echo "✅ Build complete!"