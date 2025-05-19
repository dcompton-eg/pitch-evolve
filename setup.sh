#!/bin/bash
set -e

echo "📦 Setting up Pitch Evolve..."

# Create and activate virtual environment
echo "🔧 Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo "🔗 Installing package in development mode..."
pip install -e .

# Create necessary directories
echo "📁 Creating required directories..."
mkdir -p pitch_evolve/data/outputs

# Create .env template if it doesn't exist
if [ ! -f .env ]; then
  echo "🔑 Creating .env template..."
  echo "# API Keys" >.env
  echo "OPENAI_API_KEY=" >>.env
  echo "TAVILY_API_KEY=" >>.env
  echo "Please edit the .env file and add your API keys."
fi

echo "✅ Setup complete! Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Edit .env file and add your API keys"
echo "3. Run to evolve pitches through eval+prompt evolution"
