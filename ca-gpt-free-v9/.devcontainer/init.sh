#!/bin/bash
set -e

echo "--- AIGIS Bootstrap Initializer ---"

echo ">> Step 1: Installing all Node.js dependencies..."
npm install

echo ">> Step 2: Installing Python dependencies for 'engine'..."
(cd engine && poetry install)

echo ">> Step 3: Installing Python dependencies for 'ai-service'..."
(cd ai-service && poetry install)

echo ">> Step 4: Pulling Mistral model for Ollama..."
# We use docker exec because ollama is a separate container
docker exec ca-gpt-free-v9-ollama-1 ollama pull mistral

echo ">> Step 5: Running database migrations..."
(cd server && npm run migrate)

echo "--- ✅ Bootstrap Complete! ---"
echo "All services are initialized. You can now run 'make dev' to start."