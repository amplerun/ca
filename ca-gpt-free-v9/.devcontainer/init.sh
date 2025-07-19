#!/bin/bash
set -e

echo "--- AIGIS Bootstrap Initializer ---"

# Need to be root to install some packages
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    curl \
    git \
    gnupg \
    build-essential \
    libpq-dev \
    python3.10 \
    python3-pip \
    python3.10-venv \
    nodejs

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to path for this script
export PATH="$HOME/.local/bin:$PATH"

echo ">> Installing global node packages..."
npm install -g pnpm migrate-mongo expo-cli

echo ">> Step 1: Installing all Node.js dependencies..."
npm install

echo ">> Step 2: Installing Python dependencies for 'engine'..."
(cd engine && poetry install)

echo ">> Step 3: Installing Python dependencies for 'ai-service'..."
(cd ai-service && poetry install)

echo ">> Step 4: Pulling Mistral model for Ollama..."
docker exec ca-gpt-free-v9-ollama-1 ollama pull mistral

echo ">> Step 5: Running database migrations..."
(cd server && npm run migrate)

echo "--- ✅ Bootstrap Complete! ---"
echo "All services are initialized. You can now run 'make dev' to start."
