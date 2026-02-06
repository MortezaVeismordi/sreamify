#!/bin/bash
set -e

echo "Setting up development environment..."

# Copy environment files
cp docker/env/.env.example docker/env/.env.dev

# Create virtual environments
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r services/auth-service/requirements.txt
pip install -r services/stream-service/requirements.txt
pip install -r services/chat-service/requirements.txt
pip install -r services/notification-service/requirements.txt

echo "Development environment setup complete!"
