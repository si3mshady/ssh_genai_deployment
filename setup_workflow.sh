#!/bin/bash

# Create workflow folder if it doesn't exist
mkdir -p .github/workflows

# Write the deploy.yml file
cat << 'EOF' > .github/workflows/deploy.yml
name: 🚀 Auto Deploy to VPS

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repo
        uses: actions/checkout@v3

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.DEPLOY_KEY }}
          script: |
            cd /home/cloudwarrior2891/sre-genai-dockerized
            git pull origin main
            docker-compose down
            docker-compose up -d --build
EOF

echo "✅ GitHub Actions workflow created at .github/workflows/deploy.yml"

