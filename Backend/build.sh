#!/bin/bash

echo "🚀 Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Create chroma_db from chunks
echo "📚 Building vector database..."
python embedding.py

echo "✅ Build complete!"