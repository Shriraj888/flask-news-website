#!/bin/bash

# Production deployment script for Flask News Website
# Make sure to run this script from the project root directory

echo "🚀 Flask News Website - Production Deployment"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check environment variables
echo "🔧 Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration before running in production!"
fi

# Run production checks
echo "✅ Running production checks..."

# Check if SECRET_KEY is set
if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  WARNING: SECRET_KEY environment variable not set!"
    echo "   A random secret key will be generated automatically"
fi

# Generate a random secret key if not provided
if [ ! -f "secret_key.txt" ]; then
    echo "🔐 Generating secret key..."
    python -c "import secrets; print(secrets.token_urlsafe(32))" > secret_key.txt
    echo "   Secret key saved to secret_key.txt"
fi

echo ""
echo "🎉 Deployment preparation complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Configure your .env file if needed"
echo "   2. Set up a reverse proxy (nginx) if needed"
echo "   3. Configure SSL certificates"
echo "   4. Start the application with: gunicorn -c gunicorn.conf.py app:app"
echo ""
echo "🔗 Local URLs:"
echo "   Development: http://localhost:5000"
echo "   Production:  Configure your domain"
echo ""
echo "📚 For more information, see README.md"
echo "=============================================="
